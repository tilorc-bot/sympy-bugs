# mathematica_code(UnevaluatedExpr(x)*UnevaluatedExpr(y)) prints 1*x**y (NonCommutativeMultiply)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, UnevaluatedExpr
>>> from sympy.printing.mathematica import mathematica_code
>>> x, y = symbols('x y')
>>> print(mathematica_code(UnevaluatedExpr(x)*UnevaluatedExpr(y)))
1*x**y
>>> print(mathematica_code(x*y))
x*y
```

### Expected
```pycon
>>> '**' in mathematica_code(UnevaluatedExpr(x)*UnevaluatedExpr(y))
False
```

### Why it is wrong
`**` is `NonCommutativeMultiply` in the Wolfram Language, which is not `Times`: the product of two ordinary scalars becomes an unevaluated non-commutative product. The leading `1*` is noise. The reviewer checked this against the Wolfram Language documentation.

### Notes on fixing
`sympy/printing/mathematica.py:MCodePrinter._print_Mul` splits factors with `expr.args_cnc()`, which treats every factor whose `is_commutative` is not `True` as non-commutative. `UnevaluatedExpr(x).is_commutative` is `None`, so both factors land in the non-commutative part, and the empty commutative part prints as `1`. The printer should treat only factors with `is_commutative is False` as non-commutative (or `UnevaluatedExpr` should inherit `is_commutative` from its argument), and should omit the `1*` when there are no commutative factors (`A*B` with non-commutative `A`, `B` also prints `1*A**B`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
