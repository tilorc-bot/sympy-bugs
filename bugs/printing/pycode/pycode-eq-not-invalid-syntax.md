# pycode(Eq(Not(x), Not(y))) prints `(not x == not y)`, a SyntaxError

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Eq, Not
>>> from sympy.printing.pycode import pycode
>>> x, y = symbols('x y')
>>> print(pycode(Eq(Not(x), Not(y))))
(not x == not y)
```

### Expected
```pycon
>>> eval(pycode(Eq(Not(x), Not(y))), {'x': True, 'y': True})
True
```

### Why it is wrong
`not x == not y` is not valid Python, and even `not x == y` would parse as `not (x == y)`. The operands of a relational are never parenthesized.

### Notes on fixing
`sympy/printing/pycode.py:AbstractPythonCodePrinter._print_Relational` prints `self._print(expr.lhs)` and `self._print(expr.rhs)` without `parenthesize`. Operands with lower precedence than the relational (here `Not`, which binds looser than `==` in Python) need parentheses.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
