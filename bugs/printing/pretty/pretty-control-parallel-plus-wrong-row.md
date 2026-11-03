# pretty() of a control Parallel puts the + on the middle row instead of the fraction bar of the first transfer function

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, pretty
>>> from sympy.physics.control.lti import TransferFunction, Parallel
>>> s = symbols('s')
>>> tf1 = TransferFunction(1 + 1/(s + 1), 1, s)
>>> tf2 = TransferFunction(1, s + 1, s)
>>> print(pretty(Parallel(tf1, tf2), use_unicode=True))
      1
1 + ─────     1
    s + 1 + ─────
─────────   s + 1
    1
```

### Expected
```pycon
>>> '───────── + ─────' in pretty(Parallel(tf1, tf2), use_unicode=True)
True
```

### Why it is wrong
The `+` and the second transfer function are aligned with the denominator of the inner fraction, so the picture reads as `(1 + 1/(s + 1 + 1/(s + 1)))/1` instead of `(1 + 1/(s + 1))/1 + 1/(s + 1)`.

### Notes on fixing
`PrettyPrinter._print_Parallel` in `sympy/printing/pretty/pretty.py` resets the baseline of the accumulated picture to `s.height()//2` before appending ` + `, discarding the baseline of the transfer function (its main fraction bar). `_print_MIMOParallel` does the same.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
