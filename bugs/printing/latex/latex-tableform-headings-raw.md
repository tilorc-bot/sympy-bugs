# TableForm.as_latex() inserts headings raw in text mode (r_1, c&1 break the tabular)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy.printing.tableform import TableForm
>>> print(TableForm([[1, 2]], headings=[['r_1'], ['c_1', 'c_2']]).as_latex())
\begin{tabular}{r l l}
 & c_1 & c_2 \\
\hline
r_1 & $1$ & $2$ \\
\end{tabular}
>>> print(TableForm([[1, 2]], headings=[None, ['c&1', 'c%2']]).as_latex())
\begin{tabular}{l l}
c&1 & c%2 \\
\hline
$1$ & $2$ \\
\end{tabular}
```

### Expected
```pycon
>>> 'r_1 &' in TableForm([[1, 2]], headings=[['r_1'], ['c_1', 'c_2']]).as_latex()
False
>>> TableForm([[1, 2]], headings=[None, ['c&1', 'c%2']]).as_latex().splitlines()[1].replace(r'\&', '').count('&')
1
>>> TableForm([[1, 2]], headings=[None, ['c&1', 'c%2']]).as_latex().splitlines()[1].replace(r'\%', '').count('%')
0
```

### Why it is wrong
The cells are put in math mode (`$1$`) but headings are inserted verbatim in text mode: `r_1` fails with "Missing $ inserted", `&` adds a column ("Extra alignment tab") and `%` comments out the rest of the row.

### Notes on fixing
`sympy/printing/tableform.py:TableForm._latex` converts headings with `str()` and joins them with ` & `. Headings should be escaped (`latex_escape`) or, consistently with the cells, printed with the LaTeX printer in math mode (which would also make `r_1` a subscript).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
