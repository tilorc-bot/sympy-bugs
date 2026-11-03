# tree(Matrix([[1]])) raises AttributeError: no attribute 'args'

### Kind
crash

### Actual
```pycon
>>> from sympy import Matrix
>>> from sympy.printing.tree import tree
>>> tree(Matrix([[1]]))
Traceback (most recent call last):
...
AttributeError: 'MutableDenseMatrix' object has no attribute 'args'
```

### Expected
```pycon
>>> _ = tree(Matrix([[1]]))
```

### Why it is wrong
`tree` (and `print_tree`) fail for the most common matrix type, while `tree(ImmutableMatrix([[1]]))` works.

### Notes on fixing
`sympy/printing/tree.py:tree` recurses over `node.args` unconditionally; mutable matrices (and other non-`Basic` objects) have no `args`. Converting with `sympify`/`as_immutable()` or treating non-`Basic` nodes as leaves would fix it.

### Related
[dot-non-basic-input-attributeerror](dot-non-basic-input-attributeerror.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
