# SciPyPrinter prints lowergamma(a, x) as an unparenthesized product, so lowergamma(a, x)**2 evaluates wrongly

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, lowergamma, lambdify, N
>>> from sympy.printing.numpy import SciPyPrinter
>>> a, x = symbols('a x')
>>> print(SciPyPrinter().doprint(lowergamma(a, x)**2))
scipy.special.gamma(a)*scipy.special.gammainc(a, x)**2
>>> print(lambdify((a, x), lowergamma(a, x)**2, 'scipy')(3.0, 1.5))
0.0730790683906917
>>> print(N(lowergamma(3, 1.5)**2))
0.146158136781384
```

### Expected
```pycon
>>> import math, numpy, scipy.special
>>> ns = {'numpy': numpy, 'scipy': scipy, 'a': 3.0, 'x': 1.5}
>>> math.isclose(eval(SciPyPrinter().doprint(lowergamma(a, x)**2), ns), float(N(lowergamma(3, 1.5)**2)))
True
>>> math.isclose(lambdify((a, x), lowergamma(a, x)**2, 'scipy')(3.0, 1.5), float(N(lowergamma(3, 1.5)**2)))
True
```

### Why it is wrong
The power applies only to the `gammainc` factor, so the lambdified function returns a wrong value whenever `lowergamma` is raised to a power or is the divisor of a quotient.

### Related
[sympy/sympy#16536](https://redirect.github.com/sympy/sympy/issues/16536)

### Notes on fixing
`sympy/printing/numpy.py:SciPyPrinter._print_lowergamma` returns `gamma(a)*gammainc(a, x)` without parentheses; the caller treats it as an atom (function call). The mapping was added for [sympy/sympy#16536](https://redirect.github.com/sympy/sympy/issues/16536). `_print_uppergamma` has the same defect (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
