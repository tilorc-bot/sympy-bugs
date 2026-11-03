# rust_code(Rational(1, 2)**x) and rust_code(sin(S.Half)) raise TypeError: unexpected keyword argument '_type'

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Rational, S, sin, UnevaluatedExpr, rust_code
>>> x = symbols('x')
>>> rust_code(Rational(1, 2)**x)
Traceback (most recent call last):
...
TypeError: RustCodePrinter._print_Rational() got an unexpected keyword argument '_type'
>>> rust_code(sin(S.Half))
Traceback (most recent call last):
...
TypeError: RustCodePrinter._print_Rational() got an unexpected keyword argument '_type'
>>> rust_code(UnevaluatedExpr(2)**x)
Traceback (most recent call last):
...
TypeError: StrPrinter._print_UnevaluatedExpr() got an unexpected keyword argument '_type'
```

### Expected
```pycon
>>> _ = rust_code(Rational(1, 2)**x)
>>> _ = rust_code(sin(S.Half))
>>> _ = rust_code(UnevaluatedExpr(2)**x)
```

### Why it is wrong
Printing must not fail for a valid expression; a rational number as the receiver of a method call (`sin(1/2)`, `(1/2)**x`) is common.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_caller_var` calls `self._print(expr, _type=True)` for every `expr.is_number`, but only `_print_Integer`, `_print_Float` and a few constant printers accept `_type`. `_print_Rational` already prints an `f64` literal (`1_f64/2.0`) and could simply accept and ignore `_type` (the result also needs parentheses as a receiver); other numbers (`UnevaluatedExpr` of a number, `NumberSymbol`s without `_type`, ...) need a fallback without the keyword.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
