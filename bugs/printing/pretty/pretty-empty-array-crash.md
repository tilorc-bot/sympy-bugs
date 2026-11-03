# pretty() of an empty Array raises IndexError

### Kind
crash

### Actual
```pycon
>>> from sympy import Array, pretty
>>> pretty(Array([]))
Traceback (most recent call last):
...
IndexError: list index out of range
```

### Why it is wrong
`Array([])` is a valid (shape `(0,)`) array and `str` prints it as `[]`, but the pretty printer fails on it.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_NDimArray` builds nested lists by iterating over all index tuples and then takes `level_str[0][0]`, which does not exist when a dimension is 0. Arrays with a zero in their shape (`Array([], (0, 2))`, `Array([], (2, 0))`) need a special case. `LatexPrinter._print_NDimArray` (`sympy/printing/latex.py`) has the same `level_str[0][0]` crash.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
