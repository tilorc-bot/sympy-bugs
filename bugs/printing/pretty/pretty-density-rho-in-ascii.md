# pretty(use_unicode=False) prints a Greek rho for Density

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.physics.quantum.density import Density
>>> from sympy.physics.quantum.state import Ket
>>> print(pretty(Density([Ket('psi'), 0.5], [Ket('phi'), 0.5]), use_unicode=False))
ρ((|psi>, 0.5),(|phi>, 0.5))
```

### Expected
```pycon
>>> pretty(Density([Ket('psi'), 0.5], [Ket('phi'), 0.5]), use_unicode=False).isascii()
True
```

### Why it is wrong
`use_unicode=False` is meant to produce pure ASCII, but the operator name is always `ρ` (U+03C1).

### Notes on fixing
`sympy/physics/quantum/density.py:Density._print_operator_name_pretty` returns `prettyForm('\N{GREEK SMALL LETTER RHO}')` unconditionally; it should return e.g. `rho` when `printer._use_unicode` is false (the usual ASCII spelling of Greek letters in the pretty printer).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
