# udivisor_sigma(n, k + 1) prints the subscript without braces: \sigma^*_k + 1\left(n\right)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.functions.combinatorial.numbers import udivisor_sigma
>>> n, k = symbols('n k')
>>> print(latex(udivisor_sigma(n, k + 1)))
\sigma^*_k + 1\left(n\right)
>>> print(latex(udivisor_sigma(n, 10)))
\sigma^*_10\left(n\right)
```

### Expected
```pycon
>>> print(latex(udivisor_sigma(n, 10)))
\sigma^*_{10}\left(n\right)
>>> print(latex(udivisor_sigma(n, k + 1)))
\sigma^*_{k + 1}\left(n\right)
```

### Why it is wrong
A TeX subscript without braces takes one token, so `\sigma^*_10(n)` renders as `σ*₁ 0(n)` and `\sigma^*_k + 1(n)` as `σ*_k + 1(n)`.

### Notes on fixing
`LatexPrinter._print_udivisor_sigma` (`sympy/printing/latex.py`) uses the template `r"_%s\left(%s\right)"`; it needs `_{%s}`. The tests in `test_latex_functions` (`sympy/printing/tests/test_latex.py`) that assert `\sigma^*_y\left(x\right)` have to be updated with it. `_print_divisor_sigma` has the same bug (separate issue); the power form `\sigma^*^{2}` is a separate double-superscript bug.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
