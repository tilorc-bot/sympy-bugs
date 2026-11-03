# A user-defined Predicate prints as Q.<name>, which does not evaluate

### Kind
lossy

### Actual
```pycon
>>> from sympy import Predicate, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> p = Predicate('custom')
>>> srepr(p)
'Q.custom'
>>> eval(srepr(p), ns)
Traceback (most recent call last):
...
AttributeError: 'AssumptionKeys' object has no attribute 'custom'
```

### Expected
```pycon
>>> eval(srepr(p), ns) == p
True
```

### Why it is wrong
Only built-in predicates are attributes of `Q`; a predicate created with `Predicate(name)` is not, so its srepr cannot be evaluated.

### Notes on fixing
`ReprPrinter._print_Predicate` (`sympy/printing/repr.py`) always prints `"Q.%s" % expr.name`. It could print `Q.<name>` only when `getattr(Q, name, None) == expr` and otherwise `Predicate('<name>')`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
