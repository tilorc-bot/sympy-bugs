# torch_code(log(2)) prints torch.log(2), which raises TypeError because torch functions need tensors

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, log, sqrt
>>> from sympy.printing.pytorch import torch_code
>>> x = symbols('x')
>>> print(torch_code(log(2)*x))
x*torch.log(2)
>>> print(torch_code(sqrt(3)))
torch.sqrt(3)
```

### Expected
```pycon
>>> 'torch.log(2)' in torch_code(log(2)*x)
False
>>> 'torch.sqrt(3)' in torch_code(sqrt(3))
False
```

### Why it is wrong
`torch.log`, `torch.sqrt`, ... only accept tensors; with a Python number they raise `TypeError: log(): argument 'input' must be Tensor, not int`. Constant subexpressions such as `log(2)` and `sqrt(3)` must be printed as numbers (`math.log(2)`, a float literal) or wrapped in `torch.tensor(...)`. The reviewer checked this against the PyTorch documentation (torch was not run).

### Notes on fixing
`sympy/printing/pytorch.py:TorchPrinter` maps functions to `torch.*` through `known_functions` (`_print_Function`) and powers through `_print_Pow` (`torch.sqrt`), without looking at whether the argument is a number. Number-only arguments should be printed with `math` (as `PythonCodePrinter` does) or converted to tensors. Both paths need the change.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
