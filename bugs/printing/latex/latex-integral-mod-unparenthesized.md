# latex() prints Integral(Mod(x, 3), x) as "\int x \bmod 3\, dx" without brackets

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Integral, Mod, latex
>>> x = symbols('x')
>>> print(latex(Integral(Mod(x, 3), x)))
\int x \bmod 3\, dx
```

### Expected
```pycon
>>> r'\left(x \bmod 3\right)' in latex(Integral(Mod(x, 3), x))
True
```

### Why it is wrong
`\int x \bmod 3\, dx` reads as `∫ x mod (3 dx)`: the extent of the integrand is not marked, unlike an Add integrand, which is bracketed.

### Notes on fixing
`LatexPrinter._print_Integral` (`sympy/printing/latex.py`) uses `parenthesize(expr.function, PRECEDENCE['Mul'], strict=True)`, which brackets only expressions of strictly lower precedence; `Mod` has Mul precedence, so it is printed bare.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
