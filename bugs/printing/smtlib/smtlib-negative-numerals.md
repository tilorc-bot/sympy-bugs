# Negative numbers print as -1, which is not an SMT-LIB numeral

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Integer, Rational, smtlib_code
>>> x = symbols('x')
>>> print(smtlib_code(Integer(-1)))
-1
>>> print(smtlib_code(Rational(-3, 7)))
(/ -3 7)
>>> print(smtlib_code(-x, auto_declare=False))
(* -1 x)
```

### Expected
```pycon
>>> import re
>>> re.search(r'(?<![\w.])-\d', smtlib_code(Integer(-1))) is None
True
>>> re.search(r'(?<![\w.])-\d', smtlib_code(Rational(-3, 7))) is None
True
>>> re.search(r'(?<![\w.])-\d', smtlib_code(-x, auto_declare=False)) is None
True
```

### Why it is wrong
SMT-LIB numerals and decimals are non-negative; a negative constant is written `(- 1)`. cvc5 1.4.2 with `--strict-parsing` rejects `-1`, `(/ -3 7)` and `(* -1 x)` (z3 accepts them as an extension). The printer's docstring promises defaults "compatible with several solvers".

### Notes on fixing
`sympy/printing/smtlib.py:SMTLibPrinter._print_Integer`, `_print_Rational` and `_print_Float` print the sign as part of the number. Negative values should be printed as `(- n)`. Asserted by `test_Integer`, `test_Rational` and `test_basic_ops` in `sympy/printing/tests/test_smtlib.py`, and `test_parse_negative_literals` in `sympy/parsing/tests/test_smtlib_parser.py` uses printed negative literals too. The printer's defaults are "based on dReal" (comment in `SMTLibPrinter`), so check whether dReal accepts `(- 1)` before changing the default.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
