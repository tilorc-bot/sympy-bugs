# SymPyPrinter prints Piecewise as a Python conditional expression, so lambdify(..., 'sympy') raises on it

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Piecewise, lambdify
>>> from sympy.printing.pycode import SymPyPrinter
>>> x, y = symbols('x y')
>>> print(SymPyPrinter().doprint(Piecewise((x, x > 0), (0, True))))
((x) if (x > 0) else (0))
>>> lambdify(x, Piecewise((x, x > 0), (0, True)), 'sympy')(y)
Traceback (most recent call last):
...
TypeError: cannot determine truth value of Relational...
```

### Expected
```pycon
>>> lambdify(x, Piecewise((x, x > 0), (0, True)), 'sympy')(y) == Piecewise((y, y > 0), (0, True))
True
```

### Why it is wrong
A Python `if`/`else` calls `bool()` on the condition, which raises for a symbolic relational. The target of `SymPyPrinter` is SymPy, which has `Piecewise`.

### Related
[sympy/sympy#25360](https://redirect.github.com/sympy/sympy/issues/25360)

### Notes on fixing
`SymPyPrinter` (`sympy/printing/pycode.py`) inherits `AbstractPythonCodePrinter._print_Piecewise`. It should print `sympy.Piecewise(...)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
