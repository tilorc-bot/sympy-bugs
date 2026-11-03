# octave_code() prints HadamardPower with .**, which Octave 9 removed

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import symbols, MatrixSymbol, HadamardPower, octave_code
>>> n = symbols('n')
>>> A = MatrixSymbol('A', 2, 2)
>>> print(octave_code(HadamardPower(A, n)))
A.**n
```

### Expected
```pycon
>>> '.**' in octave_code(HadamardPower(A, n))
False
```

### Why it is wrong
The `.**` operator was removed in Octave 9; Octave 11.3 reports a parse error. The element-wise power operator is `.^`, which the printer already uses for `Pow` (`octave_code(x**2)` is `x.^2`). MATLAB never had `.**`.

### Notes on fixing
`sympy/printing/octave.py:OctaveCodePrinter._print_HadamardPower` joins with `'.**'`; it should be `'.^'`. The output is asserted by `test_hadamard` in `sympy/printing/tests/test_octave.py`. The Julia printer has the same operator (`julia.py:_print_HadamardPower`), listed separately in [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).

### Suggested fix
```diff
diff --git a/sympy/printing/octave.py b/sympy/printing/octave.py
index 2cf2d6a..9212bef 100644
--- a/sympy/printing/octave.py
+++ b/sympy/printing/octave.py
@@ -390,7 +390,7 @@ def _print_HadamardProduct(self, expr):
 
     def _print_HadamardPower(self, expr):
         PREC = precedence(expr)
-        return '.**'.join([
+        return '.^'.join([
             self.parenthesize(expr.base, PREC),
             self.parenthesize(expr.exp, PREC)
             ])
diff --git a/sympy/printing/tests/test_octave.py b/sympy/printing/tests/test_octave.py
index 5dc923d..8054966 100644
--- a/sympy/printing/tests/test_octave.py
+++ b/sympy/printing/tests/test_octave.py
@@ -436,9 +436,9 @@ def test_hadamard():
     assert mcode(C*x*y) == "(x.*y)*(A.*B)"
 
     # Testing HadamardPower:
-    assert mcode(HadamardPower(A, n)) == "A.**n"
-    assert mcode(HadamardPower(A, 1+n)) == "A.**(n + 1)"
-    assert mcode(HadamardPower(A*B.T, 1+n)) == "(A*B.T).**(n + 1)"
+    assert mcode(HadamardPower(A, n)) == "A.^n"
+    assert mcode(HadamardPower(A, 1+n)) == "A.^(n + 1)"
+    assert mcode(HadamardPower(A*B.T, 1+n)) == "(A*B.T).^(n + 1)"
 
 
 def test_sparse():
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844) (follow-up comment).
