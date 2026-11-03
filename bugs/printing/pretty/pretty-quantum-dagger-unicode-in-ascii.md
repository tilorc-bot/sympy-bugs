# use_unicode=False still prints a Unicode dagger for BosonOp, FermionOp and RaisingOp

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.physics.quantum import Dagger
>>> from sympy.physics.quantum.boson import BosonOp
>>> from sympy.physics.quantum.fermion import FermionOp
>>> from sympy.physics.quantum.sho1d import RaisingOp
>>> print(pretty(Dagger(BosonOp('a')), use_unicode=False))
 †
a
>>> print(pretty(Dagger(FermionOp('c')), use_unicode=False))
 †
c
>>> print(pretty(RaisingOp('a'), use_unicode=False))
 †
a
```

### Expected
```pycon
>>> pretty(Dagger(BosonOp('a')), use_unicode=False).isascii()
True
>>> pretty(Dagger(FermionOp('c')), use_unicode=False).isascii()
True
>>> pretty(RaisingOp('a'), use_unicode=False).isascii()
True
```

### Why it is wrong
`use_unicode=False` is meant to produce pure ASCII, but these operators always use `†` (U+2020). The generic `Dagger` of other operators already prints `+` in ASCII mode.

### Notes on fixing
The pretty methods hard-code `prettyForm('\N{DAGGER}')`: `BosonOp._print_contents_pretty` (`sympy/physics/quantum/boson.py`), `FermionOp._print_contents_pretty` (`sympy/physics/quantum/fermion.py`) and `RaisingOp._print_contents_pretty` (`sympy/physics/quantum/sho1d.py`). They should use `'+'` when `printer._use_unicode` is false, as `PrettyPrinter._print_Dagger` does (`sympy/printing/pretty/pretty.py`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
