#!/usr/bin/env python3
"""bugcheck: verify bug-catalogue issues against SymPy master.

Every issue states its bug as runnable doctest blocks (see SPEC.md):

  ### Actual    -- what SymPy does now; must match master while the bug exists
  ### Expected  -- what it should do; must FAIL on master and pass once fixed
  ### Workaround (optional) -- must pass on master
  ### Suggested fix (optional) -- a `diff` block; applied to master and checked

Subcommands keep untrusted code away from credentials:

  fetch   (needs GH token)  download issue bodies, comments and previous status
  run     (no token)        execute everything against a SymPy checkout
  report  (needs GH token)  post/update the status comment, labels, close fixed
  check   (local)           run draft files (first line "# Title") and print verdicts

Only the standard library is used; `run`/`check` need SymPy importable from --sympy.
"""

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time

STATUS_MARKER = "<!-- bugcheck-status -->"
DATA_RE = re.compile(r"<!-- bugcheck-data (.*?) -->", re.S)
TIMEOUT = 60
TEST_TIMEOUT = 1500
TEST_WORKERS = int(os.environ.get("BUGCHECK_TEST_WORKERS", "2"))

SECTION_ALIASES = {
    "actual": "actual", "actual (sympy master)": "actual", "actual behaviour": "actual",
    "actual behavior": "actual", "expected": "expected", "expected behaviour": "expected",
    "expected behavior": "expected", "why it is wrong": "why", "why": "why",
    "kind": "kind", "caused by": "caused_by", "related": "related",
    "notes on fixing": "notes", "workaround": "workaround", "suggested fix": "fix",
    "source": "source",
}
KINDS = ["crash", "hang", "wrong-meaning", "invalid-output", "lossy", "ignored-setting",
         "cosmetic", "internal"]
ENV_ERRORS = ("NameError", "ImportError", "ModuleNotFoundError", "SyntaxError")

PRINTER_FAMILIES = [
    ("latex", r"Latex"), ("pretty", r"Pretty"), ("mathml", r"MathML"),
    ("srepr", r"^ReprPrinter$"), ("python", r"^PythonPrinter$"),
    ("pycode", r"PythonCode|NumPy|SciPy|Mpmath|CuPy|JAX|SymPyPrinter|Tensorflow|Torch|Cmath"),
    ("c", r"^C\d\dCodePrinter|^CCodePrinter|Cxx"), ("fortran", r"FCode|Fortran"),
    ("octave", r"Octave"), ("julia", r"Julia"), ("rust", r"Rust"), ("js", r"Javascript"),
    ("r", r"^RCode"), ("mathematica", r"MCode|Mathematica"), ("maple", r"Maple"),
    ("glsl", r"GLSL"), ("dot", r"Dot"), ("tree", r"Tree"), ("str", r"Str"),
]


# ---------------------------------------------------------------- parsing

def split_sections(body):
    """Split markdown on '### ' headings that are outside code fences."""
    body = (body or "").replace("\r\n", "\n")
    sections, name, buf, fence = {}, None, [], None
    for line in body.split("\n"):
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


def code_blocks(text, langs=None):
    out = []
    for m in FENCE.finditer(text or ""):
        lang = m.group(2).lower()
        if langs is None or lang in langs:
            out.append((lang, m.group(3)))
    return out


def doctest_source(text):
    """Concatenate all doctest-style blocks in a section."""
    blocks = [b for lang, b in code_blocks(text) if ">>>" in b and lang in
              ("", "pycon", "python", "py", "python3", "doctest", "ipython")]
    return "\n".join(blocks) + "\n" if blocks else ""


def diffs(text):
    return [b + "\n" for lang, b in code_blocks(text, {"diff", "patch"}) if "@@" in b]


CODE_SPANS = re.compile(r"(```.*?```|~~~.*?~~~|`[^`\n]*`)", re.S)
DIRECT_TRACKER = re.compile(
    r"(?<![\w/\[])sympy/sympy#\d+|(?<!redirect\.)github\.com/sympy/sympy/(?:issues|pull)/\d+")


def direct_tracker_links(body):
    """Tracker references that create backlinks (outside code, not via redirect.github.com)."""
    found = []
    for i, part in enumerate(CODE_SPANS.split(body or "")):
        if i % 2 == 0:
            # link text inside [..](https://redirect.github.com/...) is fine
            part = re.sub(r"\[[^\]]*\]\(https://redirect\.github\.com/[^)]*\)", "", part)
            found += DIRECT_TRACKER.findall(part)
    return found


