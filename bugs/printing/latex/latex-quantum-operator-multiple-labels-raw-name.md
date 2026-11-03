# Operator('A', 'B') prints the class name as italic math letters

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.physics.quantum.operator import Operator, HermitianOperator
>>> print(latex(Operator('A', 'B')))
Operator\left(A,B\right)
>>> print(latex(HermitianOperator('A', 'B')))
HermitianOperator\left(A,B\right)
```

### Expected
```pycon
>>> latex(Operator('A', 'B')).startswith('Operator')
False
>>> latex(HermitianOperator('A', 'B')).startswith('HermitianOperator')
False
```

### Why it is wrong
In math mode `Operator` renders as the product of the italic variables O, p, e, r, a, t, o, r rather than as a name.

### Notes on fixing
`sympy/physics/quantum/operator.py:Operator._print_contents_latex` uses `_print_operator_name_latex`, which is the same as the plain-text `_print_operator_name` (the class name). The LaTeX variant should wrap it in `\operatorname{}` or `\text{}`. Subclasses (`HermitianOperator`, `UnitaryOperator`, ...) inherit the problem.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
