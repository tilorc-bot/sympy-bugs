# pretty() prints FunctionMatrix as a 1x1 matrix of its lambda body

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, FunctionMatrix, Lambda, Matrix, pretty
>>> i, j = symbols('i j')
>>> print(pretty(FunctionMatrix(2, 2, Lambda((i, j), i + j)), use_unicode=True))
[i + j]
>>> print(pretty(Matrix([[i + j]]), use_unicode=True))
[i + j]
```

### Expected
```pycon
>>> pretty(FunctionMatrix(2, 2, Lambda((i, j), i + j)), use_unicode=True) != pretty(Matrix([[i + j]]), use_unicode=True)
True
>>> pretty(FunctionMatrix(2, 2, Lambda((i, j), i + j)), use_unicode=True) != pretty(FunctionMatrix(3, 3, Lambda((i, j), i + j)), use_unicode=True)
True
```

### Why it is wrong
A 2x2 matrix with entries `i + j` is shown exactly like the 1x1 matrix `Matrix([[i + j]])`; the shape and the index variables are lost.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_FunctionMatrix` only prints `X.lamda.expr` in square brackets. It should show the shape and the indices, e.g. `[i + j] for i=0..1, j=0..1`, or fall back to the `FunctionMatrix(2, 2, Lambda(...))` form used by `str`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
