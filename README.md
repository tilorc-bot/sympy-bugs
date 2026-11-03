# SymPy bug catalogue (pilot: printers)

A place to record **known SymPy bugs** without asking anyone to fix them.

The main [SymPy issue tracker](https://github.com/sympy/sympy/issues) is for problems people
hit while actually using SymPy. Bugs found by *looking* for them (reviews, fuzzing, AI audits)
are usually real, but there are far more of them than maintainers can triage. They go here
instead: each one is recorded, verified automatically, and kept up to date, and nobody is
expected to act on it.

## What an issue looks like

One bug per issue, written as runnable doctests ([SPEC.md](SPEC.md)):

- **Actual**: what SymPy does now. It must match master.
- **Expected**: what it should do. It must fail on master and pass once the bug is fixed.
- **Why it is wrong**, plus optional **Caused by**, **Related**, **Notes on fixing**,
  **Workaround** and **Suggested fix** (a `diff`).

## What is checked automatically

A bot ([`checker/bugcheck.py`](checker/bugcheck.py)) runs every issue against SymPy master,
on every edit and nightly, and keeps one status comment and the labels up to date:

- whether the bug still reproduces (`reproduces`), or the issue no longer describes master
  (`needs-update`);
- which printer methods the repro reaches (`printer:*` labels);
- whether the workaround works;
- for a suggested fix: whether it applies, fixes the issue, passes the tests of the changed
  package, and which **other** issues it also fixes (this is how shared root causes are found);
- nightly: issues whose Expected block passes on master are closed, citing the commit range.

## Using it

- **Hit a bug in real work?** Search here first. If it is listed, file it on the SymPy
  tracker with a link: real-world encounters are what make a catalogued bug worth fixing.
  A 👍 on the issue here records that it affected you.
- **Looking for something to fix?** Filter by `reproduces` + `fix-verified` for bugs with a
  working fix, or by `kind:crash` / `kind:wrong-meaning` for the most harmful ones.
- **Found bugs by searching?** File them here, one per issue, using the issue form.

Run the checker locally: `checker/Dockerfile` builds a network-less sandbox with a SymPy
checkout; `python checker/bugcheck.py check draft.md --sympy path/to/sympy` checks a draft.

## Security note

Issue bodies contain code that the workflows execute. The execution job has a read-only
token and no secrets; results are posted by a separate job that runs no issue code. Keep the
repository's issue creation limited to trusted people (it is private).

## Pilot contents

Seeded from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (an AI-generated
review of the printers), split into one issue per defect and verified against master.
