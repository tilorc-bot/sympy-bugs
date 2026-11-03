#!/usr/bin/env python3
"""bugcheck: verify the bug catalogue against SymPy master.

Every bug is a Markdown file under bugs/ that states the bug as runnable doctests
(see SPEC.md). Its ID is its path without `.md`, e.g. `printing/latex/latex-mod-negative-arg`.

  check   FILE...     run files and print verdicts (local use)
  status              run bugs and write status.json (CI and local)
  summary             Markdown summary of selected bugs, for PR comments
  site                render the browsable catalogue page from bugs/ + status.json
  sync-issues         keep one readable GitHub issue per bug file (needs gh + token)

Only the standard library is used. `check`/`status` need SymPy importable from --sympy and,
for fixes, --sympy must be a git checkout.
"""

import argparse
import concurrent.futures
import datetime
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile

TIMEOUT = 60
# codecheck (compile and run printed C/C++/Rust code) and its vendored helper
LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
COMPILED = re.compile(r"\b(compiles|compile_errors|run_code)\(")
TEST_TIMEOUT = 1500
TEST_WORKERS = int(os.environ.get("BUGCHECK_TEST_WORKERS", "2"))

SECTION_ALIASES = {
    "actual": "actual", "expected": "expected", "why it is wrong": "why", "why": "why",
    "kind": "kind", "caused by": "caused_by", "related": "related",
    "notes on fixing": "notes", "workaround": "workaround", "suggested fix": "fix",
    "source": "source", "encountered": "encountered",
}
REQUIRED = ["kind", "actual", "expected", "why"]
KINDS = ["crash", "hang", "wrong-meaning", "invalid-output", "lossy", "ignored-setting",
         "cosmetic", "internal"]
ENV_ERRORS = ("NameError", "ImportError", "ModuleNotFoundError", "SyntaxError")

PRINTER_FAMILIES = [
    ("latex", r"Latex"), ("pretty", r"Pretty"), ("mathml", r"MathML"),
    ("srepr", r"^ReprPrinter$"), ("python", r"^PythonPrinter$"),
    ("pycode", r"PythonCode|NumPy|SciPy|Mpmath|CuPy|JAX|SymPyPrinter|Tensorflow|Torch|Cmath|NumExpr"),
    ("c", r"^C\d\dCodePrinter|^CCodePrinter|Cxx"), ("fortran", r"FCode|Fortran"),
    ("octave", r"Octave"), ("julia", r"Julia"), ("rust", r"Rust"), ("js", r"Javascript"),
    ("r", r"^RCode"), ("mathematica", r"MCode|Mathematica"), ("maple", r"Maple"),
    ("glsl", r"GLSL"), ("smtlib", r"SMTLib"), ("dot", r"Dot"), ("tree", r"Tree"),
    ("str", r"Str"),
]


# ---------------------------------------------------------------- reading bug files

def split_sections(body):
    """Split markdown on '### ' headings that are outside code fences."""
    sections, name, buf, fence = {}, None, [], None
    for line in (body or "").replace("\r\n", "\n").split("\n"):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if fence is None:
                fence = marker
            elif fence == marker and stripped.strip() == marker:
                fence = None
        if fence is None and line.startswith("### "):
            if name is not None:
                sections[name] = "\n".join(buf).strip()
            title = line[4:].strip().rstrip(":").lower()
            name = SECTION_ALIASES.get(title, title)
            buf = []
        elif name is not None:
            buf.append(line)
    if name is not None:
        sections[name] = "\n".join(buf).strip()
    return sections


FENCE = re.compile(r"^(```|~~~)[ \t]*([\w+-]*)[^\n]*\n(.*?)\n[ \t]*\1[ \t]*$", re.S | re.M)
CODE_SPANS = re.compile(r"(```.*?```|~~~.*?~~~|`[^`\n]*`)", re.S)
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
DIRECT_TRACKER = re.compile(
    r"(?<![\w/\[])sympy/sympy#\d+|(?<!redirect\.)github\.com/sympy/sympy/(?:issues|pull)/\d+")


def code_blocks(text, langs=None):
    return [(m.group(2).lower(), m.group(3)) for m in FENCE.finditer(text or "")
            if langs is None or m.group(2).lower() in langs]


def doctest_source(text):
    blocks = [b for lang, b in code_blocks(text) if ">>>" in b and lang in
              ("", "pycon", "python", "py", "python3", "doctest")]
    return "\n".join(blocks) + "\n" if blocks else ""


def diffs(text):
    return [b + "\n" for lang, b in code_blocks(text, {"diff", "patch"}) if "@@" in b]


def outside_code(text):
    return "".join(p for i, p in enumerate(CODE_SPANS.split(text or "")) if i % 2 == 0)


def direct_tracker_links(text):
    t = outside_code(text)
    t = re.sub(r"\[[^\]]*\]\(https://redirect\.github\.com/[^)]*\)", "", t)
    return DIRECT_TRACKER.findall(t)


def bug_links(text, path, root):
    """IDs of other bugs linked from text (relative links to .md files)."""
    out = []
    base = os.path.dirname(path)
    for target in MD_LINK.findall(outside_code(text)):
        if target.startswith(("http:", "https:", "#")) or not target.endswith(".md"):
            continue
        full = os.path.normpath(os.path.join(base, target))
        out.append(bug_id(full, root))
    return out


def bug_id(path, root):
    return os.path.relpath(path, root)[:-3].replace(os.sep, "/")


