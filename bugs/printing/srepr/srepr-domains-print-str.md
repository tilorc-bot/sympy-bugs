# srepr() prints domains with str(): RealField(prec=100) becomes RR, QQ<sqrt(2)> and ZZ[x] are not Python

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, sqrt, QQ, ZZ, RealField, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x = symbols('x')
>>> srepr(RealField(prec=100))
'RR'
>>> srepr(QQ.algebraic_field(sqrt(2)))
'QQ<sqrt(2)>'
>>> srepr(ZZ[x])
'ZZ[x]'
```

### Expected
```pycon
>>> [eval(srepr(d), ns) == d for d in (RealField(prec=100), QQ.algebraic_field(sqrt(2)), ZZ[x])]
[True, True, True]
```

### Why it is wrong
`RR` is the 53-bit field, so the precision is lost; `QQ<sqrt(2)>` is a syntax error and `ZZ[x]` uses the bare name `x` instead of `Symbol('x')`. Any srepr that contains such a domain (DMP, DomainMatrix, PolyRing) cannot be evaluated or comes back different.

### Notes on fixing
`ReprPrinter` (`sympy/printing/repr.py`) has no handler for `Domain` objects, so `emptyPrinter` falls back to `str()`. A `_print_Domain`-style method (or per-domain methods) should print constructor calls such as `RealField(prec=100)`, `QQ.algebraic_field(...)`, `ZZ[Symbol('x')]`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
