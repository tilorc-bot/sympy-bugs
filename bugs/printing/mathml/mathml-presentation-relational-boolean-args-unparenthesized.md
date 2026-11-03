# Presentation MathML prints Eq(And(p, q), r) as p ∧ q = r

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Eq, And, mathml
>>> p, q, r = symbols('p q r')
>>> mathml(Eq(And(p, q), r), printer='presentation')
'<mrow><mrow><mi>p</mi><mo>&#x2227;</mo><mi>q</mi></mrow><mo>=</mo><mi>r</mi></mrow>'
```

### Expected
```pycon
>>> '<mo>(</mo>' in mathml(Eq(And(p, q), r), printer='presentation')
True
```

### Why it is wrong
`=` binds tighter than `∧`, so the rendered p ∧ q = r reads as p ∧ (q = r).

### Notes on fixing
`MathMLPresentationPrinter._print_Relational` (`sympy/printing/mathml.py`) prints `e.lhs` and `e.rhs` with `self._print` and never parenthesizes them; it should use `self.parenthesize(..., precedence(e))`, as the other binary operators do.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
