# DFT(alpha) prints the size with str(), giving \text{DFT}_{alpha}

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import Symbol, latex
>>> from sympy.matrices.expressions.fourier import DFT
>>> print(latex(DFT(Symbol('alpha'))))
\text{DFT}_{alpha}
```

### Expected
```pycon
>>> r'\alpha' in latex(DFT(Symbol('alpha')))
True
```

### Why it is wrong
The size is inserted with `str()` instead of being printed as LaTeX, so Greek letters, subscripted names and any expression other than a plain symbol or integer come out as raw text (here the word "alpha" instead of the letter).

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_DFT` (also used for `IDFT`) formats `expr.n` directly; it should use `self._print(expr.n)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
