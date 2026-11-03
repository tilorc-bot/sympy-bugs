# latex() prints undefined functions named frac or root as the TeX commands \frac and \root

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Function, symbols, latex
>>> x = symbols('x')
>>> print(latex(Function('frac')(x)))
\frac{\left(x \right)}
>>> print(latex(Function('root')(x)))
\root{\left(x \right)}
```

### Expected
```pycon
>>> r'\frac{' in latex(Function('frac')(x)), r'\root{' in latex(Function('root')(x))
(False, False)
```

### Why it is wrong
`\frac` takes two arguments and `\root` is plain TeX's `\root n \of x`, so both outputs are TeX errors ("Missing } inserted" and similar) instead of an operator name applied to `x`.

### Notes on fixing
`sympy/printing/latex.py`: `accepted_latex_functions` contains `'frac'` and `'root'`, so `_hprint_Function` emits `\frac`/`\root` as if they were operator commands like `\sin`. SymPy's own `frac` has a dedicated `_print_frac` (`\operatorname{frac}`), and `root()` returns a `Pow`, so removing both names from the list only affects user functions (and the class-name checks in `_print_Poly`, `_print_ComplexRootOf`, `_print_RootSum`, which never see these names).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
