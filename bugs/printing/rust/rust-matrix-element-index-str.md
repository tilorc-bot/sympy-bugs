# rust_code() prints the flattened index of a MatrixElement with str(), e.g. A[i**2*m + j]

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Symbol, MatrixSymbol, rust_code
>>> i, j, n, m = symbols('i j n m')
>>> A = MatrixSymbol('A', n, m)
>>> print(rust_code(A[i**2, j]))
A[i**2*m + j]
>>> print(rust_code(Symbol('fn')))
fn_
>>> print(rust_code(A[Symbol('fn'), 0]))
A[fn*m]
```

### Expected
```pycon
>>> '**' in rust_code(A[i**2, j])
False
>>> 'fn_' in rust_code(A[Symbol('fn'), 0])
True
```

### Why it is wrong
The index is a SymPy expression formatted with `str()`, so `**` (not a Rust operator) appears and reserved words are not renamed; the generated code does not compile.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_MatrixElement` formats both `expr.parent` and `expr.j + expr.i*expr.parent.shape[1]` directly into the string; they should go through `self._print`/`self.parenthesize`. The same pattern exists in `c.py` and `jscode.py` (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
