"""Compare the instructor's printed answer against the value we computed.

`exam1_sol.verify()` proves our worked steps reach our own `want`. That is a
self-consistency check: it cannot catch a `want` that was transcribed wrong from
the official page, which is exactly the failure mode that produced the two
Lesson 10 corrections.

This module closes that loop from the other side. It reads the official answer
straight out of the vendored HTML, parses the small TeX dialect those answers
are written in, and compares it to our computed value. Any disagreement must be
a deliberate, documented correction (`fix=` in exam1_sol) or the build stops.

The parser is intentionally narrow. Prose answers ("elliptic cone with axis
along z"), set-builder domains and interval notation are reported as *not
comparable* rather than guessed at — a parser that silently mis-reads an answer
is worse than one that admits it cannot read it.
"""
import re
from sympy import sympify, simplify, Rational, sqrt, pi, E, exp, Matrix, S
import exam1_src, exam1_sol as M

def _sym(src):
    """sympify in the SAME symbol namespace the solution banks use.

    The banks declare `x, y, z, t = symbols(..., real=True)`. A bare
    `sympify("2*x")` creates an assumption-free `x`, and sympy treats the two as
    different symbols — so `Matrix([2*x,-4*y]) - Matrix([2*x,-4*y])` refuses to
    simplify to zero and an identical answer reports as a mismatch. Parsing into
    real-valued symbols is what makes the comparison mean anything.
    """
    from sympy import sympify, Symbol
    names = set(re.findall(r"(?<![A-Za-z0-9_])([a-zA-Z][a-zA-Z0-9_]*)", src))
    reserved = {"sqrt", "exp", "log", "sin", "cos", "tan", "atan", "acos",
                "asin", "pi", "E", "I", "oo", "Abs", "Rational", "Matrix"}
    local = {n: Symbol(n, real=True) for n in names - reserved}
    return sympify(src, locals=local)


def split_top(s):
    """Split on commas that are not inside braces or parentheses.

    TeX spacing macros are removed first: `\,` ends in a comma, so splitting
    before stripping them turns <-7, 5, 13> into five components, two of them
    a bare backslash.
    """
    s = s.replace("\\,", " ").replace("\\;", " ").replace("\\!", "")
    out,buf,depth=[],"",0
    for ch in s:
        if ch in "{(": depth+=1
        elif ch in ")}": depth-=1
        if ch=="," and depth==0: out.append(buf); buf=""
        else: buf+=ch
    if buf.strip(): out.append(buf)
    return out


def tex2sym(tex):
    """Tiny TeX reader for the answer dialect this page actually uses."""
    t=tex.strip()
    t=t.replace("\\dfrac","\\frac").replace("\\tfrac","\\frac")
    t=t.replace("\\hat","").replace("\\vec","")
    t=t.replace("\\,","").replace("\\!","").replace("\\;","").replace("~","")
    t=re.sub(r"\\left|\\right","",t)
    # "\operatorname{div}\vec F = ..." — drop the named-operator label.
    t=re.sub(r"\\operatorname\{[^{}]*\}","",t)
    t=re.sub(r"^\s*\\?[A-Za-z]+(_\{?\w*\}?)?\s*=\s*","",t)   # "c = ", "\theta = ", "L = "
    # \frac{a}{b}  (repeat for nesting)
    for _ in range(4):
        t=re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", t)
    t=re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", t)
    t=re.sub(r"\\sqrt(\d)", r"sqrt(\1)", t)
    t=t.replace("\\pi","pi").replace("\\cdot","*")
    t=re.sub(r"e\^\{([^{}]*)\}", r"exp(\1)", t)
    t=re.sub(r"e\^\{?(-?\d+)\}?", r"exp(\1)", t)
    # A bare `e` in these answers is Euler's number, not a symbol — and
    # sympify("2e") silently reads as the float 20. Both must be handled
    # before sympify sees the string: "3(e-1)/2" and "e^2-2e+1" were each
    # mis-read, and the second is the dangerous one because it parses.
    t=re.sub(r"(?<![A-Za-z0-9_])e(?![A-Za-z0-9_(])", "E", t)
    # Implicit multiplication — "9\pi\sqrt2", "2E", "3(e-1)" — must be inserted
    # BEFORE exponents are rewritten, or "t^2" becomes "2*t", and it must never
    # fire inside a function name, or "exp(" becomes "e*xp(".
    _FN = ("sqrt", "exp", "pi", "log", "sin", "cos", "tan", "atan", "acos", "E")
    t=re.sub(r"(\d)\s*(?=[A-Za-z(])", r"\1*", t)
    for fn in _FN:                      # repair any name we just split
        t=t.replace(fn[0] + "*" + fn[1:], fn)
    t=re.sub(r"(?<=[A-Za-z0-9_)])\s*(?=(?:sqrt|exp|pi)\()", "*", t)
    t=re.sub(r"(?<=[A-Za-z0-9_)])\s*(?=pi(?![A-Za-z0-9_]))", "*", t)
    t=re.sub(r"\^\{([^{}]*)\}", r"**(\1)", t)
    t=re.sub(r"\^(-?\w)", r"**\1", t)
    t=re.sub(r"(\))\s*\(", r"\1*(", t)
    t=re.sub(r"\*{3,}", "**", t)
    # Implicit multiplication inside what were exponent braces: e^{xy} became
    # exp((xy)) above, and "xy" is one symbol to sympy, not x*y.
    def _split_vars(m):
        body = m.group(1)
        # "xy" inside an exponent is x*y — but "pi" is one constant, not p*i,
        # and neither is any other name we know.
        if body in ("pi", "exp", "log", "sin", "cos", "tan", "oo"):
            return m.group(0)
        if re.fullmatch(r"[a-z]{2,3}", body):
            return "(" + "*".join(body) + ")"
        return m.group(0)
    t=re.sub(r"\(([A-Za-z0-9_]+)\)", _split_vars, t)
    # A lone `e` can survive the earlier pass when an `e^{...}` in the same
    # string was already turned into exp(...). Catch it now, but never touch
    # the `e` that is part of exp(.
    t=re.sub(r"(?<![A-Za-z0-9_])e(?!xp\()(?![A-Za-z0-9_])", "E", t)
    if re.search(r"[\\{}]", t): return None
    return t



