# ccode(2**70*x) prints an integer literal that does not fit in any C integer type

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.printing.c import ccode
>>> x = symbols('x')
>>> print(ccode(2**70*x))
1180591620717411303424*x
>>> from codecheck import compile_errors, run_code
>>> print(compile_errors('c', ccode(2**70*x), x=float))
error: integer constant is too large for its type
```

### Expected
```pycon
>>> run_code('c', ccode(2**70*x), x=1.0) == float(2**70)
True
```

### Why it is wrong
A decimal integer literal larger than `LLONG_MAX` has no type in C; gcc warns ("integer constant is too large for its type"; an error with `-pedantic-errors`, which is how it is compiled here) and the program computes with a truncated value (the original reviewer saw it print 0). Printing it as a floating-point literal (`1180591620717411303424.0`) would be correct.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter` prints `Integer` with the generic printer. Integers outside the range of `long long` should be printed as floating-point literals (with the type suffix of the real type).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
