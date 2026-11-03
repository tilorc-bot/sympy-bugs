# A quantum TensorProduct that is a factor of a Mul is not parenthesized: A⨂ C⋅B

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, pretty
>>> from sympy.physics.quantum import TensorProduct
>>> A, B, C = symbols('A B C', commutative=False)
>>> print(pretty(TensorProduct(A, C)*B, use_unicode=True))
A⨂ C⋅B
```

### Expected
```pycon
>>> pretty(TensorProduct(A, C)*B, use_unicode=True).startswith('(')
True
```

### Why it is wrong
`⋅` binds tighter than `⨂`, so the picture reads as `A ⨂ (C⋅B)` instead of `(A ⨂ C)⋅B`.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`TensorProduct._pretty` in `sympy/physics/quantum/tensorproduct.py` returns its picture with ATOM binding, so `prettyForm.__mul__` (via `PrettyPrinter._print_Mul`) does not parenthesize it. It should return a binding weaker than MUL when it has more than one factor.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
