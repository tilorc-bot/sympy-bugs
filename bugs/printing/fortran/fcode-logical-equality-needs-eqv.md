# fcode(Eq(x > 1, y > 1)) prints x > 1 == y > 1 instead of using .eqv.

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Eq, fcode
>>> x, y = symbols('x y')
>>> print(fcode(Eq(x > 1, y > 1), standard=95, source_format='free'))
x > 1 == y > 1
```

### Expected
```pycon
>>> '.eqv.' in fcode(Eq(x > 1, y > 1), standard=95, source_format='free')
True
```

### Why it is wrong
Both sides are logical expressions. Fortran does not allow `==` between logicals (they must be compared with `.eqv.`/`.neqv.`), and without parentheses `x > 1 == y > 1` does not even parse as the intended comparison. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Relational` prints lhs and rhs unparenthesized and always uses `==`/`/=`. For Boolean operands, `Eq`/`Ne` must be printed as `(lhs) .eqv. (rhs)` / `(lhs) .neqv. (rhs)`; parenthesizing alone (the shared root cause) is not enough here.

### Related
[sympy/sympy#11366](https://redirect.github.com/sympy/sympy/issues/11366)
[latex-relational-args-unparenthesized](../latex/latex-relational-args-unparenthesized.md)
[pretty-relational-args-unparenthesized](../pretty/pretty-relational-args-unparenthesized.md)
[ccode-relational-args-unparenthesized](../c/ccode-relational-args-unparenthesized.md)
[jscode-relational-args-unparenthesized](../js/jscode-relational-args-unparenthesized.md)
[julia-relational-args-unparenthesized](../julia/julia-relational-args-unparenthesized.md)
[octave-relational-args-unparenthesized](../octave/octave-relational-args-unparenthesized.md)
[rcode-relational-args-unparenthesized](../r/rcode-relational-args-unparenthesized.md)
[rust-relational-args-unparenthesized](../rust/rust-relational-args-unparenthesized.md)
[mathematica-relational-args-unparenthesized](../mathematica/mathematica-relational-args-unparenthesized.md)
[glsl-relational-args-unparenthesized](../glsl/glsl-relational-args-unparenthesized.md)
### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
