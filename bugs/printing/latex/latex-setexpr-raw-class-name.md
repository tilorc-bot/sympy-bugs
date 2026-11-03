# latex(SetExpr(...)) prints the class name as italic math letters

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import Interval, latex
>>> from sympy.sets.setexpr import SetExpr
>>> print(latex(SetExpr(Interval(0, 1))))
SetExpr\left(\left[0, 1\right]\right)
```

### Expected
```pycon
>>> latex(SetExpr(Interval(0, 1))).startswith('SetExpr')
False
```

### Why it is wrong
In math mode `SetExpr` renders as the product of the italic variables S, e, t, E, x, p, r; other unknown classes are printed with `\operatorname{...}`.

### Notes on fixing
`sympy/sets/setexpr.py:SetExpr._latex` returns the bare name; wrapping it in `\operatorname{}` (or `\text{}`) is enough.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
