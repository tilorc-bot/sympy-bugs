# srepr(QQ.old_frac_field(x)) raises AttributeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, QQ, srepr
>>> x = symbols('x')
>>> srepr(QQ.old_frac_field(x))
Traceback (most recent call last):
...
AttributeError: 'FractionField' object has no attribute 'field'
```

### Why it is wrong
Printing must not fail for a valid object.

### Notes on fixing
`ReprPrinter._print_FractionField` (`sympy/printing/repr.py`) assumes the new-style `FractionField` domain, which has a `.field`. The old-style `sympy.polys.domains.old_fractionfield.FractionField` has the same class name but no `.field`, and the method is chosen by class name.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
