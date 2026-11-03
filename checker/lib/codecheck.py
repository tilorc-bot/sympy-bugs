"""Compile and run printed C, C++ and Rust code from a bug file's doctests.

Built on check_printed_code.py (vendored from tilorc-bot/sympy PR #60), but it takes the
printed *string*, so it works for ccode()/cxxcode()/rust_code() output, statements and
arrays alike. Symbol types are given as keywords:

    >>> from codecheck import compiles, compile_errors, run_code
    >>> compiles('c', ccode(Mod(x, y)), x=float, y=float)
    True
    >>> run_code('c', ccode(Mod(x, y)), x=-1.0, y=3.0)    # values give the types
    2.0

Types: float (double / f64), int (int / i32), bool, [float] / [int] (an array: `const double *`
in C, `&[f64]` in Rust). `assign_to=('y', float)` declares the variable an assignment
statement writes; run_code() then returns that variable.

Languages: 'c' (C99), 'c89', 'c11', 'c++' (C++17), 'rust' (edition 2021).
"""

import ctypes
import os
import re
import tempfile
import textwrap

# Plain ASCII compiler messages, the same on every machine.
os.environ["LC_ALL"] = "C"

from check_printed_code import (C_FLAGS, C_HEADER, C99_HEADER, RUST_HEADER, PrintedCodeError,
                                run_compiler, wrap_in_c_function, wrap_in_rust_function)

CXX_HEADER = "#include <cmath>\n#include <cstdint>\n#include <cstdlib>\n#include <algorithm>\n"
LANGS = {
    # command, suffix, header, wrap, type names
    "c89": (["gcc", "-std=c89", *C_FLAGS], ".c", C_HEADER, wrap_in_c_function, "c"),
    "c": (["gcc", "-std=c99", *C_FLAGS], ".c", C99_HEADER, wrap_in_c_function, "c"),
    "c99": (["gcc", "-std=c99", *C_FLAGS], ".c", C99_HEADER, wrap_in_c_function, "c"),
    "c11": (["gcc", "-std=c11", *C_FLAGS], ".c", C99_HEADER, wrap_in_c_function, "c"),
    "c++": (["g++", "-std=c++17", "-fsyntax-only", "-pedantic-errors"], ".cpp", CXX_HEADER,
            wrap_in_c_function, "c"),
    "rust": (["rustc", "--edition=2021", "--crate-type=lib", "--emit=metadata",
              "--error-format=short"], ".rs", RUST_HEADER, wrap_in_rust_function, "rust"),
}
TYPE_NAMES = {
    "c": {"real": "double", "int": "int", "bool": "bool", "real[]": "const double *",
          "int[]": "const int *"},
    "rust": {"real": "f64", "int": "i32", "bool": "bool", "real[]": "&[f64]", "int[]": "&[i32]"},
}
LIBRARY_FLAGS = {"-fsyntax-only": ["-shared", "-fPIC"], "--crate-type=lib": ["--crate-type=cdylib"],
                 "--emit=metadata": []}


def _kind(t):
    if isinstance(t, str):
        return t
    if t is float:
        return "real"
    if t is int:
        return "int"
    if t is bool:
        return "bool"
    if isinstance(t, list) and t:
        return _kind(t[0]) + "[]"
    raise TypeError(f"unsupported type {t!r}; use float, int, bool, [float] or [int]")


def _kind_of_value(v):
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "real"
    if isinstance(v, (list, tuple)) and v:
        return _kind_of_value(v[0]) + "[]"
    raise TypeError(f"unsupported value {v!r}")


def _source(lang, code, params, assign_to, returns):
    command, suffix, header, wrap, family = LANGS[lang]
    names = TYPE_NAMES[family]
    parameters = [(name, names[kind]) for name, kind in params]
    assigned = (assign_to[0], names[_kind(assign_to[1])]) if assign_to else None
    if returns and assigned:
        # A statement: run it, then return the assigned variable.
        body = wrap(code, parameters, assigned, False)
        if family == "rust":
            body = body.replace("pub fn f(", '#[no_mangle]\npub extern "C" fn f(', 1)
            body = body.replace(")\n{", ") -> f64\n{", 1)
            body = body[:body.rindex("}")] + f"    f64::from({assigned[0]})\n}}\n"
        else:
            body = body.replace("void f(", "double f(", 1)
            body = body[:body.rindex("}")] + f"    return (double){assigned[0]};\n}}\n"
    else:
        body = wrap(code, parameters, assigned, returns)
    if lang == "c++" and returns:
        body = 'extern "C" ' + body
    return header + "\n" + body


def compile_errors(lang, code, assign_to=None, **types):
    """The compiler's error lines for the printed code, or '' if it compiles."""
    params = [(name, _kind(t)) for name, t in types.items()]
    command, suffix = LANGS[lang][:2]
    source = _source(lang, code, params, assign_to, False)
    with tempfile.TemporaryDirectory() as d:
        try:
            run_compiler(command, suffix, source, d)
        except PrintedCodeError as e:
            text = str(e)
            errors = text.split(" says\n\n", 1)[1].split("\nabout\n", 1)[0]
            lines = []
            for line in textwrap.dedent(errors).strip().split("\n"):
                line = re.sub(r"^code\.\w+:\d+:\d+: ", "", line)  # drop file:line:col
                if not line.startswith("error: aborting due to"):
                    lines.append(line)
            return "\n".join(lines)
    return ""


def compiles(lang, code, assign_to=None, **types):
    """True if the printed code compiles inside a function declaring the given symbols."""
    return compile_errors(lang, code, assign_to=assign_to, **types) == ""


def run_code(lang, code, assign_to=None, **values):
    """Compile the printed code into a shared library, call it with the given values and
    return the result as a float (the expression's value, or the assigned variable's)."""
    params = [(name, _kind_of_value(v)) for name, v in values.items()]
    command, suffix, _, _, family = LANGS[lang]
    if family == "rust" and any(k.endswith("[]") for _, k in params):
        raise TypeError("run_code does not pass arrays to Rust; use compiles()")
    command = [p for part in command for p in LIBRARY_FLAGS.get(part, [part])]
    source = _source(lang, code, params, assign_to, True)
    d = tempfile.mkdtemp()
    library = os.path.join(d, "code.so")
    extra = ("-o", library) + (("-lm",) if family == "c" else ())
    run_compiler(command, suffix, source, d, extra)  # raises PrintedCodeError if invalid
    fn = ctypes.CDLL(library).f
    fn.restype = ctypes.c_double
    args, argtypes = [], []
    for (name, kind), v in zip(params, values.values()):
        if kind == "real":
            argtypes.append(ctypes.c_double); args.append(v)
        elif kind in ("int", "bool"):
            argtypes.append(ctypes.c_int if kind == "int" else ctypes.c_bool); args.append(v)
        else:
            ctype = ctypes.c_double if kind == "real[]" else ctypes.c_int
            arr = (ctype * len(v))(*v)
            argtypes.append(ctypes.POINTER(ctype)); args.append(arr)
    fn.argtypes = argtypes
    return fn(*args)
