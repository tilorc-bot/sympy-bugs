# The multiplication sign is dropped in A*B*A for noncommutative symbols (presentation MathML)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, mathml
>>> A, B = symbols('A B', commutative=False)
>>> mathml(A*B*A, printer='presentation', mul_symbol='dot')
'<mrow><mi>A</mi><mi>B</mi><mo>&#xB7;</mo><mi>A</mi></mrow>'
```

### Expected
```pycon
>>> mathml(A*B*A, printer='presentation', mul_symbol='dot').count('<mo>&#xB7;</mo>')
2
```

### Why it is wrong
The first product A·B gets no operator at all while B·A does, so the requested `mul_symbol` is applied inconsistently. With the default `mul_symbol` the invisible-times operator is dropped in the same place.

### Notes on fixing
`MathMLPresentationPrinter._print_Mul` (`sympy/printing/mathml.py`) adds the operator after a factor only `if not term == terms[-1]`, a value comparison; since `A` is also the last factor, no operator follows the first `A`. Compare positions instead.

### Suggested fix
```diff
diff --git a/sympy/printing/mathml.py b/sympy/printing/mathml.py
index 02a02ac..521fb49 100644
--- a/sympy/printing/mathml.py
+++ b/sympy/printing/mathml.py
@@ -721,9 +721,9 @@ def multiply(expr, mrow):
                 y.appendChild(self.dom.createTextNode(self.mathml_tag(expr)))
                 mrow.appendChild(x)
                 mrow.appendChild(y)
-            for term in terms:
+            for i, term in enumerate(terms):
                 mrow.appendChild(self.parenthesize(term, PRECEDENCE['Mul']))
-                if not term == terms[-1]:
+                if i != len(terms) - 1:
                     y = self.dom.createElement('mo')
                     y.appendChild(self.dom.createTextNode(self.mathml_tag(expr)))
                     mrow.appendChild(y)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
