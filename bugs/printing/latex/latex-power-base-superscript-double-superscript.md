# latex() of a power gives a double superscript when the base prints with a superscript (Operator('A^a')**2 → A^{a}^{2})

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, exp, UnevaluatedExpr, latex
>>> from sympy.physics.quantum import Operator
>>> from sympy.physics.quantum.sho1d import RaisingOp
>>> z = symbols('z')
>>> print(latex(Operator('A^a')**2))
A^{a}^{2}
>>> print(latex(RaisingOp('a')**2))
a^{\dagger}^{2}
>>> print(latex(UnevaluatedExpr(exp(z))**2))
e^{z}^{2}
```

### Expected
```pycon
>>> ('^{a}^' in latex(Operator('A^a')**2),
...  r'^{\dagger}^' in latex(RaisingOp('a')**2),
...  '^{z}^' in latex(UnevaluatedExpr(exp(z))**2))
(False, False, False)
```

### Why it is wrong
`A^{a}^{2}` is a TeX "Double superscript" error, so the output does not compile. The base needs braces or parentheses, as is already done for `Symbol('A^a')**2`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._helper_print_standard_power` applies `parenthesize_super` (issue [sympy/sympy#12886](https://redirect.github.com/sympy/sympy/issues/12886)) only when `expr.base.is_Symbol`; any other base whose LaTeX ends in a superscript is concatenated with `^{...}`. Other cases from the same helper: `Die('D^6', 6)**2` → `D^{6}^{2}`, `units.degree**2` → `^\circ^{2}` (its `latex_repr`), and `HadamardPower(MatrixSymbol('A^b', 2, 2), 2)` → `A^{b}^{\circ {2}}` (`_print_HadamardPower` calls the helper). For `UnevaluatedExpr(exp(z))` the `is_Function` branch of `_print_Pow` (which would pass `exp=`) is skipped, and `precedence_traditional` unwraps the `UnevaluatedExpr` to Func precedence, so no parentheses are added either. Applying `parenthesize_super` to every base string is not enough as-is, since with `parenthesize_super=True` it would double the parentheses of bases that are already parenthesized.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
