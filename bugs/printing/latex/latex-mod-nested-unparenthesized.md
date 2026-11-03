# latex() prints Mod(x, Mod(y, z)) and Mod(Mod(x, y), z) identically

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex, Mod
>>> x, y, z = symbols('x y z')
>>> print(latex(Mod(x, Mod(y, z))))
x \bmod y \bmod z
>>> print(latex(Mod(Mod(x, y), z)))
x \bmod y \bmod z
```

### Expected
```pycon
>>> latex(Mod(x, Mod(y, z))) != latex(Mod(Mod(x, y), z))
True
```

### Why it is wrong
The two expressions have different values (x=7, y=5, z=3: `7 mod (5 mod 3) = 1`, `(7 mod 5) mod 3 = 2`) but print the same, so the reader cannot tell which one is meant.

### Notes on fixing
`LatexPrinter._print_Mod` (`sympy/printing/latex.py`) parenthesizes both arguments with `parenthesize(arg, PRECEDENCE['Mul'], strict=True)`. `Mod` has Mul precedence, and `strict=True` only adds brackets for strictly lower precedence, so a nested Mod is never bracketed. At least the right-hand argument (and, for readability, the left one) needs brackets when it is a Mod; the `exp is not None` branch has the same problem.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
