# AntiSymmetricTensor('v_1', ...) gives a double subscript

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.physics.secondquant import AntiSymmetricTensor
>>> i, j = symbols('i j')
>>> print(latex(AntiSymmetricTensor('v_1', (i,), (j,))))
{v_1^{i}_{j}}
```

### Expected
```pycon
>>> any(p in latex(AntiSymmetricTensor('v_1', (i,), (j,))) for p in ('v_1^', '_{1}^{i}_'))
False
```

### Why it is wrong
`v_1^{i}_{j}` has two subscripts on the same base, a TeX "Double subscript" error, so the output does not compile.

### Notes on fixing
`sympy/physics/secondquant.py:AntiSymmetricTensor._latex` inserts `self.symbol` with `%s` (plain `str`) instead of printing it, then appends `^{...}_{...}`. The symbol should be printed with `printer._print` (which also translates names such as `alpha`, currently printed raw) and wrapped in braces so its own subscript does not collide, e.g. `{v_{1}}^{i}_{j}`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
