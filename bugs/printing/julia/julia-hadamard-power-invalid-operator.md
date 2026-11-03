# julia_code(HadamardPower(A, 2)) prints A.**2, which is a Julia syntax error

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import MatrixSymbol, HadamardPower, julia_code
>>> A = MatrixSymbol('A', 2, 2)
>>> print(julia_code(HadamardPower(A, 2)))
A.**2
```

### Expected
```pycon
>>> '**' in julia_code(HadamardPower(A, 2))
False
```

### Why it is wrong
Julia's element-wise power is `.^` (as `julia_code` itself uses for `x**2`); `.**` does not exist. The reviewer ran the output with Julia 1.12 and got a `ParseError`.

### Notes on fixing
`sympy/printing/julia.py:JuliaCodePrinter._print_HadamardPower` joins base and exponent with `'.**'`; it should use `' .^ '`.

### Related
[sympy/sympy#23736](https://redirect.github.com/sympy/sympy/issues/23736)
[octave-hadamard-power-removed-operator](../octave/octave-hadamard-power-removed-operator.md)

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
