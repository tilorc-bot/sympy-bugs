# udivisor_sigma(n)**2 gives a double superscript (\sigma^*^{2})

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.functions.combinatorial.numbers import udivisor_sigma
>>> n, k = symbols('n k')
>>> print(latex(udivisor_sigma(n)**2))
\sigma^*^{2}\left(n\right)
>>> print(latex(udivisor_sigma(n, k)**2))
\sigma^*^{2}_k\left(n\right)
```

### Expected
```pycon
>>> '^*^' in latex(udivisor_sigma(n)**2), '^*^' in latex(udivisor_sigma(n, k)**2)
(False, False)
```

### Why it is wrong
`\sigma^*^{2}` is a TeX "Double superscript" error, so any power of `udivisor_sigma` does not compile.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_udivisor_sigma` returns `r"\sigma^*^{%s}%s"` when called with `exp`. The star must be grouped, e.g. `{\sigma^*}^{2}`. This is tested-buggy: `sympy/printing/tests/test_latex.py:test_latex_functions` asserts `\sigma^*^{2}\left(x\right)` and `\sigma^*^{2}_y\left(x\right)`.

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..04073fb 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -3004,7 +3004,7 @@ def _print_udivisor_sigma(self, expr, exp=None):
         else:
             tex = r"\left(%s\right)" % self._print(expr.args[0])
         if exp is not None:
-            return r"\sigma^*^{%s}%s" % (exp, tex)
+            return r"{\sigma^*}^{%s}%s" % (exp, tex)
         return r"\sigma^*%s" % tex
 
     def _print_primenu(self, expr, exp=None):
diff --git a/sympy/printing/tests/test_latex.py b/sympy/printing/tests/test_latex.py
index 31bd0af..06a5ffe 100644
--- a/sympy/printing/tests/test_latex.py
+++ b/sympy/printing/tests/test_latex.py
@@ -797,9 +797,9 @@ def test_latex_functions():
     assert latex(divisor_sigma(x, y)**2) == r"\sigma^{2}_y\left(x\right)"
 
     assert latex(udivisor_sigma(x)) == r"\sigma^*\left(x\right)"
-    assert latex(udivisor_sigma(x)**2) == r"\sigma^*^{2}\left(x\right)"
+    assert latex(udivisor_sigma(x)**2) == r"{\sigma^*}^{2}\left(x\right)"
     assert latex(udivisor_sigma(x, y)) == r"\sigma^*_y\left(x\right)"
-    assert latex(udivisor_sigma(x, y)**2) == r"\sigma^*^{2}_y\left(x\right)"
+    assert latex(udivisor_sigma(x, y)**2) == r"{\sigma^*}^{2}_y\left(x\right)"
 
     assert latex(primenu(n)) == r'\nu\left(n\right)'
     assert latex(primenu(n) ** 2) == r'\left(\nu\left(n\right)\right)^{2}'
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
