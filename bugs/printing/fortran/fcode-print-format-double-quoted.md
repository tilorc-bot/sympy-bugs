# Print([x], '(F10.3)') prints fmt=""(F10.3)"" with doubled quotes

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, fcode
>>> from sympy.codegen.ast import Print
>>> x = symbols('x')
>>> print(fcode(Print([x], '(F10.3)'), standard=95, source_format='free'))
write(*, fmt=""(F10.3)"", advance="no"), x
```

### Expected
```pycon
>>> '""' in fcode(Print([x], '(F10.3)'), standard=95, source_format='free')
False
```

### Why it is wrong
`""(F10.3)""` is an empty string followed by `(F10.3)` and another empty string, so the format specifier is not the string `(F10.3)` and the statement does not compile. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Print` puts `self._print(ps.format_string)` inside `fmt="{fmt}"`, but `format_string` is a `String`, whose printed form already includes the quotes. Use `ps.format_string.text` (and double any embedded `"`), or drop the quotes from the template.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
