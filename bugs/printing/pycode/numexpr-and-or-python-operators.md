# NumExprPrinter prints And/Or with Python `and`/`or`, which numexpr rejects

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, And, Or
>>> from sympy.printing.lambdarepr import NumExprPrinter
>>> x, y = symbols('x y')
>>> print(NumExprPrinter().doprint(And(x > 0, y > 0)))
numexpr.evaluate('(((x > 0)) and ((y > 0)))', truediv=True)
>>> print(NumExprPrinter().doprint(Or(x > 0, y > 0)))
numexpr.evaluate('(((x > 0)) or ((y > 0)))', truediv=True)
```

### Expected
```pycon
>>> code = NumExprPrinter().doprint(And(x > 0, y > 0)) + NumExprPrinter().doprint(Or(x > 0, y > 0))
>>> ' and ' in code or ' or ' in code
False
```

### Why it is wrong
numexpr only supports the bitwise operators `&`, `|`, `~` for logic; `numexpr.evaluate` raises on `and`/`or`, so `lambdify(..., 'numexpr')` fails on any expression containing `And`/`Or` (e.g. in a Piecewise condition). The original reviewer executed this with numexpr; numexpr is not available in this sandbox.

### Notes on fixing
`NumExprPrinter` (`sympy/printing/lambdarepr.py`) inherits `LambdaPrinter._print_And`/`_print_Or`, which emit `and`/`or`. It needs its own `_print_And`/`_print_Or` using `&`/`|` (as `NumPyPrinter` does with its logical functions).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
