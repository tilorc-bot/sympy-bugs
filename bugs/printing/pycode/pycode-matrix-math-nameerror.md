# lambdify(x, Matrix(...), 'math') raises NameError: name 'ImmutableDenseMatrix' is not defined

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Matrix, lambdify
>>> from sympy.printing.pycode import pycode
>>> x = symbols('x')
>>> print(pycode(Matrix([x, 2])))
ImmutableDenseMatrix([[x], [2]])
>>> lambdify(x, Matrix([x, 2]), 'math')(1)
Traceback (most recent call last):
...
NameError: name 'ImmutableDenseMatrix' is not defined
```

### Expected
```pycon
>>> _ = lambdify(x, Matrix([x, 2]), 'math')(1)
```

### Why it is wrong
Lambdifying a Matrix with `modules='math'` used to work ([sympy/sympy#4033](https://redirect.github.com/sympy/sympy/issues/4033)) and now fails when the function is called.

### Related
[sympy/sympy#4033](https://redirect.github.com/sympy/sympy/issues/4033)

### Notes on fixing
`sympy/printing/pycode.py:AbstractPythonCodePrinter._print_MatrixBase` prints the class name (`ImmutableDenseMatrix`) unless `known_functions` maps it; neither `PythonCodePrinter` nor the `math` namespace in `sympy/utilities/lambdify.py` provides that name. Either map it (e.g. to a nested list) or add the class to the `math` namespace as was done for [sympy/sympy#4033](https://redirect.github.com/sympy/sympy/issues/4033).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
