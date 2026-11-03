# str() of an expression containing Function('Rational')(x) or Function('Integer')(x) raises AttributeError

### Kind
crash

### Actual
```pycon
>>> from sympy import Function, symbols
>>> x = symbols('x')
>>> str(Function('Rational')(x) + 1)
Traceback (most recent call last):
...
AttributeError: 'Rational' object has no attribute 'p'
>>> str(Function('Integer')(x) + 1)
Traceback (most recent call last):
...
AttributeError: 'Integer' object has no attribute 'p'
```

### Expected
```pycon
>>> str(Function('Rational')(x) + 1)
'Rational(x) + 1'
>>> str(Function('Integer')(x) + 1)
'Integer(x) + 1'
```

### Why it is wrong
Undefined functions may have any name; printing `f(x)` works on its own, but as soon as such a function appears inside a sum, product, power or relational the printer crashes.

### Notes on fixing
`sympy/printing/precedence.py:precedence` walks the MRO by class *name* and dispatches to `PRECEDENCE_FUNCTIONS`, so an `AppliedUndef` named `Rational`, `Integer` or `Float` is treated as a number (`precedence_Rational` reads `item.p`; `precedence_Float` compares `item < 0` and raises `TypeError`). `Printer._print` (`sympy/printing/printer.py`) already guards against this by starting the MRO at `AppliedUndef`; `precedence` (and `precedence_traditional`) need the same guard. A user-defined `class Rational(Function)` hits the same path. Every printer that calls `precedence` is affected: `python()`, `pycode(..., strict=False)` and `ccode` raise the same `AttributeError`.

### Suggested fix
```diff
diff --git a/sympy/printing/precedence.py b/sympy/printing/precedence.py
index 33ba6fe..bf5cadb 100644
--- a/sympy/printing/precedence.py
+++ b/sympy/printing/precedence.py
@@ -133,7 +133,11 @@ def precedence(item):
     if hasattr(item, "precedence"):
         return item.precedence
     if not isinstance(item, type):
-        for i in type(item).mro():
+        from sympy.core.function import AppliedUndef
+        classes = type(item).mro()
+        if AppliedUndef in classes:
+            classes = classes[classes.index(AppliedUndef):]
+        for i in classes:
             n = i.__name__
             if n in PRECEDENCE_FUNCTIONS:
                 return PRECEDENCE_FUNCTIONS[n](item)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
