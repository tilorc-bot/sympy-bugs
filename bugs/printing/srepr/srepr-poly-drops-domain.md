# Poly drops the domain and modulus

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Poly, QQ, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x = symbols('x')
>>> p = Poly(x**2 + 1, x, modulus=5)
>>> srepr(p)
"Poly(Add(Integer(1), Pow(Symbol('x'), Integer(2))), Symbol('x'))"
>>> eval(srepr(p), ns) == p
False
>>> q = Poly(x**2 + 1, x, domain=QQ)
>>> srepr(q)
"Poly(Add(Integer(1), Pow(Symbol('x'), Integer(2))), Symbol('x'))"
```

### Expected
```pycon
>>> [eval(srepr(e), ns) == e for e in (p, q)]
[True, True]
```

### Why it is wrong
The domain is part of a Poly's value (`Poly(x**2 + 1, x, modulus=5)` is a polynomial over GF(5)), so `srepr` does not round-trip; it prints the same string for polynomials over ZZ, QQ and GF(5).

### Related
[sympy/sympy#19644](https://redirect.github.com/sympy/sympy/issues/19644)

### Notes on fixing
`ReprPrinter` (`sympy/printing/repr.py`) has no `_print_Poly`, so `emptyPrinter` prints `Poly.args`, which are the expression and generators only. `repr(p)` already prints the domain (`Poly(x**2 + 1, x, modulus=5)`), so a `_print_Poly` can pass `domain=`/`modulus=` the same way. The same applies to extension domains, e.g. `Poly(x**2 + 1, x, extension=sqrt(2))`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
