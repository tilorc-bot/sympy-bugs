# x/y*A(i) prints the tensor coefficient as x\frac{1}{y}

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.tensor.tensor import TensorIndexType, tensor_indices, TensorHead
>>> x, y = symbols('x y')
>>> L = TensorIndexType('L')
>>> i = tensor_indices('i', L)
>>> A = TensorHead('A', [L])
>>> print(latex(x/y*A(i)))
x\frac{1}{y}A{}^{i}
```

### Expected
```pycon
>>> r'\frac{1}{y}' in latex(x/y*A(i))
False
```

### Why it is wrong
The coefficient `x/y` is split into the factors `x` and `1/y`, printed side by side with no space, instead of `\frac{x}{y}`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_TensMul` concatenates the parenthesized results of `expr._get_args_for_traditional_printer()`, which returns the factors of the coefficient separately; the scalar coefficient should be printed as one `Mul`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
