# -x/(2/3) as an unevaluated Mul prints -x/2/3

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mul, Pow, Rational, sstr, sympify
>>> x = symbols('x')
>>> e = Mul(-1, x, Pow(Rational(2, 3), -1, evaluate=False), evaluate=False)
>>> print(sstr(e))
-x/2/3
>>> print(sstr(Mul(x, Pow(Rational(2, 3), -1, evaluate=False), evaluate=False)))
x/(2/3)
```

### Expected
```pycon
>>> sympify(sstr(e)) == e.doit()
True
```

### Why it is wrong
`-x/2/3` means `-x/6`, but the expression is `-3*x/2`. The same expression with a positive coefficient is correctly printed as `x/(2/3)`.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Mul` computes `prec = precedence(expr)` before stripping the sign. For a negative product that is Add precedence, so denominator factors with Mul precedence (the Rational `2/3`) are not parenthesized by `self.parenthesize(x, prec, strict=False)`. The factors should be parenthesized against `PRECEDENCE["Mul"]` once the sign has been removed.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
