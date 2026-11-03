# SymPyPrinter prints pi, E and other number symbols as decimal floats

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, pi, lambdify
>>> from sympy.printing.pycode import SymPyPrinter
>>> x, y = symbols('x y')
>>> print(SymPyPrinter().doprint(pi*x))
3.1415926535897932*x
>>> lambdify(x, pi*x, 'sympy')(y)
3.14159265358979*y
```

### Expected
```pycon
>>> import sympy
>>> eval(SymPyPrinter().doprint(pi*x), {'sympy': sympy, 'x': y}) == pi*y
True
>>> lambdify(x, pi*x, 'sympy')(y) == pi*y
True
```

### Why it is wrong
The target of `SymPyPrinter` is SymPy itself, which has exact `pi`, `E`, `EulerGamma`, etc., but the generated code replaces them with 17-digit floats, so the result is no longer exact.

### Related
[sympy/sympy#25360](https://redirect.github.com/sympy/sympy/issues/25360)

### Notes on fixing
`SymPyPrinter` (`sympy/printing/pycode.py`) inherits `CodePrinter._print_NumberSymbol` (`sympy/printing/codeprinter.py`), which evaluates the constant to `precision` digits. It should print `sympy.pi` etc.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
