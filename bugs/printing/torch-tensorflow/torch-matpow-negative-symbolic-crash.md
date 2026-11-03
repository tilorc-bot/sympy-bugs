# torch_code(MatPow(A, -1)) raises RecursionError; MatPow(A, n) raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, MatPow
>>> from sympy.printing.pytorch import torch_code
>>> n = symbols('n', integer=True)
>>> A = MatrixSymbol('A', 2, 2)
>>> print(torch_code(MatPow(A, 2)))
torch.mm(A, A)
>>> torch_code(MatPow(A, -1))
Traceback (most recent call last):
...
RecursionError: maximum recursion depth exceeded...
>>> torch_code(MatPow(A, n))
Traceback (most recent call last):
...
TypeError: can't multiply sequence by non-int of type 'Symbol'
```

### Expected
```pycon
>>> _ = torch_code(MatPow(A, -1))
>>> _ = torch_code(MatPow(A, n))
```

### Why it is wrong
Printing must not fail for a valid expression. PyTorch has both `torch.linalg.inv` (already used for `Inverse(A)`) and `torch.linalg.matrix_power(A, n)`, which also takes negative and runtime integer exponents.

### Notes on fixing
`sympy/printing/pytorch.py:TorchPrinter._print_MatPow` builds `[expr.base]*expr.exp` and folds `torch.mm` over it. For `exp = -1` the list is empty, which (via `_expand_fold_binary_op`) ends in infinite recursion; for a symbolic `exp` the list multiplication fails. Printing `torch.linalg.matrix_power(A, n)` covers all integer exponents. The TensorFlow printer has the same code, see Related.

### Related
[tensorflow-matpow-negative-symbolic-crash](tensorflow-matpow-negative-symbolic-crash.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
