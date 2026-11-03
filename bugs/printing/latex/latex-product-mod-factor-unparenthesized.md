# Product(Mod(n, 3), (n, 1, 10)) prints like (Product(n)) mod 3

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Product, Mod, latex
>>> n = symbols('n')
>>> print(latex(Product(Mod(n, 3), (n, 1, 10))))
\prod_{n=1}^{10} n \bmod 3
>>> print(latex(Mod(Product(n, (n, 1, 10)), 3, evaluate=False)))
\prod_{n=1}^{10} n \bmod 3
```

### Expected
```pycon
>>> latex(Product(Mod(n, 3), (n, 1, 10))) != latex(Mod(Product(n, (n, 1, 10)), 3, evaluate=False))
True
```

### Why it is wrong
`\prod n \bmod 3` reads as `(Π n) mod 3`, not `Π (n mod 3)`; the two print identically.

### Notes on fixing
`LatexPrinter._print_Product` (`sympy/printing/latex.py`) brackets the factor only when it is an `Add`; it should decide by precedence instead. `_print_Sum` has the same code (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
