# A[i, j]**2 puts the exponent between the matrix and the indices: (A)²[i, j]

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, pretty
>>> i, j = symbols('i j')
>>> A = MatrixSymbol('A', 2, 2)
>>> print(pretty(A[i, j]**2, use_unicode=True))
   2
(A) [i, j]
```

### Expected
```pycon
>>> (lines := pretty(A[i, j]**2, use_unicode=True).splitlines())[0].index('2') > lines[1].index(']')
True
```

### Why it is wrong
The picture reads as the `(i, j)` entry of the matrix power `A²`, not as the square of the entry `A[i, j]`.

### Notes on fixing
`PrettyPrinter._print_MatrixElement` in `sympy/printing/pretty/pretty.py` stores `prettyFunc`/`prettyArgs` on a FUNC-binding form, so `prettyForm.__pow__` (`sympy/printing/pretty/stringpict.py`) uses the inline function-power form `f²(x)`, which is right for `sin²(x)` but not for indexing. The element should not be offered to the inline form (e.g. give it ATOM binding, since `[i, j]` already delimits it).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
