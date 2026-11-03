# fcode(i**(-2)) prints integer exponentiation i**(-2), which Fortran evaluates to 0

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Pow, fcode
>>> i = symbols('i', integer=True)
>>> print(fcode(i**(-2), standard=95, source_format='free'))
i**(-2)
>>> print(fcode(Pow(2, -2, evaluate=False), standard=95, source_format='free'))
2**(-2)
```

### Expected
```pycon
>>> 'i**(-2)' in fcode(i**(-2), standard=95, source_format='free')
False
>>> '2**(-2)' in fcode(Pow(2, -2, evaluate=False), standard=95, source_format='free')
False
```

### Why it is wrong
In Fortran an integer raised to a negative integer power is computed as `1/(i**2)` in integer arithmetic, so the result is `0` for every `|i| > 1` (and `2**(-2)` is `0`), while SymPy's value is `1/4`. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Pow` only special-cases exponents `-1` and `1/2` and otherwise delegates to `CodePrinter._print_Pow`. For an integer base and a negative exponent the base has to be converted to double precision (`dble(i)**(-2)`, `2.0d0**(-2)`), as is already done for `sqrt` of an integer.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
