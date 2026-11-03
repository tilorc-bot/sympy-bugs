# floor and ceiling raise "Unsupported" for standard=95 although Fortran 90+ has them

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, floor, ceiling, fcode
>>> x = symbols('x')
>>> fcode(floor(x), standard=95, source_format='free')
Traceback (most recent call last):
...
sympy.printing.codeprinter.PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.fortran.FCodePrinter'>: floor...
>>> fcode(ceiling(x), standard=95, source_format='free')
Traceback (most recent call last):
...
sympy.printing.codeprinter.PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.fortran.FCodePrinter'>: ceiling...
```

### Expected
```pycon
>>> _ = fcode(floor(x), standard=95, source_format='free')
>>> _ = fcode(ceiling(x), standard=95, source_format='free')
```

### Why it is wrong
`floor` and `ceiling` are intrinsic functions since Fortran 90, so these common functions should be printable for `standard >= 90`.

### Notes on fixing
`sympy/printing/fortran.py` has no entry for `floor`/`ceiling` in `known_functions` and no `_print_floor`/`_print_ceiling`. They need to be added for `standard >= 90` (Fortran 77 has no such intrinsics, so raising there is fine). Note that the intrinsics return an integer; `dble(floor(x))` may be wanted when the result is used in real arithmetic.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
