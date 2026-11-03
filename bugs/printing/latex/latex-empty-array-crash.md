# An empty Array raises IndexError

### Kind
crash

### Actual
```pycon
>>> from sympy import Array, latex
>>> latex(Array([]))
Traceback (most recent call last):
...
IndexError: list index out of range
>>> latex(Array([], (2, 0)))
Traceback (most recent call last):
...
IndexError: list index out of range
```

### Expected
```pycon
>>> _ = latex(Array([]))
>>> _ = latex(Array([], (2, 0)))
```

### Why it is wrong
Printing must not fail for a valid object; empty arrays are valid and `str` prints them.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_NDimArray` builds nested row strings by iterating over all indices and finally reads `level_str[0][0]`; when any dimension is 0 nothing is appended, so the lookup fails. `Array([], (0, 2))` fails the same way. The pretty printer has the same crash in `_print_NDimArray` (reported separately).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
