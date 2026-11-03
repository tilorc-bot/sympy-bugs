# Quaternion drops real_field

### Kind
lossy

### Actual
```pycon
>>> from sympy import Quaternion, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> q = Quaternion(1, 2, 3, 4, real_field=False)
>>> srepr(q)
'Quaternion(Integer(1), Integer(2), Integer(3), Integer(4))'
>>> eval(srepr(q), ns).real_field
True
```

### Expected
```pycon
>>> eval(srepr(q), ns).real_field
False
```

### Why it is wrong
`real_field` changes how the quaternion behaves (e.g. under `conjugate`/`norm` with complex coefficients), but srepr loses it.

### Notes on fixing
`Quaternion` stores `real_field` (and `norm`) as attributes, not in `args`; `ReprPrinter` (`sympy/printing/repr.py`) has no `_print_Quaternion`, so only `args` are printed. Note that `==` ignores `real_field`, so `eval(srepr(q)) == q` does not detect this.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
