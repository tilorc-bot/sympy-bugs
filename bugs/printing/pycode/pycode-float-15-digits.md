# Code printers print 53-bit Floats with only 15 significant digits, so lambdified constants lose precision

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Float, lambdify
>>> from sympy.printing.pycode import pycode
>>> x = symbols('x')
>>> c = Float(1)/3
>>> print(pycode(c*x))
0.333333333333333*x
>>> lambdify(x, c*x, 'math')(1.0) == float(c)
False
```

### Expected
```pycon
>>> lambdify(x, c*x, 'math')(1.0) == float(c)
True
```

### Why it is wrong
A double needs 17 significant digits to round-trip; with 15, the constant in the generated code is a different double from the SymPy Float, so lambdified functions are off by up to ~1e-15 relative, even though `pycode` has `precision=17` in its settings.

### Related
[sympy/sympy#16464](https://redirect.github.com/sympy/sympy/issues/16464)

### Notes on fixing
The code printers use `StrPrinter._print_Float` (`sympy/printing/str.py`), which prints `prec_to_dps(prec)` = 15 digits for a 53-bit Float. The same happens in `jscode`, `octave_code`, `rcode`, `julia_code`, `rust_code` and `fcode`; `ccode` prints 17 digits (`C89CodePrinter._print_Float` evaluates to `decimal_dig`). `MpmathPrinter` is unaffected (it prints the exact mpf tuple).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
