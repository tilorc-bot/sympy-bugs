# SymPyPrinter prints Rationals as Python divisions, so lambdify(..., 'sympy') turns x/2 into 0.5*x

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, lambdify
>>> from sympy.printing.pycode import SymPyPrinter
>>> x, y = symbols('x y')
>>> print(SymPyPrinter().doprint(x/2))
(1/2)*x
>>> lambdify(x, x/2, 'sympy')(y)
0.5*y
```

### Expected
```pycon
>>> import sympy
>>> eval(SymPyPrinter().doprint(x/2), {'sympy': sympy, 'x': y}) == y/2
True
>>> lambdify(x, x/2, 'sympy')(y) == y/2
True
```

### Why it is wrong
The target of `SymPyPrinter` is SymPy itself, but `1/2` in Python is the float `0.5`, so exact rational coefficients become floats and the result is no longer exact.

### Related
[sympy/sympy#25360](https://redirect.github.com/sympy/sympy/issues/25360)

### Notes on fixing
`SymPyPrinter` (`sympy/printing/pycode.py`) has no `_print_Rational`; it falls back to the generic `p/q`. It should print e.g. `sympy.Rational(1, 2)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
