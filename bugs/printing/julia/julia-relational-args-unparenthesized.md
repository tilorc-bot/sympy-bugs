# Eq(x, Eq(y, z)) and Eq(Eq(x, y), z) print identically: x == y == z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq
>>> from sympy import julia_code
>>> x, y, z = symbols('x y z')
>>> print(julia_code(Eq(x, Eq(y, z), evaluate=False)))
x == y == z
>>> print(julia_code(Eq(Eq(x, y), z, evaluate=False)))
x == y == z
```

### Expected
```pycon
>>> julia_code(Eq(x, Eq(y, z), evaluate=False)) != julia_code(Eq(Eq(x, y), z, evaluate=False))
True
>>> julia_code(Eq(Eq(x, y), z, evaluate=False)) != 'x == y == z'
True
```

### Why it is wrong
The arguments of a relational are printed without parentheses, so two different expressions print identically. Julia treats `x == y == z` as a chained comparison (`x == y && y == z`), which is neither expression. The original review executed `julia_code(Eq(x > 1, y > 1, evaluate=False))` (`x > 1 == y > 1`) in Julia 1.12 and got a wrong value.

### Related
[sympy/sympy#11366](https://redirect.github.com/sympy/sympy/issues/11366)
[latex-relational-args-unparenthesized](../latex/latex-relational-args-unparenthesized.md)
[pretty-relational-args-unparenthesized](../pretty/pretty-relational-args-unparenthesized.md)
[fcode-logical-equality-needs-eqv](../fortran/fcode-logical-equality-needs-eqv.md)
[ccode-relational-args-unparenthesized](../c/ccode-relational-args-unparenthesized.md)
[jscode-relational-args-unparenthesized](../js/jscode-relational-args-unparenthesized.md)
[octave-relational-args-unparenthesized](../octave/octave-relational-args-unparenthesized.md)
[rcode-relational-args-unparenthesized](../r/rcode-relational-args-unparenthesized.md)
[rust-relational-args-unparenthesized](../rust/rust-relational-args-unparenthesized.md)
[mathematica-relational-args-unparenthesized](../mathematica/mathematica-relational-args-unparenthesized.md)
[glsl-relational-args-unparenthesized](../glsl/glsl-relational-args-unparenthesized.md)

### Notes on fixing
`_print_Relational` in `sympy/printing/julia.py` prints `expr.lhs` and `expr.rhs` without `parenthesize`. Arguments whose precedence is at most `PRECEDENCE["Relational"]` (relationals, And/Or/Not) need parentheses; note that `PRECEDENCE_VALUES` maps `Equality`/`Unequality` to Mul precedence, so `precedence()` alone is not enough. `pycode` already gets this right (`(x == (y == z))`). The same mistake is in the other printers listed under Related; each has its own `_print_Relational`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (root cause 3, split per printer).
