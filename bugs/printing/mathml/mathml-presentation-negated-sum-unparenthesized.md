# Presentation MathML prints -(a + b) as -a + b

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mul, mathml
>>> a, b, x, y, z = symbols('a b x y z')
>>> mathml(Mul(-1, a + b, evaluate=False), printer='presentation')
'<mrow><mo>-</mo><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow></mrow>'
>>> mathml(x**Mul(-1, y + z, evaluate=False), printer='presentation')
'<msup><mi>x</mi><mrow><mo>-</mo><mrow><mi>y</mi><mo>+</mo><mi>z</mi></mrow></mrow></msup>'
```

### Expected
```pycon
>>> '<mo>(</mo>' in mathml(Mul(-1, a + b, evaluate=False), printer='presentation')
True
>>> '<mo>(</mo>' in mathml(x**Mul(-1, y + z, evaluate=False), printer='presentation')
True
```

### Why it is wrong
`<mrow>` only groups for layout and draws no parentheses, so these render as −a+b and x^(−y+z). The same happens for `parse_expr('-(a+b)', evaluate=False)`.

### Notes on fixing
`MathMLPresentationPrinter._print_Mul` (`sympy/printing/mathml.py`): when `expr.could_extract_minus_sign()`, it emits `<mo>-</mo>` and then prints `-expr` with `multiply`, which returns the sum unparenthesized when `-expr` is a single term. The negated part has to be parenthesized when it is an Add (e.g. via `self.parenthesize(-expr, PRECEDENCE['Mul'])`). The issue reports that adding the parentheses here and in `_print_Add` removed all 23 wrong-value cases in 600 fuzzed trees.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
