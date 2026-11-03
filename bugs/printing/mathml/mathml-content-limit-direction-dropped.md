# Limit(f(x), x, 0, '-') and Limit(f(x), x, 0, '+') print identically (content MathML)

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, Function, Limit, mathml
>>> x = symbols('x')
>>> f = Function('f')
>>> mathml(Limit(f(x), x, 0, '-'))
'<apply><limit/><bvar><ci>x</ci></bvar><lowlimit><cn>0</cn></lowlimit><apply><f/><ci>x</ci></apply></apply>'
>>> mathml(Limit(f(x), x, 0, '+'))
'<apply><limit/><bvar><ci>x</ci></bvar><lowlimit><cn>0</cn></lowlimit><apply><f/><ci>x</ci></apply></apply>'
```

### Expected
```pycon
>>> mathml(Limit(f(x), x, 0, '-')) != mathml(Limit(f(x), x, 0, '+'))
True
>>> left = mathml(Limit(f(x), x, 0, '-'))
>>> mathml(Limit(f(x), x, 0, '+')) != left
True
```

### Why it is wrong
One-sided limits from the left and from the right are different values (e.g. for `1/x`), but print identically.

### Notes on fixing
`MathMLContentPrinter._print_Limit` (`sympy/printing/mathml.py`) prints only `e.args[0:3]` and ignores `e.args[3]` (the direction). Content MathML expresses this with `<condition>` and `<tendsto type="above"/>`/`type="below"`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
