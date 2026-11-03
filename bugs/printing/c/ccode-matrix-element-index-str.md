# ccode() prints the flattened index of a MatrixElement with str(), e.g. A[i**2*m + j]

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Symbol, MatrixSymbol
>>> from sympy.printing.c import ccode
>>> i, j, n, m = symbols('i j n m')
>>> A = MatrixSymbol('A', n, m)
>>> print(ccode(A[i**2, j]))
A[i**2*m + j]
>>> print(ccode(Symbol('float')))
float_
>>> print(ccode(A[Symbol('float'), 0]))
A[float*m]
```

### Expected
```pycon
>>> '**' in ccode(A[i**2, j])
False
>>> 'float_' in ccode(A[Symbol('float'), 0])
True
```

### Why it is wrong
The index is a SymPy expression formatted with `str()`, so `**` (not a C operator) appears, reserved words are not renamed, and other C-specific printing (functions, rationals) is skipped. The original reviewer compiled this with gcc; it was not executed here.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_MatrixElement` formats `expr.j + expr.i*expr.parent.shape[1]` directly into the string; it should go through `self._print`. The same pattern exists in `jscode.py`, `rust.py` (separate issues) and `rcode.py` (where `**` happens to be valid R).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
