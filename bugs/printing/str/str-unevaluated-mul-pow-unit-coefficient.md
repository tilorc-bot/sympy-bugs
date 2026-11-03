# str() of an unevaluated Mul prints y**(-x) in the denominator as y**(1*x)

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Mul, Pow
>>> x, y = symbols('x y')
>>> print(Mul(Pow(y, -x), 2, evaluate=False))
2/y**(1*x)
>>> print(Mul(2, Pow(y, -x), evaluate=False))
2/y**x
```

### Expected
```pycon
>>> print(Mul(Pow(y, -x), 2, evaluate=False))
2/y**x
```

### Why it is wrong
The exponent of the denominator is shown as the product `1*x`, a spurious factor that is not in the expression; the same factors in the other order print correctly.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Mul`, branch for unevaluated Muls: for a denominator `Pow` with a non-number exponent it negates the first factor of the exponent's args and rebuilds it with `Mul._from_args(dargs)`. For `-x` (`Mul(-1, x)`) that gives the unevaluated `Mul(1, x)`, printed `1*x`. A coefficient that becomes 1 should be dropped (e.g. via `_keep_coeff`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
