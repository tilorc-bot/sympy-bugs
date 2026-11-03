# latex(Mul(x, 3, evaluate=False)) prints x 3 with no multiplication sign

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, sin, Mul, latex
>>> x = symbols('x')
>>> print(latex(Mul(x, 3, evaluate=False)))
x 3
>>> print(latex(Mul(sin(2), 3, evaluate=False)))
\sin{\left(2 \right)} 3
```

### Expected
```pycon
>>> r'\cdot' in latex(Mul(x, 3, evaluate=False))
True
>>> r'\cdot' in latex(Mul(sin(2), 3, evaluate=False))
True
```

### Why it is wrong
A number written after a symbol or function renders as `x3`, which reads as a subscripted `x_3` or a misprint rather than `x*3`; the unevaluated-Mul path exists to show the factors faithfully, and between two numbers it already inserts `\cdot`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Mul`, `convert_args`, inserts `mul_symbol_latex_numbers` only when the previous term ends with a digit and the next starts with one (`_between_two_numbers_p`); it should also do so when a non-leading factor is a number.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
