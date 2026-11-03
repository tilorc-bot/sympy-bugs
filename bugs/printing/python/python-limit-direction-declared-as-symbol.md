# python(Limit(f(x), x, 0)) emits the invalid line + = Symbol('+')

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, Function, Limit, python
>>> x = Symbol('x')
>>> f = Function('f')
>>> e = Limit(f(x), x, 0)
>>> print(python(e))
x = Symbol('x')
+ = Symbol('+')
f = Function('f')
e = Limit(f(x), x, 0, dir='+')
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> ns['e'] == e
True
```

### Why it is wrong
`python()` output is meant to be executable, but `+ = Symbol('+')` is a syntax error, so no code using a `Limit` can be regenerated.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`Limit` stores its direction as `Symbol('+')`. `StrPrinter._print_Limit` prints it with `self._print`, which in `sympy/printing/python.py:PythonPrinter._print_Symbol` registers every printed symbol for declaration. The direction should not be registered (e.g. print it with `str()` in `_print_Limit`, or override `_print_Limit` in `PythonPrinter`); more generally `python()` should skip names that are not valid identifiers.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
