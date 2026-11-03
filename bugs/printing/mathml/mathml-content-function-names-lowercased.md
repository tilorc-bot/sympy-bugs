# Content MathML turns function names into lowercased element names: F(x) and f(x) print the same, Ci(x) becomes <ci/>

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Function, Ci, mathml
>>> x = symbols('x')
>>> F, f = Function('F'), Function('f')
>>> mathml(F(x)), mathml(f(x))
('<apply><f/><ci>x</ci></apply>', '<apply><f/><ci>x</ci></apply>')
>>> mathml(Ci(x))
'<apply><ci/><ci>x</ci></apply>'
>>> mathml(Function("f'")(x))
"<apply><f'/><ci>x</ci></apply>"
```

### Expected
```pycon
>>> from xml.dom.minidom import parseString
>>> mathml(F(x)) != mathml(f(x))
True
>>> '<ci/>' in mathml(Ci(x))
False
>>> _ = parseString(mathml(Function("f'")(x)))
```

### Why it is wrong
`<f/>` and `<F/>` are not MathML elements; the lowercasing makes `F(x)` and `f(x)` identical, `Ci(x)` collides with the identifier element `<ci>`, and a name such as `f'` gives ill-formed XML.

### Related
[sympy/sympy#25271](https://redirect.github.com/sympy/sympy/issues/25271)

### Notes on fixing
`MathMLContentPrinter._print_Function` (`sympy/printing/mathml.py`) uses `self.mathml_tag(e)` as the operator element, and `mathml_tag` falls back to `e.__class__.__name__.lower()` for any name not in its table. Functions with no content-MathML element should be printed as an identifier operator, e.g. `<apply><ci type="function">F</ci>...` (with the name escaped).
`test_print_derivative` in `sympy/printing/tests/test_mathml.py` asserts `<apply><f/>...` for an undefined function `f`, so it must be updated.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
