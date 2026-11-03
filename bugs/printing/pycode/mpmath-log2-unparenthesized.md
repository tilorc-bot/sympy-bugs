# MpmathPrinter prints log2(x) as an unparenthesized quotient, so log2(x)**2 evaluates wrongly

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, lambdify
>>> from sympy.codegen.cfunctions import log2
>>> from sympy.printing.pycode import MpmathPrinter
>>> x = symbols('x')
>>> print(MpmathPrinter().doprint(log2(x)**2))
mpmath.log(x)/mpmath.log(2)**2
>>> print(lambdify(x, log2(x)**2, 'mpmath')(8))
4.32808512266689
```

### Expected
```pycon
>>> import mpmath
>>> abs(eval(MpmathPrinter().doprint(log2(x)**2), {'mpmath': mpmath, 'x': 8}) - 9) < 1e-12
True
>>> abs(lambdify(x, log2(x)**2, 'mpmath')(8) - 9) < 1e-12
True
```

### Why it is wrong
`log2(8)**2` is 9, but the generated code squares only `log(2)`. Any expression where `log2(...)` is an operand of a power or a division (e.g. `1/log2(x)`) silently computes a wrong value.

### Notes on fixing
`sympy/printing/pycode.py:MpmathPrinter._print_log2` returns `log(x)/log(2)` without parentheses; the caller treats the result as an atom (function call), so `_print_Pow` adds none. Wrapping the quotient in parentheses fixes it.

### Suggested fix
```diff
diff --git a/sympy/printing/pycode.py b/sympy/printing/pycode.py
index 1a7aa71..d581095 100644
--- a/sympy/printing/pycode.py
+++ b/sympy/printing/pycode.py
@@ -885,7 +885,7 @@ def _print_lowergamma(self, e):
             self._print(e.args[1]))
 
     def _print_log2(self, e):
-        return '{0}({1})/{0}(2)'.format(
+        return '({0}({1})/{0}(2))'.format(
             self._module_format('mpmath.log'), self._print(e.args[0]))
 
     def _print_log1p(self, e):
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