def read_bug(path, root):
    text = open(path, encoding="utf-8").read()
    first, _, body = text.partition("\n")
    s = split_sections(body)
    kind = re.sub(r"[`*\s]", "", s.get("kind", "").split("\n")[0]).lower()
    problems = []
    if not first.startswith("# "):
        problems.append("first line must be `# Title`")
    for sec in REQUIRED:
        if not s.get(sec):
            problems.append(f"missing section `### {sec.replace('why', 'Why it is wrong').title()}`")
    if kind and kind not in KINDS:
        problems.append(f"unknown kind `{kind}` (use one of: {', '.join(KINDS)})")
    links = direct_tracker_links(body)
    if links:
        problems.append("links to the SymPy tracker must go through redirect.github.com: " +
                        ", ".join(links[:3]))
    bid = bug_id(path, root)
    related = bug_links(s.get("related", ""), path, root)
    caused_by = bug_links(s.get("caused_by", ""), path, root)
    for other in related + caused_by:
        if not os.path.exists(os.path.join(root, other + ".md")):
            problems.append(f"link to missing bug `{other}`")
    return {
        "id": bid, "path": path, "title": first.lstrip("# ").strip(), "text": text,
        "kind": kind if kind in KINDS else None,
        "actual": doctest_source(s.get("actual", "")),
        "expected": doctest_source(s.get("expected", "")),
        "workaround": doctest_source(s.get("workaround", "")),
        "fixes": [{"source": "suggested fix", "diff": d} for d in diffs(s.get("fix", ""))],
        "caused_by": caused_by, "related": related,
        "tracker": sorted({int(n) for n in re.findall(
            r"redirect\.github\.com/sympy/sympy/(?:issues|pull)/(\d+)", s.get("related", ""))}),
        "encountered": [l for l in s.get("encountered", "").split("\n") if l.strip()],
        "evidence": "compiled" if COMPILED.search(doctest_source(s.get("expected", ""))) else "printed",
        "problems": problems,
    }


def find_bugs(root):
    out = []
    for d, _, files in os.walk(root):
        out += [os.path.join(d, f) for f in files if f.endswith(".md") and f != "README.md"]
    return sorted(out)


# ---------------------------------------------------------------- execution

CHILD = r'''
import doctest, json, sys, time, traceback

hits = {}
try:
    from sympy.printing.printer import Printer
    _orig = Printer._print
    def _traced(self, expr, **kw):
        meth = None
        pm = getattr(self, "printmethod", None)
        if pm and hasattr(expr, pm) and not isinstance(expr, type):
            meth = pm
        else:
            for cls in type(expr).__mro__:
                if hasattr(self, "_print_" + cls.__name__):
                    meth = "_print_" + cls.__name__
                    break
        key = type(self).__name__ + "." + (meth or "emptyPrinter")
        hits[key] = hits.get(key, 0) + 1
        return _orig(self, expr, **kw)
    Printer._print = _traced
except Exception:
    pass


class Checker(doctest.OutputChecker):
    def check_output(self, want, got, flags):
        norm = lambda s: "\n".join(l.rstrip() for l in s.strip("\n").split("\n"))
        if norm(want) == norm(got):
            return True
        return super().check_output(want, got, flags)


class Runner(doctest.DocTestRunner):
    def __init__(self):
        super().__init__(checker=Checker(), optionflags=doctest.ELLIPSIS, verbose=False)
        self.records = []
    def report_start(self, out, test, example):
        pass
    def report_success(self, out, test, example, got):
        self.records.append({"source": example.source, "ok": True,
                             "want": example.want, "got": got})
    def report_failure(self, out, test, example, got):
        self.records.append({"source": example.source, "ok": False,
                             "want": example.want, "got": got})
    def report_unexpected_exception(self, out, test, example, exc_info):
        exc = exc_info[1]
        tb = "".join(traceback.format_exception(*exc_info))[-1500:]
        self.records.append({"source": example.source, "ok": False, "want": example.want,
                             "got": tb, "exc": type(exc).__name__})


def run(src, globs, name):
    if not src.strip():
        return None, globs
    try:
        test = doctest.DocTestParser().get_doctest(src, globs, name, None, 0)
    except ValueError as e:
        return {"passed": False, "examples": [], "error": f"doctest parse error: {e}"}, globs
    runner = Runner()
    runner.run(test, clear_globs=False, out=lambda s: None)
    recs = runner.records
    return {"passed": bool(recs) and all(r["ok"] for r in recs), "examples": recs}, test.globs


job = json.loads(sys.stdin.read())
t0 = time.time()
res = {}
def compile_log(phase, start):
    cc = sys.modules.get("codecheck")
    return [dict(e, phase=phase) for e in (cc.LOG[start:] if cc else [])]

res["actual"], after = run(job["actual"], {"__name__": "__bugcheck__"}, "actual")
n = len(sys.modules["codecheck"].LOG) if "codecheck" in sys.modules else 0
res["compiled"] = compile_log("actual", 0)
res["expected"], _ = run(job["expected"], dict(after), "expected")
res["compiled"] += compile_log("expected", n)
actual_hits = dict(hits)
res["workaround"], _ = run(job.get("workaround", ""), dict(after), "workaround")
res["printer_hits"] = actual_hits
res["seconds"] = round(time.time() - t0, 2)
sys.stdout.write("\x00BUGCHECK\x00" + json.dumps(res, default=str))
'''


def clean_env():
    env = dict(os.environ)
    for k in list(env):
        if "TOKEN" in k or k.startswith(("ACTIONS_", "GITHUB_")):
            env.pop(k)
    return env


