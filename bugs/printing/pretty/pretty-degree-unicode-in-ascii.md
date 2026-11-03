# pretty(use_unicode=False) prints the non-ASCII degree sign for units.degree

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.physics.units import degree
>>> print(pretty(30*degree, use_unicode=False))
30°
```

### Expected
```pycon
>>> pretty(30*degree, use_unicode=False).isascii()
True
```

### Why it is wrong
`use_unicode=False` is meant to produce pure ASCII (for terminals, logs and files without Unicode support), but `°` (U+00B0) is not ASCII.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_Quantity` deliberately uses `chr(176)` in the non-Unicode branch, and `prettyForm.__mul__` (`sympy/printing/pretty/stringpict.py`) only omits the `*` before the degree sign by comparing against `"\N{DEGREE SIGN}"`. An ASCII fallback (e.g. `deg` or `degree`, with the usual `*`) is needed in both places.

The test `test_degree_printing` in `sympy/printing/pretty/tests/test_pretty.py` asserts the buggy output: its `pretty()` helper uses `use_unicode=False` and expects `'90°'`, `'x°'` and `'cos(x° + 90°)'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
