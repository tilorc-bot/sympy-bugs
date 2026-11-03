# A unit Quantity's abbreviation goes unescaped into \text{} (\text{K_j})

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.physics.units import josephson_constant, Quantity
>>> print(latex(josephson_constant))
\text{K_j}
>>> print(latex(Quantity('foo_bar')))
\text{foo_bar}
```

### Expected
```pycon
>>> 'K_j' in latex(josephson_constant)
False
>>> 'foo_bar' in latex(Quantity('foo_bar'))
False
```

### Why it is wrong
`_` is not allowed in text mode, so `\text{K_j}` fails with "Missing $ inserted"; printing any expression that contains one of these constants produces TeX that does not compile.

### Notes on fixing
`sympy/physics/units/quantities.py:Quantity._latex` returns `r'\text{%s}' % abbrev` (or the name) without escaping when no `latex_repr` is given. Built-in constants affected: `josephson_constant` (`K_j`), `von_klitzing_constant` (`R_k`), `coulomb_constant` (`k_e`), `planck_energy_density`, `vacuum_permittivity`, `avogadro_number`, `magnetic_constant` (`sympy/physics/units/definitions/unit_definitions.py`). Either escape with `latex_escape`, or give these constants a `latex_repr` such as `K_{\text{J}}`. Stylistic, same method: `latex(hbar)` gives `\text{hbar}` rather than `\hbar`.

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
