# The Hilbert space L2(Interval(a, b)) drops the interval

### Kind
lossy

### Actual
```pycon
>>> from sympy import Interval, pretty
>>> from sympy.physics.quantum.hilbert import L2
>>> print(pretty(L2(Interval(0, 1)), use_unicode=True))
 2
L
```

### Expected
```pycon
>>> pretty(L2(Interval(0, 1)), use_unicode=True) != pretty(L2(Interval(0, 2)), use_unicode=True)
True
```

### Why it is wrong
`L2(Interval(0, 1))` and `L2(Interval(0, 2))` are different spaces; `str` gives `L2(Interval(0, 1))` and `latex` gives `{\mathcal{L}^2}\left( \left[0, 1\right] \right)`, but the pretty form shows only `L²`.

### Notes on fixing
`sympy/physics/quantum/hilbert.py:L2._pretty` builds `L**2` and never prints `self.interval`; it should append the printed interval in parentheses, as `_latex` does.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
