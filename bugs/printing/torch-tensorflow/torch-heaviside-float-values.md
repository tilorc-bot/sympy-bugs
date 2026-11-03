# torch_code(Heaviside(x)) passes a Python number to torch.heaviside, which needs a tensor

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Heaviside
>>> from sympy.printing.pytorch import torch_code
>>> x = symbols('x')
>>> print(torch_code(Heaviside(x)))
torch.heaviside(x, 1/2)
```

### Expected
```pycon
>>> import ast
>>> def values_is_python_number(code):
...     call = ast.parse(code).body[0].value
...     arg = ast.unparse(call.args[1])
...     try:
...         return isinstance(eval(arg, {}), (int, float))
...     except NameError:
...         return False
>>> values_is_python_number(torch_code(Heaviside(x)))
False
```

### Why it is wrong
`torch.heaviside(input, values)` requires `values` to be a tensor. torch 2.15 reports `heaviside(): argument 'values' (position 2) must be Tensor, not float`, and `lambdify(x, Heaviside(x), 'torch')` fails the same way.

### Notes on fixing
`sympy/printing/pytorch.py:TorchPrinter._print_Heaviside` prints the second argument as a plain number (`Heaviside(x)` always has the second argument `1/2`, so the `"0.5"` default in that method is never used). It should wrap it, e.g. `torch.tensor(0.5, dtype=x.dtype)` or `torch.full_like(x, 0.5)`. The output is asserted by `test_torch_special_functions` in `sympy/printing/tests/test_torch.py`. `Heaviside(x, 0)` → `torch.heaviside(x, 0)` has the same problem.

The Expected block checks that the second argument is not something that evaluates to a Python number without `torch`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
