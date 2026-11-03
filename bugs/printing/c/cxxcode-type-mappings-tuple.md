# C++ declarations of bool and int64 variables print a Python tuple: (bool, None) x

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.codegen.ast import Declaration, Variable, Type, bool_
>>> from sympy.printing.cxx import cxxcode
>>> from sympy.printing.c import ccode
>>> x = symbols('x')
>>> print(cxxcode(Declaration(Variable(x, type=bool_))))
(bool, None) x
>>> print(cxxcode(Declaration(Variable(x, type=Type('int64')))))
(int64_t, {cstdint}) x
>>> print(ccode(Declaration(Variable(x, type=bool_))))
bool x
>>> from codecheck import compile_errors, compiles
>>> declarations = [Declaration(Variable(x, type=bool_)), Declaration(Variable(x, type=Type('int64')))]
>>> print(compile_errors('c++', cxxcode(declarations[0]) + ';\nx'))
error: expected primary-expression before 'bool'...
```

### Expected
```pycon
>>> [compiles('c++', cxxcode(d) + ';\nx') for d in declarations]
[True, True]
```

### Why it is wrong
The type is printed as the repr of a Python tuple, which is not C++ (g++: "expected primary-expression before 'bool'").

### Notes on fixing
`sympy/printing/cxx.py:CXX11CodePrinter.type_mappings` adds entries whose values are `(name, headers)` tuples (e.g. `Type('bool'): ('bool', None)`), but `C89CodePrinter._print_Type` (`sympy/printing/c.py`) expects `type_mappings` to map to a name and headers to be in `type_headers`. The tuples need to be split into `type_mappings` and `type_headers`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
