# rust_code(Max(2, x)) prints an if/else whose arms are 2 (integer) and x (f64)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Max, rust_code
>>> x = symbols('x')
>>> print(rust_code(Max(2, x)))
if (x <= 2.0) {
    2
} else {
    x
}
```

### Expected
```pycon
>>> import re
>>> re.search(r'\{\s*2\s*\}', rust_code(Max(2, x))) is None
True
```

### Why it is wrong
Both arms of a Rust `if` expression must have the same type; `2` is an integer literal and `x` an `f64`, so this does not compile. (The condition already uses the float literal `2.0`.) The reviewer checked this against the Rust reference only (no rustc).

### Notes on fixing
`rust_code` rewrites `Max` to `Piecewise` (`_rewrite_known_functions` in `sympy/printing/rust.py`), and `RustCodePrinter._print_Piecewise` prints each branch expression as is. Integer branch values must be printed as `f64` literals when the other branches are real (or `Max`/`Min` could be printed with `f64::max`/`f64::min`, e.g. `x.max(2.0)`).

### Related
[sympy/sympy#26967](https://redirect.github.com/sympy/sympy/issues/26967)
[sympy/sympy#27275](https://redirect.github.com/sympy/sympy/issues/27275)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
