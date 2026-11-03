# Piecewise, AccumBounds and ComplexRegion use class names that `from sympy import *` does not provide

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Piecewise, AccumBounds, ComplexRegion, Interval, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x, y = symbols('x y')
>>> p = Piecewise((x, x > 0), (y, True))
>>> srepr(p)
"Piecewise(ExprCondPair(Symbol('x'), StrictGreaterThan(Symbol('x'), Integer(0))), ExprCondPair(Symbol('y'), true))"
>>> eval(srepr(p), ns)
Traceback (most recent call last):
...
NameError: name 'ExprCondPair' is not defined
>>> srepr(AccumBounds(1, 2))
'AccumulationBounds(Integer(1), Integer(2))'
>>> c = ComplexRegion(Interval(1, 2)*Interval(3, 4))
>>> srepr(c)
'CartesianComplexRegion(ProductSet(Interval(Integer(1), Integer(2), false, false), Interval(Integer(3), Integer(4), false, false)))'
```

### Expected
```pycon
>>> eval(srepr(p), ns) == p
True
>>> eval(srepr(AccumBounds(1, 2)), ns) == AccumBounds(1, 2)
True
>>> eval(srepr(c), ns) == c
True
```

### Why it is wrong
`srepr` promises `eval(srepr(expr)) == expr` in the scope of `from sympy import *`. Every `Piecewise` fails this, as do AccumBounds and ComplexRegion, because the printed class names are not exported from `sympy`.

### Notes on fixing
These objects go through the generic fallback `ReprPrinter.emptyPrinter` (`sympy/printing/repr.py`), which prints `expr.__class__.__name__`. Each class needs either to be exported from `sympy` or a `_print_<Class>` method that prints a public constructor (e.g. `Piecewise((expr, cond), ...)`, `AccumBounds(...)`, `ComplexRegion(..., polar=True)`).

Other classes with the same problem:
- `MatrixElement` (`srepr(MatrixSymbol('X', 2, 2)[0, 1])`), which also hits the separate `Str` problem;
- `PolarComplexRegion`;
- `Class` from `sympy.categories` (also inside `srepr(Category('K'))`);
- `RandomSymbol`/`SingleContinuousPSpace`, e.g. `srepr(sympy.stats.Normal('X', 0, 1))`. These are not importable even with `from sympy.stats import *` added.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
