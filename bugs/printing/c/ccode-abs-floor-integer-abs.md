# ccode(Abs(floor(x))) uses the integer abs() on the double returned by floor()

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Abs, floor, ceiling
>>> from sympy.printing.c import ccode
>>> x = symbols('x', real=True)
>>> print(ccode(Abs(floor(x))))
abs(floor(x))
>>> print(ccode(Abs(ceiling(x)), standard='c89'))
abs(ceil(x))
```

### Expected
```pycon
>>> ccode(Abs(floor(x))) == 'fabs(floor(x))'
True
```

### Why it is wrong
In C, `floor`/`ceil` return `double`, and `abs` takes and returns `int`: the value is converted to `int` (undefined behaviour beyond `INT_MAX`, e.g. for `x = 3e9`) and `<stdlib.h>` is not requested, so it is an implicit declaration. The original reviewer compiled this with gcc; it was not executed here.

### Notes on fixing
`sympy/printing/c.py:known_functions_C89["Abs"]` chooses `abs` when the SymPy argument `is_integer`, but that says nothing about the C type of the printed expression: `floor(x)` is integer-valued in SymPy but a `double` in C. The check should only pick `abs` for arguments that are printed as C integers (integer symbols, integer literals, sums/products of them).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
