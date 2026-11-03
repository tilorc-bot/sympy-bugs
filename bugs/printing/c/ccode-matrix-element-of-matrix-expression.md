# An element of A - B prints as (A - B)[0], which does not compile

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol, ccode, cxxcode
>>> A, B, C = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2), MatrixSymbol('C', 2, 2)
>>> F = C[0, 0].subs(C, A - B)
>>> print(ccode(F))
(A - B)[0]
>>> print(cxxcode(F))
(A - B)[0]
>>> from codecheck import compile_errors, run_code
>>> print(compile_errors('c', ccode(F), A=[float], B=[float]))
error: subscripted value is neither array nor pointer nor vector
>>> print(compile_errors('c++', cxxcode(F), A=[float], B=[float]))
error: invalid types '...[int]' for array subscript
```

### Expected
```pycon
>>> run_code('c', ccode(F), A=[5.0, 0.0, 0.0, 0.0], B=[2.0, 0.0, 0.0, 0.0])
3.0
>>> run_code('c++', cxxcode(F), A=[5.0, 0.0, 0.0, 0.0], B=[2.0, 0.0, 0.0, 0.0])
3.0
>>> compile_errors('c', ccode(F), A=[float], B=[float]) == ''
True
>>> compile_errors('c++', cxxcode(F), A=[float], B=[float]) == ''
True
```

### Why it is wrong
`A` and `B` are flat C arrays, so `A - B` is pointer arithmetic (or an error) and cannot be indexed. gcc reports: `subscripted value is neither array nor pointer nor vector` (g++: `invalid types 'long int[int]' for array subscript`). The element is `A[0] - B[0]`, which is what `ccode((A - B)[0, 0])` prints.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_MatrixElement` parenthesizes `expr.parent` and appends a flat index, which is only valid when the parent is a `MatrixSymbol`. When the parent is a matrix expression it could print the evaluated entry instead (`expr.parent[expr.i, expr.j]`, which gives `A[0, 0] - B[0, 0]`), or raise. The same pattern is in `jscode.py` and `fortran.py` (separate issues).

The output is asserted by `test_MatrixElement_printing` in `sympy/printing/tests/test_c.py` (added for [sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)), so a fix must update that test.

### Related
[sympy/sympy#11821](https://redirect.github.com/sympy/sympy/issues/11821)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
