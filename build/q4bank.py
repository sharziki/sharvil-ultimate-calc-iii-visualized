"""Quiz 4 questions — 14.4 arc length, 14.5 curvature & TNB, 15.1 surfaces, 15.2 limits.

Written against the actual MyLab problem set assigned for Lessons 8-10
(14.4.9/11/13/23/40/42, 14.5.11/13/15/23, 15.1.11/15/17/19/25/28/30/34/35),
so every pattern that appears there appears here at least once:

  14.4  length when |r'| collapses to c*t          (14.4.9, 14.4.23)
  14.4  length of a circle / constant-speed curve  (14.4.11)
  14.4  the sin-minus-t-cos pair whose speed is at (14.4.13)
  14.4  "does this use arc length as a parameter?" (14.4.40 no, 14.4.42 yes)
  14.4  rewriting r(t) as r(s)                     (14.4.40)
  14.5  T and kappa for a LINE  (kappa = 0)        (14.5.11)
  14.5  T and kappa for a helix                    (14.5.13)
  14.5  T and kappa for an ellipse-in-a-plane      (14.5.15)
  14.5  alternative formula |a x v| / |v|^3        (14.5.23)
  15.1  level curves of a named surface            (15.1.11)
  15.1  domain: polynomial, radical, rational, trig(15.1.15/17/19)
  15.1  sketch + domain + range of a plane         (15.1.25)
  15.1  cylinder z = f(x) only                     (15.1.28)
  15.1  hemisphere, bounded domain and range       (15.1.30)
  15.1  match a surface to its level curves        (15.1.34/35)
  15.2  two-path test, limits along y = mx, y = x^2
"""

from sympy import (Matrix, S, sqrt, cos, sin, pi, log, symbols, integrate,
                   solve, simplify, diff, Rational)

t = symbols("t", real=True)
x, y, m = symbols("x y m", real=True)


def V(*c):
    return Matrix(list(c))


def speed(*comps):
    """|r'(t)|, simplified, for t >= 0."""
    return simplify(sqrt(sum(diff(c, t) ** 2 for c in comps)))


def _polar_limit():
    """x^2 y / (x^2+y^2) in polar is r cos^2(th) sin(th); r -> 0 kills it."""
    r, th = symbols("r th", positive=True)
    expr = simplify(((r*cos(th))**2 * (r*sin(th))) / ((r*cos(th))**2 + (r*sin(th))**2))
    return simplify(expr.subs(r, 0))


def arclen(a, b, *comps):
    return simplify(integrate(speed(*comps), (t, a, b)))


