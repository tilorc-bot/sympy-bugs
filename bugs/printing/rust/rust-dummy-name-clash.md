# rust_code(Dummy('x') + Symbol('x')) prints x + x

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Symbol, Dummy, rust_code
>>> x = Symbol('x')
>>> d = Dummy('x')
>>> print(rust_code(d + x))
x + x
>>> from codecheck import run_code
>>> values = {rust_code(s): v for s, v in [(d, 1.0), (x, 2.0)]}
>>> values
{'x': 2.0}
>>> run_code('rust', rust_code(d + x), **values), (d + x).subs({d: 1.0, x: 2.0})
(4.0, 3.00000000000000)
```

### Expected
```pycon
>>> values = {rust_code(s): v for s, v in [(d, 1.0), (x, 2.0)]}
>>> run_code('rust', rust_code(d + x), **values) == (d + x).subs({d: 1.0, x: 2.0})
True
```

### Why it is wrong
A `Dummy` is a different variable from the `Symbol` with the same name, but both print as `x`, so the generated code silently uses one variable for both: compiled, it computes `2*x` instead of `d + x`. The other code printers print `x_<index>` for a `Dummy`.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Dummy` returns `expr.name`, overriding `CodePrinter._print_Dummy`, which appends the dummy index. Removing the override fixes this, but `test_dummy_loops` in `sympy/printing/tests/test_rust.py` relies on Dummy loop indices printing as plain `i`/`m` and needs updating.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
