# A slice of MatrixSymbol('A^b') does not parenthesize the superscripted name

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import MatrixSymbol, latex
>>> Ab = MatrixSymbol('A^b', 2, 2)
>>> print(latex(Ab[0:1, 0:1]))
A^{b}\left[:1, :1\right]
>>> print(latex(Ab.T))
\left(A^{b}\right)^{T}
```

### Expected
```pycon
>>> latex(Ab[0:1, 0:1]).startswith(r'\left(A^{b}\right)')
True
```

### Why it is wrong
`Transpose`, `Adjoint` and `MatPow` wrap a parent whose printed name contains `^` in parentheses so that the following postfix is not read as applying to the superscript; the slice printer does not, so `A^{b}[:1, :1]` is inconsistent with `\left(A^{2}\right)\left[:1, :1\right]` printed for a slice of `MatPow(A, 2)`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_MatrixSlice` only uses `self.parenthesize(expr.parent, PRECEDENCE["Atom"], strict=True)`, which does not catch symbol names with a superscript; it needs the same `'^' in s` check as `_print_Transpose` / `_print_MatPow`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
