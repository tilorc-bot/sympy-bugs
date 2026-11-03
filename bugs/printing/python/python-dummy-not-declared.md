# python(Dummy('x') + 1) uses _x without declaring it

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Dummy, python
>>> e = Dummy('x') + 1
>>> print(python(e))
e = _x + 1
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> len(ns['e'].free_symbols)
1
```

### Why it is wrong
Executing the generated code raises `NameError: name '_x' is not defined`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`Dummy` is printed by `StrPrinter._print_Dummy` as `_x`, which bypasses `sympy/printing/python.py:PythonPrinter._print_Symbol` where declarations are recorded. A `_print_Dummy` that declares e.g. `_x = Dummy('x')` is needed.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
