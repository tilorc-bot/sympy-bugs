# smtlib_code() compares an Int with a Real without to_real: (> b a)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, smtlib_code
>>> a = symbols('a', integer=True)
>>> b = symbols('b', real=True)
>>> print(smtlib_code(b > a))
(declare-const a Int)
(declare-const b Real)
(assert (> b a))
```

### Expected
```pycon
>>> 'to_real' in smtlib_code(b > a)
True
```

### Why it is wrong
SMT-LIB's `Reals_Ints` theory has no implicit conversion: `>` needs two `Real` or two `Int` arguments, and an `Int` term is converted with `(to_real a)`. cvc5 1.4.2 with `--strict-parsing` rejects `(> b a)`; z3 converts silently.

### Notes on fixing
`sympy/printing/smtlib.py:SMTLibPrinter` prints every operator with `_s_expr` and never looks at the declared sorts of the arguments. Mixed `Int`/`Real` arguments of arithmetic and relational operators need `to_real` around the `Int` ones. Asserted by `test_Pow` in `sympy/printing/tests/test_smtlib.py` (`(assert (= (> b a) c))`). The printer's defaults are "based on dReal" (comment in `SMTLibPrinter`), so some of this may be deliberate; if so the docstring should say the output is not standard SMT-LIB.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
