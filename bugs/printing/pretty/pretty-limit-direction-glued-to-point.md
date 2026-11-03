# The Limit direction marker attaches to the last term of the point: x─→y + z⁺

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Limit, pretty
>>> x, y, z = symbols('x y z')
>>> print(pretty(Limit(x, x, y + z), use_unicode=True))
   lim   x
x─→y + z⁺
```

### Expected
```pycon
>>> 'z⁺' in pretty(Limit(x, x, y + z), use_unicode=True)
False
```

### Why it is wrong
`y + z⁺` reads as `y` plus the one-sided approach to `z`, not as approaching `y + z` from the right.

### Notes on fixing
`PrettyPrinter._print_Limit` in `sympy/printing/pretty/pretty.py` appends the `⁺`/`⁻` marker directly to `self._print(z0)`; the point needs parentheses when it is not an atom (e.g. binding weaker than POW).

### Related
[sympy/sympy#8175](https://redirect.github.com/sympy/sympy/issues/8175)
[latex-limit-direction-on-last-term](../latex/latex-limit-direction-on-last-term.md)
### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
