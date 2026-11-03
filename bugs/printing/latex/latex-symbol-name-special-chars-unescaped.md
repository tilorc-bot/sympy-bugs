# latex() inserts %, &, # and $ from Symbol names raw (Symbol('a%b') + 1 → a%b + 1)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, latex
>>> print(latex(Symbol('a%b') + 1))
a%b + 1
>>> print(latex(Symbol('a&b')))
a&b
>>> print(latex(Symbol('a#b')))
a#b
```

### Expected
```pycon
>>> (latex(Symbol('a%b') + 1).replace(r'\%', '').count('%'),
...  latex(Symbol('a&b')).replace(r'\&', '').count('&'),
...  latex(Symbol('a#b')).replace(r'\#', '').count('#'))
(0, 0, 0)
```

### Why it is wrong
`%` starts a TeX comment, so `a%b + 1` silently renders as `a` (the rest of the line is dropped); `&`, `#` and `$` are errors in math mode outside alignments/macros. Symbol names come from user data (e.g. column names), so this produces wrong or non-compiling output.

### Notes on fixing
`sympy/printing/latex.py:LatexPrinter._print_Symbol` → `_deal_with_super_sub` → `_split_super_sub` never escapes the name. Names containing `{` are passed through deliberately so that users can put raw LaTeX in a symbol name, so the fix should escape only characters that are never useful raw in a math-mode name (`%`, `#`, `&`, `$`), and keep the existing raw-LaTeX behaviour. A `%` in a function name crashes instead (reported separately).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
