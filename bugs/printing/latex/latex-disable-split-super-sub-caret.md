# latex(..., disable_split_super_sub=True) escapes ^ as \^, a text accent that is invalid in math mode

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, latex
>>> print(latex(Symbol('x^2'), disable_split_super_sub=True))
x\^2
```

### Expected
```pycon
>>> latex(Symbol('x^2'), disable_split_super_sub=True) != r'x\^2'
True
```

### Why it is wrong
`\^` is the circumflex text accent; in math mode TeX stops with "Please use \mathaccent for accents in math mode", so any symbol name containing `^` cannot be printed with this setting.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._split_super_sub` replaces `^` with `\^` (and `_` with `\_`, which is fine in math mode). A math-mode caret is needed instead, e.g. `\text{\textasciicircum}` or `{}^\wedge`. This is tested-buggy: `sympy/printing/tests/test_latex.py:test_latex_disable_split_super_sub` asserts `u\^a\_b`. The setting is also missing from the `latex()` docstring.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
