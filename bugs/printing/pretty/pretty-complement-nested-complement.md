# pretty() prints X \ (Y \ Z) and (X \ Y) \ Z identically

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Interval, Complement, pretty
>>> X, Y, Z = Interval(0, 1), Interval(2, 3), Interval(4, 5)
>>> print(pretty(Complement(X, Complement(Y, Z, evaluate=False), evaluate=False), use_unicode=True))
[0, 1] \ [2, 3] \ [4, 5]
>>> print(pretty(Complement(Complement(X, Y, evaluate=False), Z, evaluate=False), use_unicode=True))
[0, 1] \ [2, 3] \ [4, 5]
```

### Expected
```pycon
>>> a = pretty(Complement(X, Complement(Y, Z, evaluate=False), evaluate=False), use_unicode=True)
>>> b = pretty(Complement(Complement(X, Y, evaluate=False), Z, evaluate=False), use_unicode=True)
>>> a != b
True
```

### Why it is wrong
Set difference is not associative: `X \ (Y \ Z)` and `(X \ Y) \ Z` are different sets, but they print the same.

### Notes on fixing
`PrettyPrinter._print_Complement` in `sympy/printing/pretty/pretty.py` passes `parenthesize=lambda set: set.is_ProductSet or set.is_Intersection or set.is_Union` to `_print_seq`; a nested `Complement` (at least as the second argument) and a `SymmetricDifference` are missing from that list.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
