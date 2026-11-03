# A power of a Float in scientific notation prints as {2.5 \cdot 10^{20}}^{2}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Float, Pow, symbols, latex
>>> x = symbols('x')
>>> print(latex(Pow(Float('2.5e20'), 2, evaluate=False)))
{2.5 \cdot 10^{20}}^{2}
>>> print(latex(Float('1.453e4500')**x))
{1.453 \cdot 10^{4500}}^{x}
```

### Expected
```pycon
>>> r'\left(2.5 \cdot 10^{20}\right)' in latex(Pow(Float('2.5e20'), 2, evaluate=False))
True
```

### Why it is wrong
Braces are invisible in the rendered output, so it shows `2.5 · 10^{20}` followed by a second superscript, which reads as `2.5 · (10^{20})^{2}` (stacked scripts), not `(2.5 · 10^{20})^{2}`.

### Related
[sympy/sympy#21159](https://redirect.github.com/sympy/sympy/issues/21159)

### Notes on fixing
`LatexPrinter._helper_print_standard_power` (`sympy/printing/latex.py`) wraps every Float base in `{...}`. A Float that prints in scientific notation (`\cdot 10^{...}` / `\times 10^{...}`) is a product and needs `\left(...\right)`; plain Floats can keep the braces.

Tested-buggy: `test_Pow` in `sympy/printing/tests/test_latex.py` asserts `latex(S('1.453e4500')**x) == r'{1.453 \cdot 10^{4500}}^{x}'`.

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..fd287d6 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -728,7 +728,11 @@ def _helper_print_standard_power(self, expr, template: str) -> str:
         if expr.base.is_Symbol:
             base = self.parenthesize_super(base)
         elif expr.base.is_Float:
-            base = r"{%s}" % base
+            # scientific notation is a product: 2.5 \cdot 10^{20}
+            if '^' in base and not base.startswith(r'\left('):
+                base = self._add_parens(base)
+            else:
+                base = r"{%s}" % base
         elif (isinstance(expr.base, Derivative)
             and base.startswith(r'\left(')
             and re.match(r'\\left\(\\d?d?dot', base)
diff --git a/sympy/printing/tests/test_latex.py b/sympy/printing/tests/test_latex.py
index 31bd0af..cd59bab 100644
--- a/sympy/printing/tests/test_latex.py
+++ b/sympy/printing/tests/test_latex.py
@@ -2570,7 +2570,7 @@ def test_Pow():
     x2 = Symbol(r'x^2')
     assert latex(x2**2) == r'\left(x^{2}\right)^{2}'
     # Issue 11011
-    assert latex(S('1.453e4500')**x) == r'{1.453 \cdot 10^{4500}}^{x}'
+    assert latex(S('1.453e4500')**x) == r'\left(1.453 \cdot 10^{4500}\right)^{x}'
 
 
 def test_issue_7180():
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
