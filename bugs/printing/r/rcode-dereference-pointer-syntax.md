# rcode(..., dereference=[z]) prints C pointer syntax (*z)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, rcode
>>> x, z = symbols('x z')
>>> print(rcode(x + z, dereference=[z]))
x + (*z)
```

### Expected
```pycon
>>> '*' in rcode(x + z, dereference=[z])
False
```

### Why it is wrong
R has no pointers, so `(*z)` is a syntax error; R 4.6 reports `unexpected '*'`.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._print_Symbol` was copied from the C printer together with the `dereference` setting. In R the setting has nothing to do; it could be ignored or the setting removed. The output is asserted by `test_dereference_printing` in `sympy/printing/tests/test_rcode.py`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
