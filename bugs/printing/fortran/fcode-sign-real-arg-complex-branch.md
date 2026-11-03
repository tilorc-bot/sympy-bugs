# fcode(sign(r)) for real r takes the complex branch: merge(cmplx(0d0, 0d0), r/abs(r), ...)

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, sign, fcode
>>> r = symbols('r', real=True)
>>> x = symbols('x')
>>> print(fcode(sign(r), standard=95, source_format='free'))
merge(cmplx(0d0, 0d0), r/abs(r), abs(r) == 0d0)
>>> print(fcode(sign(x), standard=95, source_format='free'))
merge(0d0, dsign(1d0, x), x == 0d0)
```

### Expected
```pycon
>>> 'cmplx' in fcode(sign(r), standard=95, source_format='free')
False
```

### Why it is wrong
A symbol declared real gets the code meant for complex arguments, while a symbol with no assumptions gets the real code. `merge` then mixes a complex `tsource` with a real `fsource` (`r/abs(r)`), which is a type mismatch, and even if it compiled the result would be complex. The reviewer checked this against the Fortran standard only; it was not compiled.

### Notes on fixing
`sympy/printing/fortran.py:FCodePrinter._print_sign` tests `arg.is_complex or arg.is_infinite` before the real case, and every real number is also complex in SymPy. The real test (`arg.is_extended_real`) has to come before the complex one, and the complex branch should be taken only when the argument is not known to be real.

The complex branch has a separate kind mismatch (linked under Related).

### Related
[sympy/sympy#12267](https://redirect.github.com/sympy/sympy/issues/12267)
[fcode-sign-complex-single-precision-zero](fcode-sign-complex-single-precision-zero.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
