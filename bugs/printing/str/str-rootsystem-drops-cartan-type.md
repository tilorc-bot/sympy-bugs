# Every RootSystem prints as RootSystem(), dropping its Cartan type

### Kind
lossy

### Actual
```pycon
>>> from sympy.liealgebras.root_system import RootSystem
>>> print(RootSystem('A2'))
RootSystem()
>>> print(RootSystem('B2'))
RootSystem()
```

### Expected
```pycon
>>> str(RootSystem('A2')) != str(RootSystem('B2'))
True
>>> a = str(RootSystem('A2'))
>>> str(RootSystem('B2')) != a
True
```

### Why it is wrong
Root systems of different types print identically, and `RootSystem()` cannot be evaluated back (the constructor requires a Cartan type).

### Notes on fixing
`sympy/liealgebras/root_system.py:RootSystem.__new__` creates `Atom.__new__(cls)` with no args and stores the type only as the attribute `cartan_type`, so the generic `_print_Basic` prints empty parentheses. Either the Cartan type should be stored in `args` (which also makes `RootSystem('A2') == RootSystem('B2')`, currently `True`, come out right), or `RootSystem` needs its own `_sympystr`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
