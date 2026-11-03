# Polynomial rings use PolyRing, PolyElement and GlobalPolynomialRing, not in `from sympy import *`

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, ZZ, QQ, srepr
>>> from sympy.polys.rings import ring
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> R, X = ring('x', ZZ)
>>> srepr(X + 1)
"PolyElement(PolyRing((Symbol('x'),), ZZ, lex), [((1,), 1), ((0,), 1)])"
>>> eval(srepr(X + 1), ns)
Traceback (most recent call last):
...
NameError: name 'PolyElement' is not defined
>>> x = symbols('x')
>>> srepr(QQ.old_poly_ring(x))
"GlobalPolynomialRing(QQ, Symbol('x'))"
```

### Expected
```pycon
>>> eval(srepr(R), ns) == R
True
>>> eval(srepr(X + 1), ns) == X + 1
True
>>> eval(srepr(QQ.old_poly_ring(x)), ns) == QQ.old_poly_ring(x)
True
```

### Why it is wrong
`srepr` promises `eval(srepr(expr)) == expr` in the scope of `from sympy import *`, but none of these class names is exported from `sympy`.

### Notes on fixing
`_print_PolyRing`, `_print_PolyElement`, `_print_FracField`, `_print_FracElement` and `_print_PolynomialRingBase` in `sympy/printing/repr.py` print `__class__.__name__`. With `PolyRing`, `PolyElement` and `GlobalPolynomialRing` added to the namespace the strings above do evaluate back to equal objects, so exporting the names or printing a public constructor (`QQ.old_poly_ring(...)`) is enough. QQ coefficients have a separate problem (they print as `1/2`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
