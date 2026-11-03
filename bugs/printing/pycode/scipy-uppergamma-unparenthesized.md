# SciPyPrinter prints uppergamma(a, x) as an unparenthesized product, so uppergamma(a, x)**2 evaluates wrongly

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, uppergamma, lambdify, N
>>> from sympy.printing.numpy import SciPyPrinter
>>> a, x = symbols('a x')
>>> print(SciPyPrinter().doprint(uppergamma(a, x)**2))
scipy.special.gamma(a)*scipy.special.gammaincc(a, x)**2
```

### Expected
```pycon
>>> import math
>>> math.isclose(lambdify((a, x), uppergamma(a, x)**2, 'scipy')(3.0, 1.5), float(N(uppergamma(3, 1.5)**2)))
True
```

### Why it is wrong
The power applies only to the `gammaincc` factor, so the lambdified function returns a wrong value whenever `uppergamma` is raised to a power or is the divisor of a quotient.

### Related
[sympy/sympy#16536](https://redirect.github.com/sympy/sympy/issues/16536)

### Notes on fixing
`sympy/printing/numpy.py:SciPyPrinter._print_uppergamma` returns `gamma(a)*gammaincc(a, x)` without parentheses; the caller treats it as an atom (function call). `_print_lowergamma` has the same defect (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
