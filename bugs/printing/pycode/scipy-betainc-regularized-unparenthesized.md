# SciPyPrinter prints betainc_regularized(a, b, x, y) as an unparenthesized difference, so 2*betainc_regularized(...) evaluates wrongly

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, betainc_regularized, lambdify, N
>>> from sympy.printing.numpy import SciPyPrinter
>>> a, b, x, y = symbols('a b x y')
>>> print(SciPyPrinter().doprint(2*betainc_regularized(a, b, x, y)))
2*scipy.special.betainc(a, b, y) - scipy.special.betainc(a, b, x)
```

### Expected
```pycon
>>> import math
>>> math.isclose(lambdify((a, b, x, y), 2*betainc_regularized(a, b, x, y), 'scipy')(2.0, 3.0, 0.2, 0.5), float(N(2*betainc_regularized(2, 3, 0.2, 0.5))))
True
```

### Why it is wrong
The factor 2 multiplies only the first term of the difference, so the lambdified function returns a wrong value whenever `betainc_regularized` is multiplied, negated, raised to a power or subtracted.

### Notes on fixing
`sympy/printing/numpy.py:SciPyPrinter._print_betainc_regularized` returns `betainc(a, b, y) - betainc(a, b, x)` without parentheses; the caller treats it as an atom (function call). `_print_betainc` has the same defect (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
