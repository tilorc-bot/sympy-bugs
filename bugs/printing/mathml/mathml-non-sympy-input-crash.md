# mathml(1.5) and mathml({x: 1}) raise AttributeError: 'str' object has no attribute 'toxml'

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, mathml
>>> x = symbols('x')
>>> mathml(1.5)
Traceback (most recent call last):
...
AttributeError: 'str' object has no attribute 'toxml'
>>> mathml({x: 1})
Traceback (most recent call last):
...
AttributeError: 'str' object has no attribute 'toxml'
```

### Why it is wrong
Every other printer accepts plain Python numbers and containers (or sympifies them); here a float gives an obscure internal error.

### Notes on fixing
`MathMLPrinterBase.doprint` (`sympy/printing/mathml.py`) calls `.toxml()` on the result of `Printer._print`. For objects without a handler, `Printer.emptyPrinter` returns a `str`, which has no `toxml`. `mathml('abc')` fails the same way. `doprint` should wrap a string result in a text node (or the printers should define `emptyPrinter`, and `_print_float`/`_print_dict`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