def run(verbose=False):
    """Returns (agree, disagree, skipped, mismatches)."""
    # Every official guide we publish a page for, not just Exam 1.
    import exam1page
    official = {}
    for g in exam1page.GUIDES:
        d = exam1_src.read(exam1_src.HERE / "sources" / g["file"],
                           expect=g["expect"])
        for sec in d["sections"]:
            for p in sec["problems"]:
                official[p["pid"]] = p["answer"]
    agree = skip = 0
    mismatches, skipped = [], []
    for pid, sol in M.all_solutions().items():
        want, ans = sol.get("want"), official.get(pid)
        if want is None or ans is None or isinstance(want, dict):
            skip += 1; skipped.append(pid); continue
        m = re.findall(r"\$(.+?)\$", ans, re.S)
        if not m:
            skip += 1; skipped.append(pid); continue
        tex = re.sub(r"\\left|\\right", "", m[0])
        tex = tex.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
        tex = tex.replace("\\hat", "").replace("\\vec", "")
        # Drop a leading label up to the first top-level "=" — "f_x(1,2) =",
        # "D_{u}f(2,1) =", "\frac{\partial z}{\partial x} =" — but leave real
        # equations like "x^2+y^2 = 4" alone.
        if "=" in tex:
            lhs, _, rhs = tex.partition("=")
            if not re.search(r"[+\-*/^]", lhs) and rhs.strip():
                tex = rhs
        vm = re.search(r"\\langle(.*?)\\rangle", tex, re.S)
        try:
            if vm:
                if not isinstance(want, (list, tuple, Matrix)):
                    skip += 1; skipped.append(pid); continue
                parts = [tex2sym(c) for c in split_top(vm.group(1))]
                if any(c is None for c in parts):
                    skip += 1; skipped.append(pid); continue
                got, wv = Matrix([_sym(c) for c in parts]), Matrix(list(want))
                ok = got.shape == wv.shape and simplify(got - wv) == Matrix.zeros(*got.shape)
            else:
                if isinstance(want, (list, tuple, Matrix)):
                    skip += 1; skipped.append(pid); continue
                src_ = tex2sym(tex)
                if src_ is None:
                    skip += 1; skipped.append(pid); continue
                got = _sym(src_)
                ok = simplify(got - sympify(want)) == 0
        except Exception:
            skip += 1; skipped.append(pid); continue
        if ok:
            agree += 1
        else:
            mismatches.append((pid, m[0], str(want), str(got)))
    if verbose:
        print(f"{agree} agree, {len(mismatches)} disagree, {skip} not comparable")
        for x in mismatches:
            print("   ", x)
    return agree, len(mismatches), skip, mismatches


def gate():
    """Every disagreement must be a documented correction, or the build dies."""
    agree, n_dis, skip, mismatches = run()
    bank = M.all_solutions()
    undocumented = [m for m in mismatches if not bank[m[0]].get("fix")]
    if undocumented:
        import sys
        for pid, tex, want, got in undocumented:
            print(f"exam1_audit: {pid} disagrees with the official answer and "
                  f"carries no documented correction.\n"
                  f"    official TeX : {tex}\n"
                  f"    parsed as    : {got}\n"
                  f"    we computed  : {want}", file=sys.stderr)
        sys.exit("exam1_audit: undocumented disagreement with the official guide")
    return agree, n_dis, skip


if __name__ == "__main__":
    run(verbose=True)
