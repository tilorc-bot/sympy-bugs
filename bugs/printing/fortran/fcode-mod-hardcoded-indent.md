# fcode() prints Mod with six hard-coded leading spaces: "z =       modulo(i, 3)"

### Kind
cosmetic

### Actual
```pycon
>>> from sympy import symbols, Mod, fcode
>>> i, j = symbols('i j', integer=True)
>>> print(fcode(Mod(i, 3), assign_to='j', standard=95, source_format='free'))
j =       modulo(i, 3)
```

### Expected
```pycon
>>> ' modulo' in fcode(Mod(i, 3), assign_to='j', standard=95, source_format='free')
False
```

### Why it is wrong
The fixed-form statement indentation is added by `_format_code`; `_print_Mod` adds another six spaces inside the expression, so every `Mod` that is not at the start of a line is preceded by a run of blanks. The code still compiles, but it is ugly and makes lines longer than necessary.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Mod` returns `"      modulo({}, {})"`; the leading spaces should be removed. `test_Mod` in `sympy/printing/tests/test_fortran.py` asserts `"      modulo(x, y)"` for fixed form, which is the normal fixed-form statement indent and stays the same after the fix.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
