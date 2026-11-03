# Symbol('x_') prints as x, indistinguishable from Symbol('x')

### Kind
lossy

### Actual
```pycon
>>> from sympy import Symbol, pretty
>>> x = Symbol('x')
>>> print(pretty(Symbol('x_') + x, use_unicode=True))
x + x
```

### Expected
```pycon
>>> pretty(Symbol('x_'), use_unicode=True) != pretty(x, use_unicode=True)
True
```

### Why it is wrong
`x_ + x` is a sum of two different symbols, but the Unicode output shows `x + x`, which suggests `2*x`. The ASCII output keeps `x_`.

### Notes on fixing
`sympy/printing/pretty/pretty_symbology.py:pretty_symbol` uses `split_super_sub`, which turns a trailing `_` into an empty subscript; with an empty subscript list nothing is appended to the name. Empty subscripts/superscripts (also `x__`, `x^`) should keep the original characters, e.g. by returning the unchanged name when `split_super_sub` yields an empty sub/sup. `latex(Symbol('x_'))` gives `x_{}`, which renders as `x` too.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
