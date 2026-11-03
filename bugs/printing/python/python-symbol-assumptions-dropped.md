# Symbol assumptions are dropped, including commutative=False

### Kind
lossy

### Actual
```pycon
>>> from sympy import Symbol, python
>>> p = Symbol('p', positive=True)
>>> print(python(p))
p = Symbol('p')
e = p
>>> X, Y = Symbol('X', commutative=False), Symbol('Y', commutative=False)
>>> print(python(X*Y))
X = Symbol('X')
Y = Symbol('Y')
e = X*Y
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(p), ns)
>>> ns['e'] == p
True
```

### Why it is wrong
Symbols with different assumptions are different objects, so the generated code does not recreate the expression (`Symbol('p') != Symbol('p', positive=True)`); for noncommutative symbols the regenerated `X*Y` even compares equal to `Y*X`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python` writes every declaration as `name = Symbol('name')`; it should include the symbol's assumptions (`expr._assumptions_orig`, as `srepr` does).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
