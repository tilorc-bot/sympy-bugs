# latex(adjoint(Integral(A, x))) puts the dagger on dx: \int A\, dx^{\dagger}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, MatrixSymbol, Integral, Derivative, adjoint, latex
>>> x = symbols('x')
>>> A = MatrixSymbol('A', 2, 2)
>>> print(latex(adjoint(Integral(A, x))))
\int A\, dx^{\dagger}
>>> F = Function('F', commutative=False)
>>> print(latex(adjoint(Derivative(F(x), x))))
\frac{d}{d x} F{\left(x \right)}^{\dagger}
```

### Expected
```pycon
>>> latex(adjoint(Integral(A, x))).endswith(r'\right)^{\dagger}')
True
```

### Why it is wrong
The dagger is attached to `dx` (or to `F(x)`) instead of to the whole integral/derivative, so the output denotes a different (and, for `dx^{\dagger}`, meaningless) expression.

### Notes on fixing
`adjoint._latex` (`sympy/functions/elementary/complexes.py`) prints `r'%s^{\dagger}' % printer._print(self.args[0])` without ever bracketing the argument; it should use `printer.parenthesize(self.args[0], PRECEDENCE['Pow'])` (as `LatexPrinter._print_Adjoint` does for matrices). The same method is used by `sympy.physics.quantum.Dagger`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
