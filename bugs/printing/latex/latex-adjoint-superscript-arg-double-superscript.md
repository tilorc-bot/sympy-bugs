# adjoint(A) gives a double superscript when A prints with a superscript

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import Symbol, adjoint, latex
>>> from sympy.physics.quantum import Dagger, Operator
>>> print(latex(adjoint(Symbol('A^a', commutative=False))))
A^{a}^{\dagger}
>>> print(latex(Dagger(Operator('B^b'))))
B^{b}^{\dagger}
```

### Expected
```pycon
>>> r'^{a}^' in latex(adjoint(Symbol('A^a', commutative=False)))
False
>>> r'^{b}^' in latex(Dagger(Operator('B^b')))
False
```

### Why it is wrong
`A^{a}^{\dagger}` is a TeX "Double superscript" error, so the output does not compile.

### Notes on fixing
`sympy/functions/elementary/complexes.py:adjoint._latex` formats `r'%s^{\dagger}' % printer._print(self.args[0])` without protecting the argument (`printer.parenthesize_super`) and without parenthesizing it by precedence. The same method also ignores `adjoint_style` and misprints `adjoint(Integral(A, x))` as `\int A\, dx^{\dagger}` (separate findings of the same review), so a fix could cover all three.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
