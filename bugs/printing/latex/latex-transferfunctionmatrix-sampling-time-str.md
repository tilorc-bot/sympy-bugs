# A discrete TransferFunctionMatrix prints the sampling time with str()

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import Symbol, latex
>>> from sympy.physics.control.lti import DiscreteTransferFunction, TransferFunctionMatrix
>>> s = Symbol('s')
>>> print(latex(TransferFunctionMatrix([[DiscreteTransferFunction(1, s, s, 0.1)]])))
\underset{[st:\ {0.100000000000000}]}{\left[\begin{matrix}\frac{1}{s}\end{matrix}\right]_k}
>>> print(latex(TransferFunctionMatrix([[DiscreteTransferFunction(1, s, s, Symbol('alpha'))]])))
\underset{[st:\ {alpha}]}{\left[\begin{matrix}\frac{1}{s}\end{matrix}\right]_k}
```

### Expected
```pycon
>>> '0.100000000000000' in latex(TransferFunctionMatrix([[DiscreteTransferFunction(1, s, s, 0.1)]]))
False
>>> r'\alpha' in latex(TransferFunctionMatrix([[DiscreteTransferFunction(1, s, s, Symbol('alpha'))]]))
True
```

### Why it is wrong
The sampling time is inserted with `str()`, so a Float shows all 15 digits, ignores printer settings such as `full_prec`/`decimal_separator`, and symbols like `alpha` or `T_s` are not rendered as LaTeX. `latex(DiscreteTransferFunction(1, s, s, 0.1))` on its own prints `{0.1}` and `{\alpha}`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_TransferFunctionMatrix` formats `expr.sampling_time` directly; it should use `self._print(expr.sampling_time)` as the single transfer function printer does.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
