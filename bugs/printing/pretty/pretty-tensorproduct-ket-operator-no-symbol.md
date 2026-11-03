# pretty() omits the ⨂ sign after a Ket in a TensorProduct with a non-Ket: TensorProduct(Ket(x), Operator('A')) prints as ❘x⟩A

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, pretty
>>> from sympy.physics.quantum import TensorProduct, Ket, Operator
>>> x = symbols('x')
>>> print(pretty(TensorProduct(Ket(x), Operator('A')), use_unicode=True))
❘x⟩A
```

### Expected
```pycon
>>> '⨂' in pretty(TensorProduct(Ket(x), Operator('A')), use_unicode=True)
True
```

### Why it is wrong
Juxtaposition of a ket and an operator reads as their product `❘x⟩A`, not as a tensor product.

### Notes on fixing
`TensorProduct._pretty` in `sympy/physics/quantum/tensorproduct.py` omits the separator after any `KetBase`/`BraBase` factor so that `TensorProduct(Ket(x), Ket(y))` prints as `❘x⟩❘y⟩`. The separator should be omitted only when the next factor is also a ket (or bra) of the same kind.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
