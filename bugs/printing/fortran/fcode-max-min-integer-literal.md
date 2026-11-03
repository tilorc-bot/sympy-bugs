# Max(0, x) prints max(0, x), mixing integer and real arguments

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Max, Min, fcode
>>> x = symbols('x')
>>> print(fcode(Max(0, x), standard=95, source_format='free'))
max(0, x)
>>> print(fcode(Min(0, x), standard=95, source_format='free'))
min(0, x)
```

### Expected
```pycon
>>> 'max(0,' in fcode(Max(0, x), standard=95, source_format='free')
False
>>> 'min(0,' in fcode(Min(0, x), standard=95, source_format='free')
False
```

### Why it is wrong
The Fortran intrinsics `max` and `min` require all arguments to have the same type and kind; `0` is a default integer while `x` is `real*8` (as `codegen` declares it), so the compiler rejects the call. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`Max`/`Min` are printed through `known_functions` (`"Max": "max"`, `"Min": "min"` in `sympy/printing/fortran.py`) by `CodePrinter._print_Function`, which prints the arguments independently. Integer literals need to be printed as double precision (`0d0`) when another argument is real, e.g. in a `_print_Max`/`_print_Min` method.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
