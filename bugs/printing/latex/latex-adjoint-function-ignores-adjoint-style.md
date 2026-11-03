# adjoint_style is ignored for adjoint() and Dagger()

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import Symbol, adjoint, latex
>>> from sympy.physics.quantum import Dagger, Operator
>>> X = Symbol('X', commutative=False)
>>> print(latex(adjoint(X), adjoint_style='star'))
X^{\dagger}
>>> print(latex(Dagger(Operator('O')), adjoint_style='hermitian'))
O^{\dagger}
```

### Expected
```pycon
>>> r'\dagger' in latex(adjoint(X), adjoint_style='star')
False
>>> r'\dagger' in latex(Dagger(Operator('O')), adjoint_style='hermitian')
False
```

### Why it is wrong
`adjoint_style` is documented as the symbol used for the adjoint, but only the matrix `Adjoint` honours it; the scalar/operator `adjoint` function (and its subclass `Dagger`) always prints `\dagger`, so a document mixing both gets two notations.

### Notes on fixing
`sympy/functions/elementary/complexes.py:adjoint._latex` hard-codes `^{\dagger}` instead of reading `printer._settings['adjoint_style']` like `sympy/printing/latex.py:LatexPrinter._print_Adjoint`. The style table could be shared between the two.

### Suggested fix
```diff
diff --git a/sympy/functions/elementary/complexes.py b/sympy/functions/elementary/complexes.py
index 4a98063..f0d8f5c 100644
--- a/sympy/functions/elementary/complexes.py
+++ b/sympy/functions/elementary/complexes.py
@@ -1022,7 +1022,9 @@ def _eval_transpose(self):
 
     def _latex(self, printer, exp=None, *args):
         arg = printer._print(self.args[0])
-        tex = r'%s^{\dagger}' % arg
+        style = {"star": r"\ast", "hermitian": r"\mathsf{H}"}.get(
+            printer._settings.get("adjoint_style"), r"\dagger")
+        tex = r'%s^{%s}' % (arg, style)
         if exp:
             tex = r'\left(%s\right)^{%s}' % (tex, exp)
         return tex
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
