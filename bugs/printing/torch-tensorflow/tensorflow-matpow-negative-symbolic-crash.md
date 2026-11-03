# tensorflow_code(MatPow(A, -1)) raises RecursionError; MatPow(A, n) raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, MatPow
>>> from sympy.printing.tensorflow import tensorflow_code
>>> n = symbols('n')
>>> A = MatrixSymbol('A', 2, 2)
>>> print(tensorflow_code(MatPow(A, 2)))
tensorflow.linalg.matmul(A, A)
>>> tensorflow_code(MatPow(A, -1))
Traceback (most recent call last):
...
RecursionError: maximum recursion depth exceeded...
>>> tensorflow_code(MatPow(A, n))
Traceback (most recent call last):
...
TypeError: can't multiply sequence by non-int of type 'Symbol'
```

### Expected
```pycon
>>> _ = tensorflow_code(MatPow(A, -1))
```

### Why it is wrong
Printing must not fail for a valid expression; `A**-1` is the matrix inverse, for which TensorFlow has `tf.linalg.inv` (already used for `Inverse(A)`). For a symbolic exponent a clear `NotImplementedError` would be expected instead of a `TypeError`.

### Notes on fixing
`sympy/printing/tensorflow.py:TensorflowPrinter._print_MatPow` builds `[expr.base]*expr.exp` and folds `matmul` over it. For `exp = -1` that list is empty, which (via `_expand_fold_binary_op`) ends in infinite recursion; for a symbolic `exp` the list multiplication fails. Negative integer exponents should print `inv(A)` (to the power `-exp`), zero the identity, and non-integer/symbolic exponents should raise a proper "not supported" error. The PyTorch printer has the same code, see Related.

### Related
[torch-matpow-negative-symbolic-crash](torch-matpow-negative-symbolic-crash.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
