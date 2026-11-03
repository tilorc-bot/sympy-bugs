# Piecewise((x, x > 1), (0, True)) prints merge(x, 0, x > 1), mixing real and integer

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Piecewise, fcode
>>> x = symbols('x')
>>> print(fcode(Piecewise((x, x > 1), (0, True)), standard=95, source_format='free'))
merge(x, 0, x > 1)
```

### Expected
```pycon
>>> ', 0,' in fcode(Piecewise((x, x > 1), (0, True)), standard=95, source_format='free')
False
```

### Why it is wrong
Fortran's `merge(tsource, fsource, mask)` requires `tsource` and `fsource` to have the same type and kind. `x` is `real*8` (as `codegen` declares it) and `0` is a default integer, so the statement is rejected by the compiler. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Piecewise` (inline `merge` branch) prints each branch independently. When the branches do not all have the same type, integer literals (and integer expressions) have to be printed as double precision (`0d0`, or wrapped in `dble(...)`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
