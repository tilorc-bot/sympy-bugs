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
```

### Expected
```pycon
>>> a, b = rust_code(d + x).split(' + ')
>>> a != b
True
```

### Why it is wrong
A `Dummy` is a different variable from the `Symbol` with the same name, but both print as `x`, so the generated code silently uses one variable for both. The other code printers print `x_<index>` for a `Dummy`.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Dummy` returns `expr.name`, overriding `CodePrinter._print_Dummy`, which appends the dummy index. Removing the override fixes this, but `test_dummy_loops` in `sympy/printing/tests/test_rust.py` relies on Dummy loop indices printing as plain `i`/`m` and needs updating.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
