# latex(Interval(1.5, 2.5), decimal_separator='comma') still separates the endpoints with a comma

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import Interval, latex
>>> print(latex(Interval(1.5, 2.5), decimal_separator='comma'))
\left[1{,}5, 2{,}5\right]
```

### Expected
```pycon
>>> ';' in latex(Interval(1.5, 2.5), decimal_separator='comma')
True
```

### Why it is wrong
With `decimal_separator='comma'` the comma is the decimal mark, so the endpoints must be separated by `;` as is already done for tuples, lists and sets. The output renders as `[1,5, 2,5]`, which can be read as an interval with four numbers.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Interval` hard-codes `", "` between the endpoints instead of choosing the separator like `_print_tuple` does. `_print_AccumulationBounds` has the same problem: `latex(AccumBounds(1.5, 2.5), decimal_separator='comma')` gives `\left\langle 1{,}5, 2{,}5\right\rangle`.

### Related
[latex-decimal-comma-function-args-separator](latex-decimal-comma-function-args-separator.md)
[latex-decimal-comma-minmax-separator](latex-decimal-comma-minmax-separator.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
