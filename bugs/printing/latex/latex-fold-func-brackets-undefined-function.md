# latex(f(x), fold_func_brackets=True) prints "fx" for an undefined function

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Function, Symbol, latex
>>> x = symbols('x')
>>> f = Function('f')
>>> print(latex(f(x), fold_func_brackets=True))
fx
>>> print(latex(f(2*x), fold_func_brackets=True))
f2 x
>>> print(latex(Symbol('fx')))
fx
```

### Expected
```pycon
>>> latex(f(x), fold_func_brackets=True) != latex(Symbol('fx'))
True
```

### Why it is wrong
`fx` is the LaTeX of the symbol `fx` (and renders as the product `f·x`); `f2 x` renders as `f·2·x`. With `fold_func_brackets` an undefined single-letter function loses all indication that it is applied to its argument.

### Notes on fixing
In `LatexPrinter._print_Function` (`sympy/printing/latex.py`), when brackets are folded, functions in `accepted_latex_functions` get `name + r" {%s}"` but every other function gets `name + "%s"`, i.e. the argument is glued to the name. For a plain-letter name (an undefined function) folding should not happen at all, or at least a separator is needed. The same branch produces `\operatorname{asinh}x` (renders acceptably thanks to `\operatorname`), and folding a negative argument gives `\cos {- x}` for `cos(-x, evaluate=False)`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
