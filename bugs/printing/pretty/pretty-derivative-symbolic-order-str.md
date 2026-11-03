# pretty() prints a symbolic derivative order with str(): Derivative(f(x), (x, n**2)) shows d**n**2

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative, pretty
>>> x, n = symbols('x n')
>>> f = Function('f')
>>> print(pretty(Derivative(f(x), (x, n**2)), use_unicode=True))
 n**2
d
──────(f(x))
  n**2
dx
```

### Expected
```pycon
>>> '**' in pretty(Derivative(f(x), (x, n**2)), use_unicode=True)
False
```

### Why it is wrong
The exponent is shown in Python syntax `n**2` inside a two-dimensional picture, where `n²` is expected.

### Notes on fixing
`PrettyPrinter._print_Derivative` in `sympy/printing/pretty/pretty.py` builds both exponents with `prettyForm(str(num))` and `prettyForm(str(count_total_deriv))` instead of `self._print(...)`.

### Suggested fix
```diff
diff --git a/sympy/printing/pretty/pretty.py b/sympy/printing/pretty/pretty.py
index 4fa9b26..69fbff2 100644
--- a/sympy/printing/pretty/pretty.py
+++ b/sympy/printing/pretty/pretty.py
@@ -347,7 +347,7 @@ def _print_Derivative(self, deriv):
             count_total_deriv += num
 
             if (not num.is_Integer) or (num > 1):
-                ds = ds**prettyForm(str(num))
+                ds = ds**self._print(num)
 
             if x is None:
                 x = ds
@@ -361,7 +361,7 @@ def _print_Derivative(self, deriv):
         pform = prettyForm(deriv_symbol)
 
         if (count_total_deriv > 1) != False:
-            pform = pform**prettyForm(str(count_total_deriv))
+            pform = pform**self._print(count_total_deriv)
 
         pform = prettyForm(*pform.below(stringPict.LINE, x))
         pform.baseline = pform.baseline + 1
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
