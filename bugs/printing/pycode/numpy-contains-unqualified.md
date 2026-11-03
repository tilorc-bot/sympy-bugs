# NumPyPrinter prints Contains(x, Integers) with unqualified `equal`/`mod` and records no imports

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Contains, S
>>> from sympy.printing.numpy import NumPyPrinter
>>> x = symbols('x')
>>> p = NumPyPrinter()
>>> print(p.doprint(Contains(x, S.Integers)))
equal(mod(x, 1), 0)
>>> dict(p.module_imports)
{}
```

### Expected
```pycon
>>> import numpy
>>> bool(eval(NumPyPrinter().doprint(Contains(x, S.Integers)), {'numpy': numpy, 'x': 2.0}))
True
>>> 'numpy' in dict(p.module_imports)
True
```

### Why it is wrong
Every other NumPy function is printed as `numpy.<name>` (or imported via `module_imports` when `fully_qualified_modules=False`). `equal`/`mod` are neither qualified nor recorded, so the code only works inside `lambdify`'s namespace and raises `NameError` anywhere else.

### Notes on fixing
`sympy/printing/numpy.py:NumPyPrinter._print_Contains` hard-codes `"equal(mod({}, 1), 0)"`; it should use `self._module_format(self._module + '.equal')` etc. (which also makes it right for the CuPy/JAX subclasses).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
