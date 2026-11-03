"""Where in SymPy's source a bug lives: helpers for bugcheck.py and its child process.

The child runs a bug's Actual block with `Tracer` active, which records, cheaply:

- every SymPy code object that ran (sys.monitoring PY_START, disabled per code object after
  its first call, so each function costs one callback);
- for each doctest example that raised, the innermost frame inside the sympy package.

`resolve_refs` then maps the functions named in "Notes on fixing" to source lines and says
whether they ran. Locations are dicts {"path", "start", "end", "function"} with paths relative
to the SymPy root (e.g. "sympy/printing/latex.py") and 1-based inclusive line numbers.

Standard library only; Python >= 3.12 for sys.monitoring (older Pythons record nothing).
"""

import ast
import inspect
import os
import re
import sys

TOOL_NAME = "bugcheck"
_DEF_CACHE = {}


# ---------------------------------------------------------------- static: functions in a file

def def_index(source):
    """{qualname: (start, end)} for every function and class in Python source, and for the
    variables assigned in module and class bodies (`known_functions`, `Cls._default_settings`).
    start is the first decorator's line (as in co_firstlineno), end the last line."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return {}
    out = {}

    def visit(node, prefix):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                qual = prefix + child.name
                start = min([d.lineno for d in child.decorator_list] + [child.lineno])
                out.setdefault(qual, (start, child.end_lineno))
                inner = qual + (".<locals>." if not isinstance(child, ast.ClassDef) else ".")
                visit(child, inner)
            elif isinstance(child, (ast.Assign, ast.AnnAssign)) and "<locals>" not in prefix:
                targets = child.targets if isinstance(child, ast.Assign) else [child.target]
                for t in targets:
                    for n in ([t] if isinstance(t, ast.Name) else getattr(t, "elts", [])):
                        if isinstance(n, ast.Name):
                            out.setdefault(prefix + n.id, (child.lineno, child.end_lineno))
            else:
                visit(child, prefix)
    visit(tree, "")
    return out


def file_index(path):
    if path not in _DEF_CACHE:
        try:
            with open(path, encoding="utf-8") as f:
                _DEF_CACHE[path] = def_index(f.read())
        except OSError:
            _DEF_CACHE[path] = {}
    return _DEF_CACHE[path]


def enclosing(index, start, end):
    """The innermost function (else class) of a def_index that contains lines start..end."""
    best = None
    for qual, (s, e) in index.items():
        if s <= start and end <= e and (best is None or e - s < best[1][1] - best[1][0]):
            best = (qual, (s, e))
    return best


# ---------------------------------------------------------------- dynamic: the child process

class Tracer:
    """Records the SymPy code objects that run between start() and stop(), and the exception
    each doctest example raised (doctest catches it, so it is taken where doctest handles it)."""

    def __init__(self, sympy_root):
        self.root = os.path.realpath(sympy_root)
        self.pkg = os.path.join(self.root, "sympy") + os.sep
        self.executed = set()
        self.last_exc = None
        self.tool = None
        self.ours = {}

    def _in_sympy(self, filename):
        try:
            ok = self.ours[filename]
        except KeyError:
            ok = self.ours[filename] = os.path.realpath(filename).startswith(self.pkg)
        return ok

    def start(self):
        mon = getattr(sys, "monitoring", None)
        if mon is None:
            return
        import doctest
        run_code = doctest.DocTestRunner._DocTestRunner__run.__code__
        for tool in (4, 3, 1, 0):
            try:
                mon.use_tool_id(tool, TOOL_NAME)
            except ValueError:
                continue
            self.tool = tool
            break
        else:
            return
        disable = mon.DISABLE

        def on_start(code, offset):
            if self._in_sympy(code.co_filename):
                self.executed.add(code)
            return disable

        def on_handled(code, offset, exc):
            if code is run_code:  # doctest's `except:` around the example
                self.last_exc = exc

        mon.register_callback(self.tool, mon.events.PY_START, on_start)
        mon.register_callback(self.tool, mon.events.EXCEPTION_HANDLED, on_handled)
        mon.set_events(self.tool, mon.events.PY_START | mon.events.EXCEPTION_HANDLED)

    def stop(self):
        if self.tool is None:
            return
        mon = sys.monitoring
        mon.set_events(self.tool, 0)
        mon.register_callback(self.tool, mon.events.PY_START, None)
        mon.register_callback(self.tool, mon.events.EXCEPTION_HANDLED, None)
        mon.free_tool_id(self.tool)
        self.tool = None

    def take_exception(self):
        exc, self.last_exc = self.last_exc, None
        return exc

    # ------------------------------------------------------------ locations

    def rel(self, filename):
        return os.path.relpath(os.path.realpath(filename), self.root).replace(os.sep, "/")

    def code_location(self, code):
        path = self.rel(code.co_filename)
        qual = getattr(code, "co_qualname", code.co_name)
        span = file_index(os.path.realpath(code.co_filename)).get(qual)
        if span is None:
            lines = [l for _, _, l in code.co_lines() if l]
            span = (code.co_firstlineno, max(lines + [code.co_firstlineno]))
        return {"path": path, "start": span[0], "end": span[1], "function": qual}

    def raised_at(self, exc):
        """Innermost frame inside the sympy package of an exception's traceback."""
        tb, found = getattr(exc, "__traceback__", None), None
        while tb is not None:
            code = tb.tb_frame.f_code
            if self._in_sympy(code.co_filename):
                found = (code, tb.tb_lineno)
            tb = tb.tb_next
        if found is None:
            return None
        code, line = found
        return {"path": self.rel(code.co_filename), "start": line, "end": line,
                "function": getattr(code, "co_qualname", code.co_name)}


