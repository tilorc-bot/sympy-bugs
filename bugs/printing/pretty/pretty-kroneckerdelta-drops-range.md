# pretty() of KroneckerDelta(i, j, (a, b)) drops the summation range

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, KroneckerDelta, pretty
>>> i, j, n = symbols('i j n')
>>> print(pretty(KroneckerDelta(i, j, (0, n)), use_unicode=True))
δ
 i,j
>>> KroneckerDelta(i, j, (0, n)) == KroneckerDelta(i, j)
False
```

### Expected
```pycon
>>> pretty(KroneckerDelta(i, j, (0, n)), use_unicode=True) != pretty(KroneckerDelta(i, j), use_unicode=True)
True
```

### Why it is wrong
`KroneckerDelta(i, j, (0, n))` and `KroneckerDelta(i, j)` are different objects (the range is used when summing), but they print identically.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_KroneckerDelta` only prints `e.args[0]` and `e.args[1]`; the optional third argument `delta_range` is ignored. The LaTeX printer (`latex.py:_print_KroneckerDelta`) drops it too.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
