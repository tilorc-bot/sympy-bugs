# Integer symbols are passed to intrinsics that need real arguments: sin(i), atan2(i, x)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, sin, exp, atan2, fcode
>>> x = symbols('x', real=True)
>>> i = symbols('i', integer=True)
>>> print(fcode(sin(i), standard=95, source_format='free'))
sin(i)
>>> print(fcode(exp(i), standard=95, source_format='free'))
exp(i)
>>> print(fcode(atan2(i, x), standard=95, source_format='free'))
atan2(i, x)
```

### Expected
```pycon
>>> import ast, re
>>> def passes_bare_i(code):
...     call = ast.parse(re.sub(r'(\d)d(\d)', r'\1e\2', code.strip())).body[0].value
...     return any(isinstance(a, ast.Name) and a.id == 'i' for a in call.args)
>>> passes_bare_i(fcode(sin(i), standard=95, source_format='free'))
False
>>> passes_bare_i(fcode(exp(i), standard=95, source_format='free'))
False
>>> passes_bare_i(fcode(atan2(i, x), standard=95, source_format='free'))
False
```

### Why it is wrong
`codegen` declares integer symbols as `INTEGER`, and these intrinsics only accept `REAL`/`COMPLEX` arguments of matching kind. gfortran 15.2 reports `'x' argument of 'sin' intrinsic at (1) must be REAL or COMPLEX` and `'y' argument of 'atan2' intrinsic at (1) must be REAL`.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Function` (via `CodePrinter._print_Function` and `known_functions`) prints the arguments unchanged. Integer arguments of real intrinsics need a conversion, as `_print_Pow` already does for `sqrt` (`sqrt(dble(i))`). Other cases with the same cause: `log(i)` → `log(i)`, and `Min(i, x)` → `min(i, x)` (gfortran: `'a2' argument of 'min' intrinsic must be INTEGER(4)`), which is the symbol version of the `max(0, x)` integer-literal case in [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844). Not covered by a test.

The Expected block checks that `i` is not passed directly as an argument of the printed call (it parses the call as Python after turning `1d0` into `1e0`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
