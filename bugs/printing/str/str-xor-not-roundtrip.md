# Xor(x, y) prints x ^ y, which sympify() reads back as x**y

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Xor, sympify
>>> x, y = symbols('x y')
>>> print(Xor(x, y))
x ^ y
>>> sympify(str(Xor(x, y)))
x**y
```

### Expected
```pycon
>>> '^' in str(Xor(x, y))
False
>>> sympify(str(Xor(x, y))) == Xor(x, y)
True
```

### Why it is wrong
`str` output is expected to be re-readable by `sympify`, and `x | y` and `x & y` round-trip, but `^` is converted to `**` by `sympify` (`convert_xor=True` is the default), so a Boolean expression silently turns into a power.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Xor` joins the arguments with `" ^ "`. Printing `Xor(x, y)` instead would round-trip under every parser setting.

The test `test_Xor` in `sympy/printing/tests/test_str.py` asserts the current output: `assert str(Xor(y, x, evaluate=False)) == "y ^ x"`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
