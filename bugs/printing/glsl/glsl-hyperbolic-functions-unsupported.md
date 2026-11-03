# glsl_code(sinh(x)) raises "Unsupported" although GLSL has sinh, cosh, tanh, asinh, acosh, atanh

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, sinh
>>> from sympy.printing.glsl import glsl_code
>>> x = symbols('x')
>>> glsl_code(sinh(x))
Traceback (most recent call last):
...
sympy.printing.codeprinter.PrintMethodNotImplementedError: Unsupported by <class 'sympy.printing.glsl.GLSLPrinter'>: sinh...
```

### Expected
```pycon
>>> _ = glsl_code(sinh(x))
```

### Why it is wrong
`sinh`, `cosh`, `tanh`, `asinh`, `acosh` and `atanh` are GLSL built-ins since GLSL 1.30, so these functions should be printable. The reviewer checked this against the GLSL specification only.

### Notes on fixing
`sympy/printing/glsl.py`: `known_functions` has no hyperbolic functions (nor `sqrt`, `exp2`, `log2`, ...). Adding `'sinh': 'sinh'`, `'cosh': 'cosh'`, `'tanh': 'tanh'`, `'asinh': 'asinh'`, `'acosh': 'acosh'`, `'atanh': 'atanh'` fixes this.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
