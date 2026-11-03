# Mod(i**2, j) applies % to the double returned by pow(), a compile error

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
>>> from codecheck import compile_errors, compiles
>>> print(compile_errors('c', ccode(Mod(i**2, j)), i=int, j=int))
error: invalid operands to binary % (have 'double' and 'int')
>>> print(compile_errors('c', ccode(Mod(ceiling(r), ceiling(s))), r=float, s=float))
error: invalid operands to binary % (have 'double' and 'double')
```

### Expected
```pycon
>>> compile_errors('c', ccode(Mod(i**2, j)), i=int, j=int) == ''
True
>>> compile_errors('c', ccode(Mod(ceiling(r), ceiling(s))), r=float, s=float) == ''
True
```

### Why it is wrong
`pow` and `ceil` return `double`, and C's `%` operator requires integer operands, so gcc rejects the generated code ("invalid operands to binary %").

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_Mod` uses `%` whenever both SymPy arguments are `is_integer`, but integer-valued SymPy expressions such as `i**2` or `ceiling(r)` are printed as calls returning `double`. Either use `%` only for operands that are printed as C integers, or cast/print the operands as integers. Tested-buggy: `test_ccode_functions2` in `sympy/printing/tests/test_c.py` asserts `ccode(Mod(ceiling(r), ceiling(s))) == '((ceil(r) % ceil(s)) + ceil(s)) % ceil(s)'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
