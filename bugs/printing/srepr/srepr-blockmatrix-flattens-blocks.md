# srepr() of BlockMatrix evaluates back to a flattened explicit matrix

### Kind
lossy

### Actual
```pycon
>>> from sympy import MatrixSymbol, BlockMatrix, srepr
>>> from sympy.core.symbol import Str
>>> ns = {'Str': Str}
>>> exec('from sympy import *', ns)
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> M = BlockMatrix([[A, B]])
>>> srepr(M)
"BlockMatrix(ImmutableDenseMatrix([[MatrixSymbol(Str('A'), Integer(2), Integer(2)), MatrixSymbol(Str('B'), Integer(2), Integer(2))]]))"
>>> eval(srepr(M), ns).blocks.shape
(2, 4)
```

### Expected
```pycon
>>> eval(srepr(M), ns) == M
True
```

### Why it is wrong
Evaluating the srepr gives a BlockMatrix whose single "block" is the explicit 2x4 matrix of elements `A[0, 0], ...`, not the 1x2 block matrix `[[A, B]]`. (`Str` is added to the namespace here so that only this problem is shown.)

### Notes on fixing
`BlockMatrix` stores its blocks in an `ImmutableDenseMatrix`; `ReprPrinter._print_MatrixBase` (`sympy/printing/repr.py`) prints that as `ImmutableDenseMatrix([[A, B]])`, and the matrix constructor then expands the matrix symbols into their elements. A `_print_BlockMatrix` printing `BlockMatrix([[A, B]])` (a list of lists) avoids this.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
