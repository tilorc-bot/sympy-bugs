# rust_code(log(x)/log(2)) prints 2_i32.ln(): integer-literal receivers are typed i32

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, log, atan2, rust_code
>>> x = symbols('x')
>>> print(rust_code(log(x)/log(2)))
x.ln()/2_i32.ln()
>>> print(rust_code(atan2(1, x)))
1_i32.atan2(x)
>>> from codecheck import compiles, compile_errors
>>> print(compile_errors('rust', rust_code(log(x)/log(2)), x=float))
error[E0599]: no method named `ln` found for type `i32` in the current scope...
>>> print(compile_errors('rust', rust_code(atan2(1, x)), x=float))
error[E0599]: no method named `atan2` found for type `i32` in the current scope...
```

### Expected
```pycon
>>> compiles('rust', rust_code(log(x)/log(2)), x=float)
True
>>> compiles('rust', rust_code(atan2(1, x)), x=float)
True
```

### Why it is wrong
`ln`, `atan2`, `sqrt`, ... are methods of `f64`; `i32` has none of them, so the code does not compile (rustc: `no method named 'ln' found for type 'i32'`). An integer argument of a floating-point function must be printed as an `f64` literal (`2_f64.ln()`, `1_f64.atan2(x)`).

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_caller_var` prints a numeric receiver with `self._print(expr, _type=True)`, and `_print_Integer` with `_type=True` appends the integer suffix `_i32`. For float methods the receiver should be cast to `f64` (e.g. `_cast_to_float`, which turns an integer into a `Float`).

### Related
[sympy/sympy#26967](https://redirect.github.com/sympy/sympy/issues/26967)
[sympy/sympy#27275](https://redirect.github.com/sympy/sympy/issues/27275)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
