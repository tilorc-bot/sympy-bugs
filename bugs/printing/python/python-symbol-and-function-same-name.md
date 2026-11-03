# python(f(x) + Symbol('f')) declares f both as a Symbol and as a Function

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, Function, python
>>> x = Symbol('x')
>>> e = Function('f')(x) + Symbol('f')
>>> print(python(e))
f = Symbol('f')
x = Symbol('x')
f = Function('f')
e = f + f(x)
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> ns['e'] == e
True
```

### Why it is wrong
The second assignment overwrites the first, so the generated code computes `Function('f') + f(x)`, which raises `TypeError` instead of recreating the expression.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python` emits one assignment per symbol name and one per function name with no check for clashes between the two lists; one of them has to be renamed (and substituted in the expression).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
