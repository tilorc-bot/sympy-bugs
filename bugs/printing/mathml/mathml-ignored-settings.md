# mathml() accepts symbol_names, inv_trig_style, fold_func_brackets and long_frac_ratio but ignores them

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import symbols, asin, mathml
>>> x = symbols('x')
>>> mathml(x, printer='presentation', symbol_names={x: 'y'})
'<mi>x</mi>'
>>> mathml(asin(x), printer='presentation', inv_trig_style='power')
'<mrow><mi>arcsin</mi><mrow><mo>(</mo><mi>x</mi><mo>)</mo></mrow></mrow>'
```

### Expected
```pycon
>>> mathml(x, printer='presentation', symbol_names={x: 'y'}) != mathml(x, printer='presentation')
True
>>> mathml(asin(x), printer='presentation', inv_trig_style='power') != mathml(asin(x), printer='presentation')
True
```

### Why it is wrong
The settings are accepted without error (they are in the printer's default settings), so a user who passes them gets no warning that nothing happens.

### Notes on fixing
`MathMLPrinterBase._default_settings` (`sympy/printing/mathml.py`) declares `symbol_names`, `inv_trig_style`, `fold_func_brackets` and `long_frac_ratio`, but nothing in `mathml.py` reads them. Either implement them like the LaTeX printer does, or remove them so that passing them raises `TypeError: Unknown setting`. `fold_func_brackets` and `long_frac_ratio` are not checked in Expected because their effect in MathML is not obvious.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
