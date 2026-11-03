# cxxcode() does not rename a symbol named `catch` (typo 'catch,' in the C++ reserved words)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol
>>> from sympy.printing.cxx import cxxcode
>>> print(cxxcode(Symbol('class')))
class_
>>> print(cxxcode(Symbol('catch')))
catch
```

### Expected
```pycon
>>> cxxcode(Symbol('catch')) != 'catch'
True
```

### Why it is wrong
`catch` is a C++ keyword, so a variable named `catch` does not compile; other keywords are renamed.

### Notes on fixing
`sympy/printing/cxx.py:reserved['C++98']` contains `'catch,'` instead of `'catch'`; the C++11 and C++17 lists are built from it.

### Suggested fix
```diff
diff --git a/sympy/printing/cxx.py b/sympy/printing/cxx.py
index f6c5d50..3a7a983 100644
--- a/sympy/printing/cxx.py
+++ b/sympy/printing/cxx.py
@@ -16,7 +16,7 @@
 reserved = {
     'C++98': [
         'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break',
-        'case', 'catch,', 'char', 'class', 'compl', 'const', 'const_cast',
+        'case', 'catch', 'char', 'class', 'compl', 'const', 'const_cast',
         'continue', 'default', 'delete', 'do', 'double', 'dynamic_cast',
         'else', 'enum', 'explicit', 'export', 'extern', 'false', 'float',
         'for', 'friend', 'goto', 'if', 'inline', 'int', 'long', 'mutable',
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
