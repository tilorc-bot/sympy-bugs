# Comments print as "// text", but R comments start with #

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import rcode
>>> from sympy.codegen.ast import Comment
>>> print(rcode(Comment('hi')))
// hi
```

### Expected
```pycon
>>> rcode(Comment('hi')).startswith('#')
True
```

### Why it is wrong
`//` is not a comment in R (it is a syntax error), so any comment the printer emits, including the "Not supported in R" notes written for unsupported expressions with `strict=False`, breaks the generated code. The reviewer checked this against the R documentation.

### Notes on fixing
`sympy/printing/rcode.py:RCodePrinter._get_comment` returns `"// {}"`; it should return `"# {}"`.

### Suggested fix
```diff
diff --git a/sympy/printing/rcode.py b/sympy/printing/rcode.py
index 3107e6e..1359b5c 100644
--- a/sympy/printing/rcode.py
+++ b/sympy/printing/rcode.py
@@ -109,7 +109,7 @@ def _get_statement(self, codestring):
         return "%s;" % codestring
 
     def _get_comment(self, text):
-        return "// {}".format(text)
+        return "# {}".format(text)
 
     def _declare_number_const(self, name, value):
         return "{} = {};".format(name, value)
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
