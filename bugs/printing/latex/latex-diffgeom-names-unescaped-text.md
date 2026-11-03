# diffgeom Manifold/Patch/CoordSystem names go unescaped into \text{} (\text{P_1})

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.diffgeom import Manifold, Patch
>>> M = Manifold('M', 2)
>>> print(latex(Patch('P_1', M)))
\text{P_1}_{\text{M}}
>>> print(latex(Manifold('alpha', 2)))
\text{\alpha}
```

### Expected
```pycon
>>> 'P_1' in latex(Patch('P_1', M))
False
>>> r'\text{\alpha}' in latex(Manifold('alpha', 2))
False
```

### Why it is wrong
`_` is not allowed in text mode (`\text{P_1}` fails with "Missing $ inserted") and `\alpha` is a math-mode command (`\text{\alpha}` fails the same way), so these names produce TeX that does not compile.

### Notes on fixing
`sympy/printing/latex.py`: `_print_Manifold` splits super/subscripts and translates the name (to `\alpha`) and then wraps it in `\text{}`; `_print_Patch` and `_print_CoordSystem` wrap the printed `Str` name in `\text{}` without escaping or splitting it. The name should either be printed in math mode like a `Symbol` (`P_{1}`, `\alpha`), or escaped with `latex_escape` and not translated.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
