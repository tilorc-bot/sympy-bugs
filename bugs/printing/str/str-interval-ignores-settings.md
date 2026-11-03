# sstr() ignores sympy_integers and full_prec for the endpoints of an Interval

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import Interval, S, Float, sstr
>>> print(sstr(Interval(S.Half, 1), sympy_integers=True))
Interval(1/2, 1)
>>> print(sstr(S.Half, sympy_integers=True))
S(1)/2
>>> print(sstr(Interval(Float(0.1), 1), full_prec=False))
Interval(0.100000000000000, 1)
```

### Expected
```pycon
>>> 'S(1)/2' in sstr(Interval(S.Half, 1), sympy_integers=True)
True
>>> sstr(Interval(Float(0.1), 1), full_prec=False)
'Interval(0.1, 1)'
```

### Why it is wrong
The settings are applied everywhere else (e.g. `sstr(FiniteSet(S.Half), sympy_integers=True)`), so `sstr(..., sympy_integers=True)` cannot be relied on to produce code that keeps rationals exact when an Interval is involved.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Interval` fills the endpoints with `fin.format(**{'a': a, 'b': b, 'm': m})`, which calls `str()` on them instead of `self._print`. The `min`/`max` Float settings are ignored for the same reason.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
