# Integer literals are printed next to f64 values: 2/x, 2*x, x + 1

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, cos, rust_code
>>> x = symbols('x')
>>> print(rust_code(2/x))
2/x
>>> print(rust_code(2*x))
2*x
>>> print(rust_code(x + 1))
x + 1
>>> print(rust_code(cos(2*x)))
(2*x).cos()
>>> from codecheck import compiles, compile_errors
>>> print(compile_errors('rust', rust_code(2/x), x=float))
error[E0277]: cannot divide `{integer}` by `f64`...
>>> print(compile_errors('rust', rust_code(2*x), x=float))
error[E0277]: cannot multiply `{integer}` by `f64`...
>>> print(compile_errors('rust', rust_code(x + 1), x=float))
error[E0277]: cannot add `{integer}` to `f64`...
>>> print(compile_errors('rust', rust_code(cos(2*x)), x=float))
error[E0277]: cannot multiply `{integer}` by `f64`...
```

### Expected
```pycon
>>> [compiles('rust', rust_code(e), x=float) for e in (2/x, 2*x, x + 1, cos(2*x))]
[True, True, True, True]
```

### Why it is wrong
Rust has no implicit numeric conversion: with `x: f64` (as `codegen` declares a symbol without assumptions) `2/x`, `2*x` and `x + 1` combine an `{integer}` with an `f64` and do not compile; the literals must be `2.0`, `1.0`. The reviewer checked `2/x` against the Rust reference; in the follow-up comment, rustc 1.98 rejected `codegen` output containing `(2*x).cos()` ("cannot multiply `{integer}` by `f64`") and `rust_code(sign(x + y) + 42)` ("cannot add `{integer}` to `f64`").

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Mul` and `_print_Add` convert integer arguments to floats only when some argument `is_real and not is_integer`. A symbol without assumptions has `is_real = None`, so nothing is converted and `CodePrinter` prints the integer literals as they are. Since non-integer symbols are `f64` in generated code, integer literals should be printed as floats unless all operands are known integers.

Existing tests assert such output (tested-buggy, from the follow-up comment): `test_sign` in `sympy/printing/tests/test_rust.py` (`... + 42`), and `test_complicated_rs_codegen`, `test_output_arg_mixed_unordered` and `test_piecewise_` in `sympy/utilities/tests/test_codegen_rust.py`.

### Related
[sympy/sympy#26967](https://redirect.github.com/sympy/sympy/issues/26967)
[sympy/sympy#27275](https://redirect.github.com/sympy/sympy/issues/27275)
[rust-integer-symbol-division](rust-integer-symbol-division.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
