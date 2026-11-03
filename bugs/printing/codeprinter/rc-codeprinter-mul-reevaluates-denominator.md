# Code printers print Mul(x, 1/(1/y)) as x/1/y (CodePrinter._print_Mul re-evaluates the denominator)

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, Mul, Pow, pycode, ccode, jscode, octave_code
>>> x, y = symbols('x y')
>>> e = Mul(x, Pow(Pow(y, -1), -1, evaluate=False), evaluate=False)
>>> print(e)
x/(1/y)
>>> print(pycode(e))
x/1/y
>>> print(ccode(e))
x/1.0/y
>>> print(jscode(e))
x/1/y
>>> print(octave_code(e))
x./1./y
>>> from codecheck import run_code
>>> run_code('c', ccode(e), x=6.0, y=2.0), e.subs({x: 6, y: 2})
(3.0, 12)
```

### Expected
```pycon
>>> run_code('c', ccode(e), x=6.0, y=2.0)
12.0
>>> v = {'x': 6, 'y': 2}
>>> [eval(printer(e), v) == 12 for printer in (pycode, jscode)]
[True, True]
```

### Why it is wrong
`x/(1/y)` equals `x*y`, but the generated code computes `(x/1)/y = x/y` (compiled with gcc, `ccode(e)` gives 3 at `(x, y) = (6, 2)`). The same expression arises from `parse_expr('x/(1/y)', evaluate=False)`, and the wrong code is silently emitted by every printer derived from `CodePrinter`.

### Notes on fixing
`sympy/printing/codeprinter.py:CodePrinter._print_Mul` moves a factor `Pow(b, -1)` to the denominator as `Pow(b, 1)`, which evaluates to `b`. When `b` is itself `Pow(y, -1)` it has Pow precedence, so `parenthesize(b, PRECEDENCE["Mul"])` adds no parentheses, yet it prints as `1/y`. `StrPrinter._print_Mul` already handles this case (`pow_paren`, issue [sympy/sympy#14160](https://redirect.github.com/sympy/sympy/issues/14160)), which is why `str(e)` is right.

Wrong in pycode, C, R, GLSL (`x/1.0/y`), JavaScript and Maple (`x/1/y`), Fortran (`x/1d0/y`), Julia (`x ./ 1 ./ y`) and Octave (`x./1./y`); Julia and Octave have their own `_print_Mul` with the same pattern. Rust (`x/y.recip()`) and Mathematica (`x*y`) are correct. The review executed the generated code in Python, C, JavaScript and Julia.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (root cause 2).
