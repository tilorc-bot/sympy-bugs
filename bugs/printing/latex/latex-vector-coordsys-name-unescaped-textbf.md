# latex() of a sympy.vector base scalar puts the coordinate system name unescaped in \textbf{} (CoordSys3D('C_1').x)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.vector import CoordSys3D
>>> C = CoordSys3D('C_1')
>>> print(latex(C.x))
\boldsymbol{x}_{\textbf{C_1}}
```

### Expected
```pycon
>>> 'C_1' in latex(C.x)
False
```

### Why it is wrong
`_` is not allowed in text mode, so `\textbf{C_1}` fails with "Missing $ inserted"; any expression in the coordinates of such a system produces TeX that does not compile.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_BaseScalar` formats the system name into `\textbf{%s}` verbatim. It should be escaped with `latex_escape`, or printed in math mode (`\mathbf{C_{1}}`) the way base vectors already are (`latex(C.i)` gives `\mathbf{\hat{i}_{C_1}}`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
