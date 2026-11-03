# Operator(x + y)**2 prints as x + y^{2}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.physics.quantum import Operator, Dagger
>>> x, y = symbols('x y')
>>> print(latex(Operator(x + y)**2))
x + y^{2}
>>> print(latex(Dagger(Operator(x + y))))
x + y^{\dagger}
```

### Expected
```pycon
>>> latex(Operator(x + y)**2) != latex(x + y**2)
True
>>> latex(Dagger(Operator(x + y))) != latex(x + Dagger(Operator(y)))
True
```

### Why it is wrong
The power (or dagger) is attached to `y` only, so the output is exactly the LaTeX of the scalar expression `x + y**2`.

### Notes on fixing
`QExpr._latex` (`sympy/physics/quantum/qexpr.py`) prints the label sequence as is; an Operator whose label is not an atom gets Atom precedence (QExpr has no precedence entry), so neither `LatexPrinter._helper_print_standard_power` nor `adjoint._latex` brackets it. Operators with composite labels need brackets (or a precedence that reflects the printed label). Products such as `Operator(x + y)*Operator(z)` (`x + y z`) are affected too.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
