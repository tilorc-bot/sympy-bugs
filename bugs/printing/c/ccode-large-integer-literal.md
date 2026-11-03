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
```

### Expected
```pycon
>>> import re
>>> all(int(lit) < 2**63 for lit in re.findall(r'(?<![\w.])\d+(?![\w.])', ccode(2**70*x)))
True
```

### Why it is wrong
A decimal integer literal larger than `LLONG_MAX` has no type in C; gcc warns ("integer constant is too large for its type") and the program computes with a truncated value (the original reviewer saw it print 0). It was not compiled here. Printing it as a floating-point literal (`1180591620717411303424.0`) would be correct.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter` prints `Integer` with the generic printer. Integers outside the range of `long long` should be printed as floating-point literals (with the type suffix of the real type).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
