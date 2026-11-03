# inv_trig_style='full' is ignored for a bare function class such as asin

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import MatrixSymbol, asin, latex
>>> print(latex(asin, inv_trig_style='full'))
\operatorname{asin}
>>> A = MatrixSymbol('A', 2, 2)
>>> print(latex(A.applyfunc(asin), inv_trig_style='full'))
{\operatorname{asin}}_{\circ}\left({A}\right)
```

### Expected
```pycon
>>> 'arcsin' in latex(asin, inv_trig_style='full')
True
>>> 'arcsin' in latex(A.applyfunc(asin), inv_trig_style='full')
True
```

### Why it is wrong
`inv_trig_style` is honoured for `asin(x)` (`\arcsin{\left(x \right)}`) but not for the bare function class, so an elementwise application such as `A.applyfunc(asin)` uses a different name than `asin(x)` in the same document.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_FunctionClass` passes the class name straight to `_hprint_Function`; the `inv_trig_style` handling lives only in `_print_Function` and would need to be shared (the `power` style would give `\sin^{-1}`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
