# jscode() does not rename symbols named after JavaScript keywords (var, new, ...)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol
>>> from sympy.printing.jscode import jscode
>>> print(jscode(Symbol('var') + Symbol('new')))
new + var
```

### Expected
```pycon
>>> jscode(Symbol('var')) != 'var' and jscode(Symbol('new')) != 'new'
True
```

### Why it is wrong
`var` and `new` are JavaScript keywords, so the generated code is a syntax error. Other code printers (C, C++, Python, Rust, ...) rename such symbols (e.g. `var_`). The original reviewer ran this with node; it was not executed here.

### Notes on fixing
`sympy/printing/jscode.py:JavascriptCodePrinter` has no `reserved_words` set (it inherits the empty one from `CodePrinter`). It needs the list of JavaScript reserved words.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
