# sign(z) for complex z mixes a single-precision cmplx(0d0, 0d0) with double-precision z

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, sign, fcode
>>> z = symbols('z', complex=True)
>>> print(fcode(sign(z), standard=95, source_format='free'))
merge(cmplx(0d0, 0d0), z/abs(z), abs(z) == 0d0)
```

### Expected
```pycon
>>> 'cmplx(0d0, 0d0)' in fcode(sign(z), standard=95, source_format='free')
False
```

### Why it is wrong
`cmplx` without a `kind` argument returns a default (single-precision) complex even for double arguments, while `z/abs(z)` is double-precision complex, and `merge` requires both branches to have the same type and kind. gfortran 15.2 reports: `'fsource' argument of 'merge' intrinsic at (1) must be the same type and kind as 'tsource'`.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_sign` builds `cmplx(literal_dp(0), literal_dp(0))`. It needs a double-precision complex zero, e.g. `cmplx(0d0, 0d0, kind(z))`, `cmplx(0d0, 0d0, 8)` or the literal `(0d0, 0d0)`.

The output is asserted by `test_fcode_sign` in `sympy/printing/tests/test_fortran.py` (the test for [sympy/sympy#12267](https://redirect.github.com/sympy/sympy/issues/12267)). The same method also sends real arguments to the complex branch (`is_complex` is checked first); that is a separate defect.

### Related
[sympy/sympy#12267](https://redirect.github.com/sympy/sympy/issues/12267)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
