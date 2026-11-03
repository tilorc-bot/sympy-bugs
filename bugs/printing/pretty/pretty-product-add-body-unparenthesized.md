# An Add body of a Product is not parenthesized: Product(k + 1, (k, 1, n)) + 1 shows ∏ k + 1 + 1

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Product, Add, pretty
>>> k, n = symbols('k n')
>>> print(pretty(Product(k + 1, (k, 1, n)) + 1, use_unicode=True))
  n
─┬─┬─
 │ │  k + 1 + 1
 │ │
k = 1
>>> print(pretty(Product(Add(k, 1, 1, evaluate=False), (k, 1, n)), use_unicode=True))
  n
─┬─┬─
 │ │  k + 1 + 1
 │ │
k = 1
```

### Expected
```pycon
>>> a = pretty(Product(k + 1, (k, 1, n)) + 1, use_unicode=True)
>>> b = pretty(Product(Add(k, 1, 1, evaluate=False), (k, 1, n)), use_unicode=True)
>>> a != b
True
```

### Why it is wrong
`∏(k + 1) + 1` and `∏(k + 1 + 1)` are different values but print the same.

### Notes on fixing
`PrettyPrinter._print_Sum` in `sympy/printing/pretty/pretty.py` parenthesizes an Add body (`Sum(k + 1, (k, 1, n)) + 1` prints `(k + 1) + 1` next to the sign), but `_print_Product` prints `self._print(expr.term)` unchanged.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
