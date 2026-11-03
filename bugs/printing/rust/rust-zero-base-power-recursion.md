# rust_code(0**x) raises RecursionError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, rust_code
>>> x = symbols('x')
>>> rust_code(0**x)
Traceback (most recent call last):
...
RecursionError: maximum recursion depth exceeded...
```

### Why it is wrong
Printing must not fail for a valid expression.

### Notes on fixing
`sympy/printing/rust.py:RustCodePrinter._print_Pow` replaces an integer base by `Float(base)` and prints the new power again. `Float(0).is_integer` is `True` (a nonzero `Float` gives `None`), so `0.0**x` takes the same branch forever. The check should skip bases that are already `Float`s. Not covered by a test.

### Suggested fix
```diff
diff --git a/sympy/printing/rust.py b/sympy/printing/rust.py
index d1719b5..f34ca27 100644
--- a/sympy/printing/rust.py
+++ b/sympy/printing/rust.py
@@ -413,7 +413,7 @@ def _print_Add(self, expr, order=None):
         return super()._print_Add(expr, order)
 
     def _print_Pow(self, expr):
-        if expr.base.is_integer and not expr.exp.is_integer:
+        if expr.base.is_integer and not expr.base.is_Float and not expr.exp.is_integer:
             expr = type(expr)(Float(expr.base), expr.exp)
             return self._print(expr)
         return self._print_Function(expr)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
