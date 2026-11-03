# The quotient of two integer symbols becomes C integer division

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mod, ccode
>>> p1, p2 = symbols('p1 p2', integer=True)
>>> print(ccode(p1/p2))
p1/p2
>>> q1, q2 = symbols('q1 q2', integer=True, positive=True)
>>> print(ccode(-q1/Mod(q1, q2)))
-q1/(q1 % q2)
>>> from codecheck import run_code
>>> run_code('c', ccode(p1/p2), p1=7, p2=4), float((p1/p2).subs({p1: 7, p2: 4}))
(1.0, 1.75)
>>> e = -q1/Mod(q1, q2)
>>> run_code('c', ccode(e), q1=7, q2=4), float(e.subs({q1: 7, q2: 4}))
(-2.0, -2.3333333333333335)
```

### Expected
```pycon
>>> run_code('c', ccode(p1/p2), p1=7, p2=4)
1.75
>>> abs(run_code('c', ccode(e), q1=7, q2=4) - float(e.subs({q1: 7, q2: 4}))) < 1e-12
True
```

### Why it is wrong
`p1/p2` in SymPy is exact division, but with integer operands (which is how `codegen` declares integer symbols, `double ratio(int p1, int p2)`) C truncates: `ratio(7, 4)` returns 1 instead of 7/4, and `-q1/(q1 % q2)` is -2 at (7, 4) instead of -7/3 (compiled and run with gcc).

### Notes on fixing
The quotient is printed by `sympy/printing/codeprinter.py:CodePrinter._print_Mul`, which C and C++ use unchanged. [sympy/sympy#4428](https://redirect.github.com/sympy/sympy/issues/4428) fixed this only for numeric fractions (`Rational`); when numerator and denominator are both integer-valued, one side needs a cast (e.g. `(double)p1/p2`). C++ (`cxxcode`) prints the same.

The second case is asserted by `test_ccode_functions2` in `sympy/printing/tests/test_c.py` (`ccode(-p1/Mod(p1, p2)) == '-p1/(p1 % p2)'`), so a fix must update that test. The unevaluated literal case `Mul(2, Pow(3, -1), evaluate=False)` → `2/3` is a separate item in [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).

### Related
[sympy/sympy#4428](https://redirect.github.com/sympy/sympy/issues/4428)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
