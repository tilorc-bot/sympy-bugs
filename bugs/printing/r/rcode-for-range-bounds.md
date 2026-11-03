# For(i, Range(10, 0, -1), ...) loops to -1, and an empty Range gives seq(from=0, to=-1, by=1)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Range, rcode
>>> from sympy.codegen.ast import For, Assignment
>>> x = symbols('x')
>>> i = symbols('i', integer=True)
>>> 'seq(from=10, to=-1, by=-1)' in rcode(For(i, Range(10, 0, -1), [Assignment(x, i)]))
True
>>> 'seq(from=0, to=-1, by=1)' in rcode(For(i, Range(0, 0), [Assignment(x, i)]))
True
```

### Expected
```pycon
>>> 'to=1,' in rcode(For(i, Range(10, 0, -1), [Assignment(x, i)]))
True
>>> 'seq(from=0, to=-1, by=1)' in rcode(For(i, Range(0, 0), [Assignment(x, i)]))
False
```

### Why it is wrong
`Range(10, 0, -1)` is `10, ..., 1`, but `seq(from=10, to=-1, by=-1)` runs to `-1`, two iterations too many. For the empty `Range(0, 0)` the loop should not run at all, but `seq(from=0, to=-1, by=1)` is an R error ("wrong sign in 'by' argument"). The reviewer checked this against the R documentation.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._print_For` prints `stop - 1` as the inclusive end regardless of the sign of the step. For a negative step it must be `stop + 1`; an empty range needs a loop that runs zero times (e.g. `seq_len(0)`, or `seq(from, to, by)` only when the range is non-empty). The Fortran printer has the same bound bug (see Related). The same method also drops the closing parenthesis of `for(...)`, which is a separate issue.

### Related
[fcode-for-negative-step-overshoots](../fortran/fcode-for-negative-step-overshoots.md)
[rcode-for-missing-paren](rcode-for-missing-paren.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
