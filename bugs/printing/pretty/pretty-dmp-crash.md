# pretty() of a DMP (Poly.rep) raises AttributeError

### Kind
crash

### Actual
```pycon
>>> from sympy import Poly, pretty, symbols
>>> x = symbols('x')
>>> pretty(Poly(x**2 + 1, x).rep)
Traceback (most recent call last):
...
AttributeError: 'DMP_Python' object has no attribute 'ring'
```

### Expected
```pycon
>>> _ = pretty(Poly(x**2 + 1, x).rep)
```

### Why it is wrong
`str` and `repr` of the same object work; the pretty printer (and hence the interactive display of a `Poly.rep`) crashes instead of falling back to something printable.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_DMP` reads `p.ring`, an attribute the current `DMP` classes (`DMP_Python`, `DUP_Flint`) no longer have, and only catches `SympifyError`. It should use `getattr(p, 'ring', None)` (or otherwise not assume the attribute) and fall back to `repr(p)`. `_print_DMF` delegates to it.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
