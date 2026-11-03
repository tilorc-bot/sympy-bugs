# Mul(x, Mul(-y, z), evaluate=False) prints as x - y z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mul, latex
>>> x, y, z = symbols('x y z')
>>> print(latex(Mul(x, Mul(-y, z, evaluate=False), evaluate=False)))
x - y z
>>> print(latex(Mul(2, Mul(-y, z, evaluate=False), evaluate=False)))
2 - y z
>>> print(latex(x - y*z))
x - y z
```

### Expected
```pycon
>>> latex(Mul(x, Mul(-y, z, evaluate=False), evaluate=False)) != latex(x - y*z)
True
```

### Why it is wrong
The product `x·(-y·z)` prints exactly like the difference `x - y z`. Unevaluated products like this come from `parse_expr(..., evaluate=False)` and `UnevaluatedExpr` work.

### Notes on fixing
`LatexPrinter._needs_mul_brackets` (`sympy/printing/latex.py`) brackets a non-first Mul factor only if `expr.could_extract_minus_sign()`. For `Mul(Mul(-1, y), z)` that returns False because it only looks at whether `args[0]` is a negative Number, not at a nested negative Mul. The check needs to look at the sign the factor will actually print with (e.g. whether its LaTeX starts with `-`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
