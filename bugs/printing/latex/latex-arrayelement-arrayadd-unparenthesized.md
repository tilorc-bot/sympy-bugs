# latex() of an element of an ArrayAdd puts the index on the last term: {{A + B}_{i}}

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, latex
>>> from sympy.tensor.array.expressions import ArraySymbol, ArrayElement, ArrayAdd
>>> i = symbols('i')
>>> A, B = ArraySymbol('A', (3,)), ArraySymbol('B', (3,))
>>> print(latex(ArrayElement(ArrayAdd(A, B), (i,))))
{{A + B}_{i}}
```

### Expected
```pycon
>>> r'\left(A + B\right)' in latex(ArrayElement(ArrayAdd(A, B), (i,)))
True
```

### Why it is wrong
Braces are invisible in the rendered output, so it shows `A + B_i`, the sum of the array `A` and the element `B_i`, instead of `(A + B)_i`.

### Notes on fixing
`LatexPrinter._print_ArrayElement` (`sympy/printing/latex.py`) calls `self.parenthesize(expr.name, PRECEDENCE["Func"], True)`, which passes `True` as the positional `is_neg` argument rather than `strict=True`. Even with that corrected, `ArrayAdd` has no precedence entry (Atom), so it would still not be bracketed; it needs Add precedence (in `sympy/printing/precedence.py`) or an explicit check.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
