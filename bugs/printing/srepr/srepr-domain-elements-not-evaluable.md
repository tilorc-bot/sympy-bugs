# Domain elements QQ(1, 2), GF(5)(3) and ZZ_I(1, 2) print as 1/2, 3 mod 5 and 1 + 2*I

### Kind
lossy

### Actual
```pycon
>>> from sympy import QQ, GF, ZZ_I, srepr
>>> from sympy.polys.rings import ring
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> R, X = ring('x', QQ)
>>> srepr(X/2)
"PolyElement(PolyRing((Symbol('x'),), QQ, lex), [((1,), 1/2)])"
>>> srepr(QQ(1, 2)), srepr(GF(5)(3)), srepr(ZZ_I(1, 2))
('1/2', '3 mod 5', '1 + 2*I')
```

### Expected
```pycon
>>> [eval(srepr(e), ns) == e for e in (QQ(1, 2), GF(5)(3), ZZ_I(1, 2))]
[True, True, True]
```

### Why it is wrong
`1/2` evaluates to the float `0.5`, `3 mod 5` is a syntax error and `1 + 2*I` is an `Add`, not a Gaussian integer. So any srepr containing QQ coefficients (PolyElement, DMP, DomainMatrix) silently turns exact rationals into floats.

### Notes on fixing
`ReprPrinter` (`sympy/printing/repr.py`) has no handlers for the domain element types (`PythonMPQ`/gmpy2 `mpq`, `ModularInteger`, `GaussianInteger`), so `emptyPrinter` falls back to `str()`. The same `1/2` shows up in `srepr(DMP([QQ(1, 2), QQ(1)], QQ))` (`DMP_Python([1/2, 1], QQ)`) and `srepr(DomainMatrix([[QQ(1, 2)]], (1, 1), QQ))`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
