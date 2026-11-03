# Piecewise, Product, Subs, Order and UnevaluatedExpr print as lowercase pseudo-functions (presentation MathML)

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
>>> '<mi>unevaluatedexpr</mi>' in mathml(UnevaluatedExpr(x), printer='presentation')
False
>>> '<mi>piecewise</mi>' in mathml(Piecewise((x, x > 0), (y, True)), printer='presentation')
False
>>> '<mi>product</mi>' in mathml(Product(x, (x, 1, n)), printer='presentation')
False
>>> '<mi>subs</mi>' in mathml(Subs(f(x), x, 1), printer='presentation')
False
>>> from sympy import O
>>> '<mi>order</mi>' in mathml(O(x), printer='presentation')
False
```

### Why it is wrong
`unevaluatedexpr(x)` renders as an unknown function applied to x, and Piecewise, Product, Subs and Order render as `piecewise(...)`, `product(...)`, etc. with their internal argument tuples, instead of the usual mathematical notation.

### Notes on fixing
`MathMLPresentationPrinter` (`sympy/printing/mathml.py`) has no `_print_UnevaluatedExpr`, `_print_Piecewise`, `_print_Product`, `_print_Subs` or `_print_Order`, so they fall back to `_print_Basic`, which prints the lowercased class name followed by the args. `Mod` (`mod(x, y)`) and units `Quantity` (`quantity(meter, m)`) have the same fallback. `UnevaluatedExpr` only needs to print its argument; Product can follow `_print_Sum`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
