# Derivative(f(x, y), x, y) raises ValueError: too many values to unpack

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative
>>> from sympy.printing.maple import maple_code
>>> x, y = symbols('x y')
>>> f = Function('f')
>>> print(maple_code(Derivative(f(x, y), x)))
diff(f(x, y), x)
>>> maple_code(Derivative(f(x, y), x, y))
Traceback (most recent call last):
...
ValueError: too many values to unpack (expected 2)
```

### Expected
```pycon
>>> _ = maple_code(Derivative(f(x, y), x, y))
```

### Why it is wrong
Printing must not fail for a valid expression; mixed partial derivatives are common, and Maple's `diff` accepts several variables (`diff(f(x, y), x, y)`).

### Notes on fixing
`sympy/printing/maple.py:MapleCodePrinter._print_Derivative` unpacks `_f, (_var, _order) = expr.args`, which only works for a single variable. It should loop over `expr.variable_count` and print `diff(f, x$m, y$n)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
