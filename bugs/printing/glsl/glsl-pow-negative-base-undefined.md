# glsl_code(x**2) prints pow(x, 2.0), which GLSL leaves undefined for x < 0

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.printing.glsl import glsl_code
>>> x = symbols('x')
>>> print(glsl_code(x**2))
pow(x, 2.0)
```

### Expected
```pycon
>>> glsl_code(x**2) != 'pow(x, 2.0)'
True
```

### Why it is wrong
The GLSL specification states that `pow(x, y)` is undefined if `x < 0` (and if `x = 0` and `y <= 0`); real implementations return NaN for negative bases. `x**2` is defined for every `x`, so the generated shader gives wrong results for negative `x`. Integer powers should be expanded into products (`x*x`). The reviewer checked this against the GLSL specification only.

### Notes on fixing
`sympy/printing/glsl.py:GLSLPrinter._print_Pow` prints every power except `-1` and `1/2` as `pow(base, float(exp))`. For small integer exponents it should print repeated multiplication (negative ones as `1.0/(...)`). `test_glsl_code_Pow` in `sympy/printing/tests/test_glsl.py` asserts `pow(x, 3.0)` for `x**3`, so it needs updating with the fix.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
