# python(Symbol('Symbol') + y) assigns to Symbol and then calls it

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, python
>>> e = Symbol('Symbol') + Symbol('y')
>>> print(python(e))
Symbol = Symbol('Symbol')
y = Symbol('y')
e = Symbol + y
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> ns['e'] == e
True
```

### Why it is wrong
After the first line `Symbol` is no longer the constructor, so executing the output raises `TypeError: 'Symbol' object is not callable`. The same happens for a symbol named `Function` before a function declaration.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python` does not rename symbol or function names that clash with the names used in the generated code (`Symbol`, `Function`) or with other SymPy names the expression is printed with (e.g. a symbol called `sin` next to `sin(x)`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
