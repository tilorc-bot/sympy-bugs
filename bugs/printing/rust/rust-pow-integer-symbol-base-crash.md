# sqrt(i) and i**x for integer i raise TypeError: cannot create mpf from i

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, sqrt, rust_code
>>> x = symbols('x')
>>> i = symbols('i', integer=True)
>>> rust_code(sqrt(i))
Traceback (most recent call last):
...
TypeError: cannot create mpf from i
>>> rust_code(i**x)
Traceback (most recent call last):
...
TypeError: cannot create mpf from i
```

### Why it is wrong
Printing must not fail for a valid expression; the square root of an integer variable is common in generated code.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Pow` replaces an integer base by `Float(expr.base)` whenever the exponent is not an integer. That only works for numbers; for a non-number integer base it must use a cast instead (`TypeCast(expr.base, real)`, i.e. `(i as f64).sqrt()`), as `_cast_to_float` does. The same lines also cause [rust-zero-base-power-recursion](rust-zero-base-power-recursion.md).

### Related
[rust-zero-base-power-recursion](rust-zero-base-power-recursion.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
