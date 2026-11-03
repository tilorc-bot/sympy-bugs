# Content MathML of a Piecewise without a True condition raises ValueError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Piecewise, mathml
>>> x = symbols('x')
>>> mathml(Piecewise((x, x > 0)))
Traceback (most recent call last):
...
ValueError: All Piecewise expressions must contain an (expr, True) statement to be used as a default condition...
```

### Why it is wrong
`Piecewise((x, x > 0))` is a valid expression (undefined for x ≤ 0), and content MathML's `<piecewise>` allows omitting `<otherwise>`; LaTeX prints it as a one-case `cases` environment.

### Notes on fixing
`MathMLContentPrinter._print_Piecewise` (`sympy/printing/mathml.py`) copies the check from the code printers, where a missing default matters for generated code. For MathML the check can be dropped: emit `<piece>` for every pair and `<otherwise>` only when the last condition is `True`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
