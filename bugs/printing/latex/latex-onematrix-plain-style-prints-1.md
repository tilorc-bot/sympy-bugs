# mat_symbol_style='plain' prints OneMatrix as a bare 1, so A*OneMatrix reads as A*1

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, MatMul, OneMatrix, S, latex
>>> A = MatrixSymbol('A', 2, 2)
>>> print(latex(MatMul(A, OneMatrix(2, 2)), mat_symbol_style='plain'))
A 1
>>> print(latex(OneMatrix(2, 2), mat_symbol_style='plain'))
1
```

### Expected
```pycon
>>> latex(OneMatrix(2, 2), mat_symbol_style='plain') != latex(S.One)
True
>>> latex(MatMul(A, OneMatrix(2, 2)), mat_symbol_style='plain') != 'A ' + latex(S.One)
True
```

### Why it is wrong
`A 1` denotes `A` times the scalar 1, i.e. `A`, while `A` times the all-ones matrix is the matrix of row sums of `A`. With the default style the all-ones matrix is `\mathbf{1}`, which is distinguishable; the plain style loses that.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_OneMatrix` returns `"1"` for `mat_symbol_style='plain'`. A distinct plain symbol is needed (e.g. `J` or `\mathbb{1}`). `_print_ZeroMatrix` likewise returns `0` (`MatAdd(A, ZeroMatrix(2, 2))` prints `A + 0`), which is less harmful since adding the zero matrix or the scalar 0 means the same thing.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
