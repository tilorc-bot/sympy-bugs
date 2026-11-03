# latex() does not bracket Add arguments of TensorProduct: TensorProduct(A + B, C) prints as A + B \otimes C

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, latex
>>> from sympy.tensor.functions import TensorProduct
>>> A, B, C = [MatrixSymbol(s, 2, 2) for s in 'ABC']
>>> print(latex(TensorProduct(A + B, C)))
A + B \otimes C
>>> from sympy.diffgeom.rn import R2_r
>>> from sympy.diffgeom import TensorProduct as DTP
>>> print(latex(DTP(R2_r.dx + R2_r.dy, R2_r.dx)))
\operatorname{d}x + \operatorname{d}y \otimes \operatorname{d}x
```

### Expected
```pycon
>>> latex(TensorProduct(A + B, C)) != latex(A + TensorProduct(B, C))
True
```

### Why it is wrong
`A + B \otimes C` reads as `A + (B ⊗ C)`, which is a different tensor from `(A + B) ⊗ C`; both print the same.

### Notes on fixing
`LatexPrinter._print_TensorProduct` (`sympy/printing/latex.py`) joins `self._print(a)` for every argument with ` \otimes `; it should parenthesize arguments of lower precedence (`self.parenthesize(a, precedence_traditional(expr))`). It is used by both `sympy.tensor.functions.TensorProduct` and `sympy.diffgeom.TensorProduct`. `_print_WedgeProduct` has the same code (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
