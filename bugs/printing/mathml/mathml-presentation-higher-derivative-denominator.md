# d²f/dx² puts the exponent on the d in the denominator: d²/d² x (presentation MathML)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative, mathml
>>> x = symbols('x')
>>> f = Function('f')
>>> mathml(Derivative(f(x), (x, 2)), printer='presentation')
'<mrow><mfrac><mrow><msup><mo>&dd;</mo><mn>2</mn></msup></mrow><mrow><msup><mo>&dd;</mo><mn>2</mn></msup><mi>x</mi></mrow></mfrac><mrow><mi>f</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow></mrow>'
```

### Expected
```pycon
>>> '<msup><mi>x</mi><mn>2</mn></msup>' in mathml(Derivative(f(x), (x, 2)), printer='presentation')
True
```

### Why it is wrong
The standard notation is d²/dx², with the order on the variable in the denominator; d²/(d² x) is not the usual notation and reads as a different quantity.

### Notes on fixing
`MathMLPresentationPrinter._print_Derivative` (`sympy/printing/mathml.py`) puts the exponent on the `d` operator in the denominator (`msup(d, num)` followed by `sym`) instead of on the variable (`d` followed by `msup(sym, num)`). The LaTeX printer prints `\frac{d^{2}}{d x^{2}}`.
`test_print_derivative` in `sympy/printing/tests/test_mathml.py` asserts the current form (`<msup><mo>&#x2202;</mo><mn>2</mn></msup><mi>z</mi>`), so it must be updated.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
