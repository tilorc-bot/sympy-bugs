# jscode() indexes a parenthesized matrix expression: (A - B)[0]

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, jscode
>>> A, B, C = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2), MatrixSymbol('C', 2, 2)
>>> F = C[0, 0].subs(C, A - B)
>>> print(jscode(F))
(A - B)[0]
```

### Expected
```pycon
>>> eval(jscode(F), {'A': [5, 0, 0, 0], 'B': [2, 0, 0, 0]})
3
```

### Why it is wrong
In JavaScript `A - B` on two arrays is `NaN`, so `(A - B)[0]` is `undefined` instead of `A[0] - B[0]` (checked with node 24). The code runs but silently produces the wrong value.

### Notes on fixing
`sympy/printing/jscode.py:JavascriptCodePrinter._print_MatrixElement` parenthesizes `expr.parent` and appends a flat index, which is only valid when the parent is a `MatrixSymbol`. For a matrix-expression parent it could print the evaluated entry (`expr.parent[expr.i, expr.j]` gives `A[0, 0] - B[0, 0]`), or raise. Same pattern as in `c.py` and `fortran.py` (separate issues).

The output is asserted by `test_MatrixElement_printing` in `sympy/printing/tests/test_jscode.py` (added for [sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)).

### Related
[sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
