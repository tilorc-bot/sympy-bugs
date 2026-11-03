# Piecewise(...) raises "Unsupported ... ExprCondPair"

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Piecewise
>>> from sympy.printing.mathematica import mathematica_code
>>> x, y = symbols('x y')
>>> mathematica_code(Piecewise((x, x > 0), (y, True)))
Traceback (most recent call last):
...
sympy.printing.codeprinter.PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.mathematica.MCodePrinter'>: <class 'sympy.functions.elementary.piecewise.ExprCondPair'>...
```

### Why it is wrong
Mathematica has a direct equivalent, `Piecewise[{{x, x > 0}}, y]`, and `Piecewise` results are common (e.g. from `integrate`), but printing them fails.

### Notes on fixing
`sympy/printing/mathematica.py:MCodePrinter` has no `_print_Piecewise`; the generic `_print_Function` fallback prints `Piecewise[...]` and fails on the `ExprCondPair` arguments. A `_print_Piecewise` should print `Piecewise[{{e1, c1}, {e2, c2}, ...}, default]`, using the `(expr, True)` pair as the default.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
