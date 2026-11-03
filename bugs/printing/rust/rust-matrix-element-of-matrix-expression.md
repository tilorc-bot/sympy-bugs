# An element of A - B prints as A - B[0]

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol, rust_code
>>> A, B, C = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2), MatrixSymbol('C', 2, 2)
>>> F = C[0, 0].subs(C, A - B)
>>> print(rust_code(F))
A - B[0]
>>> from codecheck import compiles, compile_errors
>>> print(compile_errors('rust', rust_code(F), A=[float], B=[float]))
error[E0369]: cannot subtract `f64` from `&[f64]`...
```

### Expected
```pycon
>>> compiles('rust', rust_code(F), A=[float], B=[float])
True
>>> eval(rust_code(F), {'A': [5, 0, 0, 0], 'B': [2, 0, 0, 0]})
3
```

### Why it is wrong
The index binds to `B` only, so the code means `A - (B[0])` (an array minus a scalar; rustc: cannot subtract `f64` from `&[f64]`) instead of the element `A[0] - B[0]`.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_MatrixElement` formats `expr.parent` with `%s` (i.e. `str()`), without the printer and without parentheses. Parenthesizing alone would give `(A - B)[0]`, which is still not valid Rust for arrays; for a matrix-expression parent it should print the evaluated entry (`expr.parent[expr.i, expr.j]` gives `A[0, 0] - B[0, 0]`, which prints as `A[0] - B[0]`). Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
