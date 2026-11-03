# maple_code prints sign, gamma, atan2, loggamma and polygamma under their SymPy names, which mean something else (or nothing) in Maple

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, sign, gamma, atan2, loggamma, polygamma
>>> from sympy.printing.maple import maple_code
>>> x, y, n = symbols('x y n')
>>> print(maple_code(sign(x)))
sign(x)
>>> print(maple_code(gamma(x)))
gamma(x)
>>> print(maple_code(atan2(y, x)))
atan2(y, x)
>>> print(maple_code(loggamma(x)))
loggamma(x)
>>> print(maple_code(polygamma(n, x)))
polygamma(n, x)
```

### Expected
```pycon
>>> exprs = [sign(x), gamma(x), atan2(y, x), loggamma(x), polygamma(n, x)]
>>> [maple_code(e).split('(')[0] in ('sign', 'gamma', 'atan2', 'loggamma', 'polygamma') for e in exprs]
[False, False, False, False, False]
```

### Why it is wrong
In Maple, `sign(x)` is the sign of the leading coefficient of a polynomial (so `sign(x)` is `1` for a symbol `x`), and `gamma` is Euler's constant, with `gamma(k)` the Stieltjes constants, so both silently compute something else. `atan2`, `loggamma` and `polygamma` are not Maple functions and stay unevaluated. The Maple names are `signum`, `GAMMA`, `arctan(y, x)`, `lnGAMMA` and `Psi(n, x)`. The reviewer checked this against the Maple documentation.

### Notes on fixing
`sympy/printing/maple.py`: none of these is in `known_functions`, and `MapleCodePrinter` has `allow_unknown_functions=True`, so they are printed with the SymPy name. Add `'sign': 'signum'`, `'gamma': 'GAMMA'`, `'loggamma': 'lnGAMMA'`, `'polygamma': 'Psi'` to `known_functions`, and print `atan2(y, x)` as `arctan(y, x)`. `digamma(x)` is printed as `polygamma(0, x)` and is fixed by the `polygamma` mapping.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
