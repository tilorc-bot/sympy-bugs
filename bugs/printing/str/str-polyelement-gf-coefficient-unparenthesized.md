# A polynomial over GF(p) prints coefficients as "3 mod 5*x**2"

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import GF
>>> from sympy.polys.rings import ring
>>> R, x = ring('x', GF(5))
>>> print(3*x**2 + 2)
3 mod 5*x**2 + 2 mod 5
```

### Expected
```pycon
>>> 'mod 5*x' not in str(3*x**2 + 2)
True
```

### Why it is wrong
`3 mod 5*x**2` reads as `3 mod (5*x**2)`; the coefficient `3 mod 5` has to be parenthesized (or printed without the modulus) when it is multiplied by a monomial.

### Notes on fixing
`sympy/polys/rings.py:PolyElement.str` parenthesizes non-constant-term coefficients with `printer.parenthesize(coeff, prec_mul, strict=True)`, but `precedence()` (`sympy/printing/precedence.py`) does not know the finite-field element types and returns Atom precedence for them, so no parentheses are added. Either `precedence` needs an entry for these elements, or `PolyElement.str` should print GF coefficients differently.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