def code_of(obj):
    """The code object behind a function, method, classmethod, staticmethod or property
    (through functools.wraps-style wrappers), or None."""
    try:
        for _ in range(10):
            if isinstance(obj, property):
                obj = obj.fget
            elif isinstance(obj, (classmethod, staticmethod)) or inspect.ismethod(obj):
                obj = obj.__func__
            elif inspect.isfunction(obj) and "__wrapped__" in vars(obj):
                obj = obj.__wrapped__
            else:
                break
        return obj.__code__ if inspect.isfunction(obj) else None
    except Exception:
        return None


def _sympy_classes():
    """{name: [class, ...]} for the classes defined in the loaded sympy modules."""
    out = {}
    for name, mod in list(sys.modules.items()):
        if mod is None or not (name == "sympy" or name.startswith("sympy.")):
            continue
        for k, v in list(vars(mod).items()):
            if isinstance(v, type) and v.__name__ == k and v.__module__ == name:
                out.setdefault(k, []).append(v)
    return out


def _attr_code(cls, name):
    for c in cls.__mro__:
        if name in vars(c):
            return code_of(vars(c)[name])
    return None


def _module_of_file(tracer, path):
    """Loaded module for a path relative to the SymPy root, or None."""
    full = os.path.realpath(os.path.join(tracer.root, path))
    for name, mod in list(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if f and (name == "sympy" or name.startswith("sympy.")) and os.path.realpath(f) == full:
            return mod
    return None


def _find_files(tracer, name):
    """Paths (relative to the SymPy root) of the non-test files with this basename or path."""
    if "/" in name:
        p = name if name.startswith("sympy/") else "sympy/" + name
        return [p] if os.path.exists(os.path.join(tracer.root, p)) else []
    found = []
    for d, dirs, files in os.walk(os.path.join(tracer.root, "sympy")):
        dirs[:] = [x for x in dirs if x not in ("tests", "__pycache__")]
        if name in files:
            found.append(tracer.rel(os.path.join(d, name)))
    return sorted(found, key=lambda p: (not p.startswith("sympy/printing/"), p))


_CLASS_FILES = {}


def _static_class_files(tracer, cls_name):
    """Files (not loaded) that define a class of this name, found by scanning the source once."""
    if not _CLASS_FILES:
        pat = re.compile(r"^[ \t]*class[ \t]+(\w+)", re.M)
        for d, dirs, files in os.walk(os.path.join(tracer.root, "sympy")):
            dirs[:] = [x for x in dirs if x not in ("tests", "__pycache__")]
            for f in sorted(files):
                if f.endswith(".py"):
                    p = os.path.join(d, f)
                    try:
                        text = open(p, encoding="utf-8").read()
                    except (OSError, UnicodeDecodeError):
                        continue
                    for name in set(pat.findall(text)):
                        _CLASS_FILES.setdefault(name, []).append(tracer.rel(p))
        _CLASS_FILES.setdefault("", [])
    return _CLASS_FILES.get(cls_name, [])


def _lookup(tracer, owner, attr):
    """What `owner.attr` is in SymPy's source: ("code", code object), ("data", location) for a
    variable assigned in a module or class body, ("other",) for anything else that exists (a
    class, an inherited assumption, ...), or None if there is no such attribute."""
    if isinstance(owner, type):
        for c in owner.__mro__:
            if attr in vars(c):
                obj = vars(c)[attr]
                code = code_of(obj)
                if code is not None:
                    return ("code", code)
                if isinstance(obj, type):
                    return ("other",)
                return _data(tracer, sys.modules.get(c.__module__), c.__qualname__ + "." + attr)
        return ("other",) if hasattr(owner, attr) else None
    if owner is None or not hasattr(owner, attr):
        return None
    obj = getattr(owner, attr)
    code = code_of(obj)
    if code is not None:
        return ("code", code)
    if isinstance(obj, type) or inspect.ismodule(obj):
        return ("other",)
    return _data(tracer, owner, attr)


def _data(tracer, mod, qual):
    f = getattr(mod, "__file__", None)
    if not f or not tracer._in_sympy(f):
        return ("other",)
    span = file_index(os.path.realpath(f)).get(qual)
    if span is None:  # set somewhere else (e.g. in a loop), or imported
        return ("other",)
    return ("data", {"path": tracer.rel(f), "start": span[0], "end": span[1], "function": qual})


def _classes_in(mod):
    return [c for c in vars(mod).values() if isinstance(c, type) and c.__module__ == mod.__name__]


def resolve_refs(tracer, refs, files, context_classes):
    """Resolve the functions (and module or class variables) named in "Notes on fixing".

    refs: [{"ref": text, "file": path or None, "name": "Cls.meth" or "name"}]
    files: files the notes name (paths or basenames), context for bare names
    context_classes: printer classes the Actual block used, most used first
    Returns [{"ref", "location" (or None), "executed": bool, "data": bool, "missing": bool}]:
    data: a variable, not a function (whether it was used is not known);
    missing: the file or (loaded) class it names exists, but has nothing of that name.

    Bare names (`_print_Mod`, `latex_escape`) are looked up in the classes and functions of the
    files the notes name and, if they contain "_" or were written as calls, of the printers
    Actual used; names exported by `sympy` itself (`latex`, `pycode`) are not bare refs.
    """
    import sympy
    classes = None
    paths = []
    for f in files:
        for p in _find_files(tracer, f):
            if p not in paths:
                paths.append(p)
    file_mods = [m for m in (_module_of_file(tracer, p) for p in paths) if m]
    out = []
    for ref in refs:
        name = ref["name"]
        parts = name.split(".")
        owners = []  # (object, attribute) pairs to try, best first
        static = []  # (path, qualname) found only in the source of a module never imported
        container = False
        if ref.get("file"):
            for p in _find_files(tracer, ref["file"]):
                container = True
                mod = _module_of_file(tracer, p)
                if mod is None:
                    index = file_index(os.path.join(tracer.root, p))
                    quals = [name] + [q for q in index if len(parts) == 1 and q.endswith("." + name)
                                      and "<locals>" not in q]
                    static += [(p, q) for q in quals if q in index][:1]
                    continue
                obj = mod
                for part in parts[:-1]:
                    obj = getattr(obj, part, None)
                owners.append((obj, parts[-1]))
                if len(parts) == 1:
                    owners += [(c, name) for c in _classes_in(mod)]
        elif len(parts) >= 2:
            if classes is None:
                classes = _sympy_classes()
            cands = classes.get(parts[0], [])
            container = bool(cands)
            mod_names = {m.__name__ for m in file_mods}
            for cls in sorted(cands, key=lambda c: c.__module__ not in mod_names):
                obj = cls
                for part in parts[1:-1]:
                    obj = getattr(obj, part, None)
                if isinstance(obj, type):
                    owners.append((obj, parts[-1]))
            if not cands and parts[0][:1].isupper():
                for p in _static_class_files(tracer, parts[0]):
                    if name in file_index(os.path.join(tracer.root, p)):
                        static.append((p, name))
        elif not hasattr(sympy, name):
            wide = "_" in name.strip("_") or name.startswith("_") or ref["ref"].strip().endswith("()")
            owners += [(c, name) for m in file_mods for c in _classes_in(m)]
            owners += [(m, name) for m in file_mods]
            if wide:
                owners += [(c, name) for c in context_classes]
                owners += [(sys.modules.get(c.__module__), name) for c in context_classes]
        codes, data, exists = [], [], False
        for owner, attr in owners:
            found = _lookup(tracer, owner, attr)
            if found is None:
                continue
            exists = True
            if found[0] == "code" and tracer._in_sympy(found[1].co_filename):
                if found[1] not in codes:
                    codes.append(found[1])
            elif found[0] == "data" and (len(parts) == 1 or ref.get("file")
                                         or parts[0][:1].isupper()):
                # (`arg.is_real` in prose is a variable `arg`, not the class `arg`)
                data.append(found[1])
        ran = [c for c in codes if c in tracer.executed]
        entry = {"ref": ref["ref"], "location": None, "executed": False, "data": False,
                 "missing": False}
        if ran or codes:
            entry.update(location=tracer.code_location((ran or codes)[0]), executed=bool(ran))
        elif data:
            entry.update(location=data[0], data=True)
        elif static:
            p, qual = static[0]
            s, e = file_index(os.path.join(tracer.root, p))[qual]
            entry["location"] = {"path": p, "start": s, "end": e, "function": qual}
        else:
            entry["missing"] = (container and not exists
                                and bool(ref.get("file") or len(parts) >= 2))
        out.append(entry)
    return out
