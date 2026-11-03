# Permutation with perm_cyclic=False uses pmatrix for more than 10 columns

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.combinatorics import Permutation
>>> p = Permutation(list(range(1, 11)) + [0])
>>> print(latex(p, perm_cyclic=False))
\begin{pmatrix} 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 \\ 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 0 \end{pmatrix}
```

### Expected
```pycon
>>> 'pmatrix' in latex(p, perm_cyclic=False)
False
```

### Why it is wrong
amsmath's `pmatrix` allows at most 10 columns by default (`MaxMatrixCols`), so the output of any permutation of size above 10 fails with "Extra alignment tab has been changed to \cr".

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Permutation` always uses `pmatrix`. `_print_MatrixBase` and `_print_NDimArray` already switch to `\left(\begin{array}{cc...}...\end{array}\right)` when there are more than 10 columns; the same should be done here.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
