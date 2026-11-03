# precedence_traditional gives negative products Mul precedence instead of Add precedence

### Kind
internal

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.printing.precedence import precedence, precedence_traditional
>>> x = symbols('x')
>>> precedence(-x), precedence_traditional(-x)
(40, 50)
```

### Expected
```pycon
>>> precedence_traditional(-x) == precedence(-x)
True
```

### Why it is wrong
The LaTeX and pretty printers use `precedence_traditional` to decide where parentheses go. A negative product such as `-x` binds like a sum, but gets Mul precedence here, so it is never parenthesized where a sum would be.

### Notes on fixing
`PRECEDENCE_TRADITIONAL = PRECEDENCE.copy()` contains the key `"Mul"`, so the lookup by class name returns 50 for every `Mul` and never reaches `precedence_Mul`, which returns Add precedence for negative products (`sympy/printing/precedence.py`).

### Suggested fix
```diff
--- a/sympy/printing/precedence.py
+++ b/sympy/printing/precedence.py
@@ -179,7 +179,7 @@
         return precedence_traditional(item.args[0])
 
     n = item.__class__.__name__
-    if n in PRECEDENCE_TRADITIONAL:
+    if n in PRECEDENCE_TRADITIONAL and n not in PRECEDENCE_FUNCTIONS:
         return PRECEDENCE_TRADITIONAL[n]
 
     return precedence(item)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (root cause 1).
