# latex() prints Mod(-x, y) and -Mod(x, y) identically

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex, Mod
>>> x, y = symbols('x y')
>>> print(latex(Mod(-x, y)))
- x \bmod y
>>> print(latex(-Mod(x, y)))
- x \bmod y
```

### Expected
```pycon
>>> latex(Mod(-x, y)) != latex(-Mod(x, y))
True
```

### Why it is wrong
`- x \bmod y` reads as `-(x mod y)`, which is a different value from `(-x) mod y`.

### Caused by
[rc-precedence-traditional-mul](../precedence/rc-precedence-traditional-mul.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
