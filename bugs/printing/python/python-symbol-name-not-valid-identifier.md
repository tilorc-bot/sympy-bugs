# Symbol("a'b") emits a'b = Symbol('a'b'), which is not valid Python

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, python
>>> e = Symbol("a'b")
>>> print(python(e))
a'b = Symbol('a'b')
e = a'b
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
The symbol name is used verbatim both as the Python variable name and inside a single-quoted string, so the output is a syntax error.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python` only renames names that are Python keywords (and strips braces). It should rename every name that is not `str.isidentifier()` and quote the name with `repr()` when building `Symbol(...)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
