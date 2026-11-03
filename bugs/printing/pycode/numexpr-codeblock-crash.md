# NumExprPrinter raises TypeError on CodeBlock

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.codegen.ast import CodeBlock, Assignment
>>> from sympy.printing.lambdarepr import NumExprPrinter
>>> x = symbols('x')
>>> NumExprPrinter().doprint(CodeBlock(Assignment(x, 1)))
Traceback (most recent call last):
...
TypeError: CodePrinter._print_CodeBlock() takes 2 positional arguments but 3 were given
```

### Expected
```pycon
>>> _ = NumExprPrinter().doprint(CodeBlock(Assignment(x, 1)))
```

### Why it is wrong
Printing must not fail for a valid code block.

### Notes on fixing
`sympy/printing/lambdarepr.py:NumExprPrinter._print_CodeBlock` calls `super()._print_CodeBlock(self, expr.func(*args))`, passing `self` twice.

### Suggested fix
```diff
diff --git a/sympy/printing/lambdarepr.py b/sympy/printing/lambdarepr.py
index 7d2c145..6363317 100644
--- a/sympy/printing/lambdarepr.py
+++ b/sympy/printing/lambdarepr.py
@@ -223,7 +223,7 @@ def _print_CodeBlock(self, expr):
         from sympy.codegen.ast import CodegenAST
         from sympy.codegen.pynodes import NumExprEvaluate
         args = [ arg if isinstance(arg, CodegenAST) else NumExprEvaluate(arg) for arg in expr.args ]
-        return super()._print_CodeBlock(self, expr.func(*args))
+        return super()._print_CodeBlock(expr.func(*args))
 
 
 class IntervalPrinter(MpmathPrinter, LambdaPrinter):
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
