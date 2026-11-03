# mathematica_code(Float('1e-20')*x) prints 1.0e-20*x, which Wolfram Language reads as 1.0*e - 20

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Float
>>> from sympy.printing.mathematica import mathematica_code
>>> x = symbols('x')
>>> print(mathematica_code(Float('1e-20')*x))
1.0e-20*x
```

### Expected
```pycon
>>> 'e-20' in mathematica_code(Float('1e-20')*x)
False
```

### Why it is wrong
The Wolfram Language has no `e` exponent notation: `1.0e-20` parses as `1.0*e - 20` (with `e` an undefined symbol), so the expression silently becomes `(1.0*e - 20)*x`. Scientific notation is written `1.0*^-20`. The reviewer checked this against the Wolfram Language documentation.

### Notes on fixing
`sympy/printing/mathematica.py:MCodePrinter` has no `_print_Float`, so floats are printed by `StrPrinter._print_Float` with Python's `e` notation. A `_print_Float` should replace the exponent marker with `*^` (as `FCodePrinter._print_Float` does with `d`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
