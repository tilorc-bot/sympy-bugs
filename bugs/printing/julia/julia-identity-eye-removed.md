# Identity(3) prints eye(3), which was removed in Julia 1.0

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Identity, julia_code
>>> print(julia_code(Identity(3)))
eye(3)
```

### Expected
```pycon
>>> 'eye(' in julia_code(Identity(3))
False
```

### Why it is wrong
`eye` was deprecated in Julia 0.7 and removed in 1.0. The reviewer ran the output with Julia 1.12: `UndefVarError: eye not defined`. The current spelling is `I` from `LinearAlgebra` (e.g. `Matrix{Float64}(I, 3, 3)`, or plain `I` inside an expression).

### Notes on fixing
`sympy/printing/julia.py:JuliaCodePrinter._print_Identity` returns `"eye(%s)"`. The output is asserted by `test_special_matrices` (`julia_code(A*(B + 3*Identity(n))) == "A * (3 * eye(n) + B)"`, `julia_code(6*Identity(3)) == "6 * eye(3)"`) in `sympy/printing/tests/test_julia.py` (tested-buggy), which needs updating with the fix.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
