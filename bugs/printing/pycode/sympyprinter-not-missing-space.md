# SymPyPrinter prints Not(x) as `notx`

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Not, lambdify
>>> from sympy.printing.pycode import SymPyPrinter
>>> x, y = symbols('x y')
>>> print(SymPyPrinter().doprint(Not(x)))
notx
>>> lambdify(x, Not(x), 'sympy')(y)
Traceback (most recent call last):
...
NameError: name 'notx' is not defined
```

### Expected
```pycon
>>> lambdify(x, Not(x), 'sympy')(y) == Not(y)
True
```

### Why it is wrong
`notx` is a different identifier, so the generated code fails (or silently refers to a variable called `notx`).

### Related
[sympy/sympy#25360](https://redirect.github.com/sympy/sympy/issues/25360)

### Notes on fixing
`SymPyPrinter` derives from `AbstractPythonCodePrinter` and so uses `CodePrinter._print_Not` (`sympy/printing/codeprinter.py`), which concatenates `self._operators['not']` with the operand without a space (correct for C's `!`). `PythonCodePrinter._print_Not` adds the space, but `SymPyPrinter` does not inherit from it. For a SymPy target, printing `sympy.Not(...)` would also keep the result symbolic (Python `not` on a SymPy object returns a bool).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
