# A direct sum raised to a tensor power is not parenthesized: (C² ⊕ F)^⨂3 prints as C² ⊕ F^⨂3

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.physics.quantum.hilbert import ComplexSpace, FockSpace
>>> print(pretty((ComplexSpace(2) + FockSpace())**3, use_unicode=True))
      ⨂3
 2
C  ⊕ F
```

### Expected
```pycon
>>> p = pretty((ComplexSpace(2) + FockSpace())**3, use_unicode=True)
>>> '(' in p or '⎛' in p
True
```

### Why it is wrong
The picture reads as `C² ⊕ F^⨂3`, the direct sum of `C²` with the third tensor power of `F`, instead of the third tensor power of the direct sum.

### Notes on fixing
`TensorPowerHilbertSpace._pretty` in `sympy/physics/quantum/hilbert.py` returns `pform_base**pform_exp` without parenthesizing the base; `DirectSumHilbertSpace._pretty` and `TensorProductHilbertSpace._pretty` return pictures with ATOM binding, so `prettyForm.__pow__` adds nothing. The base needs parentheses when it is a `DirectSumHilbertSpace` or `TensorProductHilbertSpace` (as `DirectSumHilbertSpace._pretty` already does for its own arguments); `(ComplexSpace(2)*FockSpace())**3` is affected the same way. `str()` has the same problem (`C(2)+F**3`, `_sympystr`).

### Suggested fix
```diff
diff --git a/sympy/physics/quantum/hilbert.py b/sympy/physics/quantum/hilbert.py
index 0c59f65..c8e9741 100644
--- a/sympy/physics/quantum/hilbert.py
+++ b/sympy/physics/quantum/hilbert.py
@@ -646,6 +646,9 @@ def _pretty(self, printer, *args):
         else:
             pform_exp = prettyForm(*pform_exp.left(prettyForm('x')))
         pform_base = printer._print(self.base, *args)
+        if isinstance(self.base, (DirectSumHilbertSpace,
+                                  TensorProductHilbertSpace)):
+            pform_base = prettyForm(*pform_base.parens())
         return pform_base**pform_exp
 
     def _latex(self, printer, *args):
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
