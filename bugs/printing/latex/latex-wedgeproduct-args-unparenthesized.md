# Add arguments of WedgeProduct are not bracketed: WedgeProduct(dx + dy, dx) prints as dx + dy \wedge dx

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.diffgeom.rn import R2_r
>>> from sympy.diffgeom import WedgeProduct
>>> dx, dy = R2_r.dx, R2_r.dy
>>> print(latex(WedgeProduct(dx + dy, dx)))
\operatorname{d}x + \operatorname{d}y \wedge \operatorname{d}x
```

### Expected
```pycon
>>> latex(WedgeProduct(dx + dy, dx)) != latex(dx + WedgeProduct(dy, dx))
True
```

### Why it is wrong
`dx + dy \wedge dx` reads as `dx + (dy ∧ dx)`, a different form from `(dx + dy) ∧ dx`.

### Notes on fixing
`LatexPrinter._print_WedgeProduct` (`sympy/printing/latex.py`) joins `self._print(a)` for every argument with ` \wedge `; arguments of lower precedence need brackets. `_print_TensorProduct` has the same code (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
