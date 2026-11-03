# rust_code calls f64-only methods on integer symbols: i.powi(2), i.sin()

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, sin, exp, rust_code
>>> i = symbols('i', integer=True)
>>> print(rust_code(i**2))
i.powi(2)
>>> print(rust_code(sin(i)))
i.sin()
>>> print(rust_code(exp(i)))
i.exp()
```

### Expected
```pycon
>>> '.powi(' in rust_code(i**2)
False
>>> 'i.sin()' in rust_code(sin(i)), 'i.exp()' in rust_code(exp(i))
(False, False)
```

### Why it is wrong
`codegen` declares integer symbols as `i32`, and `powi`, `sin`, `exp`, ... only exist for `f32`/`f64`; the integer power method is `i32::pow(u32)`. The reviewer checked `i.powi(2)` against the Rust documentation; for `i.sin()`, rustc 1.98 reports `no method named 'sin' found for type 'i32'` (follow-up comment).

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Function` uses the method-call style (`receiver.method(...)`) with the receiver printed as is; `_print_Pow` delegates to it with the `"Pow"` entry of `known_functions`, which chooses `powi` for any integer exponent without looking at the base type. An integer receiver of a float method has to be cast (`(i as f64).sin()`); for an integer base with a nonnegative integer exponent `i.pow(2)` is the integer power.

### Related
[sympy/sympy#26967](https://redirect.github.com/sympy/sympy/issues/26967)
[sympy/sympy#27275](https://redirect.github.com/sympy/sympy/issues/27275)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
