# A codegen Variable with a parametrized attribute such as dimension(10) raises TypeError

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.codegen.ast import Variable, real
>>> from sympy.codegen.fnodes import dimension
>>> x = symbols('x')
>>> str(Variable(x, type=real, attrs=[dimension(10)]))
Traceback (most recent call last):
...
TypeError: StrPrinter._print_Integer() got an unexpected keyword argument 'joiner'
```

### Why it is wrong
`dimension(10)` is the documented way to declare a Fortran array; the Variable can be code-printed (`fcode` gives `real*8, dimension(10) :: x`) but `str`/`print` of it, or of any AST containing it, crashes.

### Notes on fixing
`sympy/codegen/ast.py:Node._indented` prints each `Token` element of a tuple field with an extra `joiner=` keyword. For an `Attribute`, `Attribute._sympystr` forwards all `**kwargs` to `printer._print(arg, ...)` for its parameters, so `joiner` reaches `_print_Integer`, which does not accept it. `Attribute._sympystr` should not forward the `joiner` keyword (or any keywords) to the printing of its parameters.

### Suggested fix
```diff
diff --git a/sympy/codegen/ast.py b/sympy/codegen/ast.py
index 93e64be..5c00a37 100644
--- a/sympy/codegen/ast.py
+++ b/sympy/codegen/ast.py
@@ -1396,7 +1396,7 @@ class Attribute(Token):
     _construct_name = String
     _construct_parameters = staticmethod(_mk_Tuple)
 
-    def _sympystr(self, printer, *args, **kwargs):
+    def _sympystr(self, printer, *args, joiner=', ', **kwargs):
         result = str(self.name)
         if self.parameters:
             result += '(%s)' % ', '.join((printer._print(
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
