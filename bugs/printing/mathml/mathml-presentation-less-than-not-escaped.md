# Presentation MathML of x < y is not well-formed XML (unescaped <)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, mathml
>>> from xml.dom.minidom import parseString
>>> x, y = symbols('x y')
>>> mathml(x < y, printer='presentation')
'<mrow><mi>x</mi><mo><</mo><mi>y</mi></mrow>'
>>> parseString(mathml(x < y, printer='presentation'))
Traceback (most recent call last):
...
xml.parsers.expat.ExpatError: not well-formed (invalid token): line 1, column 21
```

### Expected
```pycon
>>> _ = parseString(mathml(x < y, printer='presentation'))
```

### Why it is wrong
A bare `<` in text content is not allowed in XML, so the output cannot be parsed or embedded in an XML/XHTML document. `>` is tolerated by XML but should be escaped for consistency.

### Related
[sympy/sympy#25271](https://redirect.github.com/sympy/sympy/issues/25271)

### Notes on fixing
`MathMLPresentationPrinter.mathml_tag` (`sympy/printing/mathml.py`) maps `StrictLessThan` to `'<'`, and the base printer replaces `createTextNode` with a raw (unescaped) text node, so it is written verbatim. Use `'&lt;'` (and `'&gt;'`).
`test_print_logic` in `sympy/printing/tests/test_mathml.py` asserts the broken output (`<mo><</mo>`), so it must be updated.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
