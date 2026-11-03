# An element of A - B prints as A - B[0][0]

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, glsl_code
>>> A, B, C = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2), MatrixSymbol('C', 2, 2)
>>> F = C[0, 0].subs(C, A - B)
>>> print(glsl_code(F))
A - B[0][0]
```

### Expected
```pycon
>>> eval(glsl_code(F), {'A': [[5, 0], [0, 0]], 'B': [[2, 0], [0, 0]]})
3
```

### Why it is wrong
The index binds to `B` only, so the code means `A - B[0][0]` (a matrix minus a scalar) instead of the element `A[0][0] - B[0][0]`.

### Notes on fixing
`sympy/printing/glsl.py:GLSLPrinter._print_MatrixElement` formats `expr.parent` without parenthesizing it. For a matrix-expression parent it could print the evaluated entry (`expr.parent[expr.i, expr.j]` gives `A[0, 0] - B[0, 0]`), or parenthesize (`(A - B)[0][0]` is valid GLSL for `mat2`). Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
