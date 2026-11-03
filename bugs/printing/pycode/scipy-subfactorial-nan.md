# lambdify(k, subfactorial(k), 'scipy') returns nan

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, subfactorial, lambdify
>>> from sympy.printing.numpy import SciPyPrinter
>>> k = symbols('k')
>>> print(SciPyPrinter().doprint(subfactorial(k)))
(numpy.exp(-1)*scipy.special.gamma(k + 1)*scipy.special.gammaincc(k + 1, -1))
>>> print(lambdify(k, subfactorial(k), 'scipy')(3))
nan
```

### Expected
```pycon
>>> bool(abs(lambdify(k, subfactorial(k), 'scipy')(3) - 2) < 1e-9)
True
```

### Why it is wrong
`subfactorial(3)` is 2, but the generated code evaluates `scipy.special.gammaincc` at `x = -1`, outside its domain (`x >= 0`), which returns `nan`.

### Notes on fixing
`sympy/printing/codeprinter.py` rewrites `subfactorial` to `uppergamma` (`_rewriteable_functions`), and `SciPyPrinter._print_uppergamma` (`sympy/printing/numpy.py`) maps `uppergamma(a, x)` to `gamma(a)*gammaincc(a, x)`, which is only valid for `x >= 0`. Either give `SciPyPrinter` a direct `subfactorial` printer or avoid the rewrite for SciPy.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
