# pretty() does not parenthesize the modulus of Mod: Mod(x, y + z) prints as x mod y + z

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mod, pretty
>>> x, y, z = symbols('x y z')
>>> print(pretty(Mod(x, y + z), use_unicode=True))
x mod y + z
>>> print(pretty(Mod(x, Mod(y, z)), use_unicode=True))
x mod y mod z
```

### Expected
```pycon
>>> '(y + z)' in pretty(Mod(x, y + z), use_unicode=True)
True
>>> '(y mod z)' in pretty(Mod(x, Mod(y, z)), use_unicode=True)
True
```

### Why it is wrong
`x mod y + z` reads as `(x mod y) + z`, and `x mod y mod z` reads as `(x mod y) mod z` (which is how `Mod(Mod(x, y), z)` is printed apart from its parentheses); both are different values.

### Related
[sympy/sympy#23912](https://redirect.github.com/sympy/sympy/issues/23912)
[sympy/sympy#11375](https://redirect.github.com/sympy/sympy/issues/11375)

### Notes on fixing
`PrettyPrinter._print_Mod` in `sympy/printing/pretty/pretty.py` parenthesizes the first argument when its binding is weaker than MUL, but appends the second argument unconditionally. The same check is needed for `expr.args[1]`. [sympy/sympy#11375](https://redirect.github.com/sympy/sympy/issues/11375) (closed) fixed only the left-hand side.

### Suggested fix
```diff
diff --git a/sympy/printing/pretty/pretty.py b/sympy/printing/pretty/pretty.py
index 4fa9b26..a5712d6 100644
--- a/sympy/printing/pretty/pretty.py
+++ b/sympy/printing/pretty/pretty.py
@@ -1975,7 +1975,10 @@ def _print_Mod(self, expr):
         if pform.binding > prettyForm.MUL:
             pform = prettyForm(*pform.parens())
         pform = prettyForm(*pform.right(' mod '))
-        pform = prettyForm(*pform.right(self._print(expr.args[1])))
+        pform_rhs = self._print(expr.args[1])
+        if pform_rhs.binding > prettyForm.MUL:
+            pform_rhs = prettyForm(*pform_rhs.parens())
+        pform = prettyForm(*pform.right(pform_rhs))
         pform.binding = prettyForm.OPEN
         return pform
 
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
