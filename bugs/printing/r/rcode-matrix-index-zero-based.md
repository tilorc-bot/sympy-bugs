# A[0, 0] prints A[0] and matrix assignment prints B[0] = x: R indices are 1-based

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Matrix, MatrixSymbol, rcode
>>> x, y, z = symbols('x y z')
>>> A = MatrixSymbol('A', 3, 3)
>>> B = MatrixSymbol('B', 3, 1)
>>> print(rcode(A[0, 0]))
A[0]
>>> print(rcode(A[0, 1]))
A[1]
>>> print(rcode(Matrix([x, y, z]), assign_to=B))
B[0] = x;
B[1] = y;
B[2] = z;
```

### Expected
```pycon
>>> '0' in rcode(A[0, 0])
False
>>> 'B[0]' in rcode(Matrix([x, y, z]), assign_to=B)
False
```

### Why it is wrong
R vectors and matrices are indexed from 1, and `A[0]` selects nothing (an empty vector); `B[0] = x` silently does nothing. Moreover the flat index is computed row-major (`A[0, 1]` becomes `A[1]`), while R stores matrices column-major, so even shifted by one it would address the wrong element; `A[1, 2]` is the unambiguous R form. The reviewer checked this against the R documentation.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._print_MatrixElement` prints `expr.j + expr.i*expr.parent.shape[1]`, copied from the C printer. It should print `A[i + 1, j + 1]` (through `self._print`). Matrix assignment goes through the same method. The current output is asserted by `test_Matrix_printing` and `test_MatrixElement_printing` in `sympy/printing/tests/test_rcode.py` (tested-buggy).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
