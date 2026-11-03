# use_unicode=False still prints ∇ and ∆ for sympy.vector Gradient and Laplacian

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import pretty
>>> from sympy.vector import CoordSys3D, Gradient, Laplacian
>>> N = CoordSys3D('N')
>>> print(pretty(Gradient(N.x), use_unicode=False))
∇(x_N)
>>> print(pretty(Laplacian(N.x), use_unicode=False))
∆(x_N)
```

### Expected
```pycon
>>> pretty(Gradient(N.x), use_unicode=False).isascii()
True
>>> pretty(Laplacian(N.x), use_unicode=False).isascii()
True
```

### Why it is wrong
`use_unicode=False` is meant to produce pure ASCII, but these operators always use the Unicode symbols NABLA and INCREMENT.

### Notes on fixing
`sympy/printing/pretty/pretty.py`: `_print_Cross`, `_print_Curl`, `_print_Divergence`, `_print_Dot`, `_print_Gradient` and `_print_Laplacian` call `U('NABLA')`, `U('INCREMENT')`, `U('MULTIPLICATION SIGN')`, `U('DOT OPERATOR')` without checking `self._use_unicode`. `Curl`, `Divergence`, `Cross` and `Dot` have the same unconditional Unicode symbols, but are not reachable in ASCII mode today because their vector arguments raise `NotImplementedError` ("ASCII pretty printing of BasisDependent is not implemented"). They need ASCII fallbacks (e.g. `grad`, `laplace`/`div(grad(...))`, `curl`, `div`, `x` and `.`), or should be routed through `pretty_atom` with an ASCII default.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
