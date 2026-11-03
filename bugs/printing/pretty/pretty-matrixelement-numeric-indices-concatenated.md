# MatrixSymbol elements A[1, 23] and A[12, 3] print identically as A₁₂₃

### Kind
lossy

### Actual
```pycon
>>> from sympy import MatrixSymbol, pretty
>>> A = MatrixSymbol('A', 30, 30)
>>> print(pretty(A[1, 23], use_unicode=True))
A₁₂₃
>>> print(pretty(A[12, 3], use_unicode=True))
A₁₂₃
```

### Expected
```pycon
>>> pretty(A[1, 23], use_unicode=True) != pretty(A[12, 3], use_unicode=True)
True
```

### Why it is wrong
Two different matrix entries print the same as soon as an index has more than one digit.

### Notes on fixing
`PrettyPrinter._print_MatrixElement` in `sympy/printing/pretty/pretty.py` prints `Symbol(expr.parent.name + '_%d%d' % (expr.i, expr.j))` for numeric indices, concatenating the digits. A separator (e.g. `A_{1,23}` style `₁,₂₃`) is needed when any index has more than one digit.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
