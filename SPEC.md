# Bug file format

One file = one bug, at `bugs/<area>/<topic>/<slug>.md` (e.g.
`bugs/printing/latex/latex-mod-negative-arg.md`). The path without `.md` is the bug's ID, so
pick a slug that says what is wrong and do not rename files casually.

The file states the bug as runnable doctest blocks, so that `checker/bugcheck.py` can verify
it against SymPy master without anyone triaging it. Write only what a person has to supply:
dates and authorship come from git; status, the printer methods involved, and whether a fix
works are computed into `status.json`.

## Title

The first line is `# Title`: what goes wrong, specific enough to recognise in a list:
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
| `internal` | an internal helper returns the wrong thing (typically a root cause of other bugs) |

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
- The checker runs Python 3.13 with `PYTHONHASHSEED=0`, so term order is reproducible.

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

**C, C++ and Rust code can be compiled and run.** For bugs in those printers, prove the claim
with the compiler instead of only inspecting the string (`checker/lib/codecheck.py`, built on
the `check_printed_code` helper from tilorc-bot/sympy PR #60):

```pycon
>>> from codecheck import compiles, compile_errors, run_code
>>> print(compile_errors('c', ccode(Mod(i, j)), i=float, j=float))   # invalid code
error: invalid operands to binary % (have 'double' and 'double')
>>> run_code('c', ccode(Mod(x, y)), x=-1.0, y=3.0), float(Mod(-1, 3))   # wrong value
(-1.0, 2.0)
```

Expected then says `compiles(...)` is `True`, or that `run_code(...)` equals SymPy's value.
Languages: `'c'` (C99), `'c89'`, `'c11'`, `'c++'`, `'rust'`. Symbol types are keywords
(`x=float`, `i=int`, `b=bool`, `A=[float]`); for `run_code` the values give the types. Bugs
verified this way get `"evidence": "compiled"` in `status.json` and the
`verified-by-compiler` label on their issue. Compiler messages differ between versions, so
match them with `...` or with `'fragment' in compile_errors(...)`.

### Why it is wrong

One or two sentences: why this is a bug and what it costs a user.

### Caused by

A relative link to the bug file describing the root cause, if known, e.g.
`[rc-precedence-traditional-mul](../precedence/rc-precedence-traditional-mul.md)`. When the
root cause gets a verified fix, the checker reports which bugs that fix also fixes, so a
wrong link shows up. A root cause is just another bug, usually written against the internal
helper that is wrong (kind `internal`).

### Related

Relative links to other bug files, and links to the SymPy tracker.

**Link to the SymPy tracker through `redirect.github.com`**, e.g.
`[sympy/sympy#23912](https://redirect.github.com/sympy/sympy/issues/23912)`. The link works
the same for readers, but GitHub does not add a "mentioned this issue" entry to the tracker
issue. A plain `sympy/sympy#N` or `github.com/sympy/sympy/issues/N` link does, and that
backlink stays even if the text is edited later. The catalogue should not add noise to the
tracker; link an issue there deliberately, by filing or commenting on the tracker itself.

### Notes on fixing

Where the cause is (`file.py:function`), what a fix needs, why it is not simple. Name
functions so the checker can find them: `sympy/printing/latex.py:LatexPrinter._print_Mod`,
`LatexPrinter._print_Mod`, or `_print_Mod` next to the file it is in. The checker records the
ones the Actual block runs as the bug's location, and warns about named functions that never
run (`location_warnings`).

### Workaround

A doctest that gets the right result on master today. The bot checks it passes.

### Suggested fix

A ` ```diff ` block made with `git diff` against SymPy master. The checker applies each diff
and checks:

1. it applies to master (otherwise: stale);
2. with it applied, Expected passes and Actual no longer matches;
3. the tests of the changed package pass (`sympy/<package>/tests/`);
4. which other catalogued bugs it also fixes, and whether it breaks any.

Passing these means "verified to work", not "reviewed".

### Encountered

One line per real-world report of this bug: a link to a SymPy tracker issue, forum post or
downstream bug where someone hit it while actually using SymPy. This is the strongest input
to the priority score.

## What the checker records

`status.json` has one entry per bug, updated on every merge and nightly:

| field | meaning |
|---|---|
| `verdict` | `reproduces` (Actual matches master, Expected fails), `fixed` (Expected passes), `changed` (neither matches: the file needs updating), `check-broken`, `malformed`, `timeout` |
| `sympy`, `checked` | the SymPy commit and date of the check |
| `first_reproduced`, `last_reproduced`, `fixed_between` | SymPy commits; `fixed_between` brackets the commit that fixed it |
| `printers`, `printer_methods` | printers and `_print_*` methods the Actual block reaches |
| `locations` | where in SymPy's code the bug lives, most certain first (below) |
| `location_warnings` | functions named in Notes on fixing that never run in Actual, or do not exist |
| `examples` | every Actual and Expected example with what master printed |
| `fixes` | per suggested fix: `applies`, `fixes_this`, `tests`, `verified`, `also_fixes`, `breaks` |
| `problems` | format problems (missing sections, unknown kind, direct tracker links, broken links) |

A pull request fails its check if a changed bug does not reproduce on master or has problems
(location warnings do not fail it).

### Locations

`locations` lists 1 to 3 places in SymPy's source, line numbers at the checked commit
(`sympy`), paths relative to the SymPy root:

```json
{"path": "sympy/printing/latex.py", "start": 1883, "end": 1888,
 "function": "LatexPrinter._print_Mod", "how": "fix", "confirmed": true}
```

`function` is the qualified name of the enclosing function, or of a variable assigned in a
module or class body (`known_fcns_src1`, `C89CodePrinter.type_mappings`) when the lines are
one; `null` elsewhere at module level. `how` says where the location comes from, most
certain first:

| how | lines | confirmed |
|---|---|---|
| `fix` | the original lines a suggested fix that applies changes, per enclosing function | the fix is verified |
| `raises` | `crash` only: the innermost line inside `sympy/` of the exception an Actual example raises | always |
| `notes` | a function (or module/class variable) named in Notes on fixing, whole definition | the function ran during Actual (never for a variable) |
| `reached` | only when there is no `fix`, `raises` or confirmed `notes` location: up to two printer methods Actual reached that the fewest bugs reach, preferring the files the notes name and skipping generic ones (`_print_Symbol`, `_print_Add`, `emptyPrinter`, ...) unless nothing else ran | never |

Duplicates (same function) keep the first, more certain entry; unconfirmed `notes` come last.
