# RustCodePrinter().doprint and codegen(..., 'Rust') skip the rewrites done by rust_code: Mod is unsupported, Max prints max(x, y)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Mod, Max, rust_code
>>> from sympy.printing.rust import RustCodePrinter
>>> from sympy.utilities.codegen import codegen
>>> x, y = symbols('x y')
>>> print(rust_code(Mod(x, y)))
x - y*(x/y).floor()
>>> RustCodePrinter().doprint(Mod(x, y))
Traceback (most recent call last):
...
sympy.printing.codeprinter.PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.rust.RustCodePrinter'>: Mod...
>>> print(RustCodePrinter().doprint(Max(x, y)))
max(x, y)
>>> 'unsupported: Mod' in codegen(('f', Mod(x, y)), 'Rust')[0][1]
True
>>> from codecheck import compiles, compile_errors
>>> print(compile_errors('rust', codegen(('f', Mod(x, y)), 'Rust')[0][1]))
error[E0425]: cannot find function, tuple struct or tuple variant `Mod` in this scope...
>>> print(compile_errors('rust', codegen(('f', Max(x, y)), 'Rust')[0][1]))
error[E0425]: cannot find function `max` in this scope...
>>> print(compile_errors('rust', RustCodePrinter().doprint(Max(x, y)), x=float, y=float))
error[E0425]: cannot find function `max` in this scope...
```

### Expected
```pycon
>>> _ = RustCodePrinter().doprint(Mod(x, y))
>>> 'unsupported: Mod' in codegen(('f', Mod(x, y)), 'Rust')[0][1]
False
>>> compile_errors('rust', codegen(('f', Mod(x, y)), 'Rust')[0][1]) == ''
True
>>> compile_errors('rust', codegen(('f', Max(x, y)), 'Rust')[0][1]) == ''
True
>>> compile_errors('rust', RustCodePrinter().doprint(Max(x, y)), x=float, y=float) == ''
True
```

### Why it is wrong
`codegen(..., 'Rust')` uses `RustCodePrinter` directly and therefore emits `// unsupported: Mod` and `Mod(x, y)` in the function body, and `max(x, y)` (no such function in scope for `f64`; `std::cmp::max` needs `Ord`, which `f64` does not implement), although `rust_code` can print both; rustc rejects both generated functions (`cannot find function 'Mod'` / `'max'`).

### Notes on fixing
The rewrites (`Mod` to `floor`, `Max`/`Min` to `Piecewise`, ...) are applied by `rust_code` in `sympy/printing/codeprinter.py` (`expr = printer._rewrite_known_functions(expr)`) before calling `doprint`, not by the printer. Moving the call into `RustCodePrinter.doprint` (or `_print`) makes `codegen` and direct printer use consistent.

### Related
[sympy/sympy#26993](https://redirect.github.com/sympy/sympy/issues/26993)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
