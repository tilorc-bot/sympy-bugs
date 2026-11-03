# Abs(floor(x)) uses the integer abs() on the double returned by floor()

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
>>> from codecheck import run_code
>>> run_code('c', ccode(Abs(floor(x))), x=-3e9)
-2147483648.0
>>> run_code('c89', ccode(Abs(ceiling(x)), standard='c89'), x=-3e9)
-2147483648.0
```

### Expected
```pycon
>>> [run_code('c', ccode(Abs(floor(x))), x=-3e9),
...  run_code('c89', ccode(Abs(ceiling(x)), standard='c89'), x=-3e9)]
[3000000000.0, 3000000000.0]
```

### Why it is wrong
In C, `floor`/`ceil` return `double`, and `abs` takes and returns `int`: the value is converted to `int` (undefined behaviour beyond `INT_MAX`), so compiled with gcc it returns -2147483648 at `x = -3e9` instead of 3e9. `<stdlib.h>` is also not requested, so without it `abs` is an implicit declaration.

### Notes on fixing
`sympy/printing/c.py:known_functions_C89["Abs"]` chooses `abs` when the SymPy argument `is_integer`, but that says nothing about the C type of the printed expression: `floor(x)` is integer-valued in SymPy but a `double` in C. The check should only pick `abs` for arguments that are printed as C integers (integer symbols, integer literals, sums/products of them).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
