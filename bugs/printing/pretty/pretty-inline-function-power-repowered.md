# Pow(sin(x)**2, 3) puts the 3 above sin²(x) without parentheses

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, sin, Pow, pretty
>>> x = symbols('x')
>>> print(pretty(Pow(sin(x)**2, 3, evaluate=False), use_unicode=True))
       3
   2
sin (x)
```

### Expected
```pycon
>>> p = pretty(Pow(sin(x)**2, 3, evaluate=False), use_unicode=True)
>>> '⎝sin' in p or '(sin' in p
True
```

### Why it is wrong
The `3` is a power of a power, but it is stacked above the `2` like a tower exponent, so the picture does not show what is raised to the third power; it should read `(sin²(x))³`.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`prettyForm.__pow__` in `sympy/printing/pretty/stringpict.py` returns the inline function form `sin²(x)` (the `use_inline_func_form` branch) with the default ATOM binding, so a second `__pow__` does not parenthesize it. That branch should return `binding=prettyForm.POW` like the general branch.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
