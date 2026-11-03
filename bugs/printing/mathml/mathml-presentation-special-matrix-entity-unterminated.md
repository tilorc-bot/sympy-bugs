# Presentation MathML of ZeroMatrix and OneMatrix has a character reference without ";"

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import ZeroMatrix, OneMatrix, mathml
>>> from xml.dom.minidom import parseString
>>> mathml(ZeroMatrix(2, 2), printer='presentation')
'<mn>&#x1D7D8</mn>'
>>> mathml(OneMatrix(2, 2), printer='presentation')
'<mn>&#x1D7D9</mn>'
```

### Expected
```pycon
>>> _ = parseString(mathml(ZeroMatrix(2, 2), printer='presentation'))
>>> _ = parseString(mathml(OneMatrix(2, 2), printer='presentation'))
```

### Why it is wrong
An XML character reference must end with `;`; without it the document is not well-formed.

### Notes on fixing
`MathMLPresentationPrinter._print_ZeroMatrix` and `_print_OneMatrix` (`sympy/printing/mathml.py`) use `'&#x1D7D8'` / `'&#x1D7D9'`; `_print_Identity` next to them correctly has `'&#x1D540;'`.
`test_mathml_special_matrices` in `sympy/printing/tests/test_mathml.py` asserts the broken strings, so it must be updated.

### Suggested fix
```diff
diff --git a/sympy/printing/mathml.py b/sympy/printing/mathml.py
index 02a02ac..ddec6b4 100644
--- a/sympy/printing/mathml.py
+++ b/sympy/printing/mathml.py
@@ -1867,12 +1867,12 @@ def _print_HadamardProduct(self, expr):
 
     def _print_ZeroMatrix(self, Z):
         x = self.dom.createElement('mn')
-        x.appendChild(self.dom.createTextNode('&#x1D7D8'))
+        x.appendChild(self.dom.createTextNode('&#x1D7D8;'))
         return x
 
     def _print_OneMatrix(self, Z):
         x = self.dom.createElement('mn')
-        x.appendChild(self.dom.createTextNode('&#x1D7D9'))
+        x.appendChild(self.dom.createTextNode('&#x1D7D9;'))
         return x
 
     def _print_Identity(self, I):
diff --git a/sympy/printing/tests/test_mathml.py b/sympy/printing/tests/test_mathml.py
index 033f423..3de0d94 100644
--- a/sympy/printing/tests/test_mathml.py
+++ b/sympy/printing/tests/test_mathml.py
@@ -2007,8 +2007,8 @@ def test_mathml_matrix_functions():
 def test_mathml_special_matrices():
     from sympy.matrices import Identity, ZeroMatrix, OneMatrix
     assert mathml(Identity(4), printer='presentation') == '<mi>&#x1D540;</mi>'
-    assert mathml(ZeroMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D8</mn>'
-    assert mathml(OneMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D9</mn>'
+    assert mathml(ZeroMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D8;</mn>'
+    assert mathml(OneMatrix(2, 2), printer='presentation') == '<mn>&#x1D7D9;</mn>'
 
 def test_mathml_piecewise():
     from sympy.functions.elementary.piecewise import Piecewise
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
