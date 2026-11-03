# An element of A - B prints as (A - B)(1, 1), which does not compile

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol, fcode
>>> A, B, C = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2), MatrixSymbol('C', 2, 2)
>>> F = C[0, 0].subs(C, A - B)
>>> print(fcode(F, source_format='free'))
(A - B)(1, 1)
```

### Expected
```pycon
>>> A_ = lambda i, j: 10*i + j
>>> B_ = lambda i, j: 100*i + j
>>> eval(fcode(F, source_format='free'), {'A': A_, 'B': B_})
-90
```

### Why it is wrong
Fortran cannot subscript a parenthesized expression. gfortran 15.2 reports `Unclassifiable statement`. The element is `A(1, 1) - B(1, 1)`, which is what `fcode((A - B)[0, 0])` prints.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_MatrixElement` parenthesizes `expr.parent` and appends the subscript, which is only valid when the parent is a `MatrixSymbol`. For a matrix-expression parent it could print the evaluated entry (`expr.parent[expr.i, expr.j]`), or raise. Same pattern as in `c.py` and `jscode.py` (separate issues).

The output is asserted by `test_MatrixElement_printing` in `sympy/printing/tests/test_fortran.py` (added for [sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)).

The Expected block evaluates the free-form output as Python, with `A` and `B` as functions of the 1-based indices.

### Related
[sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
