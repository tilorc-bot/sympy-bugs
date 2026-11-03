# SymPy bug catalogue (pilot: printers)

**Browse it: https://tilorc-bot.github.io/sympy-bugs/**

A place to record **known SymPy bugs** without asking anyone to fix them.

The main [SymPy issue tracker](https://redirect.github.com/sympy/sympy/issues) is for
problems people hit while actually using SymPy. Bugs found by *looking* for them (reviews,
fuzzing, AI audits) are usually real, but there are far more of them than maintainers can
triage. They go here instead: each one is recorded as a file, verified automatically, and
kept up to date, and nobody is expected to act on it.

## Bugs as files, read as issues

The files under `bugs/` are the source of truth. Every bug file also has a GitHub issue,
opened and kept up to date by the catalogue's workflow (`github-actions[bot]`): the issue shows
the report with its current status on top (reproduces / fixed, verified fix, which other bugs
it is the root cause of) and labels for kind, printer, status, fix and priority. When the file
or its status changes, the issue is regenerated; when SymPy fixes the bug, the issue is closed.
Comments and reactions on issues are kept, so issues are the place to discuss a bug or say
"I hit this too" (👍). To change the bug itself, edit its file in a pull request.

## Layout

```
bugs/printing/<printer>/<slug>.md   one bug per file; its path (without .md) is its ID
status.json                         generated: result of checking every bug against master
checker/bugcheck.py                 the checker (standard library only)
checker/site.html                   template for the browsable catalogue page
SPEC.md                             the bug file format
```

Each bug file states the bug as runnable doctests ([SPEC.md](SPEC.md)):

- **Actual**: what SymPy does now. It must match master.
- **Expected**: what it should do. It must fail on master and pass once the bug is fixed.
- **Why it is wrong**, plus optional **Caused by**, **Related**, **Notes on fixing**,
  **Workaround**, **Suggested fix** (a `diff`) and **Encountered** (real-world reports).

## What is checked automatically

- **On every pull request** that adds or changes bug files: each changed bug must reproduce
  on SymPy master (Actual matches, Expected fails) and follow the format. Suggested fixes are
  applied and checked: do they fix the bug, do the tests of the changed SymPy package pass,
  and which **other** catalogued bugs do they also fix (this is how shared root causes are
  found). The PR gets a comment with the results, including possible duplicates.
- **After merging, and nightly**: every bug is re-run against the latest SymPy master and
  `status.json` is updated in one commit. Bugs whose Expected block starts passing are marked
  fixed, with the range of SymPy commits that fixed them. Suggested fixes that no longer
  apply are marked stale.

Nothing here creates issues, comments or backlinks on the SymPy tracker.

After each update, the issues are synced: new bug files get an issue, changed ones get
their issue regenerated, fixed ones get it closed, and removed files get it closed as not planned.

## Using it

- **Hit a bug in real work?** Search the catalogue first. If it is listed, file it on the
  SymPy tracker and link the catalogue entry, then add your report under **Encountered** in
  the bug file: real-world encounters are what raise a catalogued bug's priority.
- **Looking for something to fix?** Bugs with a verified suggested fix, or crashes and
  wrong-meaning bugs in widely used printers, are the best candidates.
- **Found bugs by searching?** Add them as files in a pull request, one file per bug.

Check a bug file locally:

```
python checker/bugcheck.py check bugs/printing/latex/my-bug.md --root bugs --sympy path/to/sympy
```

`checker/Dockerfile` builds a network-less sandbox with a SymPy checkout for doing this safely.

## Security note

Bug files contain code that the workflows execute. The jobs that execute it have a read-only
token; results are posted or committed by separate jobs that run no bug code.

## Pilot contents

Seeded from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (an
AI-generated review of the printers) and its follow-up comment, split into one file per
defect and verified against master. Findings that master has already fixed were left out.
