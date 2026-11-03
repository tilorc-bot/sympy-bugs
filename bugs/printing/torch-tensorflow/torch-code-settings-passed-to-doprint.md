# torch_code(expr, strict=False) raises TypeError: settings are passed to doprint()

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.printing.pytorch import torch_code
>>> x = symbols('x')
>>> torch_code(x, strict=False)
Traceback (most recent call last):
...
TypeError: ...doprint() got an unexpected keyword argument 'strict'
```

### Why it is wrong
`torch_code(expr, **settings)` accepts printer settings like the other `*_code` functions, but every printer setting (`strict`, `fully_qualified_modules`, `user_functions`, ...) makes it fail.

### Notes on fixing
`sympy/printing/pytorch.py:torch_code` builds `TorchPrinter(settings={'requires_grad': ..., 'dtype': ...})` and then calls `printer.doprint(expr, **settings)`. The settings belong in the printer constructor: `TorchPrinter(settings={'requires_grad': requires_grad, 'dtype': dtype, **settings})` and `printer.doprint(expr)`.

### Suggested fix
```diff
diff --git a/sympy/printing/pytorch.py b/sympy/printing/pytorch.py
index 62da8fb..11048de 100644
--- a/sympy/printing/pytorch.py
+++ b/sympy/printing/pytorch.py
@@ -294,5 +294,5 @@ def _print_polygamma(self, expr):
     _zeros = "zeros"
 
 def torch_code(expr, requires_grad=False, dtype="torch.float64", **settings):
-    printer = TorchPrinter(settings={'requires_grad': requires_grad, 'dtype': dtype})
-    return printer.doprint(expr, **settings)
+    printer = TorchPrinter(settings={'requires_grad': requires_grad, 'dtype': dtype, **settings})
+    return printer.doprint(expr)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
