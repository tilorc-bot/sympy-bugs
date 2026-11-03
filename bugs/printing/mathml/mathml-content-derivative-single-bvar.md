# All variables of a mixed partial derivative go into one <bvar> (content MathML)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Function, Derivative, mathml
>>> x, y = symbols('x y')
>>> f = Function('f')
>>> mathml(Derivative(f(x, y), x, y))
'<apply><partialdiff/><bvar><ci>y</ci><ci>x</ci></bvar><apply><f/><ci>x</ci><ci>y</ci></apply></apply>'
```

### Expected
```pycon
>>> mathml(Derivative(f(x, y), x, y)).count('<bvar>')
2
```

### Why it is wrong
In content MathML each `<bvar>` holds one bound variable (with an optional `<degree>`); several `<ci>` in one `<bvar>` is not valid, and the `<degree>` of one variable cannot be told apart from the next variable.

### Notes on fixing
`MathMLContentPrinter._print_Derivative` (`sympy/printing/mathml.py`) creates one `bvar` element before the loop over `e.variable_count` and appends every variable to it; create one `bvar` per variable inside the loop.
`test_print_derivative` in `sympy/printing/tests/test_mathml.py` asserts the single-`bvar` output, so it must be updated.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
