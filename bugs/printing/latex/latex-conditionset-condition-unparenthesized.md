# latex() does not bracket an Or condition of a ConditionSet: x \in \mathbb{R} \wedge x > 1 \vee x < 0

### Kind
wrong-meaning

### Actual
```pycon
>>> from sympy import symbols, ConditionSet, Or, S, latex
>>> x = symbols('x')
>>> print(latex(ConditionSet(x, Or(x > 1, x < 0), S.Reals)))
\left\{x\; \middle|\; x \in \mathbb{R} \wedge x > 1 \vee x < 0 \right\}
```

### Expected
```pycon
>>> r'\left(x > 1 \vee x < 0\right)' in latex(ConditionSet(x, Or(x > 1, x < 0), S.Reals))
True
```

### Why it is wrong
∧ binds more tightly than ∨, so the condition reads as `(x ∈ ℝ ∧ x > 1) ∨ x < 0` instead of the set's actual condition `x ∈ ℝ ∧ (x > 1 ∨ x < 0)`.

### Notes on fixing
`LatexPrinter._print_ConditionSet` (`sympy/printing/latex.py`) formats `%s \in %s \wedge %s` with `self._print(s.condition)`; the condition should be parenthesized at And precedence (`self.parenthesize(s.condition, PRECEDENCE['And'])`).

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
