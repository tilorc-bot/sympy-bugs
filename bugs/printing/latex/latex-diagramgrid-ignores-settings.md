# Printer settings are ignored for the entries of a DiagramGrid

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import Symbol, latex
>>> from sympy.categories import Object, NamedMorphism, Diagram
>>> from sympy.categories.diagram_drawing import DiagramGrid
>>> A1, B = Object('A_1'), Object('B')
>>> grid = DiagramGrid(Diagram([NamedMorphism(A1, B, 'f')]))
>>> print(latex(A1, symbol_names={Symbol('A_1'): 'Q'}))
Q
>>> print(latex(grid, symbol_names={Symbol('A_1'): 'Q'}))
\begin{array}{cc}
A_{1} & B
\end{array}
```

### Expected
```pycon
>>> 'Q' in latex(grid, symbol_names={Symbol('A_1'): 'Q'})
True
```

### Why it is wrong
Settings passed to `latex()` (here `symbol_names`) apply to an `Object` on its own but are silently dropped for the same object inside a `DiagramGrid`.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_DiagramGrid` calls the module-level `latex(grid[i, j])`, which starts a fresh printer with default settings, instead of `self._print(grid[i, j])`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
