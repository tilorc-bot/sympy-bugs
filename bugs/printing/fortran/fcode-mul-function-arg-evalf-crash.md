# fcode() raises AttributeError for 2*Piecewise(...) and turns 2*Mod(i, 3) into real arithmetic

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Piecewise, Mod, fcode
>>> x, y = symbols('x y')
>>> i = symbols('i', integer=True)
>>> fcode(2*Piecewise((x, x > 1), (y, True)), standard=95, source_format='free')
Traceback (most recent call last):
...
AttributeError: 'ExprCondPair' object has no attribute 'evalf'
>>> print(fcode(Mod(i, 3), standard=95, source_format='free'))
modulo(i, 3)
>>> '1.0d0*i' in fcode(2*Mod(i, 3), standard=95, source_format='free')
True
```

### Expected
```pycon
>>> _ = fcode(2*Piecewise((x, x > 1), (y, True)), standard=95, source_format='free')
>>> '1.0d0' in fcode(2*Mod(i, 3), standard=95, source_format='free')
False
```

### Why it is wrong
`Piecewise` alone prints fine (`merge(x, y, x > 1)`), but any `Piecewise` that is a factor or operand of a power cannot be printed at all. The same code silently changes `2*Mod(i, 3)` (integer `modulo`) into `2*(modulo(1.0d0*i, 3.0d0))`, a real-valued computation, although `Mod(i, 3)` on its own prints `modulo(i, 3)`.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter.parenthesize` calls `_eval_function` (which applies `N()` to every argument) on every `Function` instance before parenthesizing it. That is only meant for functions printed by `_print_Function`, but it is also applied to `Piecewise` (whose arguments are `ExprCondPair`s, which have no `evalf`) and to `Mod` (which has its own `_print_Mod` that keeps integer arguments). According to the review this override was added in [sympy/sympy#30514](https://redirect.github.com/sympy/sympy/issues/30514) (commit 31e03dc7ed), so this is a regression. The override should skip functions that have their own `_print_<name>` method (or be dropped in favour of the evaluation already done in `_print_Function`).

The output of `2*Mod(i, 3)` also contains the hard-coded indent from `_print_Mod`; that is a separate issue.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
