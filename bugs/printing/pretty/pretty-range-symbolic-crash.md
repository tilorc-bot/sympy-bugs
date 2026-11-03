# pretty() of a Range with a symbolic stop raises ValueError

### Kind
crash

### Actual
```pycon
>>> from sympy import Symbol, Range, pretty
>>> m = Symbol('m')
>>> pretty(Range(0, m))
Traceback (most recent call last):
...
ValueError: Invalid method for symbolic Range
```

### Why it is wrong
`Range(0, m)` is a valid object (`str` prints `Range(0, m)`), but the pretty printer cannot display it, so `pprint` and the interactive Unicode display of any expression containing it fail.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_Range` calls `len(s)` and iterates `s` to pick the printed elements; both raise for a Range with symbolic bounds. A symbolic Range needs a separate branch, e.g. printing `{0, 1, ..., m - 1}` from `s.start`, `s.start + s.step` and `s.stop - s.step` (or falling back to the `Range(0, m)` form).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
