# divisor_sigma(n, k + 1) prints the subscript without braces: \sigma_k + 1\left(n\right)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.functions.combinatorial.numbers import divisor_sigma
>>> n, k = symbols('n k')
>>> print(latex(divisor_sigma(n, k + 1)))
\sigma_k + 1\left(n\right)
>>> print(latex(divisor_sigma(n, 10)))
\sigma_10\left(n\right)
```

### Expected
```pycon
>>> print(latex(divisor_sigma(n, 10)))
\sigma_{10}\left(n\right)
>>> print(latex(divisor_sigma(n, k + 1)))
\sigma_{k + 1}\left(n\right)
```

### Why it is wrong
A TeX subscript without braces takes one token, so `\sigma_10(n)` renders as `σ₁ 0(n)` and `\sigma_k + 1(n)` as `σ_k + 1(n)`.

### Notes on fixing
`LatexPrinter._print_divisor_sigma` (`sympy/printing/latex.py`) uses the template `r"_%s\left(%s\right)"`; it needs `_{%s}`. The tests in `test_latex_functions` (`sympy/printing/tests/test_latex.py`) that assert `\sigma_y\left(x\right)` and `\sigma^{2}_y\left(x\right)` have to be updated with it. `_print_udivisor_sigma` has the same bug (separate issue).

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..5d2e9ad 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -2989,7 +2989,7 @@ def _print_reduced_totient(self, expr, exp=None):
 
     def _print_divisor_sigma(self, expr, exp=None):
         if len(expr.args) == 2:
-            tex = r"_%s\left(%s\right)" % tuple(map(self._print,
+            tex = r"_{%s}\left(%s\right)" % tuple(map(self._print,
                                                 (expr.args[1], expr.args[0])))
         else:
             tex = r"\left(%s\right)" % self._print(expr.args[0])
diff --git a/sympy/printing/tests/test_latex.py b/sympy/printing/tests/test_latex.py
index 31bd0af..977c599 100644
--- a/sympy/printing/tests/test_latex.py
+++ b/sympy/printing/tests/test_latex.py
@@ -793,8 +793,8 @@ def test_latex_functions():
 
     assert latex(divisor_sigma(x)) == r"\sigma\left(x\right)"
     assert latex(divisor_sigma(x)**2) == r"\sigma^{2}\left(x\right)"
-    assert latex(divisor_sigma(x, y)) == r"\sigma_y\left(x\right)"
-    assert latex(divisor_sigma(x, y)**2) == r"\sigma^{2}_y\left(x\right)"
+    assert latex(divisor_sigma(x, y)) == r"\sigma_{y}\left(x\right)"
+    assert latex(divisor_sigma(x, y)**2) == r"\sigma^{2}_{y}\left(x\right)"
 
     assert latex(udivisor_sigma(x)) == r"\sigma^*\left(x\right)"
     assert latex(udivisor_sigma(x)**2) == r"\sigma^*^{2}\left(x\right)"
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
