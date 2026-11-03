# str() prints O(1, x) as O(1), which is a different object

### Kind
lossy

### Actual
```pycon
>>> from sympy import O, symbols, sympify
>>> x = symbols('x')
>>> print(O(1, x))
O(1)
>>> O(1, x) == O(1)
False
```

### Expected
```pycon
>>> sympify(str(O(1, x))) == O(1, x)
True
```

### Why it is wrong
`O(1, x)` (bounded as `x -> 0`) and `O(1)` (no variables) are different objects, but print the same, so `str` does not round-trip.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Order` omits the variables whenever there is at most one of them and the point is 0, assuming `O(expr)` re-infers the variable from `expr`. That fails when `expr` does not contain the variable (`O(1, x)`, `O(y, x)`); the variable must be printed when `expr.expr.free_symbols` differs from `set(expr.variables)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
