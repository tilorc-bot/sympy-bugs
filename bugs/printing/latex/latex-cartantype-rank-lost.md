# CartanType('A2') prints \text{TypeA}, dropping the rank

### Kind
lossy

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.liealgebras.cartan_type import CartanType
>>> print(latex(CartanType('A2')))
\text{TypeA}
>>> print(latex(CartanType('A3')))
\text{TypeA}
```

### Expected
```pycon
>>> latex(CartanType('A2')) != latex(CartanType('A3'))
True
```

### Why it is wrong
The rank is the essential part of a Cartan type (`A_2` and `A_3` are different Lie algebras), but the printed form only shows the series as a raw class name.

### Notes on fixing
`CartanType('A2')` returns a `TypeA` instance, which is an `Atom` with no args (the rank is stored as an attribute, `sympy/liealgebras/cartan_type.py:Standard_Cartan`), so `sympy/printing/latex.py:LatexPrinter._print_Basic` prints just `\text{TypeA}`. `str()` loses the rank as well (`TypeA()`), and `CartanType('A2') == CartanType('A3')` is `True` for the same reason. A `_latex` method printing e.g. `A_{2}` would fix the printing; storing the rank in `args` would fix all three.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
