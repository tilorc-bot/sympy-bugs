# Presentation MathML of Range(x, y) with symbolic bounds raises ValueError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Range, mathml
>>> x, y = symbols('x y', integer=True)
>>> mathml(Range(x, y), printer='presentation')
Traceback (most recent call last):
...
ValueError: Invalid method for symbolic Range
```

### Why it is wrong
Printing must not fail for a valid object.

### Notes on fixing
`MathMLPresentationPrinter._print_Range` (`sympy/printing/mathml.py`) calls `len(s)`, iterates and indexes `s[-1]`, all of which raise for symbolic bounds. A symbolic Range should be printed from `start`, `step` and `stop` (e.g. `{x, x+1, …, y-1}`); the LaTeX printer at least does not crash (it prints `\text{Range}\left(x, y\right)`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
