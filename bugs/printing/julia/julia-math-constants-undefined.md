# E*x prints e * x; e, eulergamma, catalan and golden are undefined in Julia

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, E, EulerGamma, Catalan, GoldenRatio, julia_code
>>> x = symbols('x')
>>> print(julia_code(E*x))
e * x
>>> print(julia_code(x + EulerGamma + Catalan + GoldenRatio))
x + eulergamma + catalan + golden
```

### Expected
```pycon
>>> [julia_code(c) in ('e', 'eulergamma', 'catalan', 'golden') for c in (E, EulerGamma, Catalan, GoldenRatio)]
[False, False, False, False]
```

### Why it is wrong
Since Julia 1.0 these names are not exported from `Base`; they only exist as `Base.MathConstants.e`, `.eulergamma`, `.catalan`, `.golden` (Base exports `ℯ`, `pi` and `π`). The reviewer ran the output with Julia 1.12: `UndefVarError: e not defined` (and likewise for the others).

### Notes on fixing
`sympy/printing/julia.py:JuliaCodePrinter._print_Exp1`, `_print_EulerGamma`, `_print_Catalan` and `_print_GoldenRatio` return `"e"`, `"eulergamma"`, `"catalan"` and `"golden"` (with the default `inline=True`). They should print qualified names such as `MathConstants.e` / `Base.MathConstants.eulergamma`, or `ℯ` for `E`.

The wrong strings are asserted by `test_mix_number_mult_symbols` and `test_constants` / `test_constants_other` in `sympy/printing/tests/test_julia.py` (tested-buggy), which need updating with the fix.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
