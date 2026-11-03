# TableForm(wipe_zeros=True) does not wipe Float zeros

### Kind
ignored-setting

### Actual
```pycon
>>> from sympy import TableForm, Float
>>> print(TableForm([[0, 1]], wipe_zeros=True))
  1
>>> print(TableForm([[Float(0), 1]], wipe_zeros=True))
0.0 1
>>> print(TableForm([[Float(0), 1]], wipe_zeros=True).as_latex())
\begin{tabular}{l l}
$0.0$ & $1$ \\
\end{tabular}
```

### Expected
```pycon
>>> '0.0' in str(TableForm([[Float(0), 1]], wipe_zeros=True))
False
>>> '0.0' in TableForm([[Float(0), 1]], wipe_zeros=True).as_latex()
False
```

### Why it is wrong
`wipe_zeros` is documented as "Do not show zeros in the table"; a floating-point zero is a zero, and tables of numerical results typically contain `Float` zeros.

### Notes on fixing
`sympy/printing/tableform.py`: `TableForm._sympystr` (via `as_str`) only wipes entries whose `str()` is exactly `"0"` (so neither `Float(0)` nor Python `0.0` is wiped), and `TableForm._latex` tests `x in (0, "0")`, which is false for `Float(0)` because `Float(0) != 0` in SymPy. Both should test for a numeric zero (e.g. `getattr(x, 'is_zero', x == 0)`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