def execute(bug, sympy_dir, timeout=TIMEOUT):
    env = clean_env()
    env["PYTHONPATH"] = os.pathsep.join([os.path.abspath(sympy_dir), LIB_DIR,
                                         env.get("PYTHONPATH", "")])
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONHASHSEED"] = "0"  # some printers order terms by hash; keep runs reproducible
    job = {k: bug[k] for k in ("actual", "expected", "workaround")}
    with tempfile.TemporaryDirectory() as cwd:
        try:
            p = subprocess.run([sys.executable, "-c", CHILD], input=json.dumps(job), text=True,
                               capture_output=True, timeout=timeout, env=env, cwd=cwd)
        except subprocess.TimeoutExpired:
            return {"timeout": True}
    marker = "\x00BUGCHECK\x00"
    if marker not in p.stdout:
        return {"crashed": (p.stderr or p.stdout)[-1500:]}
    return json.loads(p.stdout.rsplit(marker, 1)[1])


def examples(block):
    """Every doctest example with what master printed (trimmed), for showing the evidence."""
    out = []
    for ex in (block or {}).get("examples", []):
        out.append({"source": ex["source"], "ok": ex["ok"], "want": (ex.get("want") or "")[-1500:],
                    "got": (ex.get("got") or "")[-1500:], **({"exc": ex["exc"]} if ex.get("exc") else {})})
    return out


def run_info(sympy_dir):
    """Where and how this status was produced, so it can be checked rather than trusted."""
    env = os.environ
    info = {"python": sys.version.split()[0]}
    if env.get("GITHUB_RUN_ID"):
        info["run_url"] = (f"{env.get('GITHUB_SERVER_URL', 'https://github.com')}/"
                           f"{env.get('GITHUB_REPOSITORY')}/actions/runs/{env['GITHUB_RUN_ID']}")
        info["checker_commit"] = env.get("GITHUB_SHA")
    else:
        p = subprocess.run(["git", "-C", os.path.dirname(os.path.abspath(__file__)), "rev-parse",
                            "HEAD"], capture_output=True, text=True)
        info["checker_commit"] = p.stdout.strip() or None
        info["run_url"] = None
    for tool, cmd in (("gcc", ["gcc", "--version"]), ("rustc", ["rustc", "--version"])):
        try:
            info[tool] = subprocess.run(cmd, capture_output=True, text=True).stdout.split("\n")[0]
        except OSError:
            info[tool] = None
    return info


def first_failure(block):
    for ex in (block or {}).get("examples", []):
        if not ex["ok"]:
            return {k: (v[-1500:] if isinstance(v, str) else v) for k, v in ex.items()}
    return None


def verdict(bug, res):
    if not bug["actual"] or not bug["expected"]:
        return "malformed", "no doctest (`>>>`) block in Actual or Expected"
    if res.get("timeout"):
        if bug["kind"] == "hang":
            return "reproduces", f"still hangs (no result within {TIMEOUT}s)"
        return "timeout", f"did not finish within {TIMEOUT}s"
    if res.get("crashed"):
        return "check-broken", "the checker process crashed: " + res["crashed"][-300:]
    a, e = res["actual"], res["expected"]
    if a.get("error") or e.get("error"):
        return "malformed", a.get("error") or e.get("error")
    fa = first_failure(a)
    if fa and fa.get("exc") in ENV_ERRORS:
        return "check-broken", f"Actual raises {fa['exc']}, so it cannot run as written"
    if a["passed"] and not e["passed"]:
        return "reproduces", "Actual matches master; Expected fails"
    if not a["passed"] and e["passed"]:
        return "fixed", "Expected passes on master; Actual no longer matches"
    if not a["passed"] and not e["passed"]:
        return "changed", "neither block matches master: behaviour changed, the file needs updating"
    return "check-broken", "both blocks pass on master, so Expected does not detect the bug"


def family(cls):
    for fam, pat in PRINTER_FAMILIES:
        if re.search(pat, cls):
            return fam
    return None


def printer_families(hits):
    fams = []
    for key, _ in sorted(hits.items(), key=lambda kv: -kv[1]):
        fam = family(key.split(".")[0])
        if fam and fam not in fams:
            fams.append(fam)
    if len(fams) > 1 and "str" in fams:
        fams.remove("str")  # the doctest echo uses the str printer for everything
    return fams[:3]


# ---------------------------------------------------------------- fixes

def git(sympy_dir, *args, check=True):
    return subprocess.run(["git", "-C", sympy_dir, *args], capture_output=True, text=True,
                          check=check)


def reset(sympy_dir):
    git(sympy_dir, "reset", "-q", "--hard")
    git(sympy_dir, "clean", "-q", "-fd", "sympy")


def touched_tests(sympy_dir, diff):
    tests = []
    for path in re.findall(r"^\+\+\+ b/(\S+)", diff, re.M):
        if "/tests/" in path:
            if os.path.exists(os.path.join(sympy_dir, path)):
                tests.append(path)
            continue
        # The whole tests/ directory of the changed package: a change to a shared helper
        # (e.g. precedence.py) shows up in the tests of the printers that use it.
        d = os.path.dirname(path)
        while d and not os.path.isdir(os.path.join(sympy_dir, d, "tests")):
            d = os.path.dirname(d)
        if d:
            tests.append(os.path.join(d, "tests"))
    return sorted(set(tests))


