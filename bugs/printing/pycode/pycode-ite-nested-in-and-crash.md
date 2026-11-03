# An ITE whose condition contains another ITE inside And raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, ITE, And, pycode
>>> x, y, z = symbols('x y z')
>>> e = ITE(And(ITE(x < 0, y < 0, z < 0), x < 1), y < 1, z < 1)
>>> pycode(e)
Traceback (most recent call last):
...
TypeError: expecting bool or Boolean, not `Piecewise((y < 0, x < 0), (z < 0, True))`.
```

### Why it is wrong
Printing must not fail for a valid expression; `ccode(e)` prints it.

### Related
[sympy/sympy#27647](https://redirect.github.com/sympy/sympy/issues/27647)
[sympy/sympy#24961](https://redirect.github.com/sympy/sympy/issues/24961)

### Notes on fixing
`AbstractPythonCodePrinter._print_ITE` (`sympy/printing/pycode.py`) calls `expr.rewrite(Piecewise)`, which rewrites deeply: the inner ITE becomes a (non-Boolean) Piecewise inside `And`, and `And` rejects it. `C89CodePrinter._print_ITE` uses `expr.rewrite(Piecewise, deep=False)`, which avoids this, since the inner ITE is then printed by `_print_ITE` again. `RCodePrinter._print_ITE` (`sympy/printing/rcode.py`) has the same deep rewrite and the same crash.

### Suggested fix
```diff
diff --git a/sympy/printing/pycode.py b/sympy/printing/pycode.py
index 1a7aa71..604fc97 100644
--- a/sympy/printing/pycode.py
+++ b/sympy/printing/pycode.py
@@ -261,7 +261,7 @@ def _print_Relational(self, expr):
 
     def _print_ITE(self, expr):
         from sympy.functions.elementary.piecewise import Piecewise
-        return self._print(expr.rewrite(Piecewise))
+        return self._print(expr.rewrite(Piecewise, deep=False))
 
     def _print_Sum(self, expr):
         loops = (
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
