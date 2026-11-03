# Identity(n), ZeroMatrix(m, n) and OneMatrix(m, n) print as I, 0 and 1

### Kind
lossy

### Actual
```pycon
>>> from sympy import Identity, ZeroMatrix, OneMatrix, sympify
>>> print(Identity(2), ZeroMatrix(2, 3), OneMatrix(2, 3))
I 0 1
>>> sympify(str(Identity(2)))
I
```

### Expected
```pycon
>>> str(Identity(2)) != str(Identity(3))
True
>>> sympify(str(ZeroMatrix(2, 3))) == ZeroMatrix(2, 3)
True
>>> sympify(str(OneMatrix(2, 3))) == OneMatrix(2, 3)
True
```

### Why it is wrong
The output drops the shape and coincides with the imaginary unit `I` and the integers `0` and `1`, so it cannot be read back (`sympify` gives the scalar `I`, `0`, `1`) and matrices of different sizes print identically.

### Notes on fixing
`sympy/printing/str.py`: `_print_Identity`, `_print_ZeroMatrix` and `_print_OneMatrix` return the constant strings `"I"`, `"0"` and `"1"`. Printing `Identity(2)`, `ZeroMatrix(2, 3)`, `OneMatrix(2, 3)` would match `srepr` and round-trip.

The test `test_str_special_matrices` in `sympy/printing/tests/test_str.py` asserts the current output: `assert str(Identity(4)) == 'I'`, `assert str(ZeroMatrix(2, 2)) == '0'` and `assert str(OneMatrix(2, 2)) == '1'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
