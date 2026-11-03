# Max(x, sqrt(Abs(y) - 1)) evaluates sqrt(-y - 1) in a guard: Max/Min become Piecewise

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Max, Abs, sqrt, julia_code
>>> x, y = symbols('x y', real=True)
>>> print(julia_code(Max(x, y)))
(((x >= y) ? (x) : (y)))
>>> print(julia_code(Max(x, sqrt(Abs(y) - 1))))
((((x >= sqrt(-y - 1) || y >= 0) && (x >= sqrt(y - 1) || y < 0)) ? (x) : (sqrt(((y >= 0) ? (y) : (-y)) - 1))))
```

### Expected
```pycon
>>> 'sqrt(-y - 1)' in julia_code(Max(x, sqrt(Abs(y) - 1)))
False
```

### Why it is wrong
Julia has `max`/`min`, but `Max`/`Min` are rewritten to `Piecewise`. With real symbols the rewrite also expands `Abs` into cases and evaluates both cases in the condition: at `x = 1, y = 3` the first test computes `sqrt(-4)`, which raises `DomainError` in Julia although `Max(1, sqrt(2))` is well defined. The reviewer ran this with Julia 1.12. The output is also needlessly long.

### Notes on fixing
`sympy/printing/julia.py` has no entry for `Max`/`Min` in `known_fcns_src2`, so `CodePrinter._print_Function` falls back to the `_rewriteable_functions` rewrite `'Max': ('Piecewise', [])` (`sympy/printing/codeprinter.py`), and the rewrite also rewrites the `Abs` inside. Mapping `"Max": "max"` and `"Min": "min"` (Julia's `max`/`min` accept any number of arguments) avoids both problems.

The review also reports that `Dummy` symbols from the core rewrite can leak into the output (`_Dummy_48`); no small reproducer for that was found on current master.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
