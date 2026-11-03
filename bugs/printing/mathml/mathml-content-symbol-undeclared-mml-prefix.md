# A subscripted symbol uses the mml: prefix without declaring it (content MathML)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, mathml
>>> from xml.dom.minidom import parseString
>>> mathml(Symbol('x_1'))
'<ci><mml:msub><mml:mi>x</mml:mi><mml:mi>1</mml:mi></mml:msub></ci>'
>>> parseString(mathml(Symbol('x_1')))
Traceback (most recent call last):
...
xml.parsers.expat.ExpatError: unbound prefix: line 1, column 4
```

### Expected
```pycon
>>> _ = parseString(mathml(Symbol('x_1')))
```

### Why it is wrong
A namespace-aware XML parser rejects the undeclared `mml:` prefix, and nothing else in the output (which has no root `math` element) declares it.

### Notes on fixing
`MathMLContentPrinter._print_Symbol` (`sympy/printing/mathml.py`) creates `mml:msub`, `mml:msup`, `mml:msubsup`, `mml:mi`, `mml:mrow` and `mml:mo` elements. Either drop the prefix (MathML allows presentation markup inside `<ci>`) or declare `xmlns:mml="http://www.w3.org/1998/Math/MathML"` on the element.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
