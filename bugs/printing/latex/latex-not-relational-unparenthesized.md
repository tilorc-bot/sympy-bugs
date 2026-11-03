# latex(Not(x > y)) prints "\neg x > y" without parentheses

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex, Not, Contains, Interval
>>> x, y = symbols('x y')
>>> print(latex(Not(x > y, evaluate=False)))
\neg x > y
>>> print(latex(Not(Contains(x, Interval(0, 1)))))
\neg x \in \left[0, 1\right]
```

### Expected
```pycon
>>> print(latex(Not(x > y, evaluate=False)))
\neg \left(x > y\right)
```

### Why it is wrong
`\neg x > y` reads as `(\neg x) > y`; the negation applies to the whole relation, and other Boolean arguments (e.g. `Not(And(x, y))`) are already printed as `\neg \left(...\right)`.

### Related
[pretty-not-relational-unparenthesized](../pretty/pretty-not-relational-unparenthesized.md)

### Notes on fixing
`LatexPrinter._print_Not` (`sympy/printing/latex.py`) only adds brackets when `e.args[0].is_Boolean`, which is False for `Relational` and `Contains`. It should bracket any argument that is not an atom (e.g. by precedence).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
