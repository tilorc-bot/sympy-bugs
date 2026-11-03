# PurePoly(x**2 + 1, x) prints the generator _0 as a subscript with an empty base

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, PurePoly, latex
>>> x = symbols('x')
>>> print(latex(PurePoly(x**2 + 1, x)))
\operatorname{PurePoly}{\left( _0^{2} + 1, _0, domain=\mathbb{Z} \right)}
```

### Expected
```pycon
>>> import re
>>> re.search(r'(^|[\s(,{])_', latex(PurePoly(x**2 + 1, x))) is None
True
```

### Why it is wrong
`_0^{2}` and `, _0,` attach a subscript `0` to nothing, so the rendered generator is a lowered `0` that looks like a stray index rather than a variable.

### Notes on fixing
The generator of a `PurePoly` is `Symbol('_0')`; `sympy/printing/latex.py:LatexPrinter._print_Symbol` / `_deal_with_super_sub` splits a name with a leading underscore into an empty base and a subscript (`latex(Symbol('_x'))` gives `_x` too). Either `_print_Poly` should print `PurePoly` generators specially, or names with a leading `_` should not be split (escape the `_`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
