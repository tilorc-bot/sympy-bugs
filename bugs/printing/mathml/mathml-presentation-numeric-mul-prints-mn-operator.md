# Mul(-2, 3, evaluate=False) prints as "- 6 mn 1" (presentation MathML)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import Mul, mathml
>>> mathml(Mul(-2, 3, evaluate=False), printer='presentation')
'<mrow><mo>-</mo><mn>6</mn><mo>mn</mo><mn>1</mn></mrow>'
```

### Expected
```pycon
>>> '<mo>mn</mo>' in mathml(Mul(-2, 3, evaluate=False), printer='presentation')
False
```

### Why it is wrong
The output renders as "−6 mn 1": the element name `mn` is shown as an operator.

### Notes on fixing
`MathMLPresentationPrinter._print_Mul` (`sympy/printing/mathml.py`): after extracting the minus sign, `multiply(-expr, ...)` gets the evaluated `Integer(6)`. `as_coeff_mul()` then gives `(6, ())`, the empty factor list becomes `[1]`, and `self.mathml_tag(expr)` (here `'mn'`, because `expr` is an Integer, not a Mul) is used as the multiplication operator. The content printer gives `<apply><minus/><apply><times/><cn>6</cn><cn>1</cn></apply></apply>`, which has the right value but the same stray `1`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
