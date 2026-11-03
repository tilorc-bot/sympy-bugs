# pretty() merges a -1 factor into the next factor of an unevaluated Mul (x*(-1)*2 shows as x⋅-2)

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Mul, pretty
>>> x = symbols('x')
>>> print(pretty(Mul(x, -1, 2, evaluate=False), use_unicode=True))
x⋅-2
>>> print(pretty(Mul(x, -2, evaluate=False), use_unicode=True))
x⋅-2
>>> print(pretty(Mul(2, -1, x, evaluate=False), use_unicode=True))
2⋅-x
```

### Expected
```pycon
>>> pretty(Mul(x, -1, 2, evaluate=False), use_unicode=True) != pretty(Mul(x, -2, evaluate=False), use_unicode=True)
True
```

### Why it is wrong
The point of an unevaluated Mul is to show its factors as given; here the `-1` factor in the middle is glued onto the following factor, so `x*(-1)*2` and `x*(-2)` look the same. `str` prints `x*(-1)*2` and `latex` prints `x \left(-1\right) 2`.

### Notes on fixing
`sympy/printing/pretty/stringpict.py:prettyForm.__mul__` replaces every `-1` followed by `*` with a bare `-`, wherever it occurs; that is only right for a leading `-1` (`-1*x -> -x`). Negative factors after the first are also not parenthesized (`x⋅-2`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
