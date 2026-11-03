# ArrayAdd(A, -B) prints A + -1 \boxtimes B

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.tensor.array.expressions import ArraySymbol, ArrayAdd
>>> A, B = ArraySymbol('A', (2, 2)), ArraySymbol('B', (2, 2))
>>> print(latex(ArrayAdd(A, -B)))
A + -1 \boxtimes B
```

### Expected
```pycon
>>> '+ -' in latex(ArrayAdd(A, -B))
False
```

### Why it is wrong
A difference of arrays should print as `A - B`; instead a `+ -` sequence appears and the scalar factor is shown as a tensor product with `-1`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_ArrayAdd` joins the printed terms with `' + '` without any sign handling (compare `_print_TensAdd`, which at least replaces `+ -`). `-B` is `ArrayTensorProduct(-1, B)`, so `_print_ArrayTensorProduct` would also need to print a leading scalar coefficient as a sign/coefficient rather than a `\boxtimes` factor.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
