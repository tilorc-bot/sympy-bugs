# sstr() and latex() of the class TableForm (not an instance) raise TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import sstr, latex
>>> from sympy.printing.tableform import TableForm
>>> sstr(TableForm)
Traceback (most recent call last):
...
TypeError: TableForm._sympystr() missing 1 required positional argument: 'p'
>>> latex(TableForm)
Traceback (most recent call last):
...
TypeError: TableForm._latex() missing 1 required positional argument: 'printer'
```

### Why it is wrong
Printing a class object should not crash (`sstr(Symbol)` gives `<class 'sympy.core.symbol.Symbol'>`); here e.g. printing a list or dict that contains such a class fails.

### Notes on fixing
`sympy/printing/printer.py:Printer._print` finds the method named `printmethod` (`_sympystr`, `_latex`, ...) on `expr` and calls it as a bound method. It skips classes only if they are subclasses of `Basic` (`isinstance(expr, type) and issubclass(expr, Basic)`); for any other class that defines the print method (TableForm, or user classes) the unbound function is called and is missing its `printer` argument. The check should skip all classes (`isinstance(expr, type)`). The issue's other example, `sstr(Vector)`, now prints `<class 'sympy.vector.vector.Vector'>` because Vector is a Basic subclass.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
