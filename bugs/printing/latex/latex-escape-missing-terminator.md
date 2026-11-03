# latex_escape emits \textbackslash etc. without a terminator, so the next letter joins the command

### Kind
invalid-output

### Actual
```pycon
>>> from sympy import latex
>>> from sympy.printing.latex import latex_escape
>>> print(latex('a\\b'))
\mathtt{\text{a\textbackslashb}}
>>> print(latex_escape('a~b^c'))
a\textasciitildeb\textasciicircumc
```

### Expected
```pycon
>>> r'\textbackslashb' in latex('a\\b')
False
>>> r'\textasciitildeb' in latex_escape('a~b^c')
False
```

### Why it is wrong
TeX reads `\textbackslashb` as one (undefined) control sequence, so any string containing `\`, `~` or `^` followed by a letter fails with "Undefined control sequence".

### Notes on fixing
`sympy/printing/latex.py:latex_escape` should emit `\textbackslash{}`, `\textasciitilde{}` and `\textasciicircum{}`. `sympy/printing/tests/test_latex.py:test_latex_escape` asserts the unterminated forms (it only passes TeX because each is followed by another backslash) and needs updating.

### Suggested fix
```diff
diff --git a/sympy/printing/latex.py b/sympy/printing/latex.py
index fe44b0e..0658dd0 100644
--- a/sympy/printing/latex.py
+++ b/sympy/printing/latex.py
@@ -132,12 +132,10 @@ def latex_escape(s: str) -> str:
     We cannot use verbatim easily with mathjax, so escaping is easier.
     Rules from https://tex.stackexchange.com/a/34586/41112.
     """
-    s = s.replace('\\', r'\textbackslash')
-    for c in '&%$#_{}':
-        s = s.replace(c, '\\' + c)
-    s = s.replace('~', r'\textasciitilde')
-    s = s.replace('^', r'\textasciicircum')
-    return s
+    table = {'\\': r'\textbackslash{}', '~': r'\textasciitilde{}',
+             '^': r'\textasciicircum{}'}
+    table.update({c: '\\' + c for c in '&%$#_{}'})
+    return ''.join(table.get(c, c) for c in s)
 
 
 class LatexPrinter(Printer):
diff --git a/sympy/printing/tests/test_latex.py b/sympy/printing/tests/test_latex.py
index 31bd0af..c03a7e6 100644
--- a/sympy/printing/tests/test_latex.py
+++ b/sympy/printing/tests/test_latex.py
@@ -3323,9 +3323,9 @@ def test_Str():
 
 def test_latex_escape():
     assert latex_escape(r"~^\&%$#_{}") == "".join([
-        r'\textasciitilde',
-        r'\textasciicircum',
-        r'\textbackslash',
+        r'\textasciitilde{}',
+        r'\textasciicircum{}',
+        r'\textbackslash{}',
         r'\&',
         r'\%',
         r'\$',
```

### Source
Imported from [sympy/sympy#30844](https://redirect.github.com/sympy/sympy/issues/30844).
