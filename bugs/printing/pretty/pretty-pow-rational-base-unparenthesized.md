# An inline Rational base of a power is not parenthesized: (2/3)**x prints as 2/3ˣ

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Rational, Pow, pretty
>>> x, n = symbols('x n')
>>> print(pretty(Pow(Rational(2, 3), x, evaluate=False), use_unicode=True))
   x
2/3
>>> print(pretty(Rational(-1, 2)**n, use_unicode=True))
    n
-1/2
```

### Expected
```pycon
>>> '(2/3)' in pretty(Pow(Rational(2, 3), x, evaluate=False), use_unicode=True)
True
>>> '(-1/2)' in pretty(Rational(-1, 2)**n, use_unicode=True)
True
```

### Why it is wrong
The pictures read as `2/3ˣ` and `-1/2ⁿ`, with the exponent applying only to the denominator (and the sign), not as `(2/3)ˣ` and `(-1/2)ⁿ`.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`PrettyPrinter._print_Rational` (`sympy/printing/pretty/pretty.py`, via `__print_numer_denom` and `emptyPrinter`) returns the one-line `p/q` form with ATOM binding (or NEG binding for negative ones), so `prettyForm.__pow__` in `stringpict.py` adds no parentheses. The inline form needs DIV binding (or the base needs parenthesizing in `_print_Pow`). Rationals with two-digit numerator and denominator print as a stacked fraction and are parenthesized correctly. This also shows up in `pprint(fps(sin(x)))`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
