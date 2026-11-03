# julia_code does not rename symbols that are Julia keywords: Symbol('end') prints as end

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, julia_code
>>> print(julia_code(Symbol('end') + Symbol('function')))
end + function
```

### Expected
```pycon
>>> julia_code(Symbol('end')) != 'end', julia_code(Symbol('function')) != 'function'
(True, True)
```

### Why it is wrong
`end` and `function` are Julia keywords, so the generated code does not parse. Other code printers (C, Rust, ...) append a suffix to reserved words (`end_`). The reviewer ran the output with Julia 1.12.

### Notes on fixing
`CodePrinter._print_Symbol` renames names in `self.reserved_words`, but `sympy/printing/julia.py:JuliaCodePrinter` never sets `reserved_words`, so it is the empty set from `CodePrinter.__init__`. A class attribute with Julia's keywords (`baremodule begin break catch const continue do else elseif end export false finally for function global if import let local macro module quote return struct true try using while`, plus `abstract type`/`mutable struct`/`primitive type` parts as needed) is needed.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
