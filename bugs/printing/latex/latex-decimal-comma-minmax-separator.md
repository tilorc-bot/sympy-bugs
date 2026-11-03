# latex(Max(x, y, 1.5), decimal_separator='comma') separates the arguments with a comma

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import symbols, Max, latex
>>> x, y = symbols('x y')
>>> print(latex(Max(x, y, 1.5), decimal_separator='comma'))
\max\left(1{,}5, x, y\right)
```

### Expected
```pycon
>>> ';' in latex(Max(x, y, 1.5), decimal_separator='comma')
True
```

### Why it is wrong
With `decimal_separator='comma'` the comma is the decimal mark, so the arguments must be separated by `;` as is already done for tuples, lists and sets. The output renders as `max(1,5, x, y)`, which reads like `Max(1, 5, x, y)`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._hprint_variadic_function` (used for `Min` and `Max`) joins with `", "` regardless of `decimal_separator`.

### Related
[latex-decimal-comma-interval-separator](latex-decimal-comma-interval-separator.md)
[latex-decimal-comma-function-args-separator](latex-decimal-comma-function-args-separator.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
