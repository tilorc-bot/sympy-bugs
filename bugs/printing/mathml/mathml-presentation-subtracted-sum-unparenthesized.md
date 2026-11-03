# Presentation MathML prints a - (b - c) as a - b - c

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Add, Mul, mathml
>>> a, b, c = symbols('a b c')
>>> e = Add(a, Mul(-1, b - c, evaluate=False), evaluate=False)
>>> mathml(e, printer='presentation')
'<mrow><mi>a</mi><mo>-</mo><mrow><mi>b</mi><mo>-</mo><mi>c</mi></mrow></mrow>'
```

### Expected
```pycon
>>> '<mo>(</mo>' in mathml(e, printer='presentation')
True
```

### Why it is wrong
`<mrow>` draws no parentheses, so this renders as a − b − c instead of a − (b − c). The same happens for `parse_expr('a - (b - c)', evaluate=False)`.

### Notes on fixing
`MathMLPresentationPrinter._print_Add` (`sympy/printing/mathml.py`): for a term that `could_extract_minus_sign()`, it prints `<mo>-</mo>` followed by `self._print(-arg)` without parenthesizing; `-arg` must be parenthesized when it is an Add (`self.parenthesize(-arg, PRECEDENCE['Add'], strict=True)` or similar). See also the matching problem in `_print_Mul` (`-(a + b)` printed as `-a + b`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
