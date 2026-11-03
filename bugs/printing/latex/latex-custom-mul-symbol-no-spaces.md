# latex(..., mul_symbol=r'\star') glues the symbol to the next factor (2\starx)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, latex
>>> x = symbols('x')
>>> print(latex(2*x, mul_symbol=r'\star'))
2\starx
```

### Expected
```pycon
>>> r'\starx' in latex(2*x, mul_symbol=r'\star')
False
```

### Why it is wrong
TeX reads `\starx` as one undefined control sequence, so any custom `mul_symbol` that is a control word produces output that does not compile.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter.__init__` uses a `mul_symbol` that is not in `mul_symbol_table` verbatim for `mul_symbol_latex` and `mul_symbol_latex_numbers`, whereas the table entries carry surrounding spaces (`r" \times "`). Free-group elements use the same setting (`_print_FreeGroupElement`): `x\stary`. A fix cannot simply pad every custom symbol, because `sympy/printing/tests/test_latex.py` asserts `latex(3*x**2*y, mul_symbol='\\,') == r"3\,x^{2}\,y"`; padding (or a trailing `{}`) is needed at least when the symbol ends in a letter. Custom strings are also undocumented: the `latex()` docstring lists only `None`, `'ldot'`, `'dot'` and `'times'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
