# torch_code(A.T) for a square matrix prints torch.transpose(A).t(), which needs two dimension arguments

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol
>>> from sympy.printing.pytorch import torch_code
>>> A = MatrixSymbol('A', 2, 2)
>>> print(torch_code(A.T))
torch.transpose(A).t()
```

### Expected
```pycon
>>> 'torch.transpose(A)' in torch_code(A.T)
False
```

### Why it is wrong
`torch.transpose(input, dim0, dim1)` requires both dimensions, so `torch.transpose(A)` raises `TypeError` at run time; even with dimensions, the trailing `.t()` would transpose the matrix back. The correct code is `A.t()` (or `torch.transpose(A, 0, 1)`). The reviewer checked this against the PyTorch documentation (torch was not run).

### Notes on fixing
`sympy/printing/pytorch.py:TorchPrinter._print_Transpose` returns `"torch.transpose(%s).t()"` for square matrices. It should return `"%s.t()"` (with the argument parenthesized as needed). The non-square branch `permute` is reversed as a string (`"0, 1"[::-1]` gives `"1 ,0"`), which happens to work only for two dimensions.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
