# The Limit direction marker attaches to the last term of the limit point: x \to a + b^+

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, Limit, latex
>>> x, a, b = symbols('x a b')
>>> f = Function('f')
>>> print(latex(Limit(f(x), x, a + b)))
\lim_{x \to a + b^+} f{\left(x \right)}
>>> print(latex(Limit(f(x), x, -a)))
\lim_{x \to - a^+} f{\left(x \right)}
```

### Expected
```pycon
>>> 'b^+' in latex(Limit(f(x), x, a + b))
False
>>> 'a^+' in latex(Limit(f(x), x, -a))
False
```

### Why it is wrong
`a + b^+` says that `x` tends to `a` plus (`b` from the right), not to `a + b` from the right; `- a^+` likewise reads as the negative of `a^+`, i.e. approaching `-a` from the left.

### Related
[sympy/sympy#8175](https://redirect.github.com/sympy/sympy/issues/8175)
[pretty-limit-direction-glued-to-point](../pretty/pretty-limit-direction-glued-to-point.md)
### Notes on fixing
`LatexPrinter._print_Limit` (`sympy/printing/latex.py`) formats the point as `"%s^%s" % (self._print(z0), self._print(dir))`; the point needs brackets (or braces/a different notation such as `(a + b)^{+}`) whenever it is not an atom. [sympy/sympy#8175](https://redirect.github.com/sympy/sympy/issues/8175) was closed when the direction started being printed, but the placement is still wrong.

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..11cb4ba 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -922,7 +922,8 @@ def _print_Limit(self, expr):
         if str(dir) == '+-' or z0 in (S.Infinity, S.NegativeInfinity):
             tex += r"%s}" % self._print(z0)
         else:
-            tex += r"%s^%s}" % (self._print(z0), self._print(dir))
+            tex += r"%s^%s}" % (self.parenthesize(z0, PRECEDENCE['Pow']),
+                                self._print(dir))
 
         if isinstance(e, AssocOp):
             return r"%s\left(%s\right)" % (tex, self._print(e))
diff --git a/sympy/printing/pretty/pretty.py b/sympy/printing/pretty/pretty.py
index 4fa9b26..b17db72 100644
--- a/sympy/printing/pretty/pretty.py
+++ b/sympy/printing/pretty/pretty.py
@@ -677,14 +677,17 @@ def _print_Limit(self, l):
             LimArg = prettyForm(*LimArg.right(f"{xobj('-', 1)}{pretty_atom('Arrow')}"))
         else:
             LimArg = prettyForm(*LimArg.right('->'))
-        LimArg = prettyForm(*LimArg.right(self._print(z0)))
+        z0_pform = self._print(z0)
 
         if str(dir) == '+-' or z0 in (S.Infinity, S.NegativeInfinity):
             dir = ""
         else:
+            if precedence(z0) <= PRECEDENCE["Pow"]:
+                z0_pform = prettyForm(*z0_pform.parens())
             if self._use_unicode:
                 dir = pretty_atom('SuperscriptPlus') if str(dir) == "+" else pretty_atom('SuperscriptMinus')
 
+        LimArg = prettyForm(*LimArg.right(z0_pform))
         LimArg = prettyForm(*LimArg.right(self._print(dir)))
 
         Lim = prettyForm(*Lim.below(LimArg))
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
