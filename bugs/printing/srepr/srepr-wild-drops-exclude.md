# Wild drops exclude and properties

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Wild, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x = symbols('x')
>>> w = Wild('w', exclude=[x])
>>> srepr(w)
"Wild('w')"
>>> eval(srepr(w), ns) == w
False
```

### Expected
```pycon
>>> eval(srepr(w), ns) == w
True
```

### Why it is wrong
`exclude` changes what the pattern matches, and `Wild('w')` and `Wild('w', exclude=[x])` compare unequal, so the srepr does not round-trip.

### Notes on fixing
`Wild` is a `Symbol` subclass and is printed by `ReprPrinter._print_Symbol` (`sympy/printing/repr.py`), which only prints `_assumptions_orig`. A `_print_Wild` should add `exclude=` (and `properties=`, which can only be printed if they are printable, e.g. not lambdas).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
