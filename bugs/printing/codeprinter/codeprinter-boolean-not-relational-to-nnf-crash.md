# Code printers raise ValueError for Xor/Equivalent containing an unevaluated Not(x + 1 < 0)

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Not, Xor, Equivalent, ITE, ccode, pycode, fcode
>>> x, y, z = symbols('x y z')
>>> e = Not(x + 1 < 0, evaluate=False)
>>> ccode(Xor(e, y < 0))
Traceback (most recent call last):
...
ValueError: Illegal operator <class 'sympy.core.relational.StrictLessThan'> in expression
>>> pycode(Equivalent(e, y < 0))
Traceback (most recent call last):
...
ValueError: Illegal operator <class 'sympy.core.relational.StrictLessThan'> in expression
>>> fcode(ITE(e, y < 0, z < 0))
Traceback (most recent call last):
...
ValueError: Illegal operator <class 'sympy.core.relational.StrictLessThan'> in expression
```

### Expected
```pycon
>>> _ = ccode(Xor(e, y < 0))
>>> _ = pycode(Equivalent(e, y < 0))
>>> _ = fcode(ITE(e, y < 0, z < 0))
```

### Why it is wrong
Printing must not fail for a valid expression. The same printers handle `Not(x < 0, evaluate=False)` and `Not(x + 1 < 0)` without `evaluate=False`.

### Notes on fixing
The printers convert these to negation normal form (`CodePrinter._print_Xor`/`_print_Equivalent`/`_print_BooleanFunction` in `sympy/printing/codeprinter.py` call `expr.to_nnf()`), and `Not.to_nnf` (`sympy/logic/boolalg.py`) raises: `is_literal(Not(x + 1 < 0))` is False because the relational has a non-atomic operand, and `Not.to_nnf` has no branch for a relational argument. `Not(x + 1 < 0, evaluate=False).to_nnf()` alone raises the same error. `Not.to_nnf` should return `self` (or the negated relational) for a relational argument. Affects every printer that reaches `to_nnf` (Xor and Equivalent in C, JS, Python, Octave, Julia, Rust; ITE in printers without `_print_ITE` such as Fortran, JS, Octave, Julia). `Implies` is not affected.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
