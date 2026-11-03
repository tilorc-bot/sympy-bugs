# dotprint(Matrix([[1]])) raises AttributeError: no attribute 'args'

### Kind
crash

### Actual
```pycon
>>> from sympy import Matrix, Symbol
>>> from sympy.printing.dot import dotprint
>>> x = Symbol('x')
>>> dotprint(Matrix([[1]]))
Traceback (most recent call last):
...
AttributeError: 'MutableDenseMatrix' object has no attribute 'args'
>>> dotprint([x, 1])
Traceback (most recent call last):
...
AttributeError: 'list' object has no attribute 'args'
```

### Why it is wrong
The default `atom` predicate of `dotprint` treats every non-`Basic` object as a leaf, but a non-`Basic` top-level argument (a mutable `Matrix`, a list, a plain `int` such as `dotprint(5)`) crashes instead of producing a graph. `dotprint(ImmutableMatrix([[1]]))` works.

### Notes on fixing
`sympy/printing/dot.py:dotprint`, inner `traverse`, iterates over `e.args` without checking `atom(e)`; `dotedges` already returns `[]` for atoms. Returning early for atoms (or sympifying the top-level argument first, so a `Matrix` is drawn like an `ImmutableMatrix`) avoids the crash.

### Related
[tree-mutable-matrix-attributeerror](tree-mutable-matrix-attributeerror.md)

### Suggested fix
```diff
diff --git a/sympy/printing/dot.py b/sympy/printing/dot.py
index 85f51b7..46efbbf 100644
--- a/sympy/printing/dot.py
+++ b/sympy/printing/dot.py
@@ -286,7 +286,7 @@ def dotprint(expr,
     edges = []
     def traverse(e, depth, pos=()):
         nodes.append(dotnode(e, styles, labelfunc=labelfunc, pos=pos, repeat=repeat))
-        if maxdepth and depth >= maxdepth:
+        if (maxdepth and depth >= maxdepth) or not isinstance(e, Basic):
             return
         edges.extend(dotedges(e, atom=atom, pos=pos, repeat=repeat))
         [traverse(arg, depth+1, pos + (i,)) for i, arg in enumerate(e.args) if not atom(arg)]
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
