# The flattened index of a MatrixElement is printed with str(), e.g. A[m*floor(x)]

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, floor
>>> from sympy.printing.jscode import jscode
>>> x, i, j, n, m = symbols('x i j n m')
>>> A = MatrixSymbol('A', n, m)
>>> print(jscode(floor(x)))
Math.floor(x)
>>> print(jscode(A[floor(x), 0]))
A[m*floor(x)]
```

### Expected
```pycon
>>> 'Math.floor' in jscode(A[floor(x), 0])
True
```

### Why it is wrong
The index is a SymPy expression formatted with `str()`, so JavaScript-specific printing is skipped: `floor` is undefined in JavaScript (it is `Math.floor`). The original reviewer ran this kind of code with node; it was not executed here.

### Notes on fixing
`sympy/printing/jscode.py:JavascriptCodePrinter._print_MatrixElement` formats `expr.j + expr.i*expr.parent.shape[1]` directly into the string; it should go through `self._print`. The same pattern exists in `c.py` and `rust.py` (separate issues).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
