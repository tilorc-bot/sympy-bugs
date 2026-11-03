# python() prints Rational(1, 3) as 1/3 (a float) when a symbol had to be renamed

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Symbol, Rational, python
>>> e = Symbol('if') + Rational(1, 3)
>>> print(python(e))
if_ = Symbol('if')
e = if_ + 1/3
>>> print(python(Symbol('x') + Rational(1, 3)))
x = Symbol('x')
e = x + Rational(1, 3)
```

### Expected
```pycon
>>> ns = {}
>>> exec('from sympy import *\n' + python(e), ns)
>>> ns['e'] == e
True
```

### Why it is wrong
`python()` is meant to produce code that recreates the expression; executing this output gives `if + 0.333333333333333`, a Float instead of the exact rational. Without the keyword symbol the same Rational is printed correctly as `Rational(1, 3)`.

### Related
[sympy/sympy#5520](https://redirect.github.com/sympy/sympy/issues/5520)

### Notes on fixing
`sympy/printing/python.py:python`: when `renamings` is non-empty it does `exprp = expr.subs(renamings)` and then `printer._str(exprp)`, i.e. plain `str()`, instead of printing the substituted expression with the `PythonPrinter`. Any renaming triggers it (keyword names such as `if`, `lambda`, and names with braces such as `x_{1}`).

### Suggested fix
```diff
diff --git a/sympy/printing/python.py b/sympy/printing/python.py
index 470a5be..2ad3436 100644
--- a/sympy/printing/python.py
+++ b/sympy/printing/python.py
@@ -83,8 +83,8 @@ def python(expr, **settings):
         result += newfunctionname + ' = Function(\'' + functionname + '\')\n'
 
     if renamings:
-        exprp = expr.subs(renamings)
-    result += 'e = ' + printer._str(exprp)
+        exprp = printer.doprint(expr.subs(renamings))
+    result += 'e = ' + exprp
     return result
 
 
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