def run_tests(sympy_dir, tests):
    if not tests:
        return {"ran": False}
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--no-header", "-n", str(TEST_WORKERS), *tests], cwd=sympy_dir,
                           capture_output=True, text=True, timeout=TEST_TIMEOUT, env=clean_env())
    except subprocess.TimeoutExpired:
        return {"ran": True, "passed": False, "summary": "test run timed out", "tests": tests}
    tail = [l for l in p.stdout.strip().split("\n") if l.strip()][-1:] or ["(no output)"]
    failed = re.findall(r"^FAILED (\S+)", p.stdout, re.M)[:5]
    return {"ran": True, "passed": p.returncode == 0, "summary": tail[0].strip("= "),
            "failed": failed, "tests": tests}


def diff_hash(diff):
    return hashlib.sha256(diff.encode()).hexdigest()[:12]


def check_fix(fix, bid, bugs, baseline, sympy_dir, jobs, scope):
    """scope: 'applies' (git apply --check only), 'basic' (+ this bug + tests), 'full' (+ others)."""
    out = {"source": fix["source"], "diff": diff_hash(fix["diff"]), "scope": scope}
    with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False) as f:
        f.write(fix["diff"])
        patch = f.name
    try:
        p = git(sympy_dir, "apply", "--check", patch, check=False)
        out["applies"] = p.returncode == 0
        if not out["applies"]:
            out["error"] = p.stderr.strip()[-400:]
            return out
        if scope == "applies":
            return out
        git(sympy_dir, "apply", patch)
        v, _ = verdict(bugs[bid], execute(bugs[bid], sympy_dir))
        out["fixes_this"] = v == "fixed"
        out["verdict_with_fix"] = v
        out["tests"] = run_tests(sympy_dir, touched_tests(sympy_dir, fix["diff"]))
        out["verified"] = bool(out["fixes_this"] and out["tests"].get("passed", True))
        if scope == "full":
            others = [o for o in bugs if o != bid and baseline.get(o) in ("reproduces", "fixed")]
            with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
                after = dict(zip(others, ex.map(
                    lambda o: verdict(bugs[o], execute(bugs[o], sympy_dir))[0], others)))
            out["also_fixes"] = sorted(o for o in others
                                       if baseline[o] == "reproduces" and after[o] == "fixed")
            out["breaks"] = sorted(o for o in others
                                   if baseline[o] == "fixed" and after[o] != "fixed")
        return out
    finally:
        reset(sympy_dir)
        os.unlink(patch)


# ---------------------------------------------------------------- status

def sympy_head(sympy_dir):
    return git(sympy_dir, "rev-parse", "HEAD", check=False).stdout.strip() or None


def load_bugs(root, only=None):
    root = os.path.abspath(root)
    paths = find_bugs(root)
    bugs = {}
    for p in paths:
        b = read_bug(p, root)
        bugs[b["id"]] = b
    if only is None:
        return bugs, set(bugs)
    root = os.path.abspath(root)
    selected = {bug_id(os.path.abspath(o), root) for o in only if o.endswith(".md")} & set(bugs)
    return bugs, selected


def run_all(bugs, ids, sympy_dir, jobs):
    with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
        return dict(zip(ids, ex.map(lambda i: execute(bugs[i], sympy_dir), ids)))


def cmd_status(args):
    root = args.root
    bugs, selected = load_bugs(root, args.only)
    previous = json.load(open(args.previous)) if args.previous and os.path.exists(args.previous) else {}
    prev_bugs = previous.get("bugs", {})
    head = sympy_head(args.sympy)
    today = datetime.date.today().isoformat()

    need_baseline = args.fixes == "full" and any(bugs[i]["fixes"] for i in selected)
    to_run = sorted(set(bugs) if need_baseline else selected)
    raw = run_all(bugs, to_run, args.sympy, args.jobs)
    baseline = {i: verdict(bugs[i], raw[i])[0] for i in raw}

    out = {i: prev_bugs[i] for i in prev_bugs if i in bugs and i not in selected}
    for i in sorted(selected):
        b, r = bugs[i], raw[i]
        v, why = verdict(b, r)
        prev = prev_bugs.get(i, {})
        rec = {
            "title": b["title"], "kind": b["kind"], "verdict": v, "explanation": why,
            "sympy": head, "checked": today, "problems": b["problems"],
            "printers": printer_families(r.get("printer_hits", {})),
            "printer_methods": sorted(r.get("printer_hits", {}),
                                      key=lambda k: -r["printer_hits"][k])[:12],
            "actual_failure": first_failure(r.get("actual")),
            "expected_failure": first_failure(r.get("expected")),
            "examples": {k: examples(r.get(k)) for k in ("actual", "expected")},
            "compiled": [{**c, "source": c["source"][-4000:], "output": c["output"][-2000:]}
                         for c in r.get("compiled", [])],
            "workaround": None if not b["workaround"] else bool(
                r.get("workaround") and r["workaround"]["passed"]),
            "caused_by": b["caused_by"], "related": b["related"], "tracker": b["tracker"],
            "encountered": len(b["encountered"]), "evidence": b["evidence"],
            "first_reproduced": prev.get("first_reproduced") or (head if v == "reproduces" else None),
            "last_reproduced": head if v == "reproduces" else prev.get("last_reproduced"),
            "fixed_between": prev.get("fixed_between"),
        }
        if v == "fixed" and prev.get("verdict") == "reproduces" and prev.get("last_reproduced"):
            rec["fixed_between"] = [prev["last_reproduced"], head]
        rec["fixes"] = []
        if b["fixes"] and v == "reproduces" and args.fixes != "none":
            prev_fixes = {f.get("diff"): f for f in prev.get("fixes", [])}
            for fx in b["fixes"]:
                res = check_fix(fx, i, bugs, baseline, args.sympy, args.jobs, args.fixes)
                old = prev_fixes.get(res["diff"])
                if args.fixes == "applies" and old and res["applies"]:
                    # Diff unchanged and still applies: keep the last full verification.
                    res = {**old, "applies": True}
                rec["fixes"].append(res)
        out[i] = rec
        print(f"{v:13} {i}", file=sys.stderr)
    result = {"sympy": head, "checked": today, "run": run_info(args.sympy),
              "bugs": dict(sorted(out.items()))}
    with open(args.out, "w") as f:
        json.dump(result, f, indent=1, sort_keys=False)
        f.write("\n")
    bad = [i for i in selected if out[i]["verdict"] != "reproduces" or out[i]["problems"]]
    if args.strict and bad:
        print(f"{len(bad)} bug(s) do not reproduce cleanly: " + ", ".join(sorted(bad)[:10]),
              file=sys.stderr)
        sys.exit(1)


