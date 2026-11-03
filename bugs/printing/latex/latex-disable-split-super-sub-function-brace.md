# latex(f_1(x), disable_split_super_sub=True) gives unbalanced braces (\operatorname{f\}_1)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Function, symbols, latex
>>> x = symbols('x')
>>> print(latex(Function('f_1')(x), disable_split_super_sub=True))
\operatorname{f\}_1{\left(x \right)}
```

### Expected
```pycon
>>> s = latex(Function('f_1')(x), disable_split_super_sub=True).replace(r'\{', '').replace(r'\}', '')
>>> s.count('{') == s.count('}')
True
```

### Why it is wrong
The backslash of the escaped underscore ends up inside `\operatorname{...}` and escapes its closing brace, so the braces are unbalanced and the TeX does not compile.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._hprint_Function` first calls `_deal_with_super_sub`, which with `disable_split_super_sub=True` turns `f_1` into `f\_1`, and then splits the result at `func.find("_")`, i.e. between `\` and `_`. With the setting enabled the name must not be split at escaped underscores (the whole escaped name can go inside `\operatorname{}`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
