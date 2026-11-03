# str() of a physics.vector Dyadic with an UnevaluatedExpr(x + y) coefficient prints x + y*(N.x|N.y)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, UnevaluatedExpr
>>> from sympy.physics.vector import ReferenceFrame
>>> x, y = symbols('x y')
>>> N = ReferenceFrame('N')
>>> print(UnevaluatedExpr(x + y)*(N.x|N.y))
x + y*(N.x|N.y)
```

### Expected
```pycon
>>> print(UnevaluatedExpr(x + y)*(N.x|N.y))
(x + y)*(N.x|N.y)
```

### Why it is wrong
`x + y*(N.x|N.y)` is not even a valid expression (scalar plus dyadic); the coefficient `x + y` multiplies the dyad as a whole.

### Notes on fixing
`Dyadic._sympystr` (`sympy/physics/vector/dyadic.py`) wraps the coefficient in `(...)` only when `isinstance(coeff, Add)`; it should use `printer.parenthesize(coeff, PRECEDENCE['Mul'])`. `Vector._sympystr` and the `_latex` methods have the same pattern (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
