# rcode(For(...)) omits the closing parenthesis of for(

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Range, rcode
>>> from sympy.codegen.ast import For, Assignment
>>> x, y = symbols('x y')
>>> print(rcode(For(x, Range(0, 10, 2), [Assignment(y, x*y)])))
for(x in seq(from=0, to=9, by=2){
   y = x*y;
}
```

### Expected
```pycon
>>> line = rcode(For(x, Range(0, 10, 2), [Assignment(y, x*y)])).splitlines()[0]
>>> line.count('(') == line.count(')')
True
```

### Why it is wrong
The `for(` header is never closed, so R 4.6 reports `unexpected '{'`.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._print_For` uses the format string `'for({target} in seq(from={start}, to={stop}, by={step}){{...'`, which is missing a `)` before `{{`. The output is asserted by `test_rcode_For` in `sympy/printing/tests/test_rcode.py`.

### Suggested fix
```diff
diff --git a/sympy/printing/rcode.py b/sympy/printing/rcode.py
index 3107e6e..7f1a0bf 100644
--- a/sympy/printing/rcode.py
+++ b/sympy/printing/rcode.py
@@ -254,7 +254,7 @@ def _print_For(self, expr):
         else:
             raise NotImplementedError("Only iterable currently supported is Range")
         body = self._print(expr.body)
-        return 'for({target} in seq(from={start}, to={stop}, by={step}){{\n{body}\n}}'.format(target=target, start=start,
+        return 'for({target} in seq(from={start}, to={stop}, by={step})){{\n{body}\n}}'.format(target=target, start=start,
                 stop=stop-1, step=step, body=body)
 
 
diff --git a/sympy/printing/tests/test_rcode.py b/sympy/printing/tests/test_rcode.py
index 1443cc1..dffaf26 100644
--- a/sympy/printing/tests/test_rcode.py
+++ b/sympy/printing/tests/test_rcode.py
@@ -459,7 +459,7 @@ def test_rcode_Assignment():
 def test_rcode_For():
     f = For(x, Range(0, 10, 2), [aug_assign(y, '*', x)])
     sol = rcode(f)
-    assert sol == ("for(x in seq(from=0, to=9, by=2){\n"
+    assert sol == ("for(x in seq(from=0, to=9, by=2)){\n"
                    "   y *= x;\n"
                    "}")
 
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
