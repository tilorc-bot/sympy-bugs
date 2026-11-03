# mathematica_code prints floor, ceiling, sign and frac with lower-case names, which are undefined in Mathematica

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, floor, ceiling, sign, frac
>>> from sympy.printing.mathematica import mathematica_code
>>> x = symbols('x')
>>> [mathematica_code(f(x)) for f in (floor, ceiling, sign, frac)]
['floor[x]', 'ceiling[x]', 'sign[x]', 'frac[x]']
```

### Expected
```pycon
>>> [mathematica_code(f(x))[0].isupper() for f in (floor, ceiling, sign, frac)]
[True, True, True, True]
```

### Why it is wrong
Wolfram Language built-ins are capitalized (`Floor`, `Ceiling`, `Sign`); `floor[x]` etc. are undefined symbols and stay unevaluated. The reviewer checked this against the Wolfram Language documentation.

### Notes on fixing
`sympy/printing/mathematica.py`: these functions are missing from `known_functions`, so `MCodePrinter._print_Function` falls back to the SymPy name. Add `"floor": "Floor"`, `"ceiling": "Ceiling"`, `"sign": "Sign"`. For `frac` note that SymPy's `frac(x)` is `x - floor(x)` while Mathematica's `FractionalPart[x]` is `x - IntegerPart[x]` (different for negative `x`), so it should print `x - Floor[x]` or `Mod[x, 1]` (for real `x`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
