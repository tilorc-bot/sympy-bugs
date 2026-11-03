# Part of function names like reduced_totient and riemann_xi is rendered as a subscript

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, pretty, reduced_totient, divisor_sigma, riemann_xi
>>> n, x = symbols('n x')
>>> print(pretty(reduced_totient(n), use_unicode=True))
reducedₜₒₜᵢₑₙₜ(n)
>>> print(pretty(riemann_xi(x), use_unicode=True))
riemannₓᵢ(x)
>>> print(pretty(divisor_sigma(n), use_unicode=True))
divisor_σ(n)
```

### Expected
```pycon
>>> 'ₜₒₜᵢₑₙₜ' not in pretty(reduced_totient(n), use_unicode=True)
True
>>> 'ₓᵢ' not in pretty(riemann_xi(x), use_unicode=True)
True
>>> '_σ' not in pretty(divisor_sigma(n), use_unicode=True)
True
```

### Why it is wrong
These are names of functions, not a symbol with an index: `reducedₜₒₜᵢₑₙₜ(n)` reads as a function `reduced` with subscript `totient`. The LaTeX printer prints `\lambda`, `\sigma` etc. for them.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._helper_print_function` prints the function name via `self._print(Symbol(func_name))`, so `pretty_symbol` splits it at `_` into name and subscript (and translates Greek names like `sigma`, `xi`). That is wanted for user functions such as `Function('f_1')` (`f₁`), so the fix belongs in dedicated `_print_reduced_totient`, `_print_divisor_sigma`, `_print_udivisor_sigma` (`udivisor_σ(n)`) and `_print_riemann_xi` methods that pass an explicit `func_name` (e.g. `λ`, `σ`, `σ*`, `ξ`, matching the LaTeX printer), or in printing names of built-in functions without symbol splitting.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
