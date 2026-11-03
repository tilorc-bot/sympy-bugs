# srepr() of MutableDenseNDimArray prints a plain list

### Kind
lossy

### Actual
```pycon
>>> from sympy import MutableDenseNDimArray, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> a = MutableDenseNDimArray([1, 2])
>>> srepr(a)
'[1, 2]'
>>> type(eval(srepr(a), ns))
<class 'list'>
```

### Expected
```pycon
>>> eval(srepr(a), ns) == a
True
```

### Why it is wrong
The type, the shape and the SymPy number types of the elements are all lost (`srepr(Array([1, 2]))` keeps them).

### Notes on fixing
Mutable arrays are not `Basic` and have no `args`, so `ReprPrinter.emptyPrinter` (`sympy/printing/repr.py`) falls back to `str()`. A handler for `NDimArray` should print the class name with the nested list and shape, as for matrices (`_print_MatrixBase`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
