# 2*MatrixSymbol('A', 2, 2) uses A without declaring it

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol, python
>>> e = 2*MatrixSymbol('A', 2, 2)
>>> print(python(e))
e = 2*A
```

### Expected
```pycon
>>> def run(code):
...     ns = {}
...     exec('from sympy import *\n' + code, ns)
...     return ns['e']
>>> run(python(e)) == e
True
```

### Why it is wrong
Executing the generated code raises `NameError: name 'A' is not defined`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:PythonPrinter` records declarations only in `_print_Symbol` and `_print_Function`; `MatrixSymbol` is printed by the str printer and never declared. A `_print_MatrixSymbol` that records `A = MatrixSymbol('A', 2, 2)` is needed.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
