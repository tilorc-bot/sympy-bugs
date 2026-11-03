# rust_code() prints the quotient of two integer symbols as i32 division

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, rust_code
>>> p1, p2 = symbols('p1 p2', integer=True)
>>> print(rust_code(p1/p2))
p1/p2
>>> from codecheck import compiles, compile_errors, run_code
>>> print(rust_code(p1/p2, assign_to='y'))
y = p1/p2;
>>> print(compile_errors('rust', rust_code(p1/p2, assign_to='y'), assign_to=('y', float), p1=int, p2=int))
error[E0308]: mismatched types: expected `f64`, found `i32`...
>>> run_code('rust', rust_code(p1/p2), p1=7, p2=2), (p1/p2).subs({p1: 7, p2: 2})
(3.0, 7/2)
```

### Expected
```pycon
>>> compiles('rust', rust_code(p1/p2, assign_to='y'), assign_to=('y', float), p1=int, p2=int)
True
>>> run_code('rust', rust_code(p1/p2), p1=7, p2=2)
3.5
```

### Why it is wrong
`codegen(('ratio', p1/p2), 'Rust')` declares `fn ratio(p1: i32, p2: i32) -> f64` and returns `p1/p2`, an `i32` (and an integer division). rustc reports `mismatched types: expected f64, found i32` when `p1/p2` is assigned to an `f64`, and the value computed is `7/2 = 3`, not 3.5. The printer already casts in similar cases: `rust_code(i/2)` is `(1_f64/2.0)*i as f64`.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Mul` casts the factors to `f64` only when some factor `is_real and not is_integer`; for a quotient of integers it falls through to `CodePrinter._print_Mul`, which prints `p1/p2`. A `Pow` with a negative exponent of an integer base should count as non-integer here (e.g. `p1 as f64/p2 as f64`). Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
