# x + Wild('w') uses w_ without declaring it

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, Wild, python
>>> x = Symbol('x')
>>> e = x + Wild('w')
>>> print(python(e))
x = Symbol('x')
e = x + w_
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
Executing the generated code raises `NameError: name 'w_' is not defined`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`PythonPrinter` (`sympy/printing/python.py`) registers names only in `_print_Symbol`; `Wild` is printed by `StrPrinter._print_Wild` as `w_` and never declared. A `_print_Wild` that records a `w_ = Wild('w')` declaration (keeping `exclude`/`properties`) is needed.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
