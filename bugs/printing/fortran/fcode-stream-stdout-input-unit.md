# Printing stdout raises AttributeError; the branch meant for it would print input_unit

### Kind
internal

### Actual
```pycon
>>> from sympy import fcode
>>> from sympy.printing.fortran import FCodePrinter
>>> from sympy.codegen.ast import stdout
>>> p = FCodePrinter({'standard': 2003})
>>> type(p._print(stdout)).__name__
'String'
>>> fcode(stdout, standard=2003, source_format='free')
Traceback (most recent call last):
...
AttributeError: 'String' object has no attribute 'splitlines'
```

### Expected
```pycon
>>> type(p._print(stdout)).__name__
'str'
>>> _ = fcode(stdout, standard=2003, source_format='free')
>>> q = FCodePrinter({'standard': 2003})
>>> code = q._print(stdout)
>>> isinstance(code, str) and code != 'input_unit'
True
```

### Why it is wrong
A `_print_*` method must return a string. Beyond that, the branch meant for `stdout` under Fortran 2003 maps standard output to `input_unit` (standard input) and imports it as `stdint=>input_unit` from `iso_c_binding`, which defines no such names (`input_unit`/`output_unit`/`error_unit` live in `iso_fortran_env`). The reviewer checked this against the Fortran standard only.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_Stream` compares `strm.name` (a `String`) with the Python strings `'stdout'`/`'stderr'`, which is never true, so it always falls through to `return strm.name` and returns the `String` object itself. Fixing the comparison (`strm.name.text`, or comparing with `stdout`/`stderr`) would expose the wrong mapping: it should print `output_unit` (and `error_unit`) with `self.module_uses['iso_fortran_env']`. `_print_Print` currently bypasses the method by mapping `stdout`/`stderr` to the unit numbers `6`/`0` itself, so the method is dead code for `Print`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
