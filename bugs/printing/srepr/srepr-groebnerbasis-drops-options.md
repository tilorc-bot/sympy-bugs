# GroebnerBasis drops the order and domain

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, groebner, QQ, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x, y = symbols('x y')
>>> G = groebner([x**2 - y, x*y - 1], x, y, order='grevlex', domain=QQ)
>>> srepr(G)
"GroebnerBasis(Tuple(Add(Pow(Symbol('x'), Integer(2)), Mul(Integer(-1), Symbol('y'))), Add(Integer(-1), Mul(Symbol('x'), Symbol('y'))), Add(Pow(Symbol('y'), Integer(2)), Mul(Integer(-1), Symbol('x')))), Tuple(Symbol('x'), Symbol('y')))"
>>> eval(srepr(G), ns) == G
False
```

### Expected
```pycon
>>> eval(srepr(G), ns) == G
True
```

### Why it is wrong
Evaluating the srepr recomputes the basis with the default `lex` order, which is a different basis, so the round trip fails.

### Notes on fixing
`GroebnerBasis` (`sympy/polys/polytools.py`) keeps `order` and `domain` in its options, not in `args`, and `ReprPrinter` (`sympy/printing/repr.py`) has no `_print_GroebnerBasis`, so the generic fallback prints only `args`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
