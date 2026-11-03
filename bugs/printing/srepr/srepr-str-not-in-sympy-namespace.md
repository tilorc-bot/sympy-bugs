# srepr() of MatrixSymbol uses Str, which `from sympy import *` does not provide

### Kind
lossy

### Actual
```pycon
>>> from sympy import MatrixSymbol, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> X = MatrixSymbol('X', 2, 2)
>>> srepr(X)
"MatrixSymbol(Str('X'), Integer(2), Integer(2))"
>>> eval(srepr(X), ns)
Traceback (most recent call last):
...
NameError: name 'Str' is not defined
```

### Expected
```pycon
>>> eval(srepr(X), ns) == X
True
```

### Why it is wrong
`srepr` promises `eval(srepr(expr)) == expr` in the scope of `from sympy import *`, but every object with a `Str` argument (MatrixSymbol, BlockMatrix, CoordSys3D, Category, ...) fails to evaluate there.

### Notes on fixing
`ReprPrinter._print_Str` (`sympy/printing/repr.py`) prints `Str(...)`, but `Str` (`sympy/core/symbol.py`) is not exported from `sympy`. Either export it, or print the name as a plain Python string where the constructor accepts one (`MatrixSymbol('X', 2, 2)`).
The tests do not notice because `sympy/printing/tests/test_repr.py` adds `Str` to the evaluation namespace by hand (`ENV = {"Str": Str}`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
