# Pretty printer gives inline fractions and negative numbers ATOM binding, so powers of them lose parentheses

### Kind
internal

### Actual
```pycon
>>> from sympy import symbols, Rational, Float, Pow, pretty
>>> from sympy.printing.pretty.pretty import PrettyPrinter
>>> from sympy.printing.pretty.stringpict import prettyForm
>>> x, n = symbols('x n')
>>> p = PrettyPrinter()
>>> p._print(Rational(2, 3)).binding == prettyForm.ATOM, p._print(Float(-2.5)).binding == prettyForm.ATOM
(True, True)
>>> print(pretty(Pow(Rational(2, 3), x, evaluate=False)))
   x
2/3
>>> print(pretty(Rational(-1, 2)**n + x))
    n
-1/2  + x
```

### Expected
```pycon
>>> p._print(Rational(2, 3)).binding != prettyForm.ATOM, p._print(Float(-2.5)).binding != prettyForm.ATOM
(True, True)
```

### Why it is wrong
`prettyForm.__pow__` and `__mul__` decide on parentheses from the `binding` of the operands. A picture such as `2/3` or `-2.5` is a quotient or a negation, but is returned with `ATOM` binding, so `(2/3)**x` prints as `2/3` with superscript `x` (reads `2/(3**x)`) and `(-1/2)**n` reads `-(1/2**n)`. The same shows up in `fps(sin(x))`, whose general term prints `-1/4` raised to a power.

### Notes on fixing
`sympy/printing/pretty/pretty.py`: `_print_Rational`/`_print_Fraction` fall back to `emptyPrinter` (a plain `prettyForm(str)`, ATOM) for small inline fractions, and `_print_Float` returns `prettyForm(sstr(e))` without `binding=prettyForm.NEG` for negative values. The review lists further printers that return composite pictures with ATOM binding: `Union`/`_print_seq`, `MatAdd`, `Dot`, `TensorProduct`, and the inline `sin²(x)` form. Each needs the binding that matches its outermost operator (DIV, NEG, ADD, MUL, ...).

