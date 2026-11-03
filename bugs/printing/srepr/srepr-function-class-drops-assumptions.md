# srepr() of an undefined function class drops its assumptions and nargs

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Function, srepr
>>> ns = {}
>>> exec('from sympy import *', ns)
>>> x = symbols('x')
>>> f = Function('f', real=True)
>>> g = Function('g', nargs=2)
>>> srepr(f(x)), srepr(g)
("Function('f')(Symbol('x'))", "Function('g')")
>>> f(x).is_real, eval(srepr(f(x)), ns).is_real
(True, None)
```

### Expected
```pycon
>>> [eval(srepr(e), ns) == e for e in (f, f(x), g)]
[True, True, True]
```

### Why it is wrong
`Function('f', real=True)(x)` is real and `Function('f')(x)` is not; they are different objects but srepr prints both the same, so the round trip loses the assumptions (and `nargs`).

### Related
[sympy/sympy#15938](https://redirect.github.com/sympy/sympy/issues/15938)

### Notes on fixing
`ReprPrinter._print_FunctionClass` (`sympy/printing/repr.py`) prints only `Function(%r) % expr.__name__`. It should add the class's original assumptions and `nargs` when they are not the defaults.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
