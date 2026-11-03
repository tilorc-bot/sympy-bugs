# SymmetricDifference never parenthesizes its arguments: (X ∪ Y) ∆ Z prints as X ∪ Y ∆ Z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Interval, Union, SymmetricDifference, pretty
>>> X, Y, Z = Interval(0, 1), Interval(2, 3), Interval(4, 5)
>>> print(pretty(SymmetricDifference(Union(X, Y), Z, evaluate=False), use_unicode=True))
[0, 1] ∪ [2, 3] ∆ [4, 5]
>>> print(pretty(Union(X, SymmetricDifference(Y, Z, evaluate=False), evaluate=False), use_unicode=True))
[0, 1] ∪ [2, 3] ∆ [4, 5]
```

### Expected
```pycon
>>> a = pretty(SymmetricDifference(Union(X, Y), Z, evaluate=False), use_unicode=True)
>>> b = pretty(Union(X, SymmetricDifference(Y, Z, evaluate=False), evaluate=False), use_unicode=True)
>>> pretty(SymmetricDifference(Union(X, Y), Z, evaluate=False), use_unicode=True) != b
True
>>> pretty(Union(X, SymmetricDifference(Y, Z, evaluate=False), evaluate=False), use_unicode=True) != a
True
```

### Why it is wrong
`(X ∪ Y) ∆ Z` and `X ∪ (Y ∆ Z)` are different sets but print the same.

### Notes on fixing
`PrettyPrinter._print_SymmetricDifference` in `sympy/printing/pretty/pretty.py` calls `_print_seq` without a `parenthesize` argument, so no argument is ever parenthesized. Conversely, the `parenthesize` lists of `_print_Union`, `_print_Intersection`, `_print_Complement` and `_print_ProductSet` do not include `SymmetricDifference`, which is why the second expression above is also unparenthesized.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
