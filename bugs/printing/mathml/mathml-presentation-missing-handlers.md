# Presentation MathML prints Piecewise, Product, Subs, Order and UnevaluatedExpr as lowercase pseudo-functions

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, Piecewise, Product, Subs, UnevaluatedExpr, mathml
>>> x, y, n = symbols('x y n')
>>> f = Function('f')
>>> mathml(UnevaluatedExpr(x), printer='presentation')
'<mrow><mi>unevaluatedexpr</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
>>> mathml(Piecewise((x, x > 0), (y, True)), printer='presentation')
'<mrow><mi>piecewise</mi><mrow><mo>(</mo><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mrow><mi>x</mi><mo>></mo><mn>0</mn></mrow><mo>)</mo></mrow><mo>,</mo><mrow><mo>(</mo><mi>y</mi><mo>,</mo><mi>True</mi><mo>)</mo></mrow><mo>)</mo></mrow></mrow>'
>>> mathml(Product(x, (x, 1, n)), printer='presentation')
'<mrow><mi>product</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mn>1</mn><mo>,</mo><mi>n</mi><mo>)</mo></mrow><mo>)</mo></mrow></mrow>'
```

### Expected
```pycon
>>> from sympy import O
>>> cases = {'unevaluatedexpr': UnevaluatedExpr(x), 'piecewise': Piecewise((x, x > 0), (y, True)),
...          'product': Product(x, (x, 1, n)), 'subs': Subs(f(x), x, 1), 'order': O(x)}
>>> [name for name, e in cases.items() if '<mi>%s</mi>' % name in mathml(e, printer='presentation')]
[]
```

### Why it is wrong
`unevaluatedexpr(x)` renders as an unknown function applied to x, and Piecewise, Product, Subs and Order render as `piecewise(...)`, `product(...)`, etc. with their internal argument tuples, instead of the usual mathematical notation.

### Notes on fixing
`MathMLPresentationPrinter` (`sympy/printing/mathml.py`) has no `_print_UnevaluatedExpr`, `_print_Piecewise`, `_print_Product`, `_print_Subs` or `_print_Order`, so they fall back to `_print_Basic`, which prints the lowercased class name followed by the args. `Mod` (`mod(x, y)`) and units `Quantity` (`quantity(meter, m)`) have the same fallback. `UnevaluatedExpr` only needs to print its argument; Product can follow `_print_Sum`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
