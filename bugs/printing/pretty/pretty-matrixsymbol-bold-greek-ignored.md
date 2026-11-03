# mat_symbol_style='bold' has no effect on MatrixSymbols with Greek names

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import MatrixSymbol, pretty
>>> omega = MatrixSymbol('omega', 2, 2)
>>> print(pretty(omega, use_unicode=True, mat_symbol_style='bold'))
ω
>>> print(pretty(omega, use_unicode=True))
ω
```

### Expected
```pycon
>>> pretty(omega, use_unicode=True, mat_symbol_style='bold') != pretty(omega, use_unicode=True)
True
```

### Why it is wrong
Latin-named matrix symbols are printed bold (`𝐀`), and `latex(omega, mat_symbol_style='bold')` gives `\mathbf{\omega}`, but Greek-named ones are printed in the normal style, so a matrix is indistinguishable from a scalar of the same name.

### Notes on fixing
In `sympy/printing/pretty/pretty_symbology.py` the `greek_bold_unicode` table is built with `g`/`G` (the plain Greek letter lambdas) instead of the bold `gb`/`GB` defined just above it, and `GB` contains a typo (`'MATHEMATICAL BOLD CAPITAL  %s'` with two spaces). `greek_bold_unicode['lambda']`/`['Lambda']` are also set to the non-bold letters. Using `gb`/`GB` (after fixing the typo; Unicode has MATHEMATICAL BOLD SMALL/CAPITAL letters for the whole Greek alphabet, with `LAMDA` spelling) fixes the table.

The test `test_matrixSymbolBold` in `sympy/printing/pretty/tests/test_pretty.py` asserts the buggy output: `assert boldpretty(omega) == 'ω'`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
