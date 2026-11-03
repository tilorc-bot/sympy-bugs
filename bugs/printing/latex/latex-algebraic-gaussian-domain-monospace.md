# Algebraic fields and Gaussian domains print as monospace str() text (QQ<sqrt(2)>, ZZ_I)

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, sqrt, Poly, QQ, ZZ_I, latex
>>> x = symbols('x')
>>> print(latex(QQ.algebraic_field(sqrt(2))))
\mathtt{\text{QQ<sqrt(2)>}}
>>> print(latex(ZZ_I))
\mathtt{\text{ZZ\_I}}
>>> print(latex(Poly(x + sqrt(2), x, extension=True)))
\operatorname{Poly}{\left( x + \sqrt{2}, x, domain=\mathtt{\text{QQ<sqrt(2)>}} \right)}
```

### Expected
```pycon
>>> 'mathtt' in latex(QQ.algebraic_field(sqrt(2)))
False
>>> 'mathtt' in latex(ZZ_I)
False
>>> 'mathtt' in latex(Poly(x + sqrt(2), x, extension=True))
False
```

### Why it is wrong
`ZZ`, `QQ`, `GF(p)`, `RR`, `CC` and polynomial rings print as mathematical notation (`\mathbb{Q}` etc.), but these domains fall back to the monospace `str()` form, so a `Poly` over `QQ<sqrt(2)>` shows `domain=QQ<sqrt(2)>` in typewriter font instead of `\mathbb{Q}\left(\sqrt{2}\right)`.

### Notes on fixing
`sympy/printing/latex.py` has no `_print_AlgebraicField`, `_print_GaussianIntegerRing` or `_print_GaussianRationalField`, so `LatexPrinter.emptyPrinter` is used. `QQ_I` (`\mathtt{\text{QQ\_I}}`) and `EX`/`EXRAW` are affected the same way.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
