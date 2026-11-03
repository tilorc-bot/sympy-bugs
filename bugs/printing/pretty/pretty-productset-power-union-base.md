# ProductSet(U, U) for a Union U prints as X ∪ Y² without parentheses

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Interval, Union, ProductSet, pretty
>>> U = Union(Interval(0, 1), Interval(2, 3))
>>> print(pretty(ProductSet(U, U), use_unicode=True))
               2
[0, 1] ∪ [2, 3]
```

### Expected
```pycon
>>> any(c in pretty(ProductSet(U, U), use_unicode=True) for c in '(⎛')
True
```

### Why it is wrong
The picture reads as `[0, 1] ∪ [2, 3]²`, i.e. the union of an interval with a square, instead of the square of the union.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`PrettyPrinter._print_ProductSet` in `sympy/printing/pretty/pretty.py` prints a product of equal sets as `self._print(p.sets[0]) ** self._print(len(p.sets))`. The Union picture comes from `_print_seq` with ATOM binding, so `prettyForm.__pow__` does not parenthesize it. The base needs parentheses when it is a Union, Intersection, Complement, SymmetricDifference or ProductSet (as in the non-power branch), or `_print_seq` results joined by an operator need a weaker binding.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
