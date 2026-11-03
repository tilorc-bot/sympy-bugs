# ccode(For(i, Range(10, 0, -1), ...)) prints the condition `i < 0`, so the loop never runs

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Range
>>> from sympy.codegen.ast import For, aug_assign
>>> from sympy.printing.c import ccode
>>> i, x = symbols('i x')
>>> print(ccode(For(i, Range(10, 0, -1), [aug_assign(x, '+', i)])))
for (i = 10; i < 0; i += -1) {
   x += i;
}
```

### Expected
```pycon
>>> 'i < 0' in ccode(For(i, Range(10, 0, -1), [aug_assign(x, '+', i)]))
False
```

### Why it is wrong
`Range(10, 0, -1)` is `10, 9, ..., 1`, but the printed loop condition `i < 0` is false at the start, so the body never executes. The original reviewer compiled and ran this with gcc; it was not executed here.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_For` always uses `<`; for a negative step it needs `>` (and for a symbolic step the sign is unknown). The same method also formats `start`/`stop`/`step` with `str()` (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
