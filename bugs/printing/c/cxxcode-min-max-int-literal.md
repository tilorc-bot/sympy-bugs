# cxxcode(Min(x, 2)) prints std::min(2, x), which does not compile for a double x

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Min, Max
>>> from sympy.printing.cxx import cxxcode
>>> x = symbols('x')
>>> print(cxxcode(Min(x, 2)))
std::min(2, x)
>>> print(cxxcode(Max(x, 2), standard='c++98'))
std::max(2, x)
```

### Expected
```pycon
>>> import re
>>> re.search(r'std::(min|max)\(-?\d+,', cxxcode(Min(x, 2)) + cxxcode(Max(x, 2))) is None
True
```

### Why it is wrong
`std::min`/`std::max` are templates `min(const T&, const T&)`; with an `int` literal and a `double` variable, template argument deduction fails ("no matching function for call to min(int, double)"). The original reviewer compiled this with g++; it was not executed here.

### Related
[sympy/sympy#20557](https://redirect.github.com/sympy/sympy/issues/20557)

### Notes on fixing
`sympy/printing/cxx.py:_CXXCodePrinterBase._print_Min`/`_print_Max` print the arguments as is. Integer literals need to be printed as floating-point (`2.0`) when mixed with real arguments, or the call needs an explicit template argument (`std::min<double>`), or `std::fmin`/`std::fmax` (C++11) can be used. Tested-buggy: `test_CXX98CodePrinter` in `sympy/printing/tests/test_cxx.py` asserts `std::max(x, 3)`/`std::max(3, x)` and `std::min(3, std::min(x, std::sqrt(x)))`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
