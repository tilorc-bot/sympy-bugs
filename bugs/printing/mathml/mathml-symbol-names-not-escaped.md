# MathML does not escape < and & in symbol names, giving ill-formed XML

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, mathml
>>> from xml.dom.minidom import parseString
>>> mathml(Symbol('a<b'), printer='presentation')
'<mi>a<b</mi>'
>>> mathml(Symbol('a&b'))
'<ci>a&b</ci>'
```

### Expected
```pycon
>>> _ = parseString(mathml(Symbol('a<b'), printer='presentation'))
>>> _ = parseString(mathml(Symbol('a&b')))
```

### Why it is wrong
`<` and `&` must be escaped in XML text; the output cannot be parsed or embedded.

### Related
[sympy/sympy#25271](https://redirect.github.com/sympy/sympy/issues/25271)

### Notes on fixing
`MathMLPrinterBase.__init__` (`sympy/printing/mathml.py`) replaces `self.dom.createTextNode` with a `RawText` node that writes its data unescaped, so that entity strings like `&#x2192;` can be passed through. User-supplied text (symbol and function names) therefore needs to be escaped explicitly (`xml.sax.saxutils.escape`) in both printers' `_print_Symbol` and wherever names are emitted, or raw text should be limited to the printer's own entity strings.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
