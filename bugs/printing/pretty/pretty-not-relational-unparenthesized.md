# Not(t < x) prints as ¬t < x without parentheses

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Not, Contains, Interval, pretty
>>> t, x = symbols('t x')
>>> print(pretty(Not(t < x, evaluate=False), use_unicode=True))
¬t < x
>>> print(pretty(Not(Contains(x, Interval(0, 1))), use_unicode=True))
¬x ∈ [0, 1]
```

### Expected
```pycon
>>> pretty(Not(t < x, evaluate=False), use_unicode=True).startswith('¬(')
True
>>> pretty(Not(Contains(x, Interval(0, 1))), use_unicode=True).startswith('¬(')
True
```

### Why it is wrong
`¬` binds tighter than `<` and `∈`, so the pictures read as `(¬t) < x` and `(¬x) ∈ [0, 1]` instead of the negation of the whole relation.

### Related
[latex-not-relational-unparenthesized](../latex/latex-not-relational-unparenthesized.md)

### Notes on fixing
`PrettyPrinter._print_Not` in `sympy/printing/pretty/pretty.py` parenthesizes the argument only when `arg.is_Boolean`, which is False for `Relational` and `Contains`. Checking `isinstance(arg, Boolean)` (or the argument's binding) and excluding atoms and `Not` would cover these.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
