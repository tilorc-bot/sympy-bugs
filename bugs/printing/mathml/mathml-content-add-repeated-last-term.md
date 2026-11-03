# Unevaluated x**2 + y + y prints with three y terms (content MathML)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Add, mathml
>>> x, y = symbols('x y')
>>> mathml(Add(x**2, y, y, evaluate=False))
'<apply><plus/><apply><power/><ci>x</ci><cn>2</cn></apply><ci>y</ci><ci>y</ci><ci>y</ci></apply>'
```

### Expected
```pycon
>>> mathml(Add(x**2, y, y, evaluate=False)).count('<ci>y</ci>')
2
```

### Why it is wrong
The output means x² + 3y instead of x² + 2y. The same happens for `parse_expr('x**2 + y + y', evaluate=False)`.

### Notes on fixing
`MathMLContentPrinter._print_Add` (`sympy/printing/mathml.py`) detects the last term with `if arg == args[-1]`, a value comparison, so every term equal to the last one is appended a second time. Compare positions (`enumerate`) instead.

### Suggested fix
```diff
diff --git a/sympy/printing/mathml.py b/sympy/printing/mathml.py
index 02a02ac..4d869bf 100644
--- a/sympy/printing/mathml.py
+++ b/sympy/printing/mathml.py
@@ -192,7 +192,8 @@ def _print_Add(self, expr, order=None):
         args = self._as_ordered_terms(expr, order=order)
         lastProcessed = self._print(args[0])
         plusNodes = []
-        for arg in args[1:]:
+        for i, arg in enumerate(args[1:], start=1):
+            is_last = i == len(args) - 1
             if arg.could_extract_minus_sign():
                 # use minus
                 x = self.dom.createElement('apply')
@@ -201,12 +202,12 @@ def _print_Add(self, expr, order=None):
                 x.appendChild(self._print(-arg))
                 # invert expression since this is now minused
                 lastProcessed = x
-                if arg == args[-1]:
+                if is_last:
                     plusNodes.append(lastProcessed)
             else:
                 plusNodes.append(lastProcessed)
                 lastProcessed = self._print(arg)
-                if arg == args[-1]:
+                if is_last:
                     plusNodes.append(self._print(arg))
         if len(plusNodes) == 1:
             return lastProcessed
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