def cmd_check(args):
    root = os.path.abspath(args.root)
    bugs = {}
    for p in args.files:
        b = read_bug(os.path.abspath(p), root)
        bugs[b["id"]] = b
    if args.fixes:  # baseline over the whole catalogue for "also fixes"
        all_bugs, _ = load_bugs(root)
        all_bugs.update(bugs)
    else:
        all_bugs = bugs
    raw = run_all(all_bugs, sorted(all_bugs), args.sympy, args.jobs)
    baseline = {i: verdict(all_bugs[i], raw[i])[0] for i in raw}
    report = []
    for i in sorted(bugs):
        b = bugs[i]
        v, why = verdict(b, raw[i])
        rec = {"id": i, "verdict": v, "explanation": why, "kind": b["kind"],
               "problems": b["problems"], "printers": printer_families(raw[i].get("printer_hits", {})),
               "actual_failure": first_failure(raw[i].get("actual")),
               "expected_failure": first_failure(raw[i].get("expected")), "fixes": []}
        if args.fixes and b["fixes"] and v == "reproduces":
            for fx in b["fixes"]:
                rec["fixes"].append(check_fix(fx, i, all_bugs, baseline, args.sympy, args.jobs, "full"))
        report.append(rec)
    if args.json:
        json.dump(report, sys.stdout, indent=1)
        return
    for rec in report:
        print(f"{rec['verdict']:13} {rec['id']}  [{rec['kind']}] {','.join(rec['printers'])}")
        for prob in rec["problems"]:
            print(f"    problem: {prob}")
        if rec["verdict"] != "reproduces":
            print(f"    {rec['explanation']}")
            for key in ("actual_failure", "expected_failure"):
                f = rec[key]
                if f:
                    print(f"    {key}: >>> {f['source'].strip()}")
                    print("      want: " + (f.get("want") or "").strip().replace("\n", "\n            "))
                    print("      got:  " + (f.get("got") or "").strip()[-600:].replace("\n", "\n            "))
        for fx in rec["fixes"]:
            print(f"    fix: applies={fx.get('applies')} fixes_this={fx.get('fixes_this')} "
                  f"tests={fx.get('tests', {}).get('summary')} verified={fx.get('verified')} "
                  f"also_fixes={fx.get('also_fixes')} breaks={fx.get('breaks')} {fx.get('error', '')}")


# ---------------------------------------------------------------- similarity (duplicate hints)

WORD = re.compile(r"[A-Za-z_]\w+")


def repro_tokens(bug):
    lines = [l[4:] for l in bug["actual"].split("\n") if l.startswith((">>> ", "... "))]
    lines = [l for l in lines if "import" not in l and "symbols(" not in l]
    return set(WORD.findall("\n".join(lines)))


def similar(bid, bugs, status, k=3):
    me = repro_tokens(bugs[bid])
    my_methods = set((status.get(bid) or {}).get("printer_methods", []))
    df = {}
    for s in status.values():
        for m in s.get("printer_methods", []):
            df[m] = df.get(m, 0) + 1
    scored = []
    for o, b in bugs.items():
        if o == bid:
            continue
        t = repro_tokens(b)
        jt = len(me & t) / len(me | t) if me and t else 0
        om = set((status.get(o) or {}).get("printer_methods", []))
        rare = [m for m in my_methods & om if df.get(m, 0) <= 5]
        score = 0.6 * jt + 0.4 * min(1, len(rare) / 2)
        if score > 0.45:
            scored.append((round(score, 2), o, sorted(rare)[:2]))
    return sorted(scored, reverse=True)[:k]


def cmd_summary(args):
    bugs, selected = load_bugs(args.root, args.only)
    status = json.load(open(args.status))["bugs"]
    lines = ["### Bug catalogue check", ""]
    if not selected:
        lines.append("No bug files changed.")
    for i in sorted(selected):
        s = status.get(i, {})
        ok = s.get("verdict") == "reproduces" and not s.get("problems")
        lines.append(f"{'✅' if ok else '❌'} **`{i}`**: {s.get('verdict', '?')}, "
                     f"{s.get('explanation', '')}")
        for p in s.get("problems", []):
            lines.append(f"  - ❌ {p}")
        f = s.get("actual_failure") if s.get("verdict") in ("changed", "fixed", "check-broken") \
            else None
        if f:
            lines.append(f"  - first Actual line that differs: `{f['source'].strip()[:120]}`")
        for fx in s.get("fixes", []):
            t = (fx.get("tests") or {})
            lines.append(f"  - 🔧 fix: applies {'✅' if fx.get('applies') else '❌'}, "
                         f"fixes this {'✅' if fx.get('fixes_this') else '❌'}, tests "
                         f"{'✅' if t.get('passed', True) else '❌'} {t.get('summary', '')}"
                         + (f", also fixes {', '.join('`' + a + '`' for a in fx['also_fixes'])}"
                            if fx.get("also_fixes") else "")
                         + (f", ❌ breaks {', '.join(fx['breaks'])}" if fx.get("breaks") else ""))
        for score, o, rare in similar(i, bugs, status):
            why = f" (shares {', '.join('`' + r + '`' for r in rare)})" if rare else ""
            lines.append(f"  - possible duplicate: `{o}` similarity {score}{why}")
    print("\n".join(lines))


