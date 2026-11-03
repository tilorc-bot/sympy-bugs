# Transpose, Inverse, MatPow, Determinant, Product, Equivalent print as non-MathML containers (content MathML)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, Determinant, Product, Equivalent, mathml
>>> x, n, p, q = symbols('x n p q')
>>> M = MatrixSymbol('M', 2, 2)
>>> mathml(M.T)
'<transpose><ci>M</ci></transpose>'
>>> mathml(M**3)
'<matpow><ci>M</ci><cn>3</cn></matpow>'
>>> mathml(Product(x, (x, 1, n)))
'<product><ci>x</ci><tuple><ci>x</ci><cn>1</cn><ci>n</ci></tuple></product>'
```

### Expected
```pycon
>>> mathml(M.T).startswith('<apply>')
True
>>> mathml(M**3).startswith('<apply>')
True
>>> mathml(Product(x, (x, 1, n))).startswith('<apply>')
True
>>> [mathml(e).startswith('<apply>') for e in (M.I, Determinant(M), Equivalent(p, q))]
[True, True, True]
```

### Why it is wrong
In content MathML, operators such as `<transpose/>`, `<inverse/>`, `<determinant/>`, `<product/>` and `<equivalent/>` are empty elements applied with `<apply>`; using them as containers, and inventing `<matpow>`, `<tuple>`, gives markup no MathML consumer understands.

### Related
[sympy/sympy#25271](https://redirect.github.com/sympy/sympy/issues/25271)

### Notes on fixing
These have no handler in `MathMLContentPrinter` (`sympy/printing/mathml.py`) and go through `_print_Basic`, which wraps the args in an element named by `mathml_tag` (the lowercased class name). Each needs a proper handler (`Product` like `_print_Sum`, with `bvar`/`lowlimit`/`uplimit`; `MatPow` as `<power/>`). Other objects with the same fallback:
- `ITE` (`<ite>`; should be `<piecewise>`);
- `UnevaluatedExpr` (`<unevaluatedexpr>`; should print its argument);
- `Interval(0, 1)` (`<interval><cn>0</cn><cn>1</cn><false/><false/></interval>`; the openness should be the `closure` attribute).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
