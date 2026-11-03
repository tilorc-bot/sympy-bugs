# Content MathML prints Heaviside(x) with its implicit second argument 1/2

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Heaviside, mathml
>>> x = symbols('x')
>>> mathml(Heaviside(x))
'<apply><heaviside/><ci>x</ci><apply><divide/><cn>1</cn><cn>2</cn></apply></apply>'
```

### Expected
```pycon
>>> '<divide/>' in mathml(Heaviside(x))
False
```

### Why it is wrong
The user wrote `Heaviside(x)`; the default value at 0 is an implementation detail that str, LaTeX and srepr hide (they print `pargs`). (`<heaviside/>` is not a content MathML element either.)

### Notes on fixing
`MathMLContentPrinter` (`sympy/printing/mathml.py`) prints Heaviside through `_print_Function`, which uses `e.args`. A `_print_Heaviside` using `e.pargs` fixes it (see `ReprPrinter._print_Heaviside`). The presentation printer has the same problem.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
