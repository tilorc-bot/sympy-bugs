# pretty() prints exp_polar(x) exactly like exp(x)

### Kind
lossy

### Actual
```pycon
>>> from sympy import symbols, exp, exp_polar, pretty
>>> x = symbols('x')
>>> print(pretty(exp_polar(x), use_unicode=True))
 x
ℯ
>>> print(pretty(exp(x), use_unicode=True))
 x
ℯ
```

### Expected
```pycon
>>> pretty(exp_polar(x), use_unicode=True) != pretty(exp(x), use_unicode=True)
True
```

### Why it is wrong
`exp_polar(x)` lives on the Riemann surface of the logarithm and behaves differently from `exp(x)` (e.g. `exp_polar(2*pi*I) != 1`); displaying both the same hides why results involving them differ.

### Notes on fixing
`sympy/printing/pretty/pretty.py:PrettyPrinter._print_ExpBase` handles both classes and prints `e**arg`; there is a `TODO should exp_polar be printed differently?` comment there. A dedicated `_print_exp_polar` (e.g. `exp_polar(x)`) is needed. The LaTeX printer has the same problem (`latex(exp_polar(x))` is `e^{x}`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
