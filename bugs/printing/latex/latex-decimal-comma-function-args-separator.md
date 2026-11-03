# With decimal_separator='comma', function arguments are still separated by a comma

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import Function, latex
>>> f = Function('f')
>>> print(latex(f(1.5, 2.5), decimal_separator='comma'))
f{\left(1{,}5,2{,}5 \right)}
```

### Expected
```pycon
>>> ';' in latex(f(1.5, 2.5), decimal_separator='comma')
True
```

### Why it is wrong
With `decimal_separator='comma'` the comma is the decimal mark, so arguments must be separated by `;` as is already done for tuples, lists and sets. The output renders as `f(1,5,2,5)`, which reads as a function of four arguments.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Function` ends with `name % ",".join(args)`; the separator should depend on `decimal_separator` as in `_print_tuple`. Functions with their own printers that join arguments with `", "` have the same problem, e.g. `latex(Heaviside(x, 0.5), decimal_separator='comma')` gives `\theta\left(x, 0{,}5\right)`.

### Related
[latex-decimal-comma-interval-separator](latex-decimal-comma-interval-separator.md)
[latex-decimal-comma-minmax-separator](latex-decimal-comma-minmax-separator.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
