# latex(x*C.i) wraps every sympy.vector coefficient in parentheses, even a single symbol

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.vector import CoordSys3D
>>> C = CoordSys3D('C')
>>> x = symbols('x')
>>> print(latex(x*C.i))
\left(x\right)\mathbf{\hat{i}_{C}}
>>> print(latex(x*C.i + 2*C.j))
\left(x\right)\mathbf{\hat{i}_{C}} + \left(2\right)\mathbf{\hat{j}_{C}}
```

### Expected
```pycon
>>> r'\left(x\right)' in latex(x*C.i)
False
```

### Why it is wrong
Parentheses around a symbol or number are noise; they are needed only for coefficients that are sums (or negative).

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_BasisDependent` always uses `r'\left(' + self._print(v) + r'\right)'`; `self.parenthesize(v, PRECEDENCE['Mul'])` would add parentheses only where needed. `test_latex_printing` in `sympy/vector/tests/test_printing.py` asserts the parenthesized form (`\left(a\right)\mathbf{\hat{i}_{N}} + ...`) and would need updating.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
