# glsl_code() prints symbols named after GLSL reserved words unchanged: input + 1

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, glsl_code
>>> print(glsl_code(Symbol('input') + 1))
input + 1
>>> print(glsl_code(Symbol('float') + 1))
float + 1
```

### Expected
```pycon
>>> import re
>>> 'input' in re.findall(r'\w+', glsl_code(Symbol('input') + 1))
False
>>> 'float' in re.findall(r'\w+', glsl_code(Symbol('float') + 1))
False
```

### Why it is wrong
`input` is reserved and `float` is a keyword in GLSL, so the output does not compile. glslang 15.2 reports `'input' : Reserved word`. The other C-like printers append `reserved_word_suffix` (`_`) to such names, or raise with `error_on_reserved=True`.

### Notes on fixing
`sympy/printing/glsl.py:GLSLPrinter` never sets `self.reserved_words`, so `CodePrinter._print_Symbol` (`sympy/printing/codeprinter.py`) finds an empty set. It needs the GLSL keyword and reserved-word lists, as `c.py` has for C. Not covered by a test.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
