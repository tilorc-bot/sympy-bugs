# physics.vector Dyadic brackets only Add coefficients: Mod(x, 2)*(N.x|N.y) reads as x mod (2 n̂x⊗n̂y)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mod, UnevaluatedExpr, latex
>>> from sympy.physics.vector import ReferenceFrame
>>> x, y = symbols('x y')
>>> N = ReferenceFrame('N')
>>> print(latex(Mod(x, 2)*(N.x|N.y)))
x \bmod 2\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_y}
>>> print(latex(UnevaluatedExpr(x + y)*(N.x|N.y)))
x + y\mathbf{\hat{n}_x}\otimes \mathbf{\hat{n}_y}
```

### Expected
```pycon
>>> latex(Mod(x, 2)*(N.x|N.y)).startswith(('(', r'\left('))
True
>>> latex(UnevaluatedExpr(x + y)*(N.x|N.y)).startswith(('(', r'\left('))
True
```

### Why it is wrong
The output reads as `x mod (2 n̂x⊗n̂y)` and `x + y n̂x⊗n̂y`: the dyad is multiplied into the last part of the coefficient only.

### Notes on fixing
`Dyadic._latex` (`sympy/physics/vector/dyadic.py`) wraps the coefficient in `(...)` only when `isinstance(coeff, Add)`; it should decide by the printer's precedence. `Vector._latex` and the `_sympystr` methods have the same pattern (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
