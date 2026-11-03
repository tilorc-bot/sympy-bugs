# torch_code(gamma(x)) prints torch.special.gamma(x), which does not exist

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, gamma
>>> from sympy.printing.pytorch import torch_code
>>> x = symbols('x')
>>> print(torch_code(gamma(x)))
torch.special.gamma(x)
```

### Expected
```pycon
>>> 'torch.special.gamma(' in torch_code(gamma(x))
False
```

### Why it is wrong
`torch.special` has `gammaln`, `digamma`, `polygamma`, `multigammaln`, `gammainc`, ... but no `gamma`, so the generated code raises `AttributeError`. The gamma function can be computed as `torch.exp(torch.lgamma(x))` (with the sign handled for negative arguments, e.g. via `torch.special.gammaln` and the reflection formula). The reviewer checked this against the PyTorch documentation (torch was not run).

### Notes on fixing
`sympy/printing/pytorch.py:TorchPrinter._print_gamma`. The current output is asserted by `test_torch_special_functions` in `sympy/printing/tests/test_torch.py` (`"torch.special.gamma(x)"` and `"torch.special.gamma(torch.sin(x))"`, tested-buggy).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
