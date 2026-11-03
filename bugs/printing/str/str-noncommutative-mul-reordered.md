# An unevaluated noncommutative Mul moves a B**-1 factor behind later factors

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mul
>>> A, B = symbols('A B', commutative=False)
>>> e = Mul(B**-1, A, 2, evaluate=False)
>>> print(e)
A*2/B
>>> print(e.doit())
2*B**(-1)*A
```

### Expected
```pycon
>>> eval(str(e), {'A': A, 'B': B}) == e.doit()
True
```

### Why it is wrong
`A*2/B` means `2*A*B**(-1)`, but the expression is `2*B**(-1)*A`; for noncommuting factors the order matters, so the printed product is a different value.

### Notes on fixing
`sympy/printing/str.py:StrPrinter._print_Mul`, branch for unevaluated Muls: `sift` moves every factor that is a `Pow` with negative exponent into the denominator `d` without checking `is_commutative`, then prints `numerator/denominator`. Noncommutative negative powers must stay in place among the numerator factors (the evaluated branch below already checks `item.is_commutative`). With the issue's `MatrixSymbol` operands the expression is a different class and prints correctly (`2*B**(-1)*A`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