def parse_issue(body, comments=()):
    s = split_sections(body)
    kind = re.sub(r"[`*\s]", "", s.get("kind", "").split("\n")[0]).lower()
    fixes = [{"source": "issue body", "diff": d} for d in diffs(s.get("fix", ""))]
    for c in comments:
        if STATUS_MARKER in (c.get("body") or ""):
            continue
        for d in diffs(c.get("body") or ""):
            fixes.append({"source": f"comment by @{c.get('user', '?')}", "url": c.get("url"),
                          "diff": d})
    return {
        "kind": kind if kind in KINDS else None,
        "kind_raw": kind,
        "actual": doctest_source(s.get("actual", "")),
        "expected": doctest_source(s.get("expected", "")),
        "workaround": doctest_source(s.get("workaround", "")),
        "fixes": fixes,
        "caused_by": [int(n) for n in re.findall(r"(?<![\w/])#(\d+)", s.get("caused_by", ""))],
        "tracker_links": direct_tracker_links(body),
    }


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
        self.records.append({"source": example.source, "ok": True})
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
    parser = doctest.DocTestParser()
    try:
        test = parser.get_doctest(src, globs, name, None, 0)
    except ValueError as e:
        return {"passed": False, "examples": [], "error": f"doctest parse error: {e}"}, globs
    runner = Runner()
    runner.run(test, clear_globs=False, out=lambda s: None)
    recs = runner.records
    return {"passed": bool(recs) and all(r["ok"] for r in recs), "examples": recs}, test.globs


