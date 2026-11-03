# rcode(erf(x)) prints erf(x), but base R has no erf function

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, erf, rcode
>>> x = symbols('x')
>>> print(rcode(erf(x)))
erf(x)
```

### Expected
```pycon
>>> rcode(erf(x)) != 'erf(x)'
True
```

### Why it is wrong
Base R does not define `erf` (it is only in add-on packages such as `pracma`), so the generated code fails with `could not find function "erf"`. The standard base-R expression is `2*pnorm(x*sqrt(2)) - 1`. The reviewer checked this against the R documentation.

### Notes on fixing
`sympy/printing/rcode.py`: `known_functions` maps `"erf": "erf"`. It should print `2*pnorm(sqrt(2)*x) - 1` (e.g. in a `_print_erf`) or be removed from `known_functions`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
