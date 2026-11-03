# Mod(x, y) prints fmod(x, y), which has the wrong sign for negative operands

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mod
>>> from sympy.printing.c import ccode
>>> x, y = symbols('x y', real=True)
>>> print(ccode(Mod(x, y)))
fmod(x, y)
>>> Mod(-1, 3)
2
>>> from codecheck import run_code
>>> run_code('c', ccode(Mod(x, y)), x=-1.0, y=3.0)
-1.0
```

### Expected
```pycon
>>> run_code('c', ccode(Mod(x, y)), x=-1.0, y=3.0)
2.0
>>> run_code('c', ccode(Mod(x, y)), x=1.0, y=-3.0)
-2.0
```

### Why it is wrong
SymPy's `Mod` takes the sign of the divisor (`Mod(-1, 3) == 2`), but C's `fmod` takes the sign of the dividend (`fmod(-1, 3) == -1`), so the generated code computes a different value whenever the operands have different signs. Compiled with gcc, the printed code returns -1 at `(x, y) = (-1, 3)`. The integer branch of the same method already corrects for this with `((a % b) + b) % b`.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_Mod` falls back to `fmod` for non-integer arguments; it needs the same sign correction as the integer branch (e.g. `fmod(fmod(x, y) + y, y)`), unless both operands are known nonnegative. Tested-buggy: `test_ccode_functions2` in `sympy/printing/tests/test_c.py` asserts `ccode(Mod(r, s)) == "fmod(r, s)"`; `test_C99CodePrinter__precision` also asserts bare `fmod{s}(...)` forms.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
