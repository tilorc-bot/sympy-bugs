# NumPyPrinter, SciPyPrinter and MpmathPrinter raise KeyError: 'ComplexInfinity' on zoo

### Kind
crash

### Actual
```pycon
>>> from sympy import zoo
>>> from sympy.printing.numpy import NumPyPrinter, SciPyPrinter
>>> from sympy.printing.pycode import MpmathPrinter, pycode
>>> NumPyPrinter().doprint(zoo)
Traceback (most recent call last):
...
KeyError: 'ComplexInfinity'
>>> MpmathPrinter().doprint(zoo)
Traceback (most recent call last):
...
KeyError: 'ComplexInfinity'
>>> pycode(zoo)
'math.nan'
```

### Expected
```pycon
>>> _ = NumPyPrinter().doprint(zoo)
>>> _ = SciPyPrinter().doprint(zoo)
>>> _ = MpmathPrinter().doprint(zoo)
```

### Why it is wrong
`PythonCodePrinter` handles `zoo`, but its subclasses crash with an internal `KeyError` instead of printing something (or raising a proper "not supported" error), so e.g. `lambdify` with the default NumPy module fails on any expression containing `zoo`.

### Notes on fixing
`sympy/printing/pycode.py` attaches `_print_known_const` as `PythonCodePrinter._print_ComplexInfinity` (because `'ComplexInfinity'` is in `_known_constants_math`). The subclasses inherit that method but their own `_kc` dicts (`_known_constants_mpmath`, `numpy.py:_known_constants_numpy`, and the SciPy/CuPy/JAX ones derived from it) have no `'ComplexInfinity'` key. Either add the key to those dicts or make `_print_known_const` fall back.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
