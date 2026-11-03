# rust_code(sign(i)) for integer i compares an i32 with 0.0

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, sign, rust_code
>>> i = symbols('i', integer=True)
>>> print(rust_code(sign(i)))
(if (i == 0.0) { 0.0 } else { (i).signum() })
```

### Expected
```pycon
>>> '(i == 0.0)' in rust_code(sign(i))
False
```

### Why it is wrong
`codegen` declares integer symbols as `i32`, and Rust does not compare an `i32` with a float literal; the two `if` arms also have different types (`0.0` vs. `i32::signum`). rustc 1.98 reports `mismatched types: expected 'i32', found floating-point number`.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_sign` uses a fixed `f64` template. For an integer argument `i.signum()` is already correct (`i32::signum(0)` is 0); alternatively cast the argument with `as f64`. Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
