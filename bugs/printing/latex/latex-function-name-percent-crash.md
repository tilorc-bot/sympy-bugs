# latex() of an undefined function whose name contains % raises ValueError

### Kind
crash

### Actual
```pycon
>>> from sympy import Function, symbols, latex
>>> x = symbols('x')
>>> latex(Function('a%b')(x))
Traceback (most recent call last):
...
ValueError: unsupported format character 'b'...
```

### Expected
```pycon
>>> _ = latex(Function('a%b')(x))
```

### Why it is wrong
Printing must not fail for a valid expression; `str` prints it.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._hprint_Function` returns a name that is then used as a `%`-format template (`name % ",".join(args)` in `_print_Function`), so a `%` in the function name is parsed as a format directive. The name should be escaped (`%` → `\%`, which then also needs `%%` in the template) or the arguments joined without `%`-formatting.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
