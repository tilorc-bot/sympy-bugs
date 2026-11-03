# latex() does not bracket a quantum TensorProduct inside a product: A*TensorProduct(A, B) prints as A {A}\otimes {B}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.physics.quantum import TensorProduct
>>> A, B, C = symbols('A B C', commutative=False)
>>> print(latex(A*TensorProduct(A, B)))
A {A}\otimes {B}
>>> print(latex(TensorProduct(A, B)*C))
{A}\otimes {B} C
```

### Expected
```pycon
>>> latex(A*TensorProduct(A, B)).startswith(r'A \left(')
True
```

### Why it is wrong
`A A ⊗ B` reads as `(A A) ⊗ B` and `A ⊗ B C` as `A ⊗ (B C)`, which are different operators from `A (A ⊗ B)` and `(A ⊗ B) C`. The quantum TensorProduct itself already brackets Mul arguments (`TensorProduct(A*B, C)` prints `\left({A B}\right)\otimes {C}`), so the reverse direction is inconsistent.

### Notes on fixing
`PRECEDENCE_TRADITIONAL['TensorProduct']` is `PRECEDENCE['Mul']` (`sympy/printing/precedence.py`), so `LatexPrinter._needs_mul_brackets` (`precedence_traditional(expr) < PRECEDENCE['Mul']`) never brackets a TensorProduct factor. ⊗ binds more loosely than juxtaposition, so the TensorProduct needs a precedence below Mul (or `_needs_mul_brackets` needs a special case); check that the pretty printer, which shares the table, still looks right.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
