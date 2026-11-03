# A physics.vector ReferenceFrame prints as its bare name, which evaluates to sympy.N

### Kind
lossy

### Actual
```pycon
>>> import sympy, sympy.physics.vector
>>> from sympy import srepr
>>> from sympy.physics.vector import ReferenceFrame, Vector
>>> ns = {}
>>> exec('from sympy import *; from sympy.physics.vector import *', ns)
>>> N = ReferenceFrame('N')
>>> srepr(N)
'N'
>>> eval(srepr(N), ns) is sympy.N
True
>>> v = N.x + 2*N.y
>>> srepr(v)
'Vector((ImmutableDenseMatrix([[Integer(1)], [Integer(2)], [Integer(0)]]), N))'
>>> eval(srepr(v), ns)
Traceback (most recent call last):
...
TypeError: 'function' object is not subscriptable
```

### Expected
```pycon
>>> isinstance(eval(srepr(N), ns), ReferenceFrame), isinstance(eval(srepr(v), ns), Vector)
(True, True)
```

### Why it is wrong
`srepr` should give an expression that rebuilds the object; for a frame named `N` it gives the numerical-evaluation function `N`, and every vector expressed in that frame fails to evaluate.

### Notes on fixing
`ReferenceFrame` is not `Basic`; `ReprPrinter.emptyPrinter` (`sympy/printing/repr.py`) falls back to `str(frame)`, which is the name. `Vector` has `args` of the form `[(matrix, frame)]` that its constructor does not accept in this shape (`Vector((matrix, N))` instead of `Vector([(matrix, N)])`). Frames have identity semantics (two `ReferenceFrame('N')` are different frames), so the best a fix can give is a fresh frame with the same name; that is why Expected only checks the types.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
