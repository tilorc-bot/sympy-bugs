# SciPyPrinter prints sparse matrix entries with str(), so lambdify fails with NameError

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, exp, SparseMatrix, lambdify
>>> from sympy.printing.numpy import SciPyPrinter
>>> x = symbols('x')
>>> print(SciPyPrinter().doprint(SparseMatrix([[exp(x), 0], [0, 1]])))
scipy.sparse.coo_array(([exp(x), 1], ([0, 1], [0, 1])), shape=(2, 2))
>>> lambdify(x, SparseMatrix([[exp(x), 0], [0, 1]]), 'scipy')(1.0)
Traceback (most recent call last):
...
NameError: name 'exp' is not defined
```

### Expected
```pycon
>>> import math
>>> m = lambdify(x, SparseMatrix([[exp(x), 0], [0, 1]]), 'scipy')(1.0)
>>> math.isclose(m.toarray()[0, 0], math.e)
True
```

### Why it is wrong
The entries are inserted as SymPy `str()` output (`exp(x)`) instead of being printed as NumPy code (`numpy.exp(x)`), so any non-constant sparse matrix produces unusable code.

### Notes on fixing
`sympy/printing/numpy.py:SciPyPrinter._print_SparseRepMatrix` formats the Python lists `data`, `i`, `j` directly into the string; the entries of `data` need to go through `self._print`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
