# (A ⨂ B)∘D and A ⨂ (B∘D) print identically: A ⨂ B∘D

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, HadamardProduct, KroneckerProduct, pretty
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> D4, D2 = MatrixSymbol('D', 4, 4), MatrixSymbol('D', 2, 2)
>>> print(pretty(HadamardProduct(KroneckerProduct(A, B), D4), use_unicode=True))
A ⨂ B∘D
>>> print(pretty(KroneckerProduct(A, HadamardProduct(B, D2)), use_unicode=True))
A ⨂ B∘D
```

### Expected
```pycon
>>> pretty(HadamardProduct(KroneckerProduct(A, B), D4), use_unicode=True) != pretty(KroneckerProduct(A, HadamardProduct(B, D2)), use_unicode=True)
True
```

### Why it is wrong
`(A ⨂ B)∘D` and `A ⨂ (B∘D)` are different matrices (here `D` is 4x4 in the first and 2x2 in the second) but print the same.

### Notes on fixing
`PrettyPrinter._print_HadamardProduct` in `sympy/printing/pretty/pretty.py` parenthesizes only `MatAdd`, `MatMul` and `HadamardProduct` arguments; `KroneckerProduct` (which prints with the looser ` ⨂ ` separator) is missing from the list.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
