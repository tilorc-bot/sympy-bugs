# pretty() does not parenthesize a MatAdd inside HadamardPower or DotProduct

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import MatrixSymbol, HadamardPower, pretty
>>> from sympy.matrices.expressions.dotproduct import DotProduct
>>> A, B = MatrixSymbol('A', 2, 2), MatrixSymbol('B', 2, 2)
>>> u, v, w = MatrixSymbol('u', 3, 1), MatrixSymbol('v', 3, 1), MatrixSymbol('w', 3, 1)
>>> print(pretty(HadamardPower(A + B, 2), use_unicode=True))
     ∘2
A + B
>>> print(pretty(DotProduct(v + w, u), use_unicode=True))
v + w⋅u
```

### Expected
```pycon
>>> '(A + B)' in pretty(HadamardPower(A + B, 2), use_unicode=True)
True
>>> '(v + w)' in pretty(DotProduct(v + w, u), use_unicode=True)
True
```

### Why it is wrong
The pictures read as `A + B∘²` and `v + w⋅u`, so the power and the dot product apply only to the last term of the sum.

### Caused by
[rc-pretty-composite-atom-binding](rc-pretty-composite-atom-binding.md)

### Notes on fixing
`PrettyPrinter._print_MatAdd` in `sympy/printing/pretty/pretty.py` builds its result with `stringPict.next` and never sets `binding=prettyForm.ADD`, so `prettyForm.__pow__` (used by `_print_HadamardPower`) and `prettyForm.__mul__` (used by `_print_DotProduct`) see an ATOM and add no parentheses. Printers that parenthesize matrix expressions explicitly (`_print_MatMul`, `_print_MatPow`, `_print_Transpose`) are not affected.

### Suggested fix
```diff
diff --git a/sympy/printing/pretty/pretty.py b/sympy/printing/pretty/pretty.py
index 4fa9b26..fb6dbc2 100644
--- a/sympy/printing/pretty/pretty.py
+++ b/sympy/printing/pretty/pretty.py
@@ -911,7 +911,8 @@ def _print_MatAdd(self, expr):
                 else:
                     s = prettyForm(*stringPict.next(s, ' + '))
                 s = prettyForm(*stringPict.next(s, pform))
-
+        if len(expr.args) > 1:
+            s.binding = prettyForm.ADD
         return s
 
     def _print_MatMul(self, expr):
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
