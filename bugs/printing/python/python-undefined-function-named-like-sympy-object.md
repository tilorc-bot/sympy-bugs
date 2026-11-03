# Function('sin')(x) is not declared, so the generated code calls SymPy's sin

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Symbol, Function, python
>>> x = Symbol('x')
>>> e = Function('sin')(x)
>>> print(python(e))
x = Symbol('x')
e = sin(x)
>>> print(python(Function('Function')(x)))
x = Symbol('x')
e = Function(x)
```

### Expected
```pycon
>>> def run(code):
...     ns = {}
...     exec('from sympy import *\n' + code, ns)
...     return ns['e']
>>> run(python(e)) == e
True
>>> run(python(Function('Function')(x))) == Function('Function')(x)
True
```

### Why it is wrong
The expression contains an undefined function that merely shares a name with something in `sympy`; the generated code silently uses SymPy's `sin` (or, for `Function('Function')`, builds a new function named `x`), which is a different expression.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:PythonPrinter._print_Function` skips the declaration whenever `hasattr(sympy, func)`. It should decide by whether the function is an `AppliedUndef`, and rename undefined functions whose names clash with SymPy names.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
