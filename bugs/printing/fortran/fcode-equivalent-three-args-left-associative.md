# Equivalent(a, b, c) prints a .eqv. b .eqv. c, which Fortran evaluates left to right

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Equivalent, fcode
>>> a, b, c = symbols('a b c')
>>> fcode(Equivalent(a, b, c), source_format='free')
'a .eqv. b .eqv. c'
```

### Expected
```pycon
>>> from itertools import product
>>> class L:
...     # Fortran LOGICAL, with Python operators of matching precedence and
...     # left-associativity: | is .eqv., ^ is .or., & is .and., ~ is .not.
...     def __init__(self, v): self.v = bool(v)
...     def __or__(self, o): return L(self.v == o.v)
...     def __xor__(self, o): return L(self.v or o.v)
...     def __and__(self, o): return L(self.v and o.v)
...     def __invert__(self): return L(not self.v)
>>> def fortran_value(code, env):
...     for f, p in (('.eqv.', '|'), ('.or.', '^'), ('.and.', '&'), ('.not.', '~'),
...                  ('.true.', 'L(1)'), ('.false.', 'L(0)')):
...         code = code.replace(f, p)
...     return eval(code, dict(env, L=L)).v
>>> code = fcode(Equivalent(a, b, c), source_format='free')
>>> all(fortran_value(code, {'a': L(va), 'b': L(vb), 'c': L(vc)})
...     == bool(Equivalent(a, b, c).subs({a: va, b: vb, c: vc}))
...     for va, vb, vc in product([False, True], repeat=3))
True
```

### Why it is wrong
`.eqv.` is a binary, left-associative operator in Fortran, so the output means `(a .eqv. b) .eqv. c`, which is true for a = b = c = .false., whereas `Equivalent(a, b, c)` (all arguments equal) is false. This was checked against the Fortran standard's operator rules only, not executed with a Fortran compiler; Expected emulates Fortran's precedence and associativity in Python.

### Notes on fixing
`CodePrinter._print_Equivalent` (`sympy/printing/codeprinter.py`) joins all arguments with the `equivalent` operator, which is only correct for two arguments. For more, print the pairwise conjunction (`a .eqv. b .and. b .eqv. c`, parenthesized) or fall back to `expr.to_nnf()`, which the method already does when the printer has no `equivalent` operator.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
