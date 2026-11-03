# A sympy.vector Vector with a fractional coefficient has its baseline on the top row

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq, pretty
>>> from sympy.vector import CoordSys3D
>>> C = CoordSys3D('C')
>>> x = symbols('x')
>>> print(pretty(Eq(C.i/x + C.j, C.j), use_unicode=True))
⎛1⎞           = j_C
⎜─⎟ i_C + j_C
⎝x⎠
```

### Expected
```pycon
>>> p = pretty(Eq(C.i/x + C.j, C.j), use_unicode=True)
>>> 'i_C' in [line for line in p.splitlines() if '=' in line][0]
True
```

### Why it is wrong
The `= j_C` is placed next to the numerator `1` instead of next to the basis vectors, so the picture reads as `1 = j_C`. Every picture that puts something beside such a vector is misaligned the same way: `Dot`, `Cross`, `Curl`, `Divergence`, Tuples and other containers.

### Notes on fixing
`PrettyPrinter._print_BasisDependent` in `sympy/printing/pretty/pretty.py` assembles the picture as a string and returns `prettyForm('\n'.join(...))`, whose baseline is 0. The row on which it writes the basis vectors and ` + ` (`flag[i]`) should become the baseline.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
