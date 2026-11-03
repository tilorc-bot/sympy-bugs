# legendre(n, x) prints legendre(n, x), which in Octave returns all associated functions P_n^m

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, legendre, octave_code
>>> n, x = symbols('n x')
>>> print(octave_code(legendre(n, x)))
legendre(n, x)
```

### Expected
```pycon
>>> octave_code(legendre(n, x)) != 'legendre(n, x)'
True
```

### Why it is wrong
Octave's `legendre(n, x)` returns the associated Legendre functions P_n^m(x) for all m = 0..n as an (n+1)-row array, not the Legendre polynomial P_n(x); only its first row is SymPy's `legendre(n, x)`. Used in an arithmetic expression the result has the wrong shape and wrong values (for n >= 1). The reviewer checked this against the Octave documentation.

### Notes on fixing
`sympy/printing/octave.py`: `"legendre"` is in `known_fcns_src1` (same name in SymPy and Octave). It needs its own printer that selects the m = 0 row (e.g. `legendre(n, x)(1, :)`, which Octave allows only as a statement on a named result, so a helper or `reshape` may be needed), or should be marked unsupported. The current output is asserted by `test_Function` in `sympy/printing/tests/test_octave.py` (`mcode(legendre(x, y)) == "legendre(x, y)"`, tested-buggy).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
