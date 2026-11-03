# strict=True still emits Python-syntax StrPrinter output for Sum, Transpose, Inverse, I, ...

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, Sum, I, MatrixSymbol, ccode, jscode
>>> x, n = symbols('x n')
>>> A = MatrixSymbol('A', 2, 2)
>>> ccode(Sum(x, (x, 1, n)), strict=True)
'Sum(x, (x, 1, n))'
>>> ccode(A.T, strict=True), ccode(A.I, strict=True)
('A.T', 'A**(-1)')
>>> jscode(I*x, strict=True)
'I*x'
>>> from codecheck import compile_errors
>>> for e in (Sum(x, (x, 1, n)), A.T, A.I):
...     print(compile_errors('c', ccode(e, strict=True), x=float, n=int, A=[float]))
error: implicit declaration of function 'Sum'...
error: request for member 'T' in something not a structure or union
error: invalid type argument of unary '*' (have 'int')
```

### Expected
```pycon
>>> from sympy.printing.codeprinter import PrintMethodNotImplementedError
>>> def raises(f):
...     try:
...         f()
...     except PrintMethodNotImplementedError:
...         return True
...     return False
>>> raises(lambda: ccode(Sum(x, (x, 1, n)), strict=True))
True
>>> raises(lambda: ccode(A.T, strict=True))
True
>>> raises(lambda: ccode(A.I, strict=True))
True
>>> raises(lambda: jscode(I*x, strict=True))
True
```

### Why it is wrong
`strict=True` (the default for `ccode`, `jscode`, ...) is documented to raise `PrintMethodNotImplementedError` for unsupported objects instead of emitting partial code. Here it silently emits SymPy/Python syntax (`A.T`, `A**(-1)`, `I*x`) that does not compile in the target language (gcc rejects all three C outputs), or compiles with a different meaning.

### Notes on fixing
`CodePrinter` (`sympy/printing/codeprinter.py`) sets `_print_Basic = _print_not_supported` plus a fixed list of `_print_<Class> = _print_not_supported`, but it subclasses `StrPrinter`, whose concrete methods (`_print_Sum`, `_print_Transpose`, `_print_Inverse`, `_print_ImaginaryUnit`, ...) are found first when dispatching on the expression's MRO. The same happens for `Lambda`, `Subs`, `Poly`, `FiniteSet`, `Dict`, `Permutation`, `Quaternion`, `MatrixSlice`, `ElementwiseApplyFunction` and `OneMatrix`, in every `CodePrinter` subclass. A fix could make dispatch in `CodePrinter` skip methods defined on `StrPrinter`, or explicitly map the inherited StrPrinter methods to `_print_not_supported`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
