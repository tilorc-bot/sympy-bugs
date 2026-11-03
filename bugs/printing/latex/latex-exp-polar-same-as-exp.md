# exp_polar(x) and exp(x) print identically

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, exp, exp_polar, latex
>>> x = symbols('x')
>>> print(latex(exp_polar(x)))
e^{x}
>>> print(latex(exp(x)))
e^{x}
```

### Expected
```pycon
>>> latex(exp_polar(x)) != latex(exp(x))
True
```

### Why it is wrong
`exp_polar(x)` lives on the Riemann surface of the logarithm (`exp_polar(2*pi*I) != 1`), unlike `exp(x)`; printing both the same hides that difference, e.g. in results of `polarify` or Meijer G simplification.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_ExpBase` handles both classes and carries a TODO ("should exp_polar be printed differently?"). `str` distinguishes them (`exp_polar(x)`); `pretty` has the same problem.

### Related
[pretty-exp-polar-like-exp](../pretty/pretty-exp-polar-like-exp.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
