# latex() of a power of InnerProduct or OuterProduct puts the exponent on the last factor only

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.physics.quantum import InnerProduct, OuterProduct, Bra, Ket
>>> print(latex(InnerProduct(Bra('a'), Ket('b'))**2))
\left\langle a \right. {\left|b\right\rangle }^{2}
>>> print(latex(OuterProduct(Ket('a'), Bra('b'))**2))
{\left|a\right\rangle }{\left\langle b\right|}^{2}
```

### Expected
```pycon
>>> (latex(Ket('b')) + '^{2}') in latex(InnerProduct(Bra('a'), Ket('b'))**2)
False
>>> (latex(Bra('b')) + '^{2}') in latex(OuterProduct(Ket('a'), Bra('b'))**2)
False
```

### Why it is wrong
The output reads as `⟨a| (|b⟩²)` and `|a⟩ (⟨b|²)` instead of the square of the whole inner/outer product (a ket or bra cannot even be squared in SymPy).

### Notes on fixing
`InnerProduct._latex` (`sympy/physics/quantum/innerproduct.py`) and `OuterProduct._latex` (`sympy/physics/quantum/operator.py`) return a juxtaposition of two printed parts, but neither class has a precedence entry, so they get Atom precedence and `LatexPrinter._helper_print_standard_power` does not bracket the base. Either give them a lower precedence or make their `_latex` output a single group (and bracket it in `_print_Pow`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
