# A DMP (Poly.rep) raises AttributeError

### Kind
crash

### Actual
```pycon
>>> from sympy import Poly, latex, symbols
>>> x = symbols('x')
>>> latex(Poly(x**2 + 1, x).rep)
Traceback (most recent call last):
...
AttributeError: '...' object has no attribute 'ring'
```

### Expected
```pycon
>>> _ = latex(Poly(x**2 + 1, x).rep)
```

### Why it is wrong
`str` and `repr` of the same object work; the LaTeX printer (and hence notebook display of a `Poly.rep`) crashes instead of falling back to something printable.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_DMP` reads `p.ring`, an attribute the current `DMP` classes (`DMP_Python`, `DUP_Flint`) no longer have, and only catches `SympifyError`. It should use `getattr(p, 'ring', None)` and fall back to `repr(p)`. `_print_DMF` delegates to it. The pretty printer has the same bug (reported separately).

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..898ffdb 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -2685,9 +2685,10 @@ def _print_InverseCosineTransform(self, expr):
 
     def _print_DMP(self, p):
         try:
-            if p.ring is not None:
+            ring = getattr(p, 'ring', None)
+            if ring is not None:
                 # TODO incorporate order
-                return self._print(p.ring.to_sympy(p))
+                return self._print(ring.to_sympy(p))
         except SympifyError:
             pass
         return self._print(repr(p))
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
