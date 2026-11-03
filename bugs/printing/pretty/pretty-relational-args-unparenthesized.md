# Relational/logical arguments of a relational are not parenthesized: x = y = y = z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq, And, pretty
>>> x, y, z, p, q, r = symbols('x y z p q r')
>>> print(pretty(Eq(Eq(x, y), Eq(y, z)), use_unicode=True))
x = y = y = z
>>> print(pretty(Eq(x, Eq(Eq(y, y, evaluate=False), z), evaluate=False), use_unicode=True))
x = y = y = z
>>> print(pretty(Eq(And(p, q), r), use_unicode=True))
p ∧ q = r
>>> print(pretty(And(p, Eq(q, r)), use_unicode=True))
p ∧ q = r
```

### Expected
```pycon
>>> a = pretty(Eq(Eq(x, y), Eq(y, z)), use_unicode=True)
>>> b = pretty(Eq(x, Eq(Eq(y, y, evaluate=False), z), evaluate=False), use_unicode=True)
>>> a != b
True
>>> pretty(Eq(And(p, q), r), use_unicode=True) != pretty(And(p, Eq(q, r)), use_unicode=True)
True
```

### Why it is wrong
Different expressions print the same: `(p ∧ q) = r` and `p ∧ (q = r)` are different booleans, and a chain `x = y = y = z` does not say which equalities are nested.

### Related
[sympy/sympy#11366](https://redirect.github.com/sympy/sympy/issues/11366)
[latex-relational-args-unparenthesized](../latex/latex-relational-args-unparenthesized.md)
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
`PrettyPrinter._print_Relational` in `sympy/printing/pretty/pretty.py` joins `self._print(e.lhs)`, the operator and `self._print(e.rhs)` without parenthesizing either side. Arguments whose binding is OPEN (relationals, `Mod`) or that are logic operators need parentheses.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
