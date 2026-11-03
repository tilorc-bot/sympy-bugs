# str(TableForm(..., formats=...)) ignores the formats argument

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import TableForm
>>> t = TableForm([[1.123456, 2]], formats=['%.2f', None])
>>> print(t)
1.12345600000000 2
>>> print(t.as_latex())
\begin{tabular}{l l}
1.12 & $2$ \\
\end{tabular}
```

### Expected
```pycon
>>> '1.12345600000000' in str(t)
False
```

### Why it is wrong
The documented `formats` option ("a list of format strings or functions ... for the table entry") is applied by `as_latex` but silently ignored by `str`/`as_str`, which is what `print` and the interactive display use.

### Notes on fixing
`sympy/printing/tableform.py:TableForm._sympystr` formats every entry with `str(line[i])`; it never consults `self._column_formats` (format strings or 3-argument functions, falling back to the printer when a function returns `None`), unlike `_latex`. It also uses `str()` instead of the printer `p`, so StrPrinter settings are not applied to entries.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
