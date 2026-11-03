# True prints True, which is not an R constant (should be TRUE)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import rcode, S
>>> print(rcode(S.true))
True
>>> print(rcode(S.false))
False
```

### Expected
```pycon
>>> rcode(S.true)
'TRUE'
>>> rcode(S.false)
'FALSE'
```

### Why it is wrong
R's logical constants are `TRUE` and `FALSE` (or `T`/`F`). R 4.6 reports `object 'True' not found`.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter` has no `_print_BooleanTrue`/`_print_BooleanFalse`, so the `str()` fallback is used. The output is asserted by `test_rcode_boolean` in `sympy/printing/tests/test_rcode.py` (`rcode(True) == "True"`).

### Suggested fix
```diff
diff --git a/sympy/printing/rcode.py b/sympy/printing/rcode.py
index 3107e6e..86551ec 100644
--- a/sympy/printing/rcode.py
+++ b/sympy/printing/rcode.py
@@ -169,6 +169,12 @@ def _print_Infinity(self, expr):
     def _print_NegativeInfinity(self, expr):
         return '-Inf'
 
+    def _print_BooleanTrue(self, expr):
+        return 'TRUE'
+
+    def _print_BooleanFalse(self, expr):
+        return 'FALSE'
+
     def _print_Assignment(self, expr):
         from sympy.codegen.ast import Assignment
 
diff --git a/sympy/printing/tests/test_rcode.py b/sympy/printing/tests/test_rcode.py
index 1443cc1..0c84d45 100644
--- a/sympy/printing/tests/test_rcode.py
+++ b/sympy/printing/tests/test_rcode.py
@@ -123,10 +123,10 @@ def test_rcode_user_functions():
 
 
 def test_rcode_boolean():
-    assert rcode(True) == "True"
-    assert rcode(S.true) == "True"
-    assert rcode(False) == "False"
-    assert rcode(S.false) == "False"
+    assert rcode(True) == "TRUE"
+    assert rcode(S.true) == "TRUE"
+    assert rcode(False) == "FALSE"
+    assert rcode(S.false) == "FALSE"
     assert rcode(x & y) == "x & y"
     assert rcode(x | y) == "x | y"
     assert rcode(~x) == "!x"
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
