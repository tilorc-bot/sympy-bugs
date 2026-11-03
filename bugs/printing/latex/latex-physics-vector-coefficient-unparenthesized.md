# latex() of a physics.vector Vector brackets only Add coefficients: Mod(x, 2)*N.x prints as x \bmod 2\mathbf{\hat{n}_x}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mod, Integral, UnevaluatedExpr, latex
>>> from sympy.physics.vector import ReferenceFrame
>>> x, y = symbols('x y')
>>> N = ReferenceFrame('N')
>>> print(latex(Mod(x, 2)*N.x))
x \bmod 2\mathbf{\hat{n}_x}
>>> print(latex(UnevaluatedExpr(x + y)*N.x))
x + y\mathbf{\hat{n}_x}
>>> print(latex(Integral(x, x)*N.x))
\int x\, dx\mathbf{\hat{n}_x}
```

### Expected
```pycon
>>> latex(Mod(x, 2)*N.x).startswith(('(', r'\left('))
True
>>> latex(UnevaluatedExpr(x + y)*N.x).startswith(('(', r'\left('))
True
```

### Why it is wrong
The output reads as `x mod (2 n̂x)`, `x + y n̂x` and `∫ x dx n̂x` (or worse), i.e. the basis vector is multiplied into the last part of the coefficient only.

### Notes on fixing
`Vector._latex` (`sympy/physics/vector/vector.py`) wraps the coefficient in `(...)` only when `isinstance(coeff, Add)`. It should decide by the printer's precedence (`printer.parenthesize(coeff, PRECEDENCE['Mul'])`) and treat Integral/Sum-like coefficients, which have Mul precedence in LaTeX, as needing brackets too. `Dyadic._latex` and the `_sympystr` methods have the same pattern (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
