# julia_code/rust_code/glsl_code raise TypeError for Min/Max containing an ITE inside And

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, ITE, And, Min, Piecewise, julia_code, rust_code, glsl_code
>>> x, y, z = symbols('x y z')
>>> e = Min(x, Piecewise((y, And(ITE(x < 0, y < 0, z < 0), x < 1)), (z, True)))
>>> julia_code(e)
Traceback (most recent call last):
...
TypeError: expecting bool or Boolean, not `Piecewise((y < 0, x < 0), (z < 0, True))`.
>>> glsl_code(e)
Traceback (most recent call last):
...
TypeError: expecting bool or Boolean, not `Piecewise((y < 0, x < 0), (z < 0, True))`.
```

### Expected
```pycon
>>> _ = julia_code(e)
>>> _ = rust_code(e)
>>> _ = glsl_code(e)
```

### Why it is wrong
Printing must not fail for a valid expression; the same printers print the inner Piecewise on its own, and `ccode(e)` prints the whole expression.

### Related
[sympy/sympy#27647](https://redirect.github.com/sympy/sympy/issues/27647)
[sympy/sympy#24961](https://redirect.github.com/sympy/sympy/issues/24961)

### Notes on fixing
`CodePrinter._print_Function` (`sympy/printing/codeprinter.py`) handles printers without a native `Min`/`Max` through `_rewriteable_functions` with `expr.rewrite(target_f)`, which rewrites deeply: the ITE in the condition becomes a (non-Boolean) Piecewise inside `And`, and `And` rejects it. Rewriting with `deep=False` lets the arguments be printed by their own methods.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
