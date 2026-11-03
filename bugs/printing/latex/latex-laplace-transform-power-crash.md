# A power of LaplaceTransform raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Function, LaplaceTransform, latex
>>> t, s = symbols('t s')
>>> f = Function('f')
>>> latex(LaplaceTransform(f(t), t, s)**2)
Traceback (most recent call last):
...
TypeError: LatexPrinter._print_LaplaceTransform() got an unexpected keyword argument 'exp'...
```

### Expected
```pycon
>>> _ = latex(LaplaceTransform(f(t), t, s)**2)
```

### Why it is wrong
Printing must not fail for a valid expression.

### Notes on fixing
`LatexPrinter._print_Pow` passes `exp=` to the base's printer for every `is_Function` base (`sympy/printing/latex.py`, `_print_Pow` / `_helper_print_standard_power`). Printers that do not accept `exp` fail. The same happens for the Mellin, Fourier, Sine and Cosine transforms and their inverses, `Pow(Piecewise(...), 2, evaluate=False)`, `Lambda(x, x**2)**2`, and any Function subclass with a `_latex(self, printer)` method (e.g. the biomechanics curves, user-defined Functions).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
