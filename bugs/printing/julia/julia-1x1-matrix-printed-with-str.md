# julia_code(Matrix([[x**2]])) prints [x**2]: the entry of a 1x1 matrix is printed with str()

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Matrix, julia_code
>>> x, y = symbols('x y')
>>> print(julia_code(Matrix([[x**2]])))
[x**2]
>>> print(julia_code(Matrix([[x**2, y]])))
[x .^ 2 y]
```

### Expected
```pycon
>>> '**' in julia_code(Matrix([[x**2]]))
False
```

### Why it is wrong
For every other shape the entries are printed as Julia (`x .^ 2`), but a 1x1 matrix gets the Python `str()` of its entry, so any power, rational, constant etc. comes out in Python syntax. The reviewer ran the output with Julia 1.12; `x**2` does not parse.

### Notes on fixing
`sympy/printing/julia.py:JuliaCodePrinter._print_MatrixBase` returns `"[%s]" % A[0, 0]` for shape `(1, 1)`; it should use `self._print(A[0, 0])`. Note also that `[e]` is a 1-element vector in Julia, not a 1x1 matrix (that would be `[e;;]` or `reshape([e], 1, 1)`).

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
