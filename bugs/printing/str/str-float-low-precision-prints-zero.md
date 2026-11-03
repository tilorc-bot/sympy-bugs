# A Float with precision below 5 bits prints 0.e+0 (zero) instead of its value

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Float
>>> f = Float(3.7, precision=4)
>>> print(f)
0.e+0
>>> float(f)
3.75
>>> print(Float(0.1, precision=4))
0.e-1
```

### Expected
```pycon
>>> abs(float(str(f)) - float(f)) < 1
True
>>> float(str(Float(0.1, precision=4))) != 0
True
```

### Why it is wrong
`0.e+0` and `0.e-1` denote zero, but the numbers are 3.75 and 0.1015625. Low precision Floats arise e.g. from `Float(x, precision=n)` or arithmetic on them, and their printed value is meaningless.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Float` sets `dps = 0 if prec < 5 else prec_to_dps(expr._prec)`. With `dps = 0`, `mlib_to_str` produces no significant digits. `prec_to_dps` already returns at least 1, so the special case should be dropped or use 1.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
