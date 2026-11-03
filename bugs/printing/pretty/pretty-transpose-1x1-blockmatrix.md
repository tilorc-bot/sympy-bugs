# pretty() of the transpose of a 1x1 BlockMatrix of a sum prints like A + Bᵀ

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, BlockMatrix, Transpose, MatAdd, pretty
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> print(pretty(Transpose(BlockMatrix([[A + B]])), use_unicode=True))
     T
A + B
>>> print(pretty(MatAdd(A, Transpose(B)), use_unicode=True))
     T
A + B
```

### Expected
```pycon
>>> pretty(Transpose(BlockMatrix([[A + B]])), use_unicode=True) != pretty(MatAdd(A, Transpose(B)), use_unicode=True)
True
```

### Why it is wrong
`(A + B)ᵀ` and `A + Bᵀ` are different matrices but print the same.

### Notes on fixing
`_print_Transpose` and `_print_Adjoint` in `sympy/printing/pretty/pretty.py` skip parentheses for any `BlockMatrix`, assuming it prints as a bracketed grid, but `_print_BlockMatrix` prints a 1x1 block matrix as its only block. `Adjoint(BlockMatrix([[A + B]]))` prints `A + B†` in the same way.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
