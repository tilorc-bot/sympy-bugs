# use_unicode=False garbles a SingularityFunction whose shift is more than one line high

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, SingularityFunction, pretty
>>> x, a, b, n = symbols('x a b n')
>>> print(pretty(SingularityFunction(x, a/b, n), use_unicode=False))
                         n
<  a     - - + x   b    >
```

### Expected
```pycon
>>> pretty(SingularityFunction(x, a/b, n), use_unicode=False) == pretty(SingularityFunction(x, a/b, n), use_unicode=True).replace('─', '-')
True
```

### Why it is wrong
The three lines of the fraction `-a/b + x` are laid out side by side, so the output reads `a - - + x b` and is not a picture of the expression at all. The Unicode output is correct:
```
         n
   a
<- ─ + x>
   b
```

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_SingularityFunction`: the ASCII branch calls `self._print_seq(shift, "<", ">", ' ')` with `shift` a `prettyForm`, so `_print_seq` iterates over its lines and joins them horizontally with spaces. The Unicode branch (building `<`, shift, `>` with `prettyForm.right`) contains nothing Unicode-specific and can be used for both.

### Suggested fix
```diff
diff --git a/sympy/printing/pretty/pretty.py b/sympy/printing/pretty/pretty.py
index 4fa9b26..12b6c18 100644
--- a/sympy/printing/pretty/pretty.py
+++ b/sympy/printing/pretty/pretty.py
@@ -1821,19 +1821,12 @@ def _print_Order(self, expr):
         return pform
 
     def _print_SingularityFunction(self, e):
-        if self._use_unicode:
-            shift = self._print(e.args[0]-e.args[1])
-            n = self._print(e.args[2])
-            base = prettyForm("<")
-            base = prettyForm(*base.right(shift))
-            base = prettyForm(*base.right(">"))
-            pform = base**n
-            return pform
-        else:
-            n = self._print(e.args[2])
-            shift = self._print(e.args[0]-e.args[1])
-            base = self._print_seq(shift, "<", ">", ' ')
-            return base**n
+        shift = self._print(e.args[0]-e.args[1])
+        n = self._print(e.args[2])
+        base = prettyForm("<")
+        base = prettyForm(*base.right(shift))
+        base = prettyForm(*base.right(">"))
+        return base**n
 
     def _print_beta(self, e):
         func_name = greek_unicode['Beta'] if self._use_unicode else 'B'
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