job = json.loads(sys.stdin.read())
t0 = time.time()
res = {}
globs = {"__name__": "__bugcheck__"}
res["actual"], after_actual = run(job["actual"], globs, "actual")
res["expected"], _ = run(job["expected"], dict(after_actual), "expected")
actual_hits = dict(hits)
res["workaround"], _ = run(job.get("workaround", ""), dict(after_actual), "workaround")
res["printer_hits"] = actual_hits
res["seconds"] = round(time.time() - t0, 2)
sys.stdout.write("\x00BUGCHECK\x00" + json.dumps(res, default=str))
'''


def execute(parsed, sympy_dir, timeout=TIMEOUT):
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.abspath(sympy_dir) + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONHASHSEED"] = "0"  # some printers order terms by hash; keep runs reproducible
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    job = {k: parsed[k] for k in ("actual", "expected", "workaround")}
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


def first_failure(block):
    if not block:
        return None
    for ex in block["examples"]:
        if not ex["ok"]:
            return ex
    return None


def verdict(parsed, res):
    """Classify one run. Returns (verdict, explanation)."""
    if not parsed["actual"] or not parsed["expected"]:
        missing = [k for k in ("actual", "expected") if not parsed[k]]
        return "malformed", "No doctest (`>>>`) block found in: " + ", ".join(missing)
    if res.get("timeout"):
        if parsed["kind"] == "hang":
            return "reproduces", f"Still hangs (no result within {TIMEOUT}s)"
        return "timeout", f"Did not finish within {TIMEOUT}s"
    if res.get("crashed"):
        return "check-broken", "The checker process crashed: " + res["crashed"][-300:]
    a, e = res["actual"], res["expected"]
    if a.get("error") or e.get("error"):
        return "malformed", a.get("error") or e.get("error")
    fa = first_failure(a)
    if fa and fa.get("exc") in ENV_ERRORS:
        return "check-broken", f"Actual block raises {fa['exc']}, so it cannot run as written"
    if a["passed"] and not e["passed"]:
        return "reproduces", "Actual block matches master; expected block fails"
    if not a["passed"] and e["passed"]:
        return "fixed", "Expected block passes on master; actual block no longer matches"
    if not a["passed"] and not e["passed"]:
        return "changed", "Neither block matches master: behaviour changed, issue needs updating"
    return "check-broken", "Both blocks pass on master, so the expected block does not detect the bug"


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
        fams.remove("str")  # doctest echo uses the str printer for everything
    return fams[:3]


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
        # Run the whole tests/ directory of the changed package: a change to a shared
        # helper (e.g. precedence.py) shows up in the tests of the printers using it.
        d = os.path.dirname(path)
        while d and not os.path.isdir(os.path.join(sympy_dir, d, "tests")):
            d = os.path.dirname(d)
        if d:
            tests.append(os.path.join(d, "tests"))
    return sorted(set(tests))


def run_tests(sympy_dir, tests):
    if not tests:
        return {"ran": False}
    env = dict(os.environ)
    env.pop("GH_TOKEN", None)
    env.pop("GITHUB_TOKEN", None)
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                            "--no-header", "-n", str(TEST_WORKERS), *tests], cwd=sympy_dir, capture_output=True,
                           text=True, timeout=TEST_TIMEOUT, env=env)
    except subprocess.TimeoutExpired:
        return {"ran": True, "passed": False, "summary": "test run timed out", "tests": tests}
    tail = [l for l in p.stdout.strip().split("\n") if l.strip()][-1:] or ["(no output)"]
    failed = re.findall(r"^FAILED (\S+)", p.stdout, re.M)[:5]
    return {"ran": True, "passed": p.returncode == 0, "summary": tail[0].strip("= "),
            "failed": failed, "tests": tests}


def check_fix(fix, number, parsed_all, baseline, sympy_dir, jobs, scan_others=True):
    """Apply one diff and verify it. parsed_all: {number: parsed}; baseline: {number: verdict}."""
    out = {"source": fix["source"], "url": fix.get("url")}
    with tempfile.NamedTemporaryFile("w", suffix=".diff", delete=False) as f:
        f.write(fix["diff"])
        patch = f.name
    try:
        p = git(sympy_dir, "apply", "--check", patch, check=False)
        if p.returncode != 0:
            out["applies"] = False
            out["error"] = p.stderr.strip()[-400:]
            return out
        out["applies"] = True
        git(sympy_dir, "apply", patch)
        v, _ = verdict(parsed_all[number], execute(parsed_all[number], sympy_dir))
        out["fixes_this"] = v == "fixed"
        out["verdict_with_fix"] = v
        out["tests"] = run_tests(sympy_dir, touched_tests(sympy_dir, fix["diff"]))
        others = [n for n in parsed_all if n != number and baseline.get(n) in
                  ("reproduces", "fixed")] if scan_others else []
        with concurrent.futures.ThreadPoolExecutor(jobs) as ex:
            after = dict(zip(others, ex.map(
                lambda n: verdict(parsed_all[n], execute(parsed_all[n], sympy_dir))[0], others)))
        out["also_fixes"] = sorted(n for n in others
                                   if baseline[n] == "reproduces" and after[n] == "fixed")
        out["breaks"] = sorted(n for n in others
                               if baseline[n] == "fixed" and after[n] != "fixed")
        out["verified"] = bool(out["fixes_this"] and out["tests"].get("passed", True))
        return out
    finally:
        reset(sympy_dir)
        os.unlink(patch)


def sympy_head(sympy_dir):
    p = git(sympy_dir, "rev-parse", "HEAD", check=False)
    return p.stdout.strip()


def cmd_run(args):
    issues = json.load(open(args.issues))
    sympy_dir = args.sympy
    head = sympy_head(sympy_dir)
    parsed = {i["number"]: parse_issue(i["body"], i.get("comments", ())) for i in issues}
    # When checking fixes we need a baseline verdict for every open issue.
    pool = issues
    need_baseline = args.fixes == "full" and any(parsed[i["number"]]["fixes"] for i in issues)
    if args.all_issues and need_baseline:
        pool = json.load(open(args.all_issues))
        for i in pool:
            parsed.setdefault(i["number"], parse_issue(i["body"], i.get("comments", ())))

    def one(n):
        r = execute(parsed[n], sympy_dir)
        return n, r

    with concurrent.futures.ThreadPoolExecutor(args.jobs) as ex:
        raw = dict(ex.map(one, sorted({i["number"] for i in pool} | set(parsed))))
    baseline = {n: verdict(parsed[n], raw[n])[0] for n in raw}

    results = []
    for issue in issues:
        n = issue["number"]
        v, why = verdict(parsed[n], raw[n])
        r = raw[n]
        rec = {
            "number": n, "verdict": v, "explanation": why, "sympy": head,
            "checked": datetime.date.today().isoformat(),
            "kind": parsed[n]["kind"], "kind_raw": parsed[n]["kind_raw"],
            "actual_failure": first_failure(r.get("actual")),
            "expected_failure": first_failure(r.get("expected")),
            "workaround": None if not parsed[n]["workaround"] else
            {"passed": bool(r.get("workaround") and r["workaround"]["passed"]),
             "failure": first_failure(r.get("workaround"))},
            "printer_methods": sorted(r.get("printer_hits", {}), key=lambda k: -r["printer_hits"][k])[:12],
            "printers": printer_families(r.get("printer_hits", {})),
            "caused_by": parsed[n]["caused_by"],
            "tracker_links": parsed[n]["tracker_links"],
            "previous": issue.get("previous"),
            "fixes": [],
        }
        if args.fixes != "none" and parsed[n]["fixes"] and v == "reproduces":
            for fix in parsed[n]["fixes"][:3]:
                rec["fixes"].append(check_fix(fix, n, parsed, baseline, sympy_dir, args.jobs,
                                              scan_others=args.fixes == "full"))
                rec["fix_scope"] = args.fixes
        results.append(rec)
        print(f"#{n}: {v}", file=sys.stderr)
    json.dump(results, open(args.out, "w"), indent=1)


# ---------------------------------------------------------------- GitHub I/O

def gh(*args, input=None):
    """Run gh; back off and retry when GitHub's (secondary) rate limit kicks in."""
    wait = 60
    for attempt in range(8):
        p = subprocess.run(["gh", *args], input=input, capture_output=True, text=True)
        if p.returncode == 0:
            return p.stdout
        err = p.stderr.lower()
        if "rate limit" not in err or attempt == 7:
            raise RuntimeError(f"gh {' '.join(args[:3])}: {p.stderr.strip()[-500:]}")
        print(f"rate limited; sleeping {wait}s", file=sys.stderr)
        time.sleep(wait)
        wait = min(wait * 2, 900)


def gh_json(*args, input=None):
    out = gh(*args, input=input)
    return json.loads(out) if out.strip() else None


def paged(endpoint):
    items, page = [], 1
    while True:
        batch = gh_json("api", "-X", "GET", endpoint, "-f", "per_page=100", "-f", f"page={page}")
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def cmd_fetch(args):
    repo = args.repo
    if args.issue:
        raw = [gh_json("api", f"repos/{repo}/issues/{n}") for n in args.issue]
    else:
        raw = [i for i in paged(f"repos/{repo}/issues?state=open")
               if "pull_request" not in i]
    out = []
    for i in raw:
        comments = (paged(f"repos/{repo}/issues/{i['number']}/comments")
                    if i["comments"] and not args.bodies_only else [])
        previous = None
        for c in comments:
            if STATUS_MARKER in (c["body"] or ""):
                m = DATA_RE.search(c["body"])
                if m:
                    try:
                        previous = json.loads(m.group(1).replace("--\\>", "-->"))
                    except ValueError:
                        pass
        out.append({
            "number": i["number"], "title": i["title"], "state": i["state"],
            "body": i["body"] or "",
            "labels": [l["name"] for l in i["labels"]],
            "comments": [{"user": c["user"]["login"], "url": c["html_url"], "body": c["body"]}
                         for c in comments],
            "previous": previous,
        })
    json.dump(out, open(args.out, "w"), indent=1)
    print(f"fetched {len(out)} issues", file=sys.stderr)


VERDICT_LINE = {
    "reproduces": "🐛 **Reproduces** on SymPy master",
    "fixed": "✅ **Fixed** on SymPy master",
    "changed": "⚠️ **Behaviour changed** on SymPy master: neither block matches; the issue needs updating",
    "check-broken": "⚠️ **Check is broken**",
    "malformed": "⚠️ **Not checkable**",
    "timeout": "⚠️ **Timed out**",
}
VERDICT_LABEL = {"reproduces": "reproduces", "fixed": "fixed-on-master",
                 "changed": "needs-update", "check-broken": "needs-update",
                 "malformed": "needs-update", "timeout": "needs-update"}
MANAGED_PREFIXES = ("printer:", "kind:")
MANAGED = {"reproduces", "fixed-on-master", "needs-update", "fix-verified", "fix-failed",
           "fix-stale"}


def fence(text, lang=""):
    text = (text or "").rstrip("\n")
    ticks = "````" if "```" in text else "```"
    return f"{ticks}{lang}\n{text}\n{ticks}"


def render(rec, repo):
    sha = rec["sympy"][:10]
    commit = f"[`{sha}`](https://github.com/sympy/sympy/commit/{rec['sympy']})"
    head = f"{VERDICT_LINE[rec['verdict']]} @ {commit} (checked {rec['checked']})"
    bits = []
    for fx in rec["fixes"]:
        if fx.get("verified"):
            extra = ""
            if fx["also_fixes"]:
                extra = " · also fixes " + ", ".join(f"#{n}" for n in fx["also_fixes"])
            bits.append(f"🔧 suggested fix ({fx['source']}) verified{extra}")
        elif fx.get("applies") is False:
            bits.append(f"🔧 suggested fix ({fx['source']}) no longer applies")
        else:
            bits.append(f"🔧 suggested fix ({fx['source']}) does not pass its checks")
    if rec.get("workaround"):
        bits.append("🩹 workaround " + ("works" if rec["workaround"]["passed"] else "fails"))
    lines = [STATUS_MARKER, head + ("  \n" + " · ".join(bits) if bits else ""), ""]
    det = [f"**Verdict:** {rec['explanation']}."]
    if rec["verdict"] in ("changed", "fixed") and rec["actual_failure"]:
        f = rec["actual_failure"]
        det += ["", "First line of **Actual** that no longer matches:",
                fence(">>> " + f["source"].rstrip(), "pycon"),
                "Master now gives:", fence(f.get("got", ""))]
    if rec["verdict"] == "reproduces" and rec["expected_failure"]:
        f = rec["expected_failure"]
        det += ["", "**Expected** fails on master as it should:",
                fence(">>> " + f["source"].rstrip(), "pycon"),
                "Wanted:", fence(f.get("want", "")), "Got:", fence(f.get("got", ""))]
    if rec["verdict"] == "check-broken" and rec["actual_failure"]:
        f = rec["actual_failure"]
        det += ["", fence(">>> " + f["source"].rstrip() + "\n" + f.get("got", ""), "pycon")]
    if rec["printer_methods"]:
        det += ["", "**Printer methods reached by Actual:** " +
                ", ".join(f"`{m}`" for m in rec["printer_methods"])]
    for fx in rec["fixes"]:
        src = f"[{fx['source']}]({fx['url']})" if fx.get("url") else fx["source"]
        det += ["", f"**Suggested fix from {src}:**"]
        if not fx.get("applies"):
            det.append(f"- ❌ does not apply to master: `{fx.get('error', '')}`")
            continue
        det.append("- ✅ applies to master")
        det.append(("- ✅" if fx["fixes_this"] else "- ❌") +
                   f" this issue with the fix applied: {fx['verdict_with_fix']}")
        t = fx["tests"]
        if t.get("ran"):
            det.append(("- ✅" if t["passed"] else "- ❌") +
                       f" tests ({', '.join('`' + x + '`' for x in t['tests'])}): {t['summary']}")
            for name in t.get("failed", []):
                det.append(f"  - failed: `{name}`")
        else:
            det.append("- ➖ no SymPy tests found next to the changed files")
        if fx["also_fixes"]:
            det.append("- also fixes " + ", ".join(f"#{n}" for n in fx["also_fixes"]))
        if fx["breaks"]:
            det.append("- ❌ breaks (makes these reproduce again) " +
                       ", ".join(f"#{n}" for n in fx["breaks"]))
    if rec.get("workaround") and not rec["workaround"]["passed"] and rec["workaround"]["failure"]:
        f = rec["workaround"]["failure"]
        det += ["", "**Workaround** fails on master:",
                fence(">>> " + f["source"].rstrip() + "\n" + f.get("got", ""), "pycon")]
    if rec.get("tracker_links"):
        det += ["", "⚠️ Links to the SymPy tracker without `redirect.github.com` (they add a "
                "backlink on the tracker; see SPEC.md): " +
                ", ".join(f"`{t}`" for t in rec["tracker_links"][:5])]
    if rec["kind_raw"] and not rec["kind"]:
        det += ["", f"Unknown kind `{rec['kind_raw']}`; use one of: " + ", ".join(KINDS)]
    lines += ["<details><summary>Details</summary>", ""] + det + ["", "</details>", ""]
    lines.append("<sub>Posted by bugcheck. This comment is rewritten on every check; "
                 "see SPEC.md for what is verified.</sub>")
    data = {k: rec[k] for k in ("verdict", "sympy", "checked", "printers", "printer_methods")}
    data["last_reproduced"] = rec["sympy"] if rec["verdict"] == "reproduces" else \
        (rec.get("previous") or {}).get("last_reproduced")
    data["fixes"] = [{k: fx.get(k) for k in ("source", "applies", "verified", "also_fixes",
                                             "breaks")} for fx in rec["fixes"]]
    lines.append("<!-- bugcheck-data " + json.dumps(data).replace("-->", "--\\>") + " -->")
    return "\n".join(lines)


def wanted_labels(rec):
    labels = {VERDICT_LABEL[rec["verdict"]]}
    if rec["kind"]:
        labels.add("kind:" + rec["kind"])
    for p in rec["printers"]:
        labels.add("printer:" + p)
    if rec["fixes"]:
        if any(fx.get("verified") for fx in rec["fixes"]):
            labels.add("fix-verified")
        elif all(fx.get("applies") is False for fx in rec["fixes"]):
            labels.add("fix-stale")
        else:
            labels.add("fix-failed")
    return labels


def ensure_label(repo, name, cache):
    if name in cache:
        return
    color = {"reproduces": "d73a4a", "fixed-on-master": "0e8a16", "needs-update": "fbca04",
             "fix-verified": "1d76db", "fix-failed": "e99695", "fix-stale": "c5def5"}.get(
        name, "5319e7" if name.startswith("printer:") else "bfd4f2")
    try:
        gh("api", f"repos/{repo}/labels", "-f", f"name={name}", "-f", f"color={color}")
    except RuntimeError as e:
        if "already_exists" not in str(e):
            raise
    cache.add(name)


def fix_state(fixes):
    return [(f.get("source"), f.get("applies"), f.get("verified")) for f in fixes or []]


def changed(rec):
    prev = rec.get("previous")
    if not prev:
        return True
    return (prev.get("verdict") != rec["verdict"]
            or fix_state(prev.get("fixes")) != fix_state(rec["fixes"]))


def cmd_report(args):
    repo = args.repo
    results = json.load(open(args.results))
    issues = {i["number"]: i for i in json.load(open(args.issues))}
    existing = {l["name"] for l in paged(f"repos/{repo}/labels")}
    bots = set(args.bot.split(","))
    for rec in results:
        n = rec["number"]
        if args.only_changed and not changed(rec) and not (
                args.close_fixed and rec["verdict"] == "fixed"):
            continue
        body = render(rec, repo)
        comment_id, old_body = None, None
        for c in paged(f"repos/{repo}/issues/{n}/comments"):
            if STATUS_MARKER in (c["body"] or "") and c["user"]["login"] in bots:
                comment_id, old_body = c["id"], c["body"]
        payload = json.dumps({"body": body})
        wrote = True
        if comment_id and old_body.strip() == body.strip():
            wrote = False  # already up to date
        elif comment_id:
            gh("api", "-X", "PATCH", f"repos/{repo}/issues/comments/{comment_id}", "--input", "-",
               input=payload)
        else:
            gh("api", f"repos/{repo}/issues/{n}/comments", "--input", "-", input=payload)
        current = set(issues[n]["labels"])
        keep = {l for l in current if l not in MANAGED and not l.startswith(MANAGED_PREFIXES)}
        new = keep | wanted_labels(rec)
        if new != current:
            for l in new - existing:
                ensure_label(repo, l, existing)
            gh("api", "-X", "PUT", f"repos/{repo}/issues/{n}/labels", "--input", "-",
               input=json.dumps({"labels": sorted(new)}))
        if args.close_fixed and rec["verdict"] == "fixed" and issues[n]["state"] == "open":
            last = (rec.get("previous") or {}).get("last_reproduced")
            rng = (f" It last reproduced at `{last[:10]}`; the fix is in "
                   f"https://github.com/sympy/sympy/compare/{last[:12]}...{rec['sympy'][:12]}"
                   if last else "")
            msg = (f"Closing: the **Expected** block now passes on SymPy master "
                   f"@ `{rec['sympy'][:10]}`.{rng}")
            gh("api", f"repos/{repo}/issues/{n}/comments", "-f", f"body={msg}")
            gh("api", "-X", "PATCH", f"repos/{repo}/issues/{n}", "-f", "state=closed",
               "-f", "state_reason=completed")
        print(f"#{n}: reported {rec['verdict']}", file=sys.stderr)
        if wrote:
            time.sleep(args.delay)


# ---------------------------------------------------------------- local drafts

def read_draft(path):
    text = open(path, encoding="utf-8").read()
    first, _, body = text.partition("\n")
    return first.lstrip("# ").strip(), body


def cmd_check(args):
    parsed_all, names, baseline = {}, {}, {}
    for idx, path in enumerate(args.files, start=1):
        title, body = read_draft(path)
        parsed_all[idx] = parse_issue(body)
        names[idx] = path

    def one(i):
        r = execute(parsed_all[i], args.sympy)
        return i, r, verdict(parsed_all[i], r)

    out = []
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as ex:
        for i, r, (v, why) in ex.map(one, sorted(parsed_all)):
            baseline[i] = v
            rec = {"file": names[i], "verdict": v, "explanation": why,
                   "kind": parsed_all[i]["kind"], "kind_raw": parsed_all[i]["kind_raw"],
                   "printers": printer_families(r.get("printer_hits", {})),
                   "actual_failure": first_failure(r.get("actual")),
                   "expected_failure": first_failure(r.get("expected")),
                   "workaround_passed": (r.get("workaround") or {}).get("passed")}
            out.append(rec)
    if args.fixes:
        for rec, i in zip(out, sorted(parsed_all)):
            if parsed_all[i]["fixes"] and rec["verdict"] == "reproduces":
                rec["fixes"] = []
                for fx in parsed_all[i]["fixes"]:
                    res = check_fix(fx, i, parsed_all, baseline, args.sympy, args.jobs)
                    res["also_fixes"] = [names[n] for n in res.get("also_fixes", [])]
                    res["breaks"] = [names[n] for n in res.get("breaks", [])]
                    rec["fixes"].append(res)
    if args.json:
        json.dump(out, sys.stdout, indent=1)
        return
    for rec in out:
        print(f"{rec['verdict']:13} {rec['file']}  [{rec['kind'] or 'NO KIND: ' + str(rec['kind_raw'])}] {','.join(rec['printers'])}")
        if rec["verdict"] != "reproduces":
            print(f"    {rec['explanation']}")
            for key in ("actual_failure", "expected_failure"):
                f = rec[key]
                if f and (rec["verdict"] != "reproduces"):
                    print(f"    {key}: >>> {f['source'].strip()}")
                    print("      want: " + (f.get("want") or "").strip().replace("\n", "\n            "))
                    print("      got:  " + (f.get("got") or "").strip()[-600:].replace("\n", "\n            "))
        if rec["workaround_passed"] is False:
            print("    workaround FAILS on master")
        for fx in rec.get("fixes", []):
            print(f"    fix: applies={fx.get('applies')} fixes_this={fx.get('fixes_this')} "
                  f"tests={fx.get('tests', {}).get('summary')} verified={fx.get('verified')} "
                  f"also_fixes={fx.get('also_fixes')} breaks={fx.get('breaks')} {fx.get('error', '')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("fetch")
    p.add_argument("--repo", required=True)
    p.add_argument("--issue", type=int, nargs="*")
    p.add_argument("--bodies-only", action="store_true",
                   help="skip comments (enough for computing baselines)")
    p.add_argument("--out", required=True)
    p = sub.add_parser("run")
    p.add_argument("issues")
    p.add_argument("--all-issues", help="JSON of all open issues, for fix side effects")
    p.add_argument("--sympy", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--fixes", choices=["none", "basic", "full"], default="full",
                   help="basic: apply + this issue + tests; full: also re-run all open issues")
    p.add_argument("--jobs", type=int, default=2)
    p = sub.add_parser("report")
    p.add_argument("results")
    p.add_argument("--issues", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--bot", default="github-actions[bot],tilorc-bot",
                   help="comma-separated authors whose status comment is updated in place")
    p.add_argument("--close-fixed", action="store_true")
    p.add_argument("--only-changed", action="store_true",
                   help="skip issues whose verdict and fix state did not change")
    p.add_argument("--delay", type=float, default=0.0)
    p = sub.add_parser("check")
    p.add_argument("files", nargs="+")
    p.add_argument("--sympy", required=True)
    p.add_argument("--fixes", action="store_true")
    p.add_argument("--json", action="store_true")
    p.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    {"fetch": cmd_fetch, "run": cmd_run, "report": cmd_report, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    main()
