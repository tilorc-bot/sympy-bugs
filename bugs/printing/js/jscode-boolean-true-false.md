# jscode(S.true) prints Python's `True` instead of JavaScript's `true`

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import S
>>> from sympy.printing.jscode import jscode
>>> print(jscode(S.true))
True
>>> print(jscode(S.false))
False
```

### Expected
```pycon
>>> jscode(S.true), jscode(S.false)
('true', 'false')
```

### Why it is wrong
JavaScript's boolean literals are lowercase; `True` is an undefined identifier (ReferenceError at run time). The original reviewer ran this with node; it was not executed here.

### Notes on fixing
`sympy/printing/jscode.py:JavascriptCodePrinter` has no `_print_BooleanTrue`/`_print_BooleanFalse`, so the `StrPrinter` versions are used. The C printer has them.

### Suggested fix
```diff
diff --git a/sympy/printing/jscode.py b/sympy/printing/jscode.py
index 390e5df..b20f77d 100644
--- a/sympy/printing/jscode.py
+++ b/sympy/printing/jscode.py
@@ -142,6 +142,12 @@ def _print_Indexed(self, expr):
             offset *= dims[i]
         return "%s[%s]" % (self._print(expr.base.label), self._print(elem))
 
+    def _print_BooleanTrue(self, expr):
+        return 'true'
+
+    def _print_BooleanFalse(self, expr):
+        return 'false'
+
     def _print_Exp1(self, expr):
         return "Math.E"
 
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