# ---------------------------------------------------------------- site

KIND_WEIGHT = {"crash": 40, "hang": 40, "wrong-meaning": 35, "internal": 30,
               "invalid-output": 30, "lossy": 20, "ignored-setting": 15, "cosmetic": 5}
REACH = {"str": 1.3, "srepr": 1.3, "pycode": 1.3, "python": 1.1, "latex": 1.15,
         "pretty": 1.15, "c": 1.1, "fortran": 1.05}


def priority(i, s, dependents):
    """Transparent importance score with its breakdown."""
    parts = [(f"kind {s.get('kind')}", KIND_WEIGHT.get(s.get("kind"), 10))]
    reach = max([REACH.get(p, 0.9) for p in s.get("printers", [])] or [1.0])
    if reach != 1:
        parts.append((f"printer reach x{reach}", round(parts[0][1] * (reach - 1))))
    if dependents.get(i):
        parts.append((f"root cause of {len(dependents[i])}", min(30, 5 * len(dependents[i]))))
    if s.get("encountered"):
        parts.append((f"hit in real use {s['encountered']}x", min(40, 15 * s["encountered"])))
    if any(f.get("verified") for f in s.get("fixes", [])):
        parts.append(("verified fix available", 5))
    total = sum(p for _, p in parts)
    if s.get("verdict") != "reproduces":
        parts.append(("not reproducing on master", -total))
        total = 0
    return total, parts


def fix_state(fixes, has_fix):
    if any(f.get("verified") for f in fixes):
        return "verified"
    if fixes and not any(f.get("applies") for f in fixes):
        return "stale"
    if any("verified" in f for f in fixes):
        return "failing"
    return "unchecked" if has_fix else None


def cmd_site(args):
    bugs, _ = load_bugs(args.root)
    st = json.load(open(args.status))
    status = st["bugs"]
    dependents = {}
    for i, s in status.items():
        for c in s.get("caused_by", []):
            dependents.setdefault(c, []).append(i)
    rows = []
    for i, b in sorted(bugs.items()):
        s = status.get(i, {"verdict": "unchecked"})
        score, parts = priority(i, {**s, "kind": b["kind"]}, dependents)
        rows.append({
            "id": i, "title": b["title"], "kind": b["kind"], "verdict": s.get("verdict"),
            "explanation": s.get("explanation"), "printers": s.get("printers", []),
            "methods": s.get("printer_methods", []), "score": score, "score_parts": parts,
            "fix": fix_state(s.get("fixes", []), bool(b["fixes"])),
            "fixes": s.get("fixes", []), "workaround": s.get("workaround"),
            "caused_by": b["caused_by"], "dependents": dependents.get(i, []),
            "related": b["related"], "tracker": b["tracker"],
            "fixed_between": s.get("fixed_between"),
            "evidence": s.get("evidence"),
            "examples": s.get("examples"), "compiled": s.get("compiled", []),
            "checked": s.get("checked"), "sympy": s.get("sympy"),
            "expected_failure": s.get("expected_failure"),
            "text": b["text"].split("\n", 1)[1],
        })
    data = {"sympy": st.get("sympy"), "checked": st.get("checked"), "repo": args.repo,
            "run": st.get("run"),
            "bugs": rows}
    template = args.template or os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.html")
    page = open(template, encoding="utf-8").read()
    blob = json.dumps(data).replace("</", "<\\/")
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page.replace("/*__DATA__*/null", blob))
    print(f"wrote {os.path.join(args.out, 'index.html')} ({len(rows)} bugs)", file=sys.stderr)


# ---------------------------------------------------------------- issue sync

ISSUE_MARKER = re.compile(r"<!-- bug-id: (\S+) -->")
SYNC_LABEL_PREFIXES = ("kind:", "printer:", "priority:")
SYNC_LABELS = {"reproduces", "fixed-on-master", "needs-update", "fix-verified", "fix-unchecked",
               "fix-failing", "fix-stale", "root-cause", "removed", "verified-by-compiler"}
LABEL_COLORS = {"reproduces": "d73a4a", "fixed-on-master": "0e8a16", "needs-update": "fbca04",
                "fix-verified": "1d76db", "fix-unchecked": "c5def5", "fix-failing": "e99695",
                "fix-stale": "ededed", "root-cause": "b60205", "removed": "ededed",
                "verified-by-compiler": "0e8a16", "priority:high": "b60205", "priority:medium": "d93f0b", "priority:low": "fef2c0"}


