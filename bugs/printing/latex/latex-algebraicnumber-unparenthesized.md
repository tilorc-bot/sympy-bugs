# latex() does not bracket an AlgebraicNumber that prints as a sum: x*AlgebraicNumber(sqrt(2), [1, 2]) prints as x \sqrt{2} + 2

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, sqrt, AlgebraicNumber, Pow, latex
>>> x = symbols('x')
>>> alpha = AlgebraicNumber(sqrt(2), [1, 2])
>>> print(latex(x*alpha))
x \sqrt{2} + 2
>>> print(latex(Pow(alpha, 2, evaluate=False)))
\sqrt{2} + 2^{2}
```

### Expected
```pycon
>>> r'\left(\sqrt{2} + 2\right)' in latex(x*alpha)
True
>>> r'\left(\sqrt{2} + 2\right)' in latex(Pow(alpha, 2, evaluate=False))
True
```

### Why it is wrong
`alpha` is `sqrt(2) + 2`, so the product is `x (sqrt(2) + 2)` and the power `(sqrt(2) + 2)^2`; the output reads as `x sqrt(2) + 2` and `sqrt(2) + 4`.

### Notes on fixing
`LatexPrinter._print_AlgebraicNumber` (`sympy/printing/latex.py`) prints `expr.as_expr()` (or `as_poly().as_expr()`), but `AlgebraicNumber` is an Atom, so `_print_Mul`/`_print_Pow` decide on brackets from Atom precedence. The precedence has to come from the expression actually printed (e.g. a precedence function for AlgebraicNumber, or parenthesizing in `_print_Mul`/`_print_Pow`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
