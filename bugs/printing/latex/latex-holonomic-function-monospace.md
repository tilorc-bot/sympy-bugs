# HolonomicFunction falls back to monospace str() text

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, QQ, latex
>>> from sympy.holonomic import HolonomicFunction, DifferentialOperators
>>> x = symbols('x')
>>> R, Dx = DifferentialOperators(QQ.old_poly_ring(x), 'Dx')
>>> print(latex(HolonomicFunction(Dx - 1, x, 0, [1])))
\mathtt{\text{HolonomicFunction((-1) + (1)*Dx, x, 0, [1])}}
```

### Expected
```pycon
>>> 'mathtt' in latex(HolonomicFunction(Dx - 1, x, 0, [1]))
False
```

### Why it is wrong
There is no LaTeX form at all: the whole object is printed as its `str()` in typewriter font, including Python syntax such as `(1)*Dx` and `[1]`.

### Notes on fixing
No `_print_HolonomicFunction` exists in `sympy/printing/latex.py` and `HolonomicFunction` (`sympy/holonomic/holonomic.py`) has no `_latex`, so `LatexPrinter.emptyPrinter` is used. The differential operator and the initial conditions both need a LaTeX rendering.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
