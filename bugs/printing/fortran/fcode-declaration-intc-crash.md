# Declaring a variable of type intc raises ValueError: too many values to unpack

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, fcode
>>> from sympy.codegen.ast import Declaration, Variable, intc
>>> x = symbols('x')
>>> fcode(Declaration(Variable(x, type=intc)), standard=2003, source_format='free')
Traceback (most recent call last):
...
ValueError: too many values to unpack (expected 2)
```

### Why it is wrong
`intc` is the one type with an entry in `FCodePrinter.type_modules` (it needs `use iso_c_binding, only: c_int`), and declaring a variable of that type always fails.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Type` iterates `for k, v in module_uses:` over the dict `{'iso_c_binding': 'c_int'}`, which unpacks the characters of the key. It should iterate `module_uses.items()`.

### Suggested fix
```diff
diff --git a/sympy/printing/fortran.py b/sympy/printing/fortran.py
index be02b4b..b994b80 100644
--- a/sympy/printing/fortran.py
+++ b/sympy/printing/fortran.py
@@ -444,7 +444,7 @@ def _print_Type(self, type_):
         type_str = self.type_mappings.get(type_, type_.name)
         module_uses = self.type_modules.get(type_)
         if module_uses:
-            for k, v in module_uses:
+            for k, v in module_uses.items():
                 self.module_uses[k].add(v)
         return type_str
 
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
