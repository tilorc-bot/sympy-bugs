# ccode/glsl_code/fcode print the unevaluated Mul(2, 1/3) as 2/3, which is integer division

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Mul, Pow, ccode, glsl_code, fcode
>>> e = Mul(2, Pow(3, -1, evaluate=False), evaluate=False)
>>> ccode(e), glsl_code(e), fcode(e, source_format='free')
('2/3', '2/3', '2/3')
```

### Expected
```pycon
>>> ['.' in s for s in (ccode(e), glsl_code(e), fcode(e, source_format='free'))]
[True, True, True]
```

### Why it is wrong
In C, GLSL and Fortran, `2/3` is integer division and evaluates to 0, but the expression is 2/3. Evaluated Rationals are printed correctly (`ccode(Rational(2, 3))` gives `2.0/3.0`), so only unevaluated input (e.g. from `parse_expr(..., evaluate=False)` or `UnevaluatedExpr`) is affected. Expected checks for a floating-point literal, which any fix will need.

### Related
[sympy/sympy#4428](https://redirect.github.com/sympy/sympy/issues/4428)

### Notes on fixing
`CodePrinter._print_Mul` (`sympy/printing/codeprinter.py`) moves `Pow(3, -1)` to the denominator list and prints both integers with `_print_Integer`, joining them with `/`. When numerator and denominator are both integer literals, one of them must be printed as a float (as `_print_Rational` does). Python's printers are not affected since `/` is true division there.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
