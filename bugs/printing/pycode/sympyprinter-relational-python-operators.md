# SymPyPrinter prints Eq/Ne with Python `==`/`!=`, so lambdify(..., 'sympy') returns False for Eq(x, y)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq, lambdify
>>> from sympy.printing.pycode import SymPyPrinter
>>> x, y = symbols('x y')
>>> print(SymPyPrinter().doprint(Eq(x, y)))
(x == y)
>>> lambdify((x, y), Eq(x, y), 'sympy')(x, y)
False
```

### Expected
```pycon
>>> lambdify((x, y), Eq(x, y), 'sympy')(x, y) == Eq(x, y)
True
```

### Why it is wrong
On SymPy objects, Python `==`/`!=` test structural equality and return a bool, so the symbolic equation `Eq(x, y)` becomes `False`. The target of `SymPyPrinter` is SymPy, which has `Eq`/`Ne`.

### Related
[sympy/sympy#25360](https://redirect.github.com/sympy/sympy/issues/25360)

### Notes on fixing
`SymPyPrinter` (`sympy/printing/pycode.py`) inherits `AbstractPythonCodePrinter._print_Relational`. It should print `sympy.Eq(...)`/`sympy.Ne(...)` (`<`, `>`, etc. already work on SymPy objects).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
