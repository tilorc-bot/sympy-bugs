# A derivative of symbolic order raises TypeError (content MathML)

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative, mathml
>>> x, n = symbols('x n')
>>> f = Function('f')
>>> mathml(Derivative(f(x), (x, n)))
Traceback (most recent call last):
...
TypeError: cannot determine truth value of Relational: n > 1
```

### Why it is wrong
Printing must not fail for a valid expression; the LaTeX and str printers handle a symbolic order.

### Notes on fixing
`MathMLContentPrinter._print_Derivative` (`sympy/printing/mathml.py`) tests `if times > 1:` on the derivative count. Use `if times != 1` (structural) so that a symbolic count gets a `<degree>`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
