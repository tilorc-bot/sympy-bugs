# fcode() prints the quotient of two integer symbols as Fortran integer division

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, fcode
>>> p1, p2 = symbols('p1 p2', integer=True)
>>> print(fcode(p1/p2, source_format='free'))
p1/p2
```

### Expected
```pycon
>>> fcode(p1/p2, source_format='free') != 'p1/p2'
True
```

### Why it is wrong
`p1/p2` in SymPy is exact division, but `codegen(('ratio', p1/p2), 'F95')` declares `INTEGER*4, intent(in) :: p1, p2` and emits `ratio = p1/p2`, which Fortran evaluates with integer division: compiled with gfortran 15.2, `ratio(7, 4)` is `1.0` instead of `1.75`.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Mul` delegates to `sympy/printing/codeprinter.py:CodePrinter._print_Mul`, which prints `numerator/denominator` without regard to types. When both are integer-valued one side needs a conversion (`dble(p1)/p2`, as `_print_Pow` already does for `sqrt(dble(i))`). [sympy/sympy#4428](https://redirect.github.com/sympy/sympy/issues/4428) fixed only numeric fractions. Not covered by a test.

### Related
[sympy/sympy#4428](https://redirect.github.com/sympy/sympy/issues/4428)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
