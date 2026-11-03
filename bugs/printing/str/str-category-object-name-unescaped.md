# A categories Object whose name contains a double quote is not valid Python

### Kind
invalid-output

### Actual
```pycon
>>> from sympy.categories import Object
>>> print(Object('a"b'))
Object("a"b")
```

### Expected
```pycon
>>> eval(str(Object('a"b')), {'Object': Object}) == Object('a"b')
True
```

### Why it is wrong
The name is pasted between double quotes without escaping, so the output is a syntax error instead of the usual re-evaluable `str` form (`str(Object('a'))` is `Object("a")`).

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Object` formats `'Object("%s")' % obj.name`; using `repr(obj.name)` (or `json`-style escaping to keep double quotes) fixes it. `_print_NamedMorphism` and `_print_Category` quote names the same way.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