def gh(*args, input=None):
    """Run gh; back off and retry when GitHub's (secondary) rate limit kicks in."""
    import time
    wait = 60
    for attempt in range(8):
        p = subprocess.run(["gh", *args], input=input, capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout) if p.stdout.strip() else None
        if "rate limit" not in p.stderr.lower() or attempt == 7:
            raise RuntimeError(f"gh {' '.join(args[:3])}: {p.stderr.strip()[-500:]}")
        print(f"rate limited; sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)
        wait = min(wait * 2, 900)


def paged(endpoint):
    items, page = [], 1
    sep = "&" if "?" in endpoint else "?"
    while True:
        batch = gh("api", f"{endpoint}{sep}per_page=100&page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def strip_timing(s):
    return re.sub(r" in [\d.]+s\b", "", s or "")


def issue_body(i, b, s, dependents, numbers, repo):
    """Readable issue body generated from a bug file and its status. Nothing in it changes
    from day to day unless the bug or its status does, so nightly syncs write little."""
    def ref(other):
        if other in numbers:
            return f"#{numbers[other]}"
        return f"[`{other}`](https://github.com/{repo}/blob/main/bugs/{other}.md)"

    v = s.get("verdict", "unchecked")
    alert = {"reproduces": "WARNING", "fixed": "TIP"}.get(v, "NOTE")
    head = {
        "reproduces": "**Reproduces on SymPy master.** Re-checked nightly",
        "fixed": "**Fixed on SymPy master.** The Expected block now passes",
        "changed": "**Behaviour changed on SymPy master.** The file needs updating",
    }.get(v, f"**{v}**: {s.get('explanation', '')}")
    if s.get("evidence") == "compiled" and v == "reproduces":
        head += "; the printed code was compiled and run to confirm it"
    if s.get("first_reproduced") and v == "reproduces":
        head += f"; first confirmed at sympy/sympy@`{s['first_reproduced'][:10]}`"
    if s.get("fixed_between"):
        a, z = s["fixed_between"]
        head += (f"; fixed between `{a[:10]}` and `{z[:10]}` ([commits]"
                 f"(https://redirect.github.com/sympy/sympy/compare/{a[:12]}...{z[:12]}))")
    lines = [f"> [!{alert}]", f"> {head}."]
    for fx in s.get("fixes", []):
        if fx.get("verified"):
            t = fx.get("tests") or {}
            msg = f"🔧 **Suggested fix verified**: applies to master, fixes this bug"
            if t.get("ran"):
                msg += f", tests pass ({strip_timing(t.get('summary'))})"
            if fx.get("also_fixes"):
                msg += ", also fixes " + ", ".join(ref(o) for o in fx["also_fixes"])
            lines += [">", "> " + msg + "."]
        elif fx.get("applies") is False:
            lines += [">", "> 🔧 The suggested fix no longer applies to master."]
        elif "verified" in fx:
            lines += [">", "> 🔧 The suggested fix does not pass its checks."]
        else:
            lines += [">", "> 🔧 Suggested fix applies to master; not verified yet."]
    if dependents.get(i):
        lines += [">", "> **Root cause of** " + ", ".join(ref(o) for o in dependents[i]) + "."]
    if s.get("caused_by"):
        lines += [">", "> **Caused by** " + ", ".join(ref(o) for o in s["caused_by"]) + "."]

    text = b["text"].split("\n", 1)[1].strip("\n")
    base = os.path.dirname(i)

    def relink(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http:", "https:", "#")) or not target.endswith(".md"):
            return m.group(0)
        other = os.path.normpath(os.path.join(base, target[:-3])).replace(os.sep, "/")
        if other in numbers:
            return f"{label} (#{numbers[other]})"
        return f"[{label}](https://github.com/{repo}/blob/main/bugs/{other}.md)"
    parts = CODE_SPANS.split(text)
    for k in range(0, len(parts), 2):
        parts[k] = re.sub(r"\[([^\]]*)\]\(([^)\s]+)\)", relink, parts[k])
    text = "".join(parts)

    methods = s.get("printer_methods", [])
    foot = [
        "", "---",
        f"<sub>Generated from [`bugs/{i}.md`](https://github.com/{repo}/blob/main/bugs/{i}.md), "
        "the source of truth. To change this bug, edit that file in a pull request; this issue "
        "is regenerated automatically and comments are kept."
        + (" Printer methods reached: " + ", ".join(f"`{m}`" for m in methods[:8]) + "."
           if methods else "") + "</sub>",
        f"<!-- bug-id: {i} -->",
    ]
    return "\n".join(lines) + "\n\n" + text + "\n" + "\n".join(foot) + "\n"


def issue_labels(i, b, s, dependents):
    labels = set()
    v = s.get("verdict")
    labels.add({"reproduces": "reproduces", "fixed": "fixed-on-master"}.get(v, "needs-update"))
    if b["kind"]:
        labels.add("kind:" + b["kind"])
    for p in s.get("printers", []):
        labels.add("printer:" + p)
    st = fix_state(s.get("fixes", []), bool(b["fixes"]))
    if st:
        labels.add("fix-" + st)
    if dependents.get(i):
        labels.add("root-cause")
    if s.get("evidence") == "compiled":
        labels.add("verified-by-compiler")
    score, _ = priority(i, {**s, "kind": b["kind"]}, dependents)
    if v == "reproduces":
        labels.add("priority:" + ("high" if score >= 45 else "medium" if score >= 30 else "low"))
    return labels


def cmd_sync_issues(args):
    import time
    repo = args.repo
    deadline = time.time() + args.max_minutes * 60
    bugs, _ = load_bugs(args.root)
    status = json.load(open(args.status))["bugs"]
    dependents = {}
    for i, s in status.items():
        for c in s.get("caused_by", []):
            dependents.setdefault(c, []).append(i)

    existing = {}
    for it in paged(f"repos/{repo}/issues?state=all&creator={args.bot}"):
        if "pull_request" in it:
            continue
        m = ISSUE_MARKER.search(it.get("body") or "")
        if m:
            existing[m.group(1)] = it
    numbers = {i: it["number"] for i, it in existing.items()}
    labels_known = {l["name"] for l in paged(f"repos/{repo}/labels")}
    writes = 0

    def write(*a, input=None):
        nonlocal writes
        if time.time() > deadline or writes >= args.max_writes:
            raise TimeoutError
        out = gh(*a, input=input)
        writes += 1
        time.sleep(args.delay)
        return out

    def ensure_labels(names):
        for name in sorted(set(names) - labels_known):
            write("api", f"repos/{repo}/labels", "-f", f"name={name}", "-f",
                  f"color={LABEL_COLORS.get(name, '5319e7' if name.startswith('printer:') else 'bfd4f2')}")
            labels_known.add(name)

    def desired(i):
        b, s = bugs[i], status.get(i, {"verdict": "unchecked"})
        state = "closed" if s.get("verdict") == "fixed" else "open"
        return (b["title"], issue_body(i, b, s, dependents, numbers, repo),
                issue_labels(i, b, s, dependents), state)

    created = updated = closed = 0
    try:
        # Pass 1: create missing issues (in path order, root causes first).
        order = sorted(bugs, key=lambda i: (not dependents.get(i), i))
        for i in order:
            if i in existing:
                continue
            title, body, labels, state = desired(i)
            ensure_labels(labels)
            it = write("api", f"repos/{repo}/issues", "--input", "-", input=json.dumps(
                {"title": title, "body": body, "labels": sorted(labels)}))
            existing[i] = it
            numbers[i] = it["number"]
            created += 1
            if state == "closed":
                write("api", "-X", "PATCH", f"repos/{repo}/issues/{it['number']}", "-f",
                      "state=closed", "-f", "state_reason=completed")
            print(f"created #{it['number']} {i}", file=sys.stderr)
        # Pass 2: bring every issue up to date (links to issues created in pass 1, status).
        for i in order:
            it = existing[i]
            title, body, labels, state = desired(i)
            have = {l["name"] for l in it["labels"]}
            keep = {l for l in have if l not in SYNC_LABELS and not l.startswith(SYNC_LABEL_PREFIXES)}
            want_labels = keep | labels
            patch = {}
            if it["title"] != title:
                patch["title"] = title
            if (it.get("body") or "").strip() != body.strip():
                patch["body"] = body
            if have != want_labels:
                ensure_labels(want_labels)
                patch["labels"] = sorted(want_labels)
            if it["state"] != state:
                patch["state"] = state
                if state == "closed":
                    patch["state_reason"] = "completed"
            if patch:
                write("api", "-X", "PATCH", f"repos/{repo}/issues/{it['number']}", "--input", "-",
                      input=json.dumps(patch))
                updated += 1
                print(f"updated #{it['number']} {i}: {', '.join(patch)}", file=sys.stderr)
        # Bugs whose file was removed: close the issue as not planned.
        for i, it in existing.items():
            if i not in bugs and it["state"] == "open":
                write("api", f"repos/{repo}/issues/{it['number']}/comments", "-f",
                      f"body=The bug file `bugs/{i}.md` was removed from the catalogue.")
                write("api", "-X", "PATCH", f"repos/{repo}/issues/{it['number']}", "-f",
                      "state=closed", "-f", "state_reason=not_planned", "-f", "labels[]=removed")
                closed += 1
    except TimeoutError:
        print("stopping early (time or write budget); the next run continues", file=sys.stderr)
    print(f"sync: {created} created, {updated} updated, {closed} closed, {writes} writes",
          file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check", help="run bug files and print verdicts")
    p.add_argument("files", nargs="+")
    p.add_argument("--root", default="bugs")
    p.add_argument("--sympy", required=True)
    p.add_argument("--fixes", action="store_true", help="verify suggested fixes too")
    p.add_argument("--json", action="store_true")
    p.add_argument("--jobs", type=int, default=2)
    p = sub.add_parser("status", help="write status.json")
    p.add_argument("--root", default="bugs")
    p.add_argument("--only", nargs="*", help="bug files to (re)check; default: all")
    p.add_argument("--previous", help="previous status.json to merge into")
    p.add_argument("--sympy", required=True)
    p.add_argument("--fixes", choices=["none", "applies", "basic", "full"], default="applies")
    p.add_argument("--jobs", type=int, default=2)
    p.add_argument("--strict", action="store_true",
                   help="exit 1 if a selected bug does not reproduce or has problems")
    p.add_argument("--out", required=True)
    p = sub.add_parser("summary", help="Markdown summary for a PR comment")
    p.add_argument("--root", default="bugs")
    p.add_argument("--only", nargs="*")
    p.add_argument("--status", required=True)
    p = sub.add_parser("site", help="render the catalogue page")
    p.add_argument("--root", default="bugs")
    p.add_argument("--status", required=True)
    p.add_argument("--repo", default="")
    p.add_argument("--template", help="page template (default: checker/site.html)")
    p.add_argument("--out", required=True)
    p = sub.add_parser("sync-issues", help="create/update one GitHub issue per bug file")
    p.add_argument("--root", default="bugs")
    p.add_argument("--status", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--bot", default="github-actions[bot]",
                   help="author of the issues this sync owns")
    p.add_argument("--delay", type=float, default=9.0, help="seconds after each write")
    p.add_argument("--max-writes", type=int, default=420)
    p.add_argument("--max-minutes", type=float, default=300)
    args = ap.parse_args()
    {"check": cmd_check, "status": cmd_status, "summary": cmd_summary,
     "site": cmd_site, "sync-issues": cmd_sync_issues}[args.cmd](args)


if __name__ == "__main__":
    main()
