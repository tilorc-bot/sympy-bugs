# A list of per-column alignments raises AttributeError

### Kind
crash

### Actual
```pycon
>>> from sympy import TableForm
>>> TableForm([[1, 2]], alignments=['l', 'r'])
Traceback (most recent call last):
...
AttributeError: 'list' object has no attribute 'strip'
```

### Expected
```pycon
>>> _ = TableForm([[1, 2]], alignments=['l', 'r'])
```

### Why it is wrong
The docstring says alignments "When given as a single value, the value is used for all columns", i.e. a list of values (one per column) is also accepted, and the constructor has code to handle such a list, but it is unreachable.

### Notes on fixing
`sympy/printing/tableform.py:TableForm.__init__` calls `_std_align(alignments)` on the whole argument before checking whether it is a single value; `_std_align` calls `.strip()`, which fails for a list. The single-value check must only be done when `alignments` is a string.

### Suggested fix
```diff
diff --git a/sympy/printing/tableform.py b/sympy/printing/tableform.py
index 2e91e42..a3f1ddb 100644
--- a/sympy/printing/tableform.py
+++ b/sympy/printing/tableform.py
@@ -167,7 +167,7 @@ def _std_align(a):
                 return {'left': 'l', 'right': 'r', 'center': 'c'}.get(a, a)
             else:
                 return {'<': 'l', '>': 'r', '^': 'c'}.get(a, a)
-        std_align = _std_align(alignments)
+        std_align = _std_align(alignments) if isinstance(alignments, str) else None
         if std_align in allow:
             _alignments = [std_align]*_w
         else:
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
