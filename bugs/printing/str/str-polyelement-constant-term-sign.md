# A PolyElement negates a constant term whose printed form does not start with "-"

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, ZZ, EX, parse_expr
>>> from sympy.polys.rings import ring
>>> t, y = symbols('t y')
>>> K = ZZ.frac_field(t)
>>> R, v = ring('v', K)
>>> p = v + K.from_sympy((1 - t)/t)
>>> print(p)
v - (-t + 1)/t
>>> p.as_expr()
v + (1 - t)/t
>>> R2, x2 = ring('x', EX)
>>> print(x2 + EX(-y - 1))
x - EX(-y - 1)
```

### Expected
```pycon
>>> parse_expr(str(p)) == p.as_expr()
True
```

### Why it is wrong
`v - (-t + 1)/t` is `v + (t - 1)/t`, the negative of the actual constant term. Over `EX` the printed `x - EX(-y - 1)` likewise means `x + y + 1` instead of `x - y - 1`, and over `QQ<sqrt(2)>` a negative constant prints as `s - ANP(...)` with the unnegated coefficient.

### Notes on fixing
`sympy/polys/rings.py:PolyElement.str`: for the constant term it chooses `" - "` from `domain.is_negative(coeff)` but then prints `coeff` itself and strips a leading `-` only if the printed string happens to start with one. For fraction-field, `EX` and algebraic-field elements it does not. The constant term should be negated before printing, as the non-constant branch already does (`if negative: coeff = -coeff`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
