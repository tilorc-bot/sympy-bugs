# latex(DomainMatrix(...)) falls back to monospace str() text instead of a matrix

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import ZZ, latex
>>> from sympy.polys.matrices import DomainMatrix
>>> print(latex(DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ)))
\mathtt{\text{DomainMatrix([[1, 2]], (1, 2), ZZ)}}
```

### Expected
```pycon
>>> 'mathtt' in latex(DomainMatrix([[ZZ(1), ZZ(2)]], (1, 2), ZZ))
False
```

### Why it is wrong
A matrix is printed as its Python constructor call in typewriter font rather than as a LaTeX matrix.

### Notes on fixing
No `_print_DomainMatrix` exists in `sympy/printing/latex.py`, so `LatexPrinter.emptyPrinter` is used. Printing `expr.to_Matrix()` would be the simplest fix.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
