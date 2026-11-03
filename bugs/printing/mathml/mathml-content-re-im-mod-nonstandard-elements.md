# re, im and Mod print as <re/>, <im/> and <mod/>, which are not MathML elements

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, re, im, Mod, mathml
>>> x, y = symbols('x y')
>>> mathml(re(x)), mathml(im(x))
('<apply><re/><ci>x</ci></apply>', '<apply><im/><ci>x</ci></apply>')
>>> mathml(Mod(x, y))
'<apply><mod/><ci>x</ci><ci>y</ci></apply>'
```

### Expected
```pycon
>>> '<real/>' in mathml(re(x)), '<imaginary/>' in mathml(im(x))
(True, True)
>>> '<rem/>' in mathml(Mod(x, y))
True
```

### Why it is wrong
Content MathML has `<real/>`, `<imaginary/>` and `<rem/>` for these operations; `<re/>`, `<im/>` and `<mod/>` are unknown elements that MathML consumers cannot interpret.

### Related
[sympy/sympy#25271](https://redirect.github.com/sympy/sympy/issues/25271)

### Notes on fixing
`MathMLContentPrinter.mathml_tag` (`sympy/printing/mathml.py`) has no entries for `re`, `im` and `Mod`, so the lowercased class name is used. Adding `'re': 'real', 'im': 'imaginary', 'Mod': 'rem'` to the `translate` table fixes it. (MathML does not specify the sign convention of `rem`; SymPy's `Mod` takes the sign of the divisor.)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
