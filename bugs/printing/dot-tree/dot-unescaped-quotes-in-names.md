# dotprint() writes unescaped double quotes into node ids and labels for symbols named x' or a"b

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol
>>> from sympy.printing.dot import dotnode
>>> print(dotnode(Symbol("x'")))
"Symbol("x'")_()" ["color"="black", "label"="x'", "shape"="ellipse"];
>>> print(dotnode(Symbol('a"b')))
"Symbol('a"b')_()" ["color"="black", "label"="a"b", "shape"="ellipse"];
>>> print(dotnode(Symbol('x')))
"Symbol('x')_()" ["color"="black", "label"="x", "shape"="ellipse"];
```

### Expected
```pycon
>>> dotnode(Symbol("x'")).replace('\\"', '').count('"')
14
>>> dotnode(Symbol('a"b')).replace('\\"', '').count('"')
14
```

### Why it is wrong
In DOT a double-quoted string ends at the first unescaped `"`, so these lines (which `dotprint` puts into the graph) are syntax errors for graphviz. `srepr` switches to double quotes for any name containing `'`, so every symbol with a prime in its name breaks the output. The Expected block checks that, apart from escaped `\"`, a node line has the same 14 quote characters as for `Symbol('x')`; it was not run through graphviz.

### Notes on fixing
`sympy/printing/dot.py`: `dotnode` and `dotedges` wrap `purestr(expr)` in `"..."` without escaping, and `attrprint` does the same for the `label` value. All three need `"` (and `\`) escaped as `\"` (`\\`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
