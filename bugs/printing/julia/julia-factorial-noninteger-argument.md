# factorial(x) prints factorial(x) for non-integer x, a MethodError in Julia

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, factorial, julia_code
>>> x = symbols('x', noninteger=True)
>>> print(julia_code(factorial(x)))
factorial(x)
```

### Expected
```pycon
>>> julia_code(factorial(x)) != 'factorial(x)'
True
```

### Why it is wrong
Julia's `factorial` is only defined for integers; calling it on a `Float64` raises a `MethodError` (the reviewer ran this with Julia 1.12). For a non-integer argument SymPy's `factorial(x)` is `gamma(x + 1)`, which Julia (SpecialFunctions) provides.

### Notes on fixing
`sympy/printing/julia.py`: `"factorial"` is in `known_fcns_src1`, so it is printed unchanged for any argument. A `_print_factorial` should print `factorial(n)` only when the argument is known to be an integer and `gamma(x + 1)` otherwise (the generic `CodePrinter` rewrite of `factorial` to `gamma` already exists, but is bypassed because `factorial` is a known function).

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
