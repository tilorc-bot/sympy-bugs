# ccode(Mod(i**2, j)) applies % to the double returned by pow(), a compile error

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Mod, ceiling
>>> from sympy.printing.c import ccode
>>> i, j = symbols('i j', integer=True)
>>> print(ccode(Mod(i**2, j)))
((pow(i, 2) % j) + j) % j
>>> r, s = symbols('r s', real=True)
>>> print(ccode(Mod(ceiling(r), ceiling(s))))
((ceil(r) % ceil(s)) + ceil(s)) % ceil(s)
```

### Expected
```pycon
>>> import re
>>> re.search(r'(?<![\w)])(pow|ceil|floor)\([^()]*\) %', ccode(Mod(i**2, j))) is None
True
```

### Why it is wrong
`pow` and `ceil` return `double`, and C's `%` operator requires integer operands, so the generated code does not compile ("invalid operands to binary %"). The original reviewer compiled this with gcc; it was not executed here.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_Mod` uses `%` whenever both SymPy arguments are `is_integer`, but integer-valued SymPy expressions such as `i**2` or `ceiling(r)` are printed as calls returning `double`. Either use `%` only for operands that are printed as C integers, or cast/print the operands as integers. Tested-buggy: `test_ccode_functions2` in `sympy/printing/tests/test_c.py` asserts `ccode(Mod(ceiling(r), ceiling(s))) == '((ceil(r) % ceil(s)) + ceil(s)) % ceil(s)'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
