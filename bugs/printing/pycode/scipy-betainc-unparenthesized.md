# SciPyPrinter prints betainc(a, b, x, y) as an unparenthesized product, so betainc(...)**2 evaluates wrongly

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, betainc, lambdify, N
>>> from sympy.printing.numpy import SciPyPrinter
>>> a, b, x, y = symbols('a b x y')
>>> print(SciPyPrinter().doprint(betainc(a, b, x, y)**2))
(scipy.special.betainc(a, b, y) - scipy.special.betainc(a, b, x))             * scipy.special.beta(a, b)**2
```

### Expected
```pycon
>>> import math
>>> math.isclose(lambdify((a, b, x, y), betainc(a, b, x, y)**2, 'scipy')(2.0, 3.0, 0.2, 0.5), float(N(betainc(2, 3, 0.2, 0.5)**2)))
True
```

### Why it is wrong
The power applies only to the `beta(a, b)` factor, so the lambdified function returns a wrong value whenever `betainc` is raised to a power or is the divisor of a quotient. The printed code also contains a run of spaces from a backslash line continuation inside the f-string.

### Notes on fixing
`sympy/printing/numpy.py:SciPyPrinter._print_betainc` returns `(betainc(...) - betainc(...)) * beta(a, b)` without outer parentheses; the caller treats it as an atom (function call). `_print_betainc_regularized` has the same defect (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
