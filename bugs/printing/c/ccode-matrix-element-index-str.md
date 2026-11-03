# The flattened index of a MatrixElement is printed with str(), e.g. A[i**2*m + j]

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
>>> from codecheck import compile_errors, compiles
>>> print(compile_errors('c', ccode(A[i**2, j]), A=[float], i=int, j=int, m=int))
error: invalid type argument of unary '*' (have 'int')
>>> print(compile_errors('c', ccode(A[Symbol('float'), 0]), A=[float], m=int, float_=int))
error: expected expression before 'float'
```

### Expected
```pycon
>>> '**' in ccode(A[i**2, j])
False
>>> compiles('c', ccode(A[Symbol('float'), 0]), A=[float], m=int, float_=int)
True
```

### Why it is wrong
The index is a SymPy expression formatted with `str()`, so `**` (not a C operator) appears, reserved words are not renamed, and other C-specific printing (functions, rationals) is skipped. gcc rejects both examples (`invalid type argument of unary '*'`, `expected expression before 'float'`). Expected checks `**` as a string because even `A[pow(i, 2)*m + j]` would not compile (`pow` returns `double`, not an array subscript).

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_MatrixElement` formats `expr.j + expr.i*expr.parent.shape[1]` directly into the string; it should go through `self._print`. The same pattern exists in `jscode.py`, `rust.py` (separate issues) and `rcode.py` (where `**` happens to be valid R).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
