# ccode(For(...)) prints the Range bounds with str(), e.g. `i < n**2`

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Range
>>> from sympy.codegen.ast import For, aug_assign
>>> from sympy.printing.c import ccode
>>> i, n, x = symbols('i n x')
>>> print(ccode(For(i, Range(0, n**2), [aug_assign(x, '+', i)])))
for (i = 0; i < n**2; i += 1) {
   x += i;
}
```

### Expected
```pycon
>>> '**' in ccode(For(i, Range(0, n**2), [aug_assign(x, '+', i)]))
False
```

### Why it is wrong
`**` is not a C operator (`n**2` is parsed as `n * *2`, a compile error). The loop bounds are SymPy expressions and must be printed as C.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_For` formats `start`, `stop` and `step` directly into the string (so `str()` is used) instead of passing them through `self._print`. The same method also uses `<` for negative steps (separate issue).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
