# use_unicode=False still prints ∂ for diffgeom base vector fields

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.diffgeom.rn import R2
>>> print(pretty(R2.e_x, use_unicode=False))
∂_x
```

### Expected
```pycon
>>> pretty(R2.e_x, use_unicode=False).isascii()
True
```

### Why it is wrong
`use_unicode=False` is meant to produce pure ASCII, but `∂` (U+2202) is not ASCII.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_BaseVectorField` builds the string from `U('PARTIAL DIFFERENTIAL')` without checking `self._use_unicode`; it needs an ASCII fallback (e.g. `d_x`, or `e_x` as in the str form).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
