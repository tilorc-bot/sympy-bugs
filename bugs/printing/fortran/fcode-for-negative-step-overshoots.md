# fcode(For(i, Range(10, 0, -1), ...)) prints do i = 10, -1, -1, running two extra iterations

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Range, fcode
>>> from sympy.codegen.ast import For, aug_assign
>>> x = symbols('x')
>>> i = symbols('i', integer=True)
>>> print(fcode(For(i, Range(10, 0, -1), [aug_assign(x, '+', i)]), source_format='free'))
do i = 10, -1, -1
   x = x + i
end do
```

### Expected
```pycon
>>> 'do i = 10, 1, -1' in fcode(For(i, Range(10, 0, -1), [aug_assign(x, '+', i)]), source_format='free')
True
```

### Why it is wrong
`Range(10, 0, -1)` is `10, 9, ..., 1`, but the Fortran loop (whose upper bound is inclusive) runs `10, 9, ..., 0, -1`, two iterations too many. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_For` prints `stop - 1` as the inclusive last value regardless of the sign of the step. For a negative step it must be `stop + 1`; in general the last value is `Range.inf`/`Range.sup` (or `iterable[-1]` for a non-empty range). `rcode` has the same bug in its own `_print_For` (see Related).

### Related
[rcode-for-range-bounds](../r/rcode-for-range-bounds.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
