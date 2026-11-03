# latex() prints Sum(Mod(n, 3), (n, 0, 10)) like (Sum(n)) mod 3

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Sum, Mod, latex
>>> n = symbols('n')
>>> print(latex(Sum(Mod(n, 3), (n, 0, 10))))
\sum_{n=0}^{10} n \bmod 3
>>> print(latex(Mod(Sum(n, (n, 0, 10)), 3, evaluate=False)))
\sum_{n=0}^{10} n \bmod 3
```

### Expected
```pycon
>>> latex(Sum(Mod(n, 3), (n, 0, 10))) != latex(Mod(Sum(n, (n, 0, 10)), 3, evaluate=False))
True
```

### Why it is wrong
`\sum n \bmod 3` reads as `(Σ n) mod 3` (= 1), not `Σ (n mod 3)` (= 10); the two print identically.

### Notes on fixing
`LatexPrinter._print_Sum` (`sympy/printing/latex.py`) brackets the summand only when it is an `Add`. It should use precedence (e.g. `parenthesize(expr.function, PRECEDENCE['Mul'])` non-strict, as Mod has Mul precedence) like `_print_Integral` does. `_print_Product` has the same code (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