### Suggested fix
```diff
diff --git a/sympy/physics/quantum/tests/test_printing.py b/sympy/physics/quantum/tests/test_printing.py
index 1a5cca6..07ca387 100644
--- a/sympy/physics/quantum/tests/test_printing.py
+++ b/sympy/physics/quantum/tests/test_printing.py
@@ -863,17 +863,17 @@ def test_big_expr():
         "Wigner3j(1, 2, 3, 4, 5, 6)*[Dagger(B) + A,C + D]x(-J2 + Jz)*|1,0><1,1|*(|1,0,j1=1,j2=1> + |1,1,j1=1,j2=1>)x|1,-1,j1=1,j2=1>"
     ascii_str = \
 """\
-          [ +          ]  /   2     \\                                                                 \n\
-/1  3  5\\*[B  + A,C + D]x |- J  + J |*|1,0><1,1|*(|1,0,j1=1,j2=1> + |1,1,j1=1,j2=1>)x |1,-1,j1=1,j2=1>\n\
-|       |                 \\        z/                                                                 \n\
-\\2  4  6/                                                                                             \
+          [ +          ]  /   2     \\                                                                   \n\
+/1  3  5\\*[B  + A,C + D]x |- J  + J |*|1,0><1,1|*((|1,0,j1=1,j2=1> + |1,1,j1=1,j2=1>)x |1,-1,j1=1,j2=1>)\n\
+|       |                 \\        z/                                                                   \n\
+\\2  4  6/                                                                                               \
 """
     ucode_str = \
 """\
-          ⎡ †          ⎤  ⎛   2     ⎞                                                                 \n\
-⎛1  3  5⎞⋅⎣B  + A,C + D⎦⨂ ⎜- J  + J ⎟⋅❘1,0⟩⟨1,1❘⋅(❘1,0,j₁=1,j₂=1⟩ + ❘1,1,j₁=1,j₂=1⟩)⨂ ❘1,-1,j₁=1,j₂=1⟩\n\
-⎜       ⎟                 ⎝        z⎠                                                                 \n\
-⎝2  4  6⎠                                                                                             \
+          ⎡ †          ⎤  ⎛   2     ⎞                                                                   \n\
+⎛1  3  5⎞⋅⎣B  + A,C + D⎦⨂ ⎜- J  + J ⎟⋅❘1,0⟩⟨1,1❘⋅((❘1,0,j₁=1,j₂=1⟩ + ❘1,1,j₁=1,j₂=1⟩)⨂ ❘1,-1,j₁=1,j₂=1⟩)\n\
+⎜       ⎟                 ⎝        z⎠                                                                   \n\
+⎝2  4  6⎠                                                                                               \
 """
     assert pretty(e3) == ascii_str
     assert upretty(e3) == ucode_str
diff --git a/sympy/printing/pretty/stringpict.py b/sympy/printing/pretty/stringpict.py
index 9212483..10af011 100644
--- a/sympy/printing/pretty/stringpict.py
+++ b/sympy/printing/pretty/stringpict.py
@@ -372,9 +372,15 @@ class prettyForm(stringPict):
     """
     ATOM, FUNC, DIV, POW, MUL, ADD, NEG, OPEN = range(8)
 
-    def __init__(self, s, baseline=0, binding=0, unicode=None):
-        """Initialize from stringPict and binding power."""
+    def __init__(self, s, baseline=0, binding=None, unicode=None):
+        """Initialize from stringPict and binding power.
+
+        If no binding is given, it is inferred from the picture: a one-line
+        picture with an operator outside brackets is not an atom.
+        """
         stringPict.__init__(self, s, baseline)
+        if binding is None:
+            binding = self._infer_binding()
         self.binding = binding
         if unicode is not None:
             sympy_deprecation_warning(
@@ -386,6 +392,44 @@ def __init__(self, s, baseline=0, binding=0, unicode=None):
                 active_deprecations_target="deprecated-pretty-printing-functions")
         self._unicode = unicode or s
 
+    _brackets = {')': '(', ']': '[', '}': '{', '>': '<',
+                 '\N{MATHEMATICAL RIGHT ANGLE BRACKET}':
+                 '\N{MATHEMATICAL LEFT ANGLE BRACKET}'}
+
+    def _infer_binding(self):
+        """Binding of a picture built without an explicit one."""
+        if self.height() != 1:
+            return prettyForm.ATOM
+        line = self.picture[0].strip()
+        # blank out matched bracket pairs; unmatched ones (as in the
+        # bra <x| or the ket |x>) are ordinary characters
+        inside = [False]*len(line)
+        stack = []
+        for i, c in enumerate(line):
+            if c in self._brackets.values():
+                stack.append(i)
+            elif c in self._brackets:
+                for k in range(len(stack) - 1, -1, -1):
+                    if line[stack[k]] == self._brackets[c]:
+                        for j in range(stack[k], i + 1):
+                            inside[j] = True
+                        del stack[k:]
+                        break
+        top = ''.join(c for c, hidden in zip(line, inside) if not hidden)
+        # an infix operator has operands on both sides (y* is an adjoint)
+        infix = ''.join(c for c, hidden in zip(line[1:-1], inside[1:-1])
+                        if not hidden)
+        if ' ' in top:
+            # operands joined by a spaced operator: x + y, A \N{UNION} B, ...
+            return prettyForm.ADD
+        if len(line) > 1 and line[0] == '-':
+            return prettyForm.NEG
+        if '/' in infix:
+            return prettyForm.DIV
+        if any(c in infix for c in '*\N{DOT OPERATOR}\N{MULTIPLICATION SIGN}'):
+            return prettyForm.MUL
+        return prettyForm.ATOM
+
     @property
     def unicode(self):
         sympy_deprecation_warning(
@@ -506,7 +550,7 @@ def __pow__(self, b):
             #  sin  +   + (x)
             b.baseline = a.prettyFunc.baseline + b.height()
             func = stringPict(*a.prettyFunc.right(b))
-            return prettyForm(*func.right(a.prettyArgs))
+            return prettyForm(binding=prettyForm.POW, *func.right(a.prettyArgs))
         else:
             #      2    <-- top
             # (x+y)     <-- bot
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (root cause 5).
