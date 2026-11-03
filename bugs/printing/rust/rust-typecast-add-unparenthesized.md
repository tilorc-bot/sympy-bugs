# rust_code(Eq(x, i + j)) prints x == i + j as f64, casting only j

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq, rust_code
>>> i, j = symbols('i j', integer=True)
>>> x = symbols('x')
>>> print(rust_code(Eq(x, i + j)))
x == i + j as f64
>>> r = symbols('r', real=True)
>>> print(rust_code(r*(i + j)))
r*i + j as f64
```

### Expected
```pycon
>>> 'i + j as f64' in rust_code(Eq(x, i + j))
False
>>> 'i + j as f64' in rust_code(r*(i + j))
False
```

### Why it is wrong
`as` binds tighter than `+` and `*` in Rust, so `i + j as f64` adds an `i32` to an `f64` (a type error), and `r*i + j as f64` is not even the product `r*(i + j)` any more. The reviewer checked this against the Rust reference only (no rustc).

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_TypeCast` prints `self._print(expr.expr) + ' as f64'` without parenthesizing the cast operand. The operand must be parenthesized unless it is an atom (`(i + j) as f64`), and the cast as a whole needs a precedence so that the enclosing `Mul` keeps `r*((i + j) as f64)` intact. This is the case of [sympy/sympy#28418](https://redirect.github.com/sympy/sympy/issues/28418) that is still broken (the review mentions a fix in [sympy/sympy#30867](https://redirect.github.com/sympy/sympy/issues/30867)).

### Related
[sympy/sympy#28418](https://redirect.github.com/sympy/sympy/issues/28418)
[sympy/sympy#30867](https://redirect.github.com/sympy/sympy/issues/30867)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
