# python(Symbol('x_{1}') + 2*Symbol('x_1')) declares x_1 twice and merges the two symbols

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Symbol, python
>>> e = Symbol('x_{1}') + 2*Symbol('x_1')
>>> print(python(e))
x_1 = Symbol('x_1')
x_1 = Symbol('x_{1}')
e = 3*x_1
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> ns['e'] == e
True
```

### Why it is wrong
The two distinct symbols `x_{1}` and `x_1` get the same Python name, so the generated code defines one of them twice and the expression collapses to `3*x_1`; executing it gives `3*x_{1}`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python` strips `{` and `}` from symbol names to make identifiers but, unlike the keyword-renaming branch, does not check whether the new name is already taken by another symbol or function.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
