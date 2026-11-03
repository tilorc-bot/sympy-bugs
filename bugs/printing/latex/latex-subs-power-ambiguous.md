# Subs(f(x), x, 1)**2 prints like an evaluation between limits 1 and 2

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, Subs, latex
>>> x = symbols('x')
>>> f = Function('f')
>>> print(latex(Subs(f(x), x, 1)**2))
\left. f{\left(x \right)} \right|_{\substack{ x=1 }}^{2}
```

### Expected
```pycon
>>> latex(Subs(f(x), x, 1)**2).endswith(r'\right)^{2}')
True
```

### Why it is wrong
`\left. f(x) \right|_{x=1}^{2}` is standard notation for evaluating between the limits 1 and 2 (`f(2) - f(1)`), not for the square of `f(1)`.

### Notes on fixing
`Subs` has no entry in `sympy/printing/precedence.py`, so it gets Atom precedence and `LatexPrinter._helper_print_standard_power` (`parenthesize(base, PRECEDENCE['Pow'])`) never brackets it. Giving `Subs` a lower traditional precedence, or bracketing it in `_print_Pow`, would fix it.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
