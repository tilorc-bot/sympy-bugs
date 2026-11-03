# Matrix element indices are printed with str(): A[i**2, 0] gives A[i**2 + 1,1]

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, julia_code
>>> i = symbols('i', integer=True)
>>> A = MatrixSymbol('A', 2, 2)
>>> print(julia_code(A[i**2, 0]))
A[i**2 + 1,1]
>>> print(julia_code(i**2))
i .^ 2
```

### Expected
```pycon
>>> '**' in julia_code(A[i**2, 0])
False
```

### Why it is wrong
Symbolic indices are printed in Python syntax instead of Julia syntax (`i**2` instead of `i .^ 2` / `i ^ 2`), so the output does not parse. The reviewer ran the output with Julia 1.12.

### Notes on fixing
`sympy/printing/julia.py:JuliaCodePrinter._print_MatrixElement` formats `'[%s,%s]' % (expr.i + 1, expr.j + 1)`, i.e. with `str()`. Both indices should go through `self._print`. The same pattern (indices printed without the printer) exists in other code printers (see Related).

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)
[ccode-matrix-element-index-str](../c/ccode-matrix-element-index-str.md)
[rust-matrix-element-index-str](../rust/rust-matrix-element-index-str.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
