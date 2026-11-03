# Pauli operators SigmaX() etc. print as their label (False, or the bare name)

### Kind
lossy

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.physics.quantum.pauli import SigmaX, SigmaY
>>> print(pretty(SigmaX() + 1, use_unicode=True))
1 + False
>>> print(pretty(SigmaX('1')*SigmaY('2'), use_unicode=True))
1⋅2
>>> print(pretty(SigmaY('1')*SigmaX('2'), use_unicode=True))
1⋅2
```

### Expected
```pycon
>>> 'False' in pretty(SigmaX() + 1, use_unicode=True)
False
>>> pretty(SigmaX('1')*SigmaY('2'), use_unicode=True) != pretty(SigmaY('1')*SigmaX('2'), use_unicode=True)
True
```

### Why it is wrong
The pretty form shows only the operator's label (`False` for the default unnamed operator), so the operator itself disappears: `SigmaX()` is displayed as the boolean `False`, and `σx⁽¹⁾σy⁽²⁾` and `σy⁽¹⁾σx⁽²⁾` look the same.

### Notes on fixing
`sympy/physics/quantum/pauli.py` defines `_print_contents` and `_print_contents_latex` for `SigmaX`, `SigmaY`, `SigmaZ`, `SigmaMinus` and `SigmaPlus`, but no `_print_contents_pretty`, so the inherited `QExpr._print_contents_pretty` (`sympy/physics/quantum/qexpr.py`) prints the label tuple `(False,)` or `('1',)`. Each class needs a `_print_contents_pretty` mirroring the LaTeX one (σ with subscript x/y/z/-/+ and the name as superscript in parentheses).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
