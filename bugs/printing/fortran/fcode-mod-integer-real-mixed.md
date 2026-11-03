# fcode(Mod(x, i)) passes a real and an integer to modulo, which needs matching types

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Mod, fcode
>>> x = symbols('x', real=True)
>>> i = symbols('i', integer=True)
>>> print(fcode(Mod(x, i), standard=95, source_format='free'))
modulo(x, i)
>>> print(fcode(Mod(i, x), standard=95, source_format='free'))
modulo(i, x)
```

### Expected
```pycon
>>> import ast, re
>>> def passes_bare_i(code):
...     call = ast.parse(re.sub(r'(\d)d(\d)', r'\1e\2', code.strip())).body[0].value
...     return any(isinstance(a, ast.Name) and a.id == 'i' for a in call.args)
>>> [passes_bare_i(fcode(e, standard=95, source_format='free')) for e in (Mod(x, i), Mod(i, x))]
[False, False]
```

### Why it is wrong
Fortran's `modulo(a, p)` requires both arguments to have the same type and kind. With `x` real and `i` integer (as `codegen` declares them), gfortran 15.2 reports: `'a' and 'p' arguments of 'modulo' intrinsic at (1) must have the same type`.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Mod` prints both arguments unchanged. When exactly one argument is an integer it needs a conversion (e.g. `dble(i)`, as `_print_Pow` does for `sqrt`). `Mod(i, j)` with both integer is fine as is. Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
