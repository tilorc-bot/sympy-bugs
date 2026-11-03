# The QFT gate name prints as italic math letters

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.physics.quantum.qft import QFT, IQFT
>>> print(latex(QFT(0, 2)))
QFT_{0,2}
>>> print(latex(IQFT(0, 2)))
{QFT^{-1}}_{0,2}
```

### Expected
```pycon
>>> latex(QFT(0, 2)).startswith('QFT')
False
>>> latex(IQFT(0, 2)).startswith('{QFT')
False
```

### Why it is wrong
In math mode `QFT` renders as the product of the italic variables Q, F, T rather than as the name of the transform.

### Notes on fixing
`sympy/physics/quantum/qft.py` sets `gate_name_latex = 'QFT'` (and `'{QFT^{-1}}'` for `IQFT`); these should be `\operatorname{QFT}` / `\operatorname{QFT}^{-1}`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