QUESTIONS = [

    # ======================================================== 14.4 ==========

    dict(
        quiz="q4", id="Q4a", sec="14.4", title="14.4 · Length when the speed is a multiple of t",
        stem=r"Find the length of $\mathbf r(t)=\langle 20t^{2},\,-6,\,48t^{2}+5\rangle$ "
             r"for $0\le t\le1$.",
        opts={"A": r"52", "B": r"104", "C": r"26", "D": r"\sqrt{104}",
              "E": r"68", "F": r"2704"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle 40t,\;0,\;96t\rangle$ — the constant $-6$ "
             r"differentiates away, and so does the $+5$.",
             r"$|\mathbf r'(t)|=\sqrt{1600t^{2}+9216t^{2}}=\sqrt{10816}\,t=104t$ "
             r"(positive on $[0,1]$, so no absolute value survives).",
             r"$L=\displaystyle\int_0^1 104t\,dt=104\cdot\tfrac12=52$."],
        trap="Forgetting the $\\tfrac12$ from $\\int t\\,dt$ and answering $104$, the speed "
             "at $t=1$. A speed that grows linearly averages to half its final value.",
        check=lambda: arclen(0, 1, 20*t**2, S(-6), 48*t**2 + 5), want=S(52),
    ),
    dict(
        quiz="q4", id="Q4b", sec="14.4", title="14.4 · Length of a circular arc",
        stem=r"Find the length of $\mathbf r(t)=\langle 3\cos t,\;3\sin t\rangle$ "
             r"for $0\le t\le\pi$.",
        opts={"A": r"3\pi", "B": r"6\pi", "C": r"\pi", "D": r"9\pi",
              "E": r"\dfrac{3\pi}{2}", "F": r"3"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle -3\sin t,\;3\cos t\rangle$.",
             r"$|\mathbf r'(t)|=\sqrt{9\sin^{2}t+9\cos^{2}t}=3$ — constant speed, which is "
             r"what a circle traced at uniform rate always gives.",
             r"$L=3(\pi-0)=3\pi$: half the circumference $2\pi(3)=6\pi$. &check;"],
        trap="Answering $6\\pi$, the whole circumference. The parameter stops at $\\pi$, "
             "which is half a turn.",
        check=lambda: arclen(0, pi, 3*cos(t), 3*sin(t)), want=3*pi,
    ),
    dict(
        quiz="q4", id="Q4c", sec="14.4", title="14.4 · The sin−t·cos pair",
        stem=r"Find the length of $\mathbf r(t)=\langle 4\sin t-4t\cos t,\;"
             r"4\cos t+4t\sin t\rangle$ for $0\le t\le\dfrac{\pi}{2}$.",
        opts={"A": r"\dfrac{\pi^{2}}{2}", "B": r"\dfrac{\pi^{2}}{4}",
              "C": r"2\pi", "D": r"\dfrac{\pi^{2}}{8}",
              "E": r"4\pi", "F": r"\dfrac{\pi}{2}"},
        key="A",
        sol=[r"Product rule: $x'=4\cos t-4\cos t+4t\sin t=4t\sin t$ — the two $\cos$ terms "
             r"cancel. Likewise $y'=-4\sin t+4\sin t+4t\cos t=4t\cos t$.",
             r"$|\mathbf r'(t)|=\sqrt{16t^{2}\sin^{2}t+16t^{2}\cos^{2}t}=4t$ on $t\ge0$.",
             r"$L=\displaystyle\int_0^{\pi/2}4t\,dt=2t^{2}\Big|_0^{\pi/2}"
             r"=2\cdot\dfrac{\pi^{2}}{4}=\dfrac{\pi^{2}}{2}$."],
        trap="Not differentiating $4t\\cos t$ as a product. The whole curve is built so that "
             "the non-$t$ terms cancel and the speed collapses to $4t$ — if your speed still "
             "has a $\\sin$ or $\\cos$ loose in it, you dropped a term.",
        check=lambda: arclen(0, pi/2, 4*sin(t) - 4*t*cos(t), 4*cos(t) + 4*t*sin(t)),
        want=pi**2/2,
    ),
    dict(
        quiz="q4", id="Q4d", sec="14.4", title="14.4 · Speed of a cubic trajectory",
        stem=r"For $\mathbf r(t)=\langle 3t^{3},\,-t^{3},\,4t^{3}\rangle$, $0\le t\le6$, "
             r"find the speed.",
        opts={"A": r"3\sqrt{26}\,t^{2}", "B": r"\sqrt{26}\,t^{2}",
              "C": r"3\sqrt{26}\,t^{3}", "D": r"26t^{2}",
              "E": r"9\sqrt{26}\,t^{2}", "F": r"\sqrt{26}\,t"},
        key="A",
        sol=[r"$\mathbf v=\mathbf r'(t)=\langle 9t^{2},\,-3t^{2},\,12t^{2}\rangle "
             r"=3t^{2}\langle 3,-1,4\rangle$.",
             r"$|\mathbf v|=3t^{2}\,|\langle3,-1,4\rangle|=3t^{2}\sqrt{9+1+16}"
             r"=3\sqrt{26}\,t^{2}$ (the $t^{2}\ge0$, so no absolute value).",
             r"Equivalently $\sqrt{234}\,t^{2}$ — same number."],
        trap="Factoring $t^{2}$ out of the square root but leaving the $3$ behind, or keeping "
             "$t^{3}$: the derivative drops the exponent by one.",
        check=lambda: speed(3*t**3, -t**3, 4*t**3), want=3*sqrt(26)*t**2,
    ),
    dict(
        quiz="q4", id="Q4e", sec="14.4", title="14.4 · Length of that cubic",
        stem=r"For the same $\mathbf r(t)=\langle 3t^{3},\,-t^{3},\,4t^{3}\rangle$, "
             r"find the length of the trajectory on $0\le t\le6$.",
        opts={"A": r"216\sqrt{26}", "B": r"72\sqrt{26}", "C": r"648\sqrt{26}",
              "D": r"108\sqrt{26}", "E": r"36\sqrt{26}", "F": r"216"},
        key="A",
        sol=[r"$L=\displaystyle\int_0^6 3\sqrt{26}\,t^{2}\,dt"
             r"=3\sqrt{26}\cdot\dfrac{t^{3}}{3}\Big|_0^6=\sqrt{26}\,t^{3}\Big|_0^6$.",
             r"$=216\sqrt{26}$."],
        trap="The $3$ in front and the $\\tfrac13$ from $\\int t^{2}dt$ cancel exactly. "
             "Forgetting one of them gives $648\\sqrt{26}$ or $72\\sqrt{26}$.",
        check=lambda: arclen(0, 6, 3*t**3, -t**3, 4*t**3), want=216*sqrt(26),
    ),
    dict(
        quiz="q4", id="Q4f", sec="14.4", title="14.4 · Is t already arc length?",
        concept=True,
        stem=r"Does $\mathbf r(t)=\left\langle \dfrac{1}{\sqrt2}\cos t,\;"
             r"\dfrac{1}{\sqrt2}\cos t,\;\sin t\right\rangle$ use arc length as its "
             r"parameter?",
        opts={"A": {"text": "Yes — $|\\mathbf r'(t)|=1$ for every $t$"},
              "B": {"text": "No — $|\\mathbf r'(t)|=\\sqrt2$"},
              "C": {"text": "No — the speed depends on $t$"},
              "D": {"text": "Yes, but only on $0\\le t\\le\\pi$"},
              "E": {"text": "No — a curve in three variables never can"},
              "F": {"text": "Only if the interval is rescaled by $2\\pi$"}},
        key="A",
        sol=[r"$\mathbf r'(t)=\left\langle -\tfrac{1}{\sqrt2}\sin t,\;"
             r"-\tfrac{1}{\sqrt2}\sin t,\;\cos t\right\rangle$.",
             r"$|\mathbf r'(t)|^{2}=\tfrac12\sin^{2}t+\tfrac12\sin^{2}t+\cos^{2}t"
             r"=\sin^{2}t+\cos^{2}t=1$.",
             r"The test is exactly $|\mathbf r'|=1$ for all $t$ — and it holds, so $t$ "
             r"<b>is</b> arc length, measured from $t=0$."],
        trap="Assuming the two $\\tfrac{1}{\\sqrt2}$ components must add to something bigger "
             "than one. They are each squared first, and $\\tfrac12+\\tfrac12=1$ — the "
             "constants are chosen precisely to make the speed unit.",
    ),
    dict(
        quiz="q4", id="Q4g", sec="14.4", title="14.4 · Reparameterising by arc length",
        stem=r"$\mathbf r(t)=\langle 7t^{2},\,8t^{2},\,2\sqrt{14}\,t^{2}\rangle$ for "
             r"$1\le t\le4$ does <b>not</b> use arc length. Which $\mathbf r(s)$ does?",
        opts={"A": r"\left\langle 7+\tfrac{7s}{13},\;8+\tfrac{8s}{13},\;"
                   r"2\sqrt{14}+\tfrac{2\sqrt{14}\,s}{13}\right\rangle,\ 0\le s\le195",
              "B": r"\left\langle 7+\tfrac{7s}{13},\;8+\tfrac{8s}{13},\;"
                   r"2\sqrt{14}+\tfrac{2\sqrt{14}\,s}{14}\right\rangle,\ 0\le s\le195",
              "C": r"\left\langle \tfrac{7s}{13},\;\tfrac{8s}{13},\;"
                   r"\tfrac{2\sqrt{14}\,s}{13}\right\rangle,\ 0\le s\le195",
              "D": r"\left\langle 7+\tfrac{7s}{13},\;8+\tfrac{8s}{13},\;"
                   r"2\sqrt{14}+\tfrac{2\sqrt{14}\,s}{13}\right\rangle,\ 0\le s\le13",
              "E": r"\left\langle 7s^{2},\;8s^{2},\;2\sqrt{14}\,s^{2}\right\rangle,\ 0\le s\le3",
              "F": r"\left\langle 7+7s,\;8+8s,\;2\sqrt{14}+2\sqrt{14}\,s\right\rangle,\ 0\le s\le15"},
        key="A",
        sol=[r"The curve is the ray $t^{2}\langle 7,8,2\sqrt{14}\rangle$, and "
             r"$|\langle 7,8,2\sqrt{14}\rangle|=\sqrt{49+64+56}=\sqrt{169}=13$.",
             r"Arc length from the start: $s(t)=\displaystyle\int_1^{t}26u\,du=13(t^{2}-1)$, "
             r"so $t^{2}=1+\dfrac{s}{13}$.",
             r"Substitute: $\mathbf r(s)=\left(1+\tfrac{s}{13}\right)"
             r"\langle 7,8,2\sqrt{14}\rangle$ — that is "
             r"$\left\langle 7+\tfrac{7s}{13},\,8+\tfrac{8s}{13},\,"
             r"2\sqrt{14}+\tfrac{2\sqrt{14}s}{13}\right\rangle$.",
             r"Upper limit: $s(4)=13(16-1)=195$."],
        trap="Putting the component's own coefficient in the denominator — $2\\sqrt{14}s/14$ "
             "instead of $2\\sqrt{14}s/13$. <b>Every</b> component is divided by the same "
             "$|\\mathbf v|$-derived constant $13$; it is the length of the direction "
             "vector, not of one entry.",
        check=lambda: (sqrt(S(7)**2 + S(8)**2 + (2*sqrt(14))**2), 13*(S(16) - 1)),
        want=(S(13), S(195)),
    ),

    # ======================================================== 14.5 ==========

    dict(
        quiz="q4", id="Q4h", sec="14.5", title="14.5 · T and curvature of a line",
        stem=r"For $\mathbf r(t)=\langle 2t+2,\;4t-8,\;5t+14\rangle$, find $\mathbf T$ "
             r"and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle \tfrac{2}{\sqrt{45}},\tfrac{4}{\sqrt{45}},"
                   r"\tfrac{5}{\sqrt{45}}\right\rangle,\ \kappa=0",
              "B": r"\mathbf T=\langle 2,4,5\rangle,\ \kappa=0",
              "C": r"\mathbf T=\left\langle \tfrac{2}{\sqrt{45}},\tfrac{4}{\sqrt{45}},"
                   r"\tfrac{5}{\sqrt{45}}\right\rangle,\ \kappa=\tfrac{1}{\sqrt{45}}",
              "D": r"\mathbf T=\left\langle \tfrac{2}{45},\tfrac{4}{45},\tfrac{5}{45}"
                   r"\right\rangle,\ \kappa=0",
              "E": r"\mathbf T=\left\langle \tfrac{2}{\sqrt{45}},\tfrac{4}{\sqrt{45}},"
                   r"\tfrac{5}{\sqrt{45}}\right\rangle,\ \kappa=45",
              "F": r"\mathbf T\ \text{is undefined},\ \kappa=0"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle 2,4,5\rangle$, constant, with "
             r"$|\mathbf r'|=\sqrt{4+16+25}=\sqrt{45}=3\sqrt5$.",
             r"$\mathbf T=\dfrac{\mathbf r'}{|\mathbf r'|}"
             r"=\left\langle \tfrac{2}{3\sqrt5},\tfrac{4}{3\sqrt5},\tfrac{5}{3\sqrt5}"
             r"\right\rangle$ — rationalised, $\left\langle \tfrac{2\sqrt5}{15},"
             r"\tfrac{4\sqrt5}{15},\tfrac{\sqrt5}{3}\right\rangle$.",
             r"$\mathbf T$ is constant, so $\dfrac{d\mathbf T}{dt}=\mathbf 0$ and "
             r"$\kappa=0$. A straight line has no curvature — as it must."],
        trap="Dividing by $45$ instead of $\\sqrt{45}$, or reporting $\\mathbf T=\\mathbf r'$ "
             "unnormalised. $\\mathbf T$ is always a <b>unit</b> vector — check that the "
             "squares of your three entries add to $1$.",
        check=lambda: V(2, 4, 5).norm(), want=3*sqrt(5),
    ),
    dict(
        quiz="q4", id="Q4i", sec="14.5", title="14.5 · T and curvature of a helix",
        stem=r"For $\mathbf r(t)=\langle \sqrt3\,t,\;3\sin t,\;3\cos t\rangle$, "
             r"find $\mathbf T$ and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle \tfrac12,\;\tfrac{\sqrt3}{2}\cos t,\;"
                   r"-\tfrac{\sqrt3}{2}\sin t\right\rangle,\ \kappa=\tfrac14",
              "B": r"\mathbf T=\left\langle \tfrac12,\;\tfrac{\sqrt3}{2}\cos t,\;"
                   r"-\tfrac{\sqrt3}{2}\cos t\right\rangle,\ \kappa=\tfrac14",
              "C": r"\mathbf T=\left\langle \tfrac{\sqrt3}{2},\;\tfrac12\cos t,\;"
                   r"-\tfrac12\sin t\right\rangle,\ \kappa=\tfrac14",
              "D": r"\mathbf T=\left\langle \tfrac12,\;\tfrac{\sqrt3}{2}\cos t,\;"
                   r"-\tfrac{\sqrt3}{2}\sin t\right\rangle,\ \kappa=\tfrac13",
              "E": r"\mathbf T=\langle \sqrt3,\;3\cos t,\;-3\sin t\rangle,\ \kappa=\tfrac14",
              "F": r"\mathbf T=\left\langle \tfrac12,\;\tfrac{\sqrt3}{2}\cos t,\;"
                   r"-\tfrac{\sqrt3}{2}\sin t\right\rangle,\ \kappa=\tfrac34"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle \sqrt3,\;3\cos t,\;-3\sin t\rangle$ and "
             r"$|\mathbf r'|=\sqrt{3+9\cos^{2}t+9\sin^{2}t}=\sqrt{12}=2\sqrt3$.",
             r"$\mathbf T=\dfrac{1}{2\sqrt3}\langle \sqrt3,3\cos t,-3\sin t\rangle"
             r"=\left\langle \tfrac12,\;\tfrac{\sqrt3}{2}\cos t,\;-\tfrac{\sqrt3}{2}\sin t"
             r"\right\rangle$.",
             r"$\mathbf T'=\left\langle 0,\,-\tfrac{\sqrt3}{2}\sin t,\,"
             r"-\tfrac{\sqrt3}{2}\cos t\right\rangle$, so $|\mathbf T'|=\tfrac{\sqrt3}{2}$.",
             r"$\kappa=\dfrac{|\mathbf T'|}{|\mathbf r'|}"
             r"=\dfrac{\sqrt3/2}{2\sqrt3}=\dfrac14$."],
        trap="Writing the third component of $\\mathbf T$ as $\\cos t$. "
             "$\\dfrac{d}{dt}(3\\cos t)=-3\\sin t$ — the derivative of cosine is "
             "<b>minus sine</b>, and this single slip is the most common lost mark on the "
             "whole section.",
        check=lambda: (speed(sqrt(3)*t, 3*sin(t), 3*cos(t)),
                       simplify(sqrt(sum(diff(c, t)**2 for c in
                                         (S(1)/2, sqrt(3)/2*cos(t), -sqrt(3)/2*sin(t))))
                                / speed(sqrt(3)*t, 3*sin(t), 3*cos(t)))),
        want=(2*sqrt(3), Rational(1, 4)),
    ),
    dict(
        quiz="q4", id="Q4j", sec="14.5", title="14.5 · T and curvature of a tilted circle",
        stem=r"For $\mathbf r(t)=\langle \sqrt{19}\cos t,\;9\cos t,\;10\sin t\rangle$, "
             r"find $\mathbf T$ and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle -\tfrac{\sqrt{19}}{10}\sin t,\;"
                   r"-\tfrac{9}{10}\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac{1}{10}",
              "B": r"\mathbf T=\left\langle -\sqrt{\tfrac{19}{10}}\sin t,\;"
                   r"-\tfrac{9}{10}\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac{1}{10}",
              "C": r"\mathbf T=\left\langle -\tfrac{\sqrt{19}}{10}\cos t,\;"
                   r"-\tfrac{9}{10}\cos t,\;\sin t\right\rangle,\ \kappa=\tfrac{1}{10}",
              "D": r"\mathbf T=\left\langle -\tfrac{\sqrt{19}}{10}\sin t,\;"
                   r"-\tfrac{9}{10}\sin t,\;\cos t\right\rangle,\ \kappa=10",
              "E": r"\mathbf T=\langle -\sqrt{19}\sin t,\;-9\sin t,\;10\cos t\rangle,\ "
                   r"\kappa=\tfrac{1}{10}",
              "F": r"\mathbf T=\left\langle -\tfrac{\sqrt{19}}{10}\sin t,\;"
                   r"-\tfrac{9}{10}\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac{1}{100}"},
        key="A",
        sol=[r"$\mathbf r'=\langle -\sqrt{19}\sin t,\;-9\sin t,\;10\cos t\rangle$.",
             r"$|\mathbf r'|^{2}=19\sin^{2}t+81\sin^{2}t+100\cos^{2}t"
             r"=100\sin^{2}t+100\cos^{2}t=100$, so $|\mathbf r'|=10$ — constant. "
             r"(The $19+81=100$ is the whole design of the problem.)",
             r"$\mathbf T=\tfrac{1}{10}\mathbf r'"
             r"=\left\langle -\tfrac{\sqrt{19}}{10}\sin t,\,-\tfrac{9}{10}\sin t,\,"
             r"\cos t\right\rangle$.",
             r"$|\mathbf T'|=\left|\left\langle -\tfrac{\sqrt{19}}{10}\cos t,"
             r"-\tfrac{9}{10}\cos t,-\sin t\right\rangle\right|=1$, so "
             r"$\kappa=\dfrac{1}{10}$ — it is a circle of radius $10$ in a tilted plane."],
        trap="Typing $\\sqrt{19/10}$ when you mean $\\dfrac{\\sqrt{19}}{10}$. The $10$ is "
             "outside the radical: it came from dividing by $|\\mathbf r'|$, not from "
             "anything under the root.",
        check=lambda: (speed(sqrt(19)*cos(t), 9*cos(t), 10*sin(t)),),
        want=(S(10),),
    ),
    dict(
        quiz="q4", id="Q4k", sec="14.5", title="14.5 · Alternative curvature formula",
        stem=r"Use $\kappa=\dfrac{|\mathbf a\times\mathbf v|}{|\mathbf v|^{3}}$ to find the "
             r"curvature of $\mathbf r(t)=\langle 3+t^{2},\,t,\,0\rangle$.",
        opts={"A": r"\dfrac{2}{(4t^{2}+1)^{3/2}}", "B": r"\dfrac{2}{(4t^{2}+1)^{1/2}}",
              "C": r"\dfrac{1}{(4t^{2}+1)^{3/2}}", "D": r"\dfrac{2}{4t^{2}+1}",
              "E": r"\dfrac{2t}{(4t^{2}+1)^{3/2}}", "F": r"\dfrac{4}{(4t^{2}+1)^{3/2}}"},
        key="A",
        sol=[r"$\mathbf v=\langle 2t,1,0\rangle$ and $\mathbf a=\langle 2,0,0\rangle$.",
             r"$\mathbf a\times\mathbf v=\langle 2,0,0\rangle\times\langle 2t,1,0\rangle"
             r"=\langle 0\cdot0-0\cdot1,\;0\cdot 2t-2\cdot0,\;2\cdot1-0\cdot2t\rangle"
             r"=\langle 0,0,2\rangle$, so $|\mathbf a\times\mathbf v|=2$.",
             r"$|\mathbf v|=\sqrt{4t^{2}+1}$, so $|\mathbf v|^{3}=(4t^{2}+1)^{3/2}$.",
             r"$\kappa=\dfrac{2}{(4t^{2}+1)^{3/2}}$ — largest at $t=0$, the vertex of the "
             r"parabola $x=3+y^{2}$."],
        trap="Cubing only the inside and writing $(4t^{2}+1)^{3}$, or forgetting to cube at "
             "all. The denominator is the <b>speed</b> cubed, and the speed already carries "
             "a square root: $\\left(\\sqrt{u}\\right)^{3}=u^{3/2}$.",
        check=lambda: simplify(V(2, 0, 0).cross(V(2*t, 1, 0)).norm()
                               / V(2*t, 1, 0).norm()**3),
        want=2/(4*t**2 + 1)**Rational(3, 2),
    ),
    dict(
        quiz="q4", id="Q4l", sec="14.5", title="14.5 · Curvature of a plane curve y = f(x)",
        stem=r"Find the curvature of $y=\tfrac12x^{2}$ at the point $\left(1,\tfrac12\right)$.",
        opts={"A": r"\dfrac{1}{2\sqrt2}", "B": r"\dfrac{1}{2}", "C": r"1",
              "D": r"\dfrac{1}{\sqrt2}", "E": r"\dfrac{1}{4}", "F": r"2\sqrt2"},
        key="A",
        sol=[r"Parameterise $\mathbf r(x)=\langle x,\;\tfrac12x^{2},\;0\rangle$, so "
             r"$\mathbf v=\langle 1,x,0\rangle$ and $\mathbf a=\langle 0,1,0\rangle$.",
             r"$\mathbf v\times\mathbf a=\langle 0,0,1\rangle$, magnitude $1$ — this is the "
             r"general $|y''|$ for a graph.",
             r"$\kappa=\dfrac{|y''|}{\left(1+(y')^{2}\right)^{3/2}}"
             r"=\dfrac{1}{(1+x^{2})^{3/2}}$; at $x=1$ that is "
             r"$\dfrac{1}{2^{3/2}}=\dfrac{1}{2\sqrt2}$."],
        trap="Using $y=\\tfrac12$ instead of $x=1$ in the formula. The variable in "
             "$\\left(1+(y')^{2}\\right)^{3/2}$ is $x$; the $y$-coordinate only tells you "
             "you are on the right curve.",
        check=lambda: (S(1)/(1 + S(1)**2)**Rational(3, 2),), want=(1/(2*sqrt(2)),),
    ),

    # ======================================================== 15.1 ==========

    dict(
        quiz="q4", id="Q4m", sec="15.1", title="15.1 · Level curves of a paraboloid",
        concept=True,
        stem=r"Describe the level curves of the paraboloid $z=x^{2}+y^{2}$.",
        opts={"A": {"text": "Circles $x^{2}+y^{2}=z_0$"},
              "B": {"text": "Parabolas $x^{2}=z_0$"},
              "C": {"text": "Parabolas $y^{2}=z_0$"},
              "D": {"text": "Lines $x+y=z_0$"},
              "E": {"text": "Ellipses $x^{2}+4y^{2}=z_0$"},
              "F": {"text": "Hyperbolas $x^{2}-y^{2}=z_0$"}},
        key="A",
        sol=[r"A level curve is what you get by setting $z$ to a constant $z_0$: "
             r"$x^{2}+y^{2}=z_0$.",
             r"For $z_0>0$ that is a circle of radius $\sqrt{z_0}$, centred at the origin; "
             r"$z_0=0$ gives the single point $(0,0)$, and $z_0<0$ gives nothing.",
             r"The radii grow like $\sqrt{z_0}$, so evenly spaced levels give rings that "
             r"<b>crowd together</b> as you climb — the bowl is steepening."],
        trap="Confusing the level curves (slices $z=z_0$, seen from above) with the traces "
             "in the $xz$- and $yz$-planes, which really are parabolas. Both are slices; "
             "only the horizontal ones are level curves.",
    ),
    dict(
        quiz="q4", id="Q4n", sec="15.1", title="15.1 · Domain of a polynomial",
        concept=True,
        stem=r"Find the domain of $f(x,y)=9xy+5x+4y$.",
        opts={"A": {"text": "$\\mathbb R^{2}$"},
              "B": {"text": "$\\{(x,y):x\\ne y\\}$"},
              "C": {"text": "$\\{(x,y):xy>0\\}$"},
              "D": {"text": "$\\{(x,y):x\\ne0\\text{ and }y\\ne0\\}$"},
              "E": {"text": "$\\{(x,y):9xy+5x+4y\\ge0\\}$"},
              "F": {"text": "$\\{(x,y):x>0\\}$"}},
        key="A",
        sol=[r"A polynomial in $x$ and $y$ is built from products and sums only.",
             r"There is no denominator to vanish, no radical to go negative and no "
             r"logarithm to hit zero.",
             r"Every point of the plane works: the domain is $\mathbb R^{2}$."],
        trap="Reading $9xy$ as something that constrains the signs. Products are fine "
             "everywhere; only division, even roots and logs ever restrict a domain.",
    ),
    dict(
        quiz="q4", id="Q4o", sec="15.1", title="15.1 · Domain under a square root",
        stem=r"Find the domain of $f(x,y)=\sqrt{12-3x^{2}-3y^{2}}$.",
        opts={"A": r"\{(x,y):x^{2}+y^{2}\le4\}", "B": r"\{(x,y):x^{2}+y^{2}\le12\}",
              "C": r"\{(x,y):x^{2}+y^{2}\ge4\}", "D": r"\{(x,y):x^{2}+y^{2}<4\}",
              "E": r"\{(x,y):x^{2}+y^{2}\le2\}", "F": r"\mathbb R^{2}"},
        key="A",
        sol=[r"An even root needs its radicand non-negative: $12-3x^{2}-3y^{2}\ge0$.",
             r"Divide by $3$: $4-x^{2}-y^{2}\ge0$, that is $x^{2}+y^{2}\le4$.",
             r"A closed disc of radius $2$ — closed, because equality is allowed and "
             r"$\sqrt0=0$ is perfectly defined."],
        trap="Forgetting to divide by the $3$ and answering $x^{2}+y^{2}\\le12$, or making "
             "the inequality strict. Strict belongs to logarithms and denominators, not to "
             "square roots.",
        check=lambda: (12 - 3*S(2)**2, 12 - 3*S(0)**2), want=(S(0), S(12)),
    ),
    dict(
        quiz="q4", id="Q4p", sec="15.1", title="15.1 · Domain of a composition",
        concept=True,
        stem=r"Find the domain of $f(x,y)=\sin\!\left(\dfrac{x-6}{y-8}\right)$.",
        opts={"A": {"text": "$\\{(x,y):y\\ne8\\}$"},
              "B": {"text": "$\\{(x,y):x\\ne6\\}$"},
              "C": {"text": "$\\{(x,y):x\\ne6\\text{ and }y\\ne8\\}$"},
              "D": {"text": "$\\{(x,y):-1\\le\\frac{x-6}{y-8}\\le1\\}$"},
              "E": {"text": "$\\mathbb R^{2}$"},
              "F": {"text": "$\\{(x,y):y>8\\}$"}},
        key="A",
        sol=[r"$\sin$ accepts every real input, so it imposes nothing.",
             r"The only restriction lives in the fraction: $y-8\ne0$.",
             r"Domain: everything except the horizontal line $y=8$."],
        trap="Restricting the argument to $[-1,1]$. That is the <b>range</b> of sine, not "
             "its domain — the constraint you would impose for $\\arcsin$, not $\\sin$.",
    ),
    dict(
        quiz="q4", id="Q4q", sec="15.1", title="15.1 · A plane: intercepts, domain, range",
        stem=r"For $f(x,y)=5x+4y-20$, which set of intercepts identifies its graph, and "
             r"what are the domain and range?",
        opts={"A": r"(4,0,0),\,(0,5,0),\,(0,0,-20);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "B": r"(5,0,0),\,(0,4,0),\,(0,0,20);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "C": r"(4,0,0),\,(0,5,0),\,(0,0,-20);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }z\ge-20",
              "D": r"(-4,0,0),\,(0,-5,0),\,(0,0,-20);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "E": r"(20,0,0),\,(0,20,0),\,(0,0,-20);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "F": r"(4,0,0),\,(0,5,0),\,(0,0,-20);\ \text{domain }x,y\ge0,\ "
                   r"\text{range }\mathbb R"},
        key="A",
        sol=[r"$x$-intercept: set $y=z=0$, so $5x=20$ and $x=4$.",
             r"$y$-intercept: set $x=z=0$, so $4y=20$ and $y=5$. Note the coefficients and "
             r"the intercepts <b>swap</b>: a big coefficient gives a small intercept.",
             r"$z$-intercept: $f(0,0)=-20$.",
             r"A plane is defined for every $(x,y)$ and, being non-constant and linear, it "
             r"attains every real value: domain $\mathbb R^{2}$, range $\mathbb R$."],
        trap="Reading the intercepts straight off the coefficients as $(5,0,0)$ and "
             "$(0,4,0)$. You divide by the coefficient, you do not copy it.",
        check=lambda: (solve(5*x - 20, x)[0], solve(4*y - 20, y)[0]), want=(S(4), S(5)),
    ),
    dict(
        quiz="q4", id="Q4r", sec="15.1", title="15.1 · A surface with a missing variable",
        concept=True,
        stem=r"Describe the graph of $f(x,y)=1-x^{2}$, and give its domain and range.",
        opts={"A": {"text": "A parabolic cylinder — the parabola $z=1-x^{2}$ dragged "
                            "along the $y$-axis; domain $\\mathbb R^{2}$, range $z\\le1$"},
              "B": {"text": "A paraboloid opening downward; domain $\\mathbb R^{2}$, "
                            "range $z\\le1$"},
              "C": {"text": "A parabolic cylinder; domain $|x|\\le1$, range $0\\le z\\le1$"},
              "D": {"text": "A saddle; domain $\\mathbb R^{2}$, range $\\mathbb R$"},
              "E": {"text": "A plane; domain $\\mathbb R^{2}$, range $\\mathbb R$"},
              "F": {"text": "A parabolic cylinder; domain $\\mathbb R^{2}$, range "
                            "$\\mathbb R$"}},
        key="A",
        sol=[r"$y$ does not appear, so the height never changes as you walk in the "
             r"$y$-direction: every cross-section $y=k$ is the same parabola $z=1-x^{2}$.",
             r"That sweeps out a <b>cylinder</b> — in the technical sense of a curve dragged "
             r"along a line, not a round tube.",
             r"$x$ is unrestricted, so the domain is $\mathbb R^{2}$. Since $x^{2}\ge0$, "
             r"$z=1-x^{2}\le1$, and every such value occurs: range $z\le1$."],
        trap="Calling it a paraboloid. A paraboloid curves in <b>both</b> directions "
             "($z=1-x^{2}-y^{2}$); this one is flat along $y$, which is exactly what a "
             "missing variable means. Also note the range is bounded above but not below.",
    ),
    dict(
        quiz="q4", id="Q4s", sec="15.1", title="15.1 · Hemisphere · domain and range",
        stem=r"For $F(x,y)=\sqrt{1-x^{2}-y^{2}}$, give the graph, domain and range.",
        opts={"A": r"\text{upper hemisphere};\ x^{2}+y^{2}\le1;\ 0\le z\le1",
              "B": r"\text{full sphere};\ x^{2}+y^{2}\le1;\ -1\le z\le1",
              "C": r"\text{upper hemisphere};\ x^{2}+y^{2}<1;\ 0<z\le1",
              "D": r"\text{cone};\ \mathbb R^{2};\ z\ge0",
              "E": r"\text{paraboloid};\ x^{2}+y^{2}\le1;\ 0\le z\le1",
              "F": r"\text{upper hemisphere};\ \mathbb R^{2};\ 0\le z\le1"},
        key="A",
        sol=[r"Squaring: $z^{2}=1-x^{2}-y^{2}$, so $x^{2}+y^{2}+z^{2}=1$ — the unit sphere.",
             r"But $z=\sqrt{\ \cdot\ }\ge0$, so only the <b>upper</b> half is the graph. A "
             r"function has one height per point; a whole sphere fails that.",
             r"Domain: $1-x^{2}-y^{2}\ge0$, the closed unit disc $x^{2}+y^{2}\le1$.",
             r"Range: the radicand runs over $[0,1]$, so $z$ runs over $[0,1]$."],
        trap="Answering &ldquo;sphere&rdquo;, or leaving the range unbounded below. The "
             "square root is non-negative <b>by definition</b>, and it is also what makes "
             "the domain a disc rather than the whole plane.",
        check=lambda: (1 - S(1)**2, 1 - S(0)**2), want=(S(0), S(1)),
    ),
    dict(
        quiz="q4", id="Q4t", sec="15.1", title="15.1 · Matching level curves to a surface",
        concept=True,
        stem=r"A surface shows <b>two separate peaks</b>, side by side along the $y$-axis, "
             r"falling away to zero everywhere else. Which contour plot is it?",
        opts={"A": {"text": "Two nested families of closed loops, one above and one below "
                            "the $x$-axis"},
              "B": {"text": "One family of concentric circles about the origin"},
              "C": {"text": "Horizontal parallel lines"},
              "D": {"text": "Two nested families of loops, one left and one right of the "
                            "$y$-axis"},
              "E": {"text": "Hyperbola-like curves asymptotic to two crossing lines"},
              "F": {"text": "Concentric ellipses elongated along $x$"}},
        key="A",
        sol=[r"Every local maximum shows up as its own nest of <b>closed</b> level curves, "
             r"shrinking toward the summit. Two peaks means two nests.",
             r"The peaks are separated along $y$, so the two nests sit one above the other "
             r"in the $xy$-plane — stacked vertically on the contour map.",
             r"Option D is the same picture rotated: that would be two peaks separated "
             r"along $x$.",
             r"Concentric circles (B) means a single summit; crossing asymptotes (E) is a "
             r"saddle; parallel lines (C) means one variable is absent."],
        trap="Getting the axis right. On the contour plot the separation direction is the "
             "same axis as on the surface, so peaks spread along $y$ give nests spread "
             "along $y$ — not along $x$.",
    ),
    dict(
        quiz="q4", id="Q4u", sec="15.1", title="15.1 · Matching four surfaces",
        concept=True,
        stem=r"Match each function to its surface: "
             r"(i) $\cos xy$, (ii) $\ln(x^{2}+y^{2})$, (iii) $\dfrac{1}{x-y}$, "
             r"(iv) $\dfrac{1}{1+x^{2}+y^{2}}$.",
        opts={"A": {"text": "(i) rippling waves · (ii) funnel to $-\\infty$ at the origin · "
                            "(iii) two sheets torn apart along the line $y=x$ · "
                            "(iv) one bump at the origin decaying to $0$"},
              "B": {"text": "(i) one bump · (ii) funnel · (iii) rippling waves · "
                            "(iv) two torn sheets"},
              "C": {"text": "(i) rippling waves · (ii) one bump · (iii) funnel · "
                            "(iv) two torn sheets"},
              "D": {"text": "(i) two torn sheets · (ii) rippling waves · (iii) funnel · "
                            "(iv) one bump"},
              "E": {"text": "(i) funnel · (ii) two torn sheets · (iii) one bump · "
                            "(iv) rippling waves"},
              "F": {"text": "(i) rippling waves · (ii) two torn sheets · (iii) funnel · "
                            "(iv) one bump"}},
        key="A",
        sol=[r"Read the <b>singularities and bounds</b> first, not the shape.",
             r"(i) $\cos xy$ is bounded in $[-1,1]$ and oscillates forever — only the "
             r"rippled surface does that.",
             r"(ii) $\ln(x^{2}+y^{2})\to-\infty$ as $(x,y)\to(0,0)$ and is radially "
             r"symmetric: a funnel drilling downward at one point.",
             r"(iii) $\dfrac{1}{x-y}$ blows up on the whole <b>line</b> $y=x$, and changes "
             r"sign across it — two sheets, $+\infty$ on one side and $-\infty$ on the "
             r"other.",
             r"(iv) $\dfrac{1}{1+x^{2}+y^{2}}$ has a denominator that never vanishes: "
             r"maximum $1$ at the origin, decaying to $0$ — a single smooth bump."],
        trap="Confusing (ii) and (iii). Both blow up, but a log of $x^{2}+y^{2}$ fails at a "
             "single <b>point</b> while $1/(x-y)$ fails along an entire <b>line</b>. Ask "
             "&ldquo;where is this undefined?&rdquo; and the picture follows.",
    ),

    # ======================================================== 15.2 ==========

    dict(
        quiz="q4", id="Q4v", sec="15.2", title="15.2 · Two-path test",
        concept=True,
        stem=r"Consider $\displaystyle\lim_{(x,y)\to(0,0)}\frac{xy}{x^{2}+y^{2}}$.",
        opts={"A": {"text": "The limit does not exist: along $y=0$ it is $0$, along $y=x$ "
                            "it is $\\tfrac12$"},
              "B": {"text": "The limit is $0$"},
              "C": {"text": "The limit is $\\tfrac12$"},
              "D": {"text": "The limit is $1$"},
              "E": {"text": "The limit exists but depends on the direction of approach"},
              "F": {"text": "The limit is $\\infty$"}},
        key="A",
        sol=[r"Along the $x$-axis ($y=0$): the expression is $\dfrac{0}{x^{2}}=0$ for all "
             r"$x\ne0$, so the limit along that path is $0$.",
             r"Along the line $y=x$: $\dfrac{x^{2}}{2x^{2}}=\dfrac12$ for all $x\ne0$.",
             r"Two paths, two values &rArr; <b>no limit</b>. In general, along $y=mx$ the "
             r"value is $\dfrac{m}{1+m^{2}}$, so every slope gives a different answer."],
        trap="Concluding &ldquo;the limit is $0$&rdquo; from the axes alone. Checking the "
             "two axes is never enough — it is the <b>slanted</b> lines that break this one.",
    ),
    dict(
        quiz="q4", id="Q4w", sec="15.2", title="15.2 · When lines are not enough",
        concept=True,
        stem=r"Consider $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^{2}y}{x^{4}+y^{2}}$.",
        opts={"A": {"text": "The limit does not exist: every line gives $0$, but $y=x^{2}$ "
                            "gives $\\tfrac12$"},
              "B": {"text": "The limit is $0$, since every line through the origin gives $0$"},
              "C": {"text": "The limit is $\\tfrac12$"},
              "D": {"text": "The limit is $1$"},
              "E": {"text": "The limit does not exist because the denominator vanishes"},
              "F": {"text": "The limit is $\\tfrac14$"}},
        key="A",
        sol=[r"Along $y=mx$: $\dfrac{mx^{3}}{x^{4}+m^{2}x^{2}}"
             r"=\dfrac{mx}{x^{2}+m^{2}}\to0$ — every straight line gives $0$.",
             r"Along the <b>parabola</b> $y=x^{2}$: "
             r"$\dfrac{x^{2}\cdot x^{2}}{x^{4}+x^{4}}=\dfrac12$, constant.",
             r"So the limit does not exist. Matching the shape of the denominator — here "
             r"$x^{4}$ against $y^{2}$ — is what tells you to try $y=x^{2}$."],
        trap="Treating &ldquo;all lines agree&rdquo; as proof. It never is. Agreeing on "
             "infinitely many paths still leaves infinitely many untried; only squeeze, "
             "polar coordinates or continuity can <b>prove</b> a limit exists.",
    ),
    dict(
        quiz="q4", id="Q4x", sec="15.2", title="15.2 · A limit that does exist",
        stem=r"Evaluate $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^{2}y}{x^{2}+y^{2}}$.",
        opts={"A": r"0", "B": r"\tfrac12", "C": r"1",
              "D": r"\text{does not exist}", "E": r"\tfrac14", "F": r"\infty"},
        key="A",
        sol=[r"Squeeze it. Since $x^{2}\le x^{2}+y^{2}$, we have "
             r"$\dfrac{x^{2}}{x^{2}+y^{2}}\le1$.",
             r"Therefore $\left|\dfrac{x^{2}y}{x^{2}+y^{2}}\right|\le|y|$.",
             r"As $(x,y)\to(0,0)$, $|y|\to0$, so the expression is squeezed to $0$.",
             r"(Polar check: $\dfrac{r^{3}\cos^{2}\theta\sin\theta}{r^{2}}"
             r"=r\cos^{2}\theta\sin\theta\to0$ as $r\to0$, uniformly in $\theta$.)"],
        trap="Assuming that because Q4w looked the same it must also fail. The exponents "
             "decide: with $x^{2}+y^{2}$ downstairs the numerator is one degree higher, and "
             "in polar form a spare factor of $r$ survives to kill it.",
        check=lambda: _polar_limit(), want=S(0),
    ),
    dict(
        quiz="q4", id="Q4y", sec="15.2", title="15.2 · Continuity and where it fails",
        concept=True,
        stem=r"Where is $f(x,y)=\dfrac{x+y}{x^{2}-y}$ continuous?",
        opts={"A": {"text": "Everywhere except on the parabola $y=x^{2}$"},
              "B": {"text": "Everywhere except at the origin"},
              "C": {"text": "Everywhere except on the line $y=x$"},
              "D": {"text": "Everywhere on $\\mathbb R^{2}$"},
              "E": {"text": "Only where $x^{2}>y$"},
              "F": {"text": "Everywhere except where $x+y=0$"}},
        key="A",
        sol=[r"A quotient of polynomials is continuous wherever the denominator is nonzero.",
             r"$x^{2}-y=0$ exactly on the parabola $y=x^{2}$.",
             r"So $f$ is continuous on $\{(x,y):y\ne x^{2}\}$ — the whole plane with one "
             r"curve removed."],
        trap="Removing the zeros of the <b>numerator</b> too. $x+y=0$ makes $f$ equal zero, "
             "not undefined. Only the denominator can break continuity here.",
    ),
]
