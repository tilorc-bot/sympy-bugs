# MatMul(A, -x, B) prints as A - x B

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, MatMul, latex
>>> x = symbols('x')
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> print(latex(MatMul(A, -x, B)))
A - x B
>>> print(latex(MatMul(A, -x)))
A - x
>>> print(latex(MatMul(A, -2)))
A \left(-2\right)
```

### Expected
```pycon
>>> ' - ' in latex(MatMul(A, -x, B))
False
```

### Why it is wrong
`A - x B` reads as the difference `A - xB`, not the product `A·(-x)·B`. A negative Integer factor is already bracketed (`A \left(-2\right)`), a negative symbolic factor is not.

### Notes on fixing
`LatexPrinter._print_MatMul` (`sympy/printing/latex.py`) prints every scalar `Mul` factor without brackets (`parens = lambda x: self._print(x) if isinstance(x, Mul) and not isinstance(x, MatMul) else ...`). The minus sign is only moved to the front when `expr.could_extract_minus_sign()`, which looks at the first argument only. A negative Mul factor that is not first needs brackets (or its sign moved to the front).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
