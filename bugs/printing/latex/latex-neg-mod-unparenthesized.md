# latex() prints -Mod(x, y) as "- x \bmod y" without parentheses

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex, Mod
>>> x, y = symbols('x y')
>>> print(latex(-Mod(x, y)))
- x \bmod y
>>> print(latex(x - Mod(x, y)))
x - \left(x \bmod y\right)
>>> print(latex(-2*Mod(x, y)))
- 2 \left(x \bmod y\right)
```

### Expected
```pycon
>>> print(latex(-Mod(x, y)))
- \left(x \bmod y\right)
```

### Why it is wrong
`- x \bmod y` reads as `(-x) mod y`, which has a different value from `-(x mod y)` (e.g. x=1, y=3 gives 2 vs -1). Every other context (`x - Mod(x, y)`, `-2*Mod(x, y)`) already parenthesizes the Mod.

### Related
[latex-mod-negative-arg](latex-mod-negative-arg.md)

### Notes on fixing
`LatexPrinter._print_Mul` (`sympy/printing/latex.py`) strips the minus sign of `Mul(-1, Mod(x, y))` and emits `"- " + convert(expr)`; it only adds `\left(...\right)` when the remaining factor is an Add, never consulting `_needs_mul_brackets` (which does return True for Mod). Independent of the `precedence_traditional` root cause: fixing that changes how `Mod(-x, y)` prints but not this.

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..ed66921 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -590,7 +590,8 @@ def convert_args(args) -> str:
         if expr.could_extract_minus_sign():
             expr = -expr
             tex = "- "
-            if is_Add(expr) or (isinstance(expr, UnevaluatedExpr) \
+            if is_Add(expr) or isinstance(expr, Mod) or \
+                    (isinstance(expr, UnevaluatedExpr) \
                     and expr.args[0].is_Number and expr.args[0].is_negative):
                 tex += r"\left("
                 include_parens = True
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).

### Encountered
- (test entry for the PR check; this PR will be closed)
