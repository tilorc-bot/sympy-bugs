# fcode(aug_assign(x, '*', y + z)) prints x = x * y + z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, fcode
>>> from sympy.codegen.ast import aug_assign
>>> x, y, z = symbols('x y z')
>>> print(fcode(aug_assign(x, '*', y + z), source_format='free'))
x = x * y + z
>>> print(fcode(aug_assign(x, '-', y + z), source_format='free'))
x = x - y + z
>>> print(fcode(aug_assign(x, '/', y*z), source_format='free'))
x = x / y*z
```

### Expected
```pycon
>>> '(y + z)' in fcode(aug_assign(x, '*', y + z), source_format='free')
True
>>> '(y + z)' in fcode(aug_assign(x, '-', y + z), source_format='free')
True
>>> '(y*z)' in fcode(aug_assign(x, '/', y*z), source_format='free')
True
```

### Why it is wrong
`x *= y + z` means `x = x*(y + z)`, but the printed statement computes `x*y + z`; likewise `x - y + z` instead of `x - (y + z)` and `(x/y)*z` instead of `x/(y*z)`. The generated code silently computes the wrong value (checked against Fortran operator precedence only; the reviewer did not compile it).

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_AugmentedAssignment` expands `x op= rhs` into `"{0} = {0} {1} {2}"` with the rhs printed unparenthesized. It needs to parenthesize the rhs with the precedence of the binary operator (e.g. build `Add`/`Mul` of lhs and rhs unevaluated, or use `self.parenthesize(expr.rhs, ...)`). Only `+` is safe as is.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
