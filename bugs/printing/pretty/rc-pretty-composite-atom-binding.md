# Pretty printer gives inline fractions and negative numbers ATOM binding, so powers of them lose parentheses

### Kind
internal

### Actual
```pycon
>>> from sympy import symbols, Rational, Float, Pow, pretty
>>> from sympy.printing.pretty.pretty import PrettyPrinter
>>> from sympy.printing.pretty.stringpict import prettyForm
>>> x, n = symbols('x n')
>>> p = PrettyPrinter()
>>> p._print(Rational(2, 3)).binding == prettyForm.ATOM, p._print(Float(-2.5)).binding == prettyForm.ATOM
(True, True)
>>> print(pretty(Pow(Rational(2, 3), x, evaluate=False)))
   x
2/3
>>> print(pretty(Rational(-1, 2)**n + x))
    n
-1/2  + x
```

### Expected
```pycon
>>> p._print(Rational(2, 3)).binding != prettyForm.ATOM, p._print(Float(-2.5)).binding != prettyForm.ATOM
(True, True)
```

### Why it is wrong
`prettyForm.__pow__` and `__mul__` decide on parentheses from the `binding` of the operands. A picture such as `2/3` or `-2.5` is a quotient or a negation, but is returned with `ATOM` binding, so `(2/3)**x` prints as `2/3` with superscript `x` (reads `2/(3**x)`) and `(-1/2)**n` reads `-(1/2**n)`. The same shows up in `fps(sin(x))`, whose general term prints `-1/4` raised to a power.

### Notes on fixing
`sympy/printing/pretty/pretty.py`: `_print_Rational`/`_print_Fraction` fall back to `emptyPrinter` (a plain `prettyForm(str)`, ATOM) for small inline fractions, and `_print_Float` returns `prettyForm(sstr(e))` without `binding=prettyForm.NEG` for negative values. The review lists further printers that return composite pictures with ATOM binding: `Union`/`_print_seq`, `MatAdd`, `Dot`, `TensorProduct`, and the inline `sin²(x)` form. Each needs the binding that matches its outermost operator (DIV, NEG, ADD, MUL, ...).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (root cause 5).
