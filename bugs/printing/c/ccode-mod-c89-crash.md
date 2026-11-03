# Mod(x, y) raises AttributeError with standard='c89' (and 'c++98')

### Kind
crash

### Actual
```pycon
>>> from sympy import symbols, Mod
>>> from sympy.printing.c import ccode
>>> from sympy.printing.cxx import cxxcode
>>> x, y = symbols('x y')
>>> ccode(Mod(x, y), standard='c89')
Traceback (most recent call last):
...
AttributeError: 'C89CodePrinter' object has no attribute '_print_math_func'...
>>> cxxcode(Mod(x, y), standard='c++98')
Traceback (most recent call last):
...
AttributeError: 'CXX98CodePrinter' object has no attribute '_print_math_func'...
```

### Expected
```pycon
>>> _ = ccode(Mod(x, y), standard='c89')
>>> _ = cxxcode(Mod(x, y), standard='c++98')
```

### Why it is wrong
`fmod` exists in C89 and C++98, and printing must not fail for a valid expression.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_Mod` ends with `return self._print_math_func(expr, known='fmod')`, but `_print_math_func` is only defined on `C99CodePrinter`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
