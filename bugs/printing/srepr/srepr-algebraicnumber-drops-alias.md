# AlgebraicNumber drops its alias

### Kind
lossy

### Actual
```pycon
>>> from sympy import sqrt, AlgebraicNumber, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> a = AlgebraicNumber(sqrt(2), alias='theta')
>>> srepr(a)
'AlgebraicNumber(Pow(Integer(2), Rational(1, 2)), [Integer(1), Integer(0)])'
>>> eval(srepr(a), ns) == a
False
```

### Expected
```pycon
>>> eval(srepr(a), ns) == a
True
```

### Why it is wrong
The alias is part of the object (it compares unequal without it and is used when printing), so srepr does not round-trip.

### Notes on fixing
`ReprPrinter._print_AlgebraicNumber` (`sympy/printing/repr.py`) prints only `root` and `coeffs()`; it should add `alias=` when `expr.alias` is set.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
