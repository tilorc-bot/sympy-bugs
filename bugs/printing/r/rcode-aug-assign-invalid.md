# aug_assign(x, '+', y + z) prints x += y + z;, which is not R

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, rcode
>>> from sympy.codegen.ast import aug_assign
>>> x, y, z = symbols('x y z')
>>> print(rcode(aug_assign(x, '+', y + z)))
x += y + z;
```

### Expected
```pycon
>>> '+=' in rcode(aug_assign(x, '+', y + z))
False
```

### Why it is wrong
R has no augmented assignment operators (`+=`, `-=`, `*=`, `/=`); the statement is a syntax error. It has to be expanded to `x = x + (y + z);`. The reviewer checked this against the R documentation.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._print_AugmentedAssignment` prints `lhs op rhs;` with the C operator. It should print `lhs = lhs binop (rhs)`, parenthesizing the rhs (unlike the Fortran printer, see Related). The current output is asserted by `test_rcode_Assignment` in `sympy/printing/tests/test_rcode.py` (tested-buggy).

### Related
[fcode-aug-assign-rhs-unparenthesized](../fortran/fcode-aug-assign-rhs-unparenthesized.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
