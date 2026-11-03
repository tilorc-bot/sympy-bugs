# TribonacciConstant + x raises KeyError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, TribonacciConstant
>>> from sympy.printing.maple import maple_code
>>> x = symbols('x')
>>> maple_code(TribonacciConstant + x)
Traceback (most recent call last):
...
KeyError: TribonacciConstant
```

### Expected
```pycon
>>> _ = maple_code(TribonacciConstant + x)
```

### Why it is wrong
Printing must not fail for a valid expression; the constant has a closed form (`(1 + (19 - 3*sqrt(33))^(1/3) + (19 + 3*sqrt(33))^(1/3))/3`) that can be printed.

### Notes on fixing
`sympy/printing/maple.py:MapleCodePrinter._print_NumberSymbol` looks the constant up in the `number_symbols` dict, which has no entry for `TribonacciConstant` (or any other `NumberSymbol` not listed). Add an entry, or fall back to `CodePrinter._print_NumberSymbol` / printing `expr.rewrite(sqrt)` for unknown constants.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
