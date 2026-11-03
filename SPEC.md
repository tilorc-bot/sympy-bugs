# Issue format

One issue = one bug. The issue states the bug as runnable doctest blocks, so that a bot
(`checker/bugcheck.py`) can verify it against SymPy master without anyone triaging it.

Write only what a person has to supply. Dates, versions, authorship, status, which printer
methods are involved, and whether a fix works are worked out by GitHub and the bot.

## Title

What goes wrong, specific enough to recognise in a list:
`latex() prints Mod(-x, y) and -Mod(x, y) identically`, not `LaTeX bug with Mod`.

## Sections

Sections are `### ` headings. **Kind**, **Actual**, **Expected** and **Why it is wrong**
are required; the rest are optional.

### Kind

One of:

| kind | meaning |
|---|---|
| `crash` | raises on valid input |
| `hang` | does not finish |
| `wrong-meaning` | output is valid but denotes a different expression (missing parentheses, wrong operator, dropped term) |
| `invalid-output` | output does not parse / compile in its target language (TeX error, C compile error, `eval` fails) |
| `lossy` | information is lost, e.g. `srepr` does not round-trip, two different objects print identically |
| `ignored-setting` | a printer setting has no effect where it should |
| `cosmetic` | correct but ugly or unidiomatic |
| `internal` | an internal helper returns the wrong thing (typically a root cause of other issues) |

### Actual

A ` ```pycon ` doctest showing what SymPy does **now**. It must be self-contained (imports,
symbols) and as small as possible. The bot checks that it still matches master exactly.

- Use `print(...)` for LaTeX/code strings so backslashes are not doubled.
- Show exceptions in doctest form; end the message with `...` where Python versions word
  it differently:
  ```pycon
  >>> latex(expr)
  Traceback (most recent call last):
  ...
  TypeError: _print_Foo() got an unexpected keyword argument 'exp'...
  ```
- Trailing whitespace on output lines is ignored; `...` matches anything (ELLIPSIS).

### Expected

A doctest that **fails on master and passes once the bug is fixed**. It runs in the same
session, after Actual, so it can reuse names.

Prefer a *property* that any correct fix satisfies over one exact output string, unless the
right output is unambiguous:

- two different expressions must print differently: `latex(a) != latex(b)` → `True`
- printed code computes the right value: `eval(pycode(e), {...})` vs `e.subs(...)`
- round trips: `eval(srepr(e)) == e`, `parse_expr(str(e)) == e`
- crash: `>>> _ = latex(expr)` (no output: passes iff no exception)
- the setting takes effect: `'{,}' in latex(e, decimal_separator='comma')`

### Why it is wrong

One or two sentences: why this is a bug and what it costs a user.

### Caused by

`#N` of the issue describing the root cause, if known. When the root cause gets a verified
fix, the bot reports which issues that fix also fixes, so a wrong link shows up.

### Related

Links to other issues here or in `sympy/sympy` (e.g. `sympy/sympy#23912`).

### Notes on fixing

Where the cause is (`file.py:function`), what a fix needs, why it is not simple.

### Workaround

A doctest that gets the right result on master today. The bot checks it passes.

### Suggested fix

A ` ```diff ` block made with `git diff` against SymPy master. Diffs in comments are checked
too. The bot applies each diff and checks:

1. it applies to master (otherwise: stale);
2. with it applied, Expected passes and Actual no longer matches;
3. the tests of the changed package pass (`sympy/<package>/tests/`);
4. which other open issues it also fixes, and whether it breaks any.

Passing these means "verified to work", not "reviewed".

## What the bot does

- On every new or edited issue and new comment: runs the blocks and any fixes, then
  rewrites one status comment and sets labels.
- Nightly: re-runs every open issue against the latest master. Issues whose Expected block
  now passes are closed, with the range of SymPy commits that fixed them.

| label | meaning |
|---|---|
| `reproduces` | Actual matches master, Expected fails |
| `fixed-on-master` | Expected passes on master (issue is closed) |
| `needs-update` | the blocks no longer describe master, or cannot run |
| `fix-verified` / `fix-failed` / `fix-stale` | state of the suggested fix(es) |
| `kind:*` | from the Kind section |
| `printer:*` | printers reached by the Actual block |
