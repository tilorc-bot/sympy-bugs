# str() of a physics.vector Vector with an UnevaluatedExpr(x + y) coefficient prints x + y*N.x

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, UnevaluatedExpr
>>> from sympy.physics.vector import ReferenceFrame
>>> x, y = symbols('x y')
>>> N = ReferenceFrame('N')
>>> print(UnevaluatedExpr(x + y)*N.x)
x + y*N.x
```

### Expected
```pycon
>>> print(UnevaluatedExpr(x + y)*N.x)
(x + y)*N.x
```

### Why it is wrong
`x + y*N.x` is not even a valid expression (scalar plus vector); the coefficient `x + y` multiplies `N.x` as a whole.

### Notes on fixing
`Vector._sympystr` (`sympy/physics/vector/vector.py`) wraps the coefficient in `(...)` only when `isinstance(coeff, Add)`; it should use `printer.parenthesize(coeff, PRECEDENCE['Mul'])`, which handles `UnevaluatedExpr` and anything else of lower precedence. `Dyadic._sympystr` and the `_latex` methods have the same pattern (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
