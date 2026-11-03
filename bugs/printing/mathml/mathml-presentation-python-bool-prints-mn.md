# Python True prints as <mi>mn</mi> (presentation MathML)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import S, mathml
>>> mathml(True, printer='presentation')
'<mi>mn</mi>'
>>> mathml(S.true, printer='presentation')
'<mi>True</mi>'
```

### Expected
```pycon
>>> t = mathml(S.true, printer='presentation')
>>> mathml(True, printer='presentation') == t
True
```

### Why it is wrong
`True` is shown as the identifier "mn".

### Notes on fixing
`MathMLPresentationPrinter._print_bool` (`sympy/printing/mathml.py`) prints `self.mathml_tag(e)`. For a Python `bool`, the MRO walk in `mathml_tag` finds `int` before anything else and returns `'mn'`. `_print_bool` should print `'True'`/`'False'` for Python bools directly (or sympify them).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
