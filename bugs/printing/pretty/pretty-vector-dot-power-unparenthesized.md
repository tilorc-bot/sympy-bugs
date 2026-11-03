# The exponent of Dot(N.i, N.j)**2 goes on the second factor only

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.vector import CoordSys3D, Dot
>>> N = CoordSys3D('N')
>>> print(pretty(Dot(N.i, N.j)**2, use_unicode=True))
           2
(i_N)⋅(j_N)
```

### Expected
```pycon
>>> '((i_N)⋅(j_N))' in pretty(Dot(N.i, N.j)**2, use_unicode=True)
True
```

### Why it is wrong
The picture reads as `i_N ⋅ (j_N)²`, the dot product of `i_N` with the square of `j_N`, instead of the square of the dot product.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`_print_Dot` (and `_print_Cross`, `_print_Curl`, `_print_Divergence`) in `sympy/printing/pretty/pretty.py` build the picture with `left`/`right` and return it with ATOM binding, so `prettyForm.__pow__` and `__mul__` do not parenthesize it. They should return `binding=prettyForm.MUL`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
