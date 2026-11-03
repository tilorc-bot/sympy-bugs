# latex() prints MatMul(2, 3, A) as "2 3 A", which renders as 23 A

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, MatMul, Mul, symbols, latex
>>> A = MatrixSymbol('A', 2, 2)
>>> print(latex(MatMul(2, 3, A)))
2 3 A
>>> x = symbols('x')
>>> print(latex(Mul(2, 3, x, evaluate=False)))
2 \cdot 3 x
```

### Expected
```pycon
>>> latex(MatMul(2, 3, A)).replace(' ', '') != latex(MatMul(23, A)).replace(' ', '')
True
```

### Why it is wrong
Spaces are ignored in TeX math mode, so `2 3 A` renders exactly like `23 A`. The scalar `Mul` printer already inserts `\cdot` between adjacent numbers.

### Notes on fixing
`LatexPrinter._print_MatMul` (`sympy/printing/latex.py`) joins the printed factors with a plain space. It needs the same rule as `_print_Mul`: use the number separator (`\cdot`, or the `mul_symbol` setting) between two factors when the second one starts with a digit.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
