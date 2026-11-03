# pretty() does not parenthesize a Complement inside a ProductSet: (X \ Y) × Z prints as X \ Y × Z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Interval, Complement, ProductSet, pretty
>>> X, Y, Z = Interval(0, 1), Interval(2, 3), Interval(4, 5)
>>> print(pretty(ProductSet(Complement(X, Y, evaluate=False), Z), use_unicode=True))
[0, 1] \ [2, 3] × [4, 5]
```

### Expected
```pycon
>>> '([0, 1] \\ [2, 3])' in pretty(ProductSet(Complement(X, Y, evaluate=False), Z), use_unicode=True)
True
```

### Why it is wrong
The picture reads as `X \ (Y × Z)`, a subset of the line, while the expression is a subset of the plane.

### Notes on fixing
`PrettyPrinter._print_ProductSet` in `sympy/printing/pretty/pretty.py` parenthesizes only `Union`, `Intersection` and `ProductSet` factors (`parenthesize=lambda set: set.is_Union or set.is_Intersection or set.is_ProductSet`); `Complement` and `SymmetricDifference` are missing. For example `ProductSet(SymmetricDifference(X, Y, evaluate=False), Z)` prints `[0, 1] ∆ [2, 3] × [4, 5]`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
