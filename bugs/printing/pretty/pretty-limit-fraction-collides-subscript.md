# pretty() of Limit(1/x, x, oo) puts the denominator right after the ∞ in the subscript: x─→∞x

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Limit, oo, pretty
>>> x = symbols('x')
>>> print(pretty(Limit(1/x, x, oo), use_unicode=True))
    1
lim ─
x─→∞x
```

### Expected
```pycon
>>> p = pretty(Limit(1/x, x, oo), use_unicode=True)
>>> '∞x' in p or '∞ x' in p
False
```

### Why it is wrong
The denominator of `1/x` is printed on the subscript row directly after `∞`, so the limit point reads as `∞x` and the fraction bar has nothing under it.

### Notes on fixing
`PrettyPrinter._print_Limit` in `sympy/printing/pretty/pretty.py` puts the body to the right of the `lim` block with their baselines aligned; the `lim` block's baseline is its first row, so a body whose baseline is the fraction bar extends into the subscript row. The body is parenthesized only when `precedence(e) <= PRECEDENCE["Mul"]`, so `1/x` (a Pow) is not. Parenthesizing multi-line bodies (as is done for `sin(x)/x`) would avoid the collision.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
