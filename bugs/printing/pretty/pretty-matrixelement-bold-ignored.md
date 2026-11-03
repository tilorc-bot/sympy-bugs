# pretty(mat_symbol_style='bold') does not make the matrix in A[0, 1] bold

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import MatrixSymbol, pretty
>>> A = MatrixSymbol('A', 2, 2)
>>> print(pretty(A[0, 1], use_unicode=True, mat_symbol_style='bold'))
A₀₁
>>> print(pretty(A, use_unicode=True, mat_symbol_style='bold'))
𝐀
```

### Expected
```pycon
>>> pretty(A[0, 1], use_unicode=True, mat_symbol_style='bold') != pretty(A[0, 1], use_unicode=True)
True
```

### Why it is wrong
With symbolic indices the element prints as `(𝐀)[i, 0]`, and `latex(A[0, 1], mat_symbol_style='bold')` gives `{\mathbf{A}}_{0,1}`, but for numeric indices the setting is silently dropped.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_MatrixElement` handles numeric indices by printing `Symbol(expr.parent.name + '_%d%d' % (i, j))`, which goes through `_print_Symbol` without `bold_name`. It should pass `bold_name=self._settings['mat_symbol_style'] == 'bold'` (as `_print_MatrixSymbol` does), so that only the base name is made bold.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
