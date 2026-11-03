# Heaviside(x) prints as Θ(x, 1/2) (presentation MathML)

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Heaviside, mathml
>>> x = symbols('x')
>>> mathml(Heaviside(x), printer='presentation')
'<mrow><mi>&#x398;</mi><mrow><mo>(</mo><mi>x</mi><mo>,</mo><mfrac><mn>1</mn><mn>2</mn></mfrac><mo>)</mo></mrow></mrow>'
```

### Expected
```pycon
>>> '<mfrac>' in mathml(Heaviside(x), printer='presentation')
False
```

### Why it is wrong
The user wrote `Heaviside(x)`; the default value at 0 is an implementation detail that str, LaTeX and pretty hide (they print `pargs`), so Θ(x, 1/2) is surprising.

### Notes on fixing
`MathMLPresentationPrinter` (`sympy/printing/mathml.py`) prints Heaviside through `_print_Function`, which uses `e.args`. A `_print_Heaviside` using `e.pargs` fixes it. The content printer has the same problem.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
