# Factors that follow a Sum, Product or Limit in a Mul end up inside its body

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Sum, Product, Limit, sin, pretty
>>> k, n, x = symbols('k n x')
>>> print(pretty(Sum(1/k, (k, 1, n))*Limit(sin(k*x)/x, x, 0), use_unicode=True))
 n
____
╲
 ╲
  ╲   1      ⎛sin(k⋅x)⎞
  ╱   ─⋅ lim ⎜────────⎟
 ╱    k x─→0⁺⎝   x    ⎠
╱
‾‾‾‾
k = 1
>>> print(pretty(Product(k, (k, 1, n))*Sum(1/k, (k, 1, n)), use_unicode=True))
         n
        ____
        ╲
  n      ╲
─┬─┬─     ╲   1
 │ │  k⋅  ╱   ─
 │ │     ╱    k
k = 1   ╱
        ‾‾‾‾
        k = 1
```

### Expected
```pycon
>>> p = pretty(Sum(1/k, (k, 1, n))*Limit(sin(k*x)/x, x, 0), use_unicode=True)
>>> p.splitlines()[0].lstrip()[0]  # the Sum is enclosed in parentheses
'⎛'
>>> '⎛' in pretty(Product(k, (k, 1, n))*Sum(1/k, (k, 1, n)), use_unicode=True)
True
```

### Why it is wrong
The first picture reads as `Σ_k (1/k · lim sin(kx)/x)`, which binds the free `k` of the Limit to the summation index (and equals `n`), while the expression is `H_n · k`. The second reads as `∏_k (k · Σ 1/k)`, i.e. `n!·H_n^n` instead of `n!·H_n`.

### Notes on fixing
`_print_Sum`, `_print_Product` and `_print_Limit` in `sympy/printing/pretty/pretty.py` return pictures with `binding=prettyForm.MUL`, and `prettyForm.__mul__` (`sympy/printing/pretty/stringpict.py`) only parenthesizes factors with binding weaker than MUL, so nothing marks where the body ends. `PrettyPrinter._print_Mul` (or `__mul__`) should parenthesize such a factor when it is not the last one (the LaTeX printer prints `\left(\sum_{k=1}^{n} \frac{1}{k}\right) \lim ...`). Integrals are not affected because `dx` closes the body.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
