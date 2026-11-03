# Presentation MathML of a derivative of symbolic order raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative, mathml
>>> x, n = symbols('x n')
>>> f = Function('f')
>>> mathml(Derivative(f(x), (x, n)), printer='presentation')
Traceback (most recent call last):
...
TypeError: cannot determine truth value of Relational: n >= 2
```

### Why it is wrong
Printing must not fail for a valid expression; the LaTeX and str printers handle a symbolic order.

### Notes on fixing
`MathMLPresentationPrinter._print_Derivative` (`sympy/printing/mathml.py`) tests `if num >= 2:` and `if dim >= 2:` on the counts. Use structural tests (`num != 1`, `dim != 1`) so that symbolic orders get a superscript.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
