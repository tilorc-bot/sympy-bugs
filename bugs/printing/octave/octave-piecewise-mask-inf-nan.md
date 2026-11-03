# octave_code(Piecewise((1/x, x > 0), (oo, True))) gives NaN: the inactive infinite branch is multiplied by a 0 mask

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Piecewise, oo, octave_code
>>> x = symbols('x')
>>> print(octave_code(Piecewise((1/x, x > 0), (oo, True))))
((x > 0).*(1./x) + (~(x > 0)).*(inf))
```

### Expected
```pycon
>>> import re
>>> re.search(r'\.\*\s*\(?inf', octave_code(Piecewise((1/x, x > 0), (oo, True)))) is None
True
```

### Why it is wrong
The inline form computes `mask1.*branch1 + mask2.*branch2`. At `x = 1` the second term is `0.*Inf = NaN`, so the result is `NaN` instead of `1`; at `x = 0` the first branch `1./0 = Inf` is masked to `NaN` in the same way. Any branch that is infinite (or NaN) where it is not selected poisons the result. The reviewer checked this against the Octave/IEEE semantics of `0*Inf`.

### Notes on fixing
`sympy/printing/octave.py:OctaveCodePrinter._print_Piecewise` (the `inline` branch) builds the expression from products with logical masks. A correct inline form needs selection instead of multiplication, e.g. `merge(x > 0, 1./x, inf)` (Octave's `merge`/`ifelse`, element-wise for arrays), or masking the branch values before combining them.

### Related
[sympy/sympy#15012](https://redirect.github.com/sympy/sympy/issues/15012)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
