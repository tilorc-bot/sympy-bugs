# Pow(Float(-2.5), 2) prints -2.5_f64.powi(2), which Rust evaluates as -(2.5^2)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Float, Pow, UnevaluatedExpr, rust_code
>>> x, y = symbols('x y')
>>> print(rust_code(Pow(Float(-2.5), 2, evaluate=False)))
-2.5_f64.powi(2)
>>> print(rust_code((-2)**x))
-2.0_f64.powf(x)
>>> print(rust_code(UnevaluatedExpr(x - y)**2))
x - y.powi(2)
>>> from codecheck import run_code
>>> run_code('rust', rust_code(Pow(Float(-2.5), 2, evaluate=False)))
-6.25
>>> run_code('rust', rust_code((-2)**x), x=2.0), ((-2)**x).subs(x, 2)
(-4.0, 4)
>>> run_code('rust', rust_code(UnevaluatedExpr(x - y)**2), x=3.0, y=1.0)
2.0
```

### Expected
```pycon
>>> run_code('rust', rust_code(Pow(Float(-2.5), 2, evaluate=False)))
6.25
>>> run_code('rust', rust_code((-2)**x), x=2.0), ((-2)**x).subs(x, 2)
(4.0, 4)
>>> run_code('rust', rust_code(UnevaluatedExpr(x - y)**2), x=3.0, y=1.0)
4.0
```

### Why it is wrong
In Rust a method call binds tighter than unary minus, so `-2.5_f64.powi(2)` is `-(2.5_f64.powi(2))` = -6.25 instead of 6.25, and `-2.0_f64.powf(x)` is `-(2^x)` instead of `(-2)^x`. `x - y.powi(2)` squares only `y`; the compiled code returns exactly these wrong values.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_caller_var` (which prints the receiver of a method call) only adds parentheses when `len(expr.args) > 1`. Negative numbers have no args, and `UnevaluatedExpr(x - y)` has one arg. The receiver must be parenthesized whenever its precedence is lower than that of a method call (e.g. `precedence(expr) < PRECEDENCE["Atom"]` or the printed string starts with `-`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
