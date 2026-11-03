# Differential(R2_r.x)**2 prints \operatorname{d}x^{2}, which reads as d(x^2)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.diffgeom.rn import R2_r
>>> from sympy.diffgeom import Differential
>>> print(latex(Differential(R2_r.x)**2))
\operatorname{d}x^{2}
```

### Expected
```pycon
>>> latex(Differential(R2_r.x)**2).endswith(r'\right)^{2}')
True
```

### Why it is wrong
`\operatorname{d}x^{2}` is the differential of `x²`, not the square of the differential `dx`.

### Notes on fixing
`LatexPrinter._print_Differential` (`sympy/printing/latex.py`) prints `\operatorname{d}x`, a juxtaposition, but `Differential` has no precedence entry (Atom), so `_helper_print_standard_power` adds no brackets around the base.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
