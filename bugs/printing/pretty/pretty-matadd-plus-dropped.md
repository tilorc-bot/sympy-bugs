# pretty() drops the + in MatAdd(B, (1 - x)*A)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, MatAdd, pretty
>>> x = symbols('x')
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> print(pretty(MatAdd(B, (1 - x)*A), use_unicode=True))
B (1 - x)⋅A
```

### Expected
```pycon
>>> p = pretty(MatAdd(B, (1 - x)*A), use_unicode=True)
>>> 'B + ' in p or 'B - ' in p
True
```

### Why it is wrong
The operator between the two terms is missing, so the sum `B + (1 - x)A` is printed as if it were a product `B (1 - x) A`.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_MatAdd` leaves out the ` + ` whenever `item.as_coeff_mmul()[0].could_extract_minus_sign()`, assuming the term's picture then starts with `-`. For the coefficient `1 - x` this is True, but the term prints as `(1 - x)⋅A`. The decision should be made from the printed form (for example `pform.binding == prettyForm.NEG`, which `prettyForm.__mul__` sets when the product starts with `-`), as `_print_Add` does.

The same code prints negative terms with no space after the minus: `test_MatrixSymbol_printing` in `sympy/printing/pretty/tests/test_pretty.py` asserts `pretty(A*B*C - A*B - B*C) == "-A*B -B*C + A*B*C"`, which should be `-A*B - B*C + A*B*C`. That test has to be updated by a fix that adds the space.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
