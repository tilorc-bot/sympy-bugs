# Trailing digits/underscores of built-in function names become subscripts (atan_{2})

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, atan2, latex
>>> from sympy.functions.combinatorial.numbers import jacobi_symbol
>>> from sympy.codegen.cfunctions import expm1
>>> x, y = symbols('x y')
>>> print(latex(atan2(y, x)))
\operatorname{atan}_{2}{\left(y,x \right)}
>>> print(latex(jacobi_symbol(x, y)))
\operatorname{jacobi}_{symbol}{\left(x,y \right)}
>>> print(latex(expm1(x)))
\operatorname{expm}_{1}{\left(x \right)}
```

### Expected
```pycon
>>> '}_{' in latex(atan2(y, x))
False
>>> '}_{' in latex(jacobi_symbol(x, y))
False
>>> '}_{' in latex(expm1(x))
False
```

### Why it is wrong
The name of a built-in function is a fixed identifier, not a symbol with a subscript: `atan_2`, `jacobi_{symbol}` and `expm_1` read as indexed functions called `atan`, `jacobi`, `expm`, and `expm_1(x)` gives no hint that it means `exp(x) - 1`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._hprint_Function` runs every name through `_deal_with_super_sub`, which is right for user-defined functions (`Function('f_1')`) but not for the class names of built-in functions reached via `_print_Function`. Built-in names should be kept whole (e.g. `\operatorname{atan2}`, with `_` escaped). Other affected built-ins include `erf2` (`\operatorname{erf}_{2}`) and the codegen function `exp2`.

### Related
[pretty-function-name-underscore-subscript](../pretty/pretty-function-name-underscore-subscript.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
