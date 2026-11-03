# Eq(x, Eq(y, z)) prints as x = y = z: operands of a Relational are not parenthesized

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex, Eq, And, Or
>>> x, y, z, p, q = symbols('x y z p q')
>>> print(latex(Eq(x, Eq(y, z), evaluate=False)))
x = y = z
>>> print(latex(Eq(Eq(x, y), z, evaluate=False)))
x = y = z
>>> print(latex(Eq(Eq(x, y), False)))
x = y = \text{False}
>>> print(latex(Eq(And(p, q), Or(p, q))))
p \wedge q = p \vee q
```

### Expected
```pycon
>>> latex(Eq(x, Eq(y, z), evaluate=False)) != latex(Eq(Eq(x, y), z, evaluate=False))
True
>>> 'y = z' in latex(Eq(Eq(x, y), z, evaluate=False))
False
>>> r'y = \text{False}' in latex(Eq(Eq(x, y), False))
False
>>> 'q = p' in latex(Eq(And(p, q), Or(p, q)))
False
```

### Why it is wrong
`x = y = z` reads as a chained equality, which is neither `x = (y = z)` nor `(x = y) = z`; likewise `p \wedge q = p \vee q` reads as `p ∧ (q = p) ∨ q`. Different expressions print identically.

### Related
[sympy/sympy#11366](https://redirect.github.com/sympy/sympy/issues/11366)
[pretty-relational-args-unparenthesized](../pretty/pretty-relational-args-unparenthesized.md)
[fcode-logical-equality-needs-eqv](../fortran/fcode-logical-equality-needs-eqv.md)
[ccode-relational-args-unparenthesized](../c/ccode-relational-args-unparenthesized.md)
[jscode-relational-args-unparenthesized](../js/jscode-relational-args-unparenthesized.md)
[julia-relational-args-unparenthesized](../julia/julia-relational-args-unparenthesized.md)
[octave-relational-args-unparenthesized](../octave/octave-relational-args-unparenthesized.md)
[rcode-relational-args-unparenthesized](../r/rcode-relational-args-unparenthesized.md)
[rust-relational-args-unparenthesized](../rust/rust-relational-args-unparenthesized.md)
[mathematica-relational-args-unparenthesized](../mathematica/mathematica-relational-args-unparenthesized.md)
[glsl-relational-args-unparenthesized](../glsl/glsl-relational-args-unparenthesized.md)

### Notes on fixing
`LatexPrinter._print_Relational` (`sympy/printing/latex.py`) prints `expr.lhs` and `expr.rhs` with plain `self._print`. They should be parenthesized when their precedence is at most `PRECEDENCE['Relational']` (Relational, And, Or, Not, ...).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
