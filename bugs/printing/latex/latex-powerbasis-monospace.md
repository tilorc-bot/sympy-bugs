# PowerBasis falls back to monospace str() text

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Poly, cyclotomic_poly, latex
>>> from sympy.polys.numberfields.modules import PowerBasis
>>> x = symbols('x')
>>> print(latex(PowerBasis(Poly(cyclotomic_poly(5, x)))))
\mathtt{\text{PowerBasis(x**4 + x**3 + x**2 + x + 1)}}
```

### Expected
```pycon
>>> 'mathtt' in latex(PowerBasis(Poly(cyclotomic_poly(5, x))))
False
```

### Why it is wrong
The defining polynomial is shown in Python syntax (`x**4`) in typewriter font instead of being printed as LaTeX.

### Notes on fixing
No `_print_PowerBasis` (or `_latex` on `sympy/polys/numberfields/modules.py:PowerBasis`) exists, so `LatexPrinter.emptyPrinter` is used. Related module classes (`Submodule`, `PowerBasisElement`) should be checked at the same time.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
