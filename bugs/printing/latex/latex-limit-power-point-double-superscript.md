# latex() of a Limit whose point is a power gives a double superscript (a^{2}^+)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Function, Limit, latex
>>> x, a = symbols('x a')
>>> f = Function('f')
>>> print(latex(Limit(f(x), x, a**2)))
\lim_{x \to a^{2}^+} f{\left(x \right)}
```

### Expected
```pycon
>>> '^{2}^' in latex(Limit(f(x), x, a**2))
False
```

### Why it is wrong
`a^{2}^+` is a TeX "Double superscript" error, so the output does not compile.

### Caused by
[latex-limit-direction-on-last-term](latex-limit-direction-on-last-term.md)

### Related
[sympy/sympy#8175](https://redirect.github.com/sympy/sympy/issues/8175)

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Limit` appends `^+`/`^-` to the printed point. Parenthesizing the point at Pow precedence (non-strict) fixes this together with the wrong-meaning cases of the root cause.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
