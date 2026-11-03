# latex(MatPow(Identity(2), 2)) wraps \mathbb{I} in redundant parentheses

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import Identity, MatPow, latex
>>> print(latex(MatPow(Identity(2), 2)))
\left(\mathbb{I}\right)^{2}
```

### Expected
```pycon
>>> print(latex(MatPow(Identity(2), 2)))
\mathbb{I}^{2}
```

### Why it is wrong
`\mathbb{I}` is a single symbol, so the parentheses are unnecessary; a `MatrixSymbol` base prints as `A^{2}`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_MatPow` parenthesizes every base that is a matrix expression but not a `MatrixSymbol`; atom-like matrix expressions (`Identity`, `ZeroMatrix`, `OneMatrix`) should be treated like symbols, e.g. by using `self.parenthesize(base, PRECEDENCE['Pow'])`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
