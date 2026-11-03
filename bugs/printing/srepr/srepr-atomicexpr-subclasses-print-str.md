# CoordSys3D base scalars and units Quantities are printed with str()

### Kind
lossy

### Actual
```pycon
>>> from sympy import srepr
>>> from sympy.core.symbol import Str
>>> from sympy.vector import CoordSys3D
>>> from sympy.physics.units import Quantity, meter
>>> ns = {'Str': Str}
>>> exec('from sympy import *; from sympy.vector import *; from sympy.physics.units import *', ns)
>>> C = CoordSys3D('C')
>>> srepr(C.x)
'C.x'
>>> q = Quantity('foo', abbrev='fo')
>>> srepr(q)
'foo'
>>> srepr(Quantity('meter'))
'meter'
>>> eval(srepr(Quantity('meter')), ns) is meter
True
```

### Expected
```pycon
>>> eval(srepr(C.x), ns) == C.x
True
>>> eval(srepr(q), ns) == q
True
>>> eval(srepr(Quantity('meter')), ns) == Quantity('meter')
True
>>> eval(srepr(Quantity('meter')), ns) is meter
False
```

### Why it is wrong
`C.x` and `foo` are names that do not exist in any namespace the user can be expected to have, and a user Quantity named like a built-in unit evaluates to the built-in unit instead (a different object with a scale factor). (`Str` is added to the namespace so that only this problem is shown.)

### Notes on fixing
`BaseScalar` and `Quantity` are `AtomicExpr` subclasses, and `ReprPrinter._print_AtomicExpr` (`sympy/printing/repr.py`) returns `str(expr)`. They need their own methods printing the constructor (`BaseScalar(0, CoordSys3D(...))` or `CoordSys3D(...).x`, `Quantity('foo', abbrev='fo')`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
