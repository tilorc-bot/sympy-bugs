# Print([x]) leaves the default format string unquoted: printf(%s\n, x)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols
>>> from sympy.codegen.ast import Print
>>> from sympy.printing.c import ccode
>>> x = symbols('x')
>>> print(ccode(Print([x])))
printf(%s
, x)
>>> from codecheck import compile_errors, compiles
>>> printf = 'int printf(const char *, ...);\n'
>>> print(compile_errors('c', printf + ccode(Print([x])), x=float))
error: expected expression before '%' token
```

### Expected
```pycon
>>> compile_errors('c', printf + ccode(Print([x])), x=float) == ''
True
```

### Why it is wrong
The format string must be a C string literal; unquoted (and containing a raw newline) it does not compile (gcc: "expected expression before '%' token"). Expected compiles it after a declaration of `printf`. When a format string is passed explicitly, it is quoted.

### Notes on fixing
`sympy/printing/c.py:C89CodePrinter._print_Print` substitutes the Python string `"%s\n"` directly when `format_string == none`, instead of printing it as a string literal (with the newline escaped). `%s` is also the wrong conversion for a `double` argument.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
