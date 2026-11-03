# pretty() prints (-2.5)**n and -(2.5**n) identically

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Float, pretty
>>> n = symbols('n')
>>> print(pretty(Float(-2.5)**n, use_unicode=True))
    n
-2.5
>>> print(pretty(-(Float(2.5)**n), use_unicode=True))
    n
-2.5
```

### Expected
```pycon
>>> pretty(Float(-2.5)**n, use_unicode=True) != pretty(-(Float(2.5)**n), use_unicode=True)
True
```

### Why it is wrong
`(-2.5)ⁿ` and `-(2.5ⁿ)` are different values (for `n = 2`: `6.25` and `-6.25`), but they print the same.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`PrettyPrinter._print_Float` (`sympy/printing/pretty/pretty.py`) returns `prettyForm(sstr(e))` with the default ATOM binding even when the string starts with `-`, so `prettyForm.__pow__` in `stringpict.py` does not parenthesize it. A negative Float should get NEG binding, as `__print_numer_denom` does for negative Integers.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
