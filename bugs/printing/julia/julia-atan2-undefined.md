# atan2(y, x) prints atan2(y, x), which Julia does not define

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, atan2, julia_code
>>> x, y = symbols('x y')
>>> print(julia_code(atan2(y, x)))
atan2(y, x)
```

### Expected
```pycon
>>> julia_code(atan2(y, x))
'atan(y, x)'
```

### Why it is wrong
Julia has no `atan2`; the two-argument arctangent is `atan(y, x)`. The reviewer ran the output with Julia 1.12: `UndefVarError: atan2 not defined`.

### Notes on fixing
`sympy/printing/julia.py`: `"atan2"` is in `known_fcns_src1` (same name in SymPy and Julia). It should be moved to `known_fcns_src2` as `"atan2": "atan"`.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Suggested fix
```diff
diff --git a/sympy/printing/julia.py b/sympy/printing/julia.py
index 3ab815a..70d7d85 100644
--- a/sympy/printing/julia.py
+++ b/sympy/printing/julia.py
@@ -25,7 +25,7 @@
                    "asin", "acos", "atan", "acot", "asec", "acsc",
                    "sinh", "cosh", "tanh", "coth", "sech", "csch",
                    "asinh", "acosh", "atanh", "acoth", "asech", "acsch",
-                   "atan2", "sign", "floor", "log", "exp",
+                   "sign", "floor", "log", "exp",
                    "cbrt", "sqrt", "erf", "erfc", "erfi",
                    "factorial", "gamma", "digamma", "trigamma",
                    "polygamma", "beta",
@@ -36,6 +36,7 @@
 # generally a mapping to (argument_conditions, julia_function).
 known_fcns_src2 = {
     "Abs": "abs",
+    "atan2": "atan",
     "ceiling": "ceil",
     "conjugate": "conj",
     "hankel1": "hankelh1",
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
