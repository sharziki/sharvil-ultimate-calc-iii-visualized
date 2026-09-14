"""Quiz 4 questions — 14.4 arc length, 14.5 curvature & TNB, 15.1 surfaces, 15.2 limits.

Written to match the *skill mix* of the MyLab set assigned for Lessons 8-10
(14.4.9/11/13/23/40/42, 14.5.11/13/15/23, 15.1.11/15/17/19/25/28/30/34/35).

**Every problem here carries different numbers from the homework.** The point is
to rehearse the pattern, not to memorise an answer you have already seen: if the
arithmetic is identical you are checking recall, not method. Where the homework
used a 3-4-5-flavoured triple to make a radical collapse, so does this — with a
different triple. The structure is the lesson; the digits are not.

  14.4  speed collapses to c*t^n, integrate            (cf. 14.4.9, .23)
  14.4  constant speed, circular arc                   (cf. 14.4.11)
  14.4  the sin-minus-t-cos pair, speed collapses to at(cf. 14.4.13)
  14.4  "does this use arc length as a parameter?"     (cf. 14.4.40 no, .42 yes)
  14.4  rewriting r(t) as r(s)                         (cf. 14.4.40)
  14.5  T and kappa for a LINE  (kappa = 0)            (cf. 14.5.11)
  14.5  T and kappa for a helix                        (cf. 14.5.13)
  14.5  T and kappa for a circle in a tilted plane     (cf. 14.5.15)
  14.5  alternative formula |a x v| / |v|^3            (cf. 14.5.23)
  14.5  curvature of a graph y = f(x)
  15.1  level curves of a named surface                (cf. 15.1.11)
  15.1  domain: polynomial, radical, rational-in-trig  (cf. 15.1.15/17/19)
  15.1  plane: intercepts, domain, range               (cf. 15.1.25)
  15.1  cylinder — one variable missing                (cf. 15.1.28)
  15.1  hemisphere, bounded domain and range           (cf. 15.1.30)
  15.1  match surfaces / level curves by singularity   (cf. 15.1.34/35)
  15.2  two-path test, lines-are-not-enough, squeeze, continuity

Answers are recomputed by the `check` lambda at build time; the build refuses to
emit on a mismatch, and `keycheck` confirms the key letter points at that value.
"""

from sympy import (Matrix, S, sqrt, cos, sin, exp, pi, symbols, integrate,
                   simplify, diff, Rational)

t = symbols("t", real=True)
x, y = symbols("x y", real=True)


def V(*c):
    return Matrix(list(c))


def speed(*comps):
    """|r'(t)|, simplified. All intervals here start at 0, so t >= 0."""
    return simplify(sqrt(sum(diff(c, t) ** 2 for c in comps)))


def arclen(a, b, *comps):
    return simplify(integrate(speed(*comps), (t, a, b)))


QUESTIONS = [

    # ======================================================== 14.4 ==========

    dict(
        quiz="q4", id="Q4a", sec="14.4", title="14.4 · Length when the speed is a multiple of t",
        stem=r"Find the length of $\mathbf r(t)=\langle 9t^{2},\,7,\,12t^{2}-4\rangle$ "
             r"for $0\le t\le2$.",
        opts={"A": r"60", "B": r"30", "C": r"120", "D": r"15",
              "E": r"\sqrt{900}", "F": r"240"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle 18t,\;0,\;24t\rangle$ — the constant $7$ "
             r"differentiates away, and so does the $-4$.",
             r"$|\mathbf r'(t)|=\sqrt{324t^{2}+576t^{2}}=\sqrt{900}\,t=30t$ "
             r"(positive on $[0,2]$, so no absolute value survives).",
             r"$L=\displaystyle\int_0^2 30t\,dt=15t^{2}\Big|_0^2=60$."],
        trap="Forgetting the $\\tfrac12$ from $\\int t\\,dt$ and answering $60\\cdot2=120$, "
             "or quoting $30\\cdot2=60$ by luck while meaning the speed at $t=2$. A speed "
             "growing linearly averages to half its final value.",
        check=lambda: arclen(0, 2, 9*t**2, S(7), 12*t**2 - 4), want=S(60),
    ),
    dict(
        quiz="q4", id="Q4b", sec="14.4", title="14.4 · Length of a circular arc",
        stem=r"Find the length of $\mathbf r(t)=\langle 5\cos t,\;5\sin t\rangle$ "
             r"for $0\le t\le\dfrac{2\pi}{3}$.",
        opts={"A": r"\dfrac{10\pi}{3}", "B": r"10\pi", "C": r"\dfrac{2\pi}{3}",
              "D": r"\dfrac{25\pi}{3}", "E": r"\dfrac{5\pi}{3}", "F": r"5"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle -5\sin t,\;5\cos t\rangle$.",
             r"$|\mathbf r'(t)|=\sqrt{25\sin^{2}t+25\cos^{2}t}=5$ — constant speed, which "
             r"is what a circle traced at a uniform rate always gives.",
             r"$L=5\cdot\dfrac{2\pi}{3}=\dfrac{10\pi}{3}$.",
             r"Sanity check: that is a third of the full circumference $2\pi(5)=10\pi$, and "
             r"$\tfrac{2\pi}{3}$ is a third of a full turn. &check;"],
        trap="Answering $10\\pi$, the whole circumference. The parameter stops at "
             "$\\tfrac{2\\pi}{3}$, one third of the way round.",
        check=lambda: arclen(0, 2*pi/3, 5*cos(t), 5*sin(t)), want=10*pi/3,
    ),
    dict(
        quiz="q4", id="Q4c", sec="14.4", title="14.4 · The sin−t·cos pair",
        stem=r"Find the length of $\mathbf r(t)=\langle 6\sin t-6t\cos t,\;"
             r"6\cos t+6t\sin t\rangle$ for $0\le t\le\pi$.",
        opts={"A": r"3\pi^{2}", "B": r"6\pi^{2}", "C": r"\dfrac{3\pi^{2}}{2}",
              "D": r"6\pi", "E": r"\dfrac{\pi^{2}}{3}", "F": r"12\pi"},
        key="A",
        sol=[r"Product rule: $x'=6\cos t-6\cos t+6t\sin t=6t\sin t$ — the two $\cos$ terms "
             r"cancel. Likewise $y'=-6\sin t+6\sin t+6t\cos t=6t\cos t$.",
             r"$|\mathbf r'(t)|=\sqrt{36t^{2}\sin^{2}t+36t^{2}\cos^{2}t}=6t$ on $t\ge0$.",
             r"$L=\displaystyle\int_0^{\pi}6t\,dt=3t^{2}\Big|_0^{\pi}=3\pi^{2}$."],
        trap="Not differentiating $6t\\cos t$ as a product. The curve is built so the "
             "non-$t$ terms cancel and the speed collapses to $6t$ — if your speed still "
             "has a loose $\\sin$ or $\\cos$ in it, you dropped a term.",
        check=lambda: arclen(0, pi, 6*sin(t) - 6*t*cos(t), 6*cos(t) + 6*t*sin(t)),
        want=3*pi**2,
    ),
    dict(
        quiz="q4", id="Q4d", sec="14.4", title="14.4 · Speed of a cubic trajectory",
        stem=r"For $\mathbf r(t)=\langle 2t^{3},\,6t^{3},\,-3t^{3}\rangle$, $0\le t\le2$, "
             r"find the speed.",
        opts={"A": r"21t^{2}", "B": r"7t^{2}", "C": r"21t^{3}",
              "D": r"49t^{2}", "E": r"3t^{2}\sqrt{7}", "F": r"7t"},
        key="A",
        sol=[r"$\mathbf v=\mathbf r'(t)=\langle 6t^{2},\,18t^{2},\,-9t^{2}\rangle "
             r"=3t^{2}\langle 2,6,-3\rangle$.",
             r"$|\langle 2,6,-3\rangle|=\sqrt{4+36+9}=\sqrt{49}=7$.",
             r"$|\mathbf v|=3t^{2}\cdot7=21t^{2}$ (the $t^{2}\ge0$, so no absolute value)."],
        trap="Factoring $3t^{2}$ out of the square root but leaving the $3$ behind, or "
             "keeping $t^{3}$: differentiating drops the exponent by one.",
        check=lambda: speed(2*t**3, 6*t**3, -3*t**3), want=21*t**2,
    ),
    dict(
        quiz="q4", id="Q4e", sec="14.4", title="14.4 · Length of that cubic",
        stem=r"For the same $\mathbf r(t)=\langle 2t^{3},\,6t^{3},\,-3t^{3}\rangle$, "
             r"find the length of the trajectory on $0\le t\le2$.",
        opts={"A": r"56", "B": r"168", "C": r"28", "D": r"112",
              "E": r"\dfrac{56}{3}", "F": r"84"},
        key="A",
        sol=[r"$L=\displaystyle\int_0^2 21t^{2}\,dt"
             r"=21\cdot\dfrac{t^{3}}{3}\Big|_0^2=7t^{3}\Big|_0^2$.",
             r"$=7\cdot8=56$."],
        trap="Forgetting the $\\tfrac13$ from $\\int t^{2}dt$ and answering "
             "$21\\cdot8=168$. Here $21/3=7$ exactly, which is the whole point of the "
             "numbers.",
        check=lambda: arclen(0, 2, 2*t**3, 6*t**3, -3*t**3), want=S(56),
    ),
    dict(
        quiz="q4", id="Q4f", sec="14.4", title="14.4 · Is t already arc length?",
        concept=True,
        stem=r"Does $\mathbf r(t)=\left\langle \dfrac{\sqrt3}{2}\cos t,\;"
             r"\dfrac{1}{2}\cos t,\;\sin t\right\rangle$ use arc length as its parameter?",
        opts={"A": {"text": "Yes — $|\\mathbf r'(t)|=1$ for every $t$"},
              "B": {"text": "No — $|\\mathbf r'(t)|=2$"},
              "C": {"text": "No — the speed depends on $t$"},
              "D": {"text": "Yes, but only on $0\\le t\\le\\pi$"},
              "E": {"text": "No — the first two components are not equal"},
              "F": {"text": "Only after rescaling the parameter by $2\\pi$"}},
        key="A",
        sol=[r"$\mathbf r'(t)=\left\langle -\tfrac{\sqrt3}{2}\sin t,\;"
             r"-\tfrac{1}{2}\sin t,\;\cos t\right\rangle$.",
             r"$|\mathbf r'(t)|^{2}=\tfrac34\sin^{2}t+\tfrac14\sin^{2}t+\cos^{2}t"
             r"=\sin^{2}t+\cos^{2}t=1$.",
             r"The test is exactly $|\mathbf r'|=1$ for all $t$ — and it holds, so $t$ "
             r"<b>is</b> arc length, measured from $t=0$."],
        trap="Assuming the two coefficients must combine to something larger than one. "
             "They are each <b>squared</b> first, and $\\tfrac34+\\tfrac14=1$ — the "
             "constants are chosen precisely to make the speed unit.",
    ),
    dict(
        quiz="q4", id="Q4g", sec="14.4", title="14.4 · Reparameterising by arc length",
        stem=r"$\mathbf r(t)=\langle 6t^{2},\,2t^{2},\,3t^{2}\rangle$ for $1\le t\le3$ does "
             r"<b>not</b> use arc length. Which $\mathbf r(s)$ does?",
        opts={"A": r"\left\langle 6+\tfrac{6s}{7},\;2+\tfrac{2s}{7},\;3+\tfrac{3s}{7}"
                   r"\right\rangle,\ 0\le s\le56",
              "B": r"\left\langle 6+\tfrac{6s}{7},\;2+\tfrac{2s}{2},\;3+\tfrac{3s}{3}"
                   r"\right\rangle,\ 0\le s\le56",
              "C": r"\left\langle \tfrac{6s}{7},\;\tfrac{2s}{7},\;\tfrac{3s}{7}"
                   r"\right\rangle,\ 0\le s\le56",
              "D": r"\left\langle 6+\tfrac{6s}{7},\;2+\tfrac{2s}{7},\;3+\tfrac{3s}{7}"
                   r"\right\rangle,\ 0\le s\le7",
              "E": r"\left\langle 6s^{2},\;2s^{2},\;3s^{2}\right\rangle,\ 0\le s\le2",
              "F": r"\left\langle 6+6s,\;2+2s,\;3+3s\right\rangle,\ 0\le s\le14"},
        key="A",
        sol=[r"The curve is the ray $t^{2}\langle 6,2,3\rangle$, and "
             r"$|\langle 6,2,3\rangle|=\sqrt{36+4+9}=\sqrt{49}=7$.",
             r"$\mathbf r'(t)=2t\langle6,2,3\rangle$, so $|\mathbf r'|=14t$.",
             r"Arc length from the start: $s(t)=\displaystyle\int_1^{t}14u\,du=7(t^{2}-1)$, "
             r"so $t^{2}=1+\dfrac{s}{7}$.",
             r"Substitute: $\mathbf r(s)=\left(1+\tfrac{s}{7}\right)\langle 6,2,3\rangle"
             r"=\left\langle 6+\tfrac{6s}{7},\,2+\tfrac{2s}{7},\,3+\tfrac{3s}{7}"
             r"\right\rangle$.",
             r"Upper limit: $s(3)=7(9-1)=56$."],
        trap="Putting each component's own coefficient in its denominator (option B). "
             "<b>Every</b> component is divided by the same constant $7$ — the length of "
             "the direction vector, not of one entry.",
        check=lambda: (V(6, 2, 3).norm(), 7*(S(9) - 1)), want=(S(7), S(56)),
    ),

    # ======================================================== 14.5 ==========

    dict(
        quiz="q4", id="Q4h", sec="14.5", title="14.5 · T and curvature of a line",
        stem=r"For $\mathbf r(t)=\langle 3t-1,\;6t+4,\;2t+7\rangle$, find $\mathbf T$ "
             r"and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle \tfrac{3}{7},\tfrac{6}{7},\tfrac{2}{7}"
                   r"\right\rangle,\ \kappa=0",
              "B": r"\mathbf T=\langle 3,6,2\rangle,\ \kappa=0",
              "C": r"\mathbf T=\left\langle \tfrac{3}{7},\tfrac{6}{7},\tfrac{2}{7}"
                   r"\right\rangle,\ \kappa=\tfrac{1}{7}",
              "D": r"\mathbf T=\left\langle \tfrac{3}{49},\tfrac{6}{49},\tfrac{2}{49}"
                   r"\right\rangle,\ \kappa=0",
              "E": r"\mathbf T=\left\langle \tfrac{3}{7},\tfrac{6}{7},\tfrac{2}{7}"
                   r"\right\rangle,\ \kappa=7",
              "F": r"\mathbf T\ \text{is undefined},\ \kappa=0"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle 3,6,2\rangle$, constant, with "
             r"$|\mathbf r'|=\sqrt{9+36+4}=\sqrt{49}=7$.",
             r"$\mathbf T=\dfrac{\mathbf r'}{|\mathbf r'|}"
             r"=\left\langle \tfrac{3}{7},\tfrac{6}{7},\tfrac{2}{7}\right\rangle$. "
             r"Check: $\tfrac{9+36+4}{49}=1$. &check;",
             r"$\mathbf T$ is constant, so $\dfrac{d\mathbf T}{dt}=\mathbf 0$ and "
             r"$\kappa=0$. A straight line has no curvature — as it must."],
        trap="Dividing by $49$ instead of $7$, or reporting $\\mathbf T=\\mathbf r'$ "
             "unnormalised. $\\mathbf T$ is always a <b>unit</b> vector — check that the "
             "squares of your three entries add to $1$.",
        check=lambda: V(3, 6, 2).norm(), want=S(7),
    ),
    dict(
        quiz="q4", id="Q4i", sec="14.5", title="14.5 · T and curvature of a helix",
        stem=r"For $\mathbf r(t)=\langle 4t,\;3\sin t,\;3\cos t\rangle$, find $\mathbf T$ "
             r"and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle \tfrac45,\;\tfrac35\cos t,\;"
                   r"-\tfrac35\sin t\right\rangle,\ \kappa=\tfrac{3}{25}",
              "B": r"\mathbf T=\left\langle \tfrac45,\;\tfrac35\cos t,\;"
                   r"-\tfrac35\cos t\right\rangle,\ \kappa=\tfrac{3}{25}",
              "C": r"\mathbf T=\left\langle \tfrac35,\;\tfrac45\cos t,\;"
                   r"-\tfrac45\sin t\right\rangle,\ \kappa=\tfrac{3}{25}",
              "D": r"\mathbf T=\left\langle \tfrac45,\;\tfrac35\cos t,\;"
                   r"-\tfrac35\sin t\right\rangle,\ \kappa=\tfrac35",
              "E": r"\mathbf T=\langle 4,\;3\cos t,\;-3\sin t\rangle,\ \kappa=\tfrac{3}{25}",
              "F": r"\mathbf T=\left\langle \tfrac45,\;\tfrac35\cos t,\;"
                   r"-\tfrac35\sin t\right\rangle,\ \kappa=\tfrac{1}{5}"},
        key="A",
        sol=[r"$\mathbf r'(t)=\langle 4,\;3\cos t,\;-3\sin t\rangle$ and "
             r"$|\mathbf r'|=\sqrt{16+9\cos^{2}t+9\sin^{2}t}=\sqrt{25}=5$.",
             r"$\mathbf T=\tfrac15\langle 4,3\cos t,-3\sin t\rangle"
             r"=\left\langle \tfrac45,\;\tfrac35\cos t,\;-\tfrac35\sin t\right\rangle$.",
             r"$\mathbf T'=\left\langle 0,\,-\tfrac35\sin t,\,-\tfrac35\cos t\right\rangle$, "
             r"so $|\mathbf T'|=\tfrac35$.",
             r"$\kappa=\dfrac{|\mathbf T'|}{|\mathbf r'|}=\dfrac{3/5}{5}"
             r"=\dfrac{3}{25}$."],
        trap="Writing the third component of $\\mathbf T$ as $\\cos t$. "
             "$\\dfrac{d}{dt}(3\\cos t)=-3\\sin t$ — the derivative of cosine is "
             "<b>minus sine</b>, and this single slip is the most common lost mark in the "
             "whole section.",
        check=lambda: (speed(4*t, 3*sin(t), 3*cos(t)),
                       simplify(sqrt(sum(diff(c, t)**2 for c in
                                         (S(4)/5, S(3)/5*cos(t), -S(3)/5*sin(t))))
                                / speed(4*t, 3*sin(t), 3*cos(t)))),
        want=(S(5), Rational(3, 25)),
    ),
    dict(
        quiz="q4", id="Q4j", sec="14.5", title="14.5 · T and curvature of a tilted circle",
        stem=r"For $\mathbf r(t)=\langle \sqrt7\cos t,\;3\cos t,\;4\sin t\rangle$, "
             r"find $\mathbf T$ and $\kappa$.",
        opts={"A": r"\mathbf T=\left\langle -\tfrac{\sqrt7}{4}\sin t,\;"
                   r"-\tfrac34\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac14",
              "B": r"\mathbf T=\left\langle -\sqrt{\tfrac74}\sin t,\;"
                   r"-\tfrac34\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac14",
              "C": r"\mathbf T=\left\langle -\tfrac{\sqrt7}{4}\cos t,\;"
                   r"-\tfrac34\cos t,\;\sin t\right\rangle,\ \kappa=\tfrac14",
              "D": r"\mathbf T=\left\langle -\tfrac{\sqrt7}{4}\sin t,\;"
                   r"-\tfrac34\sin t,\;\cos t\right\rangle,\ \kappa=4",
              "E": r"\mathbf T=\langle -\sqrt7\sin t,\;-3\sin t,\;4\cos t\rangle,\ "
                   r"\kappa=\tfrac14",
              "F": r"\mathbf T=\left\langle -\tfrac{\sqrt7}{4}\sin t,\;"
                   r"-\tfrac34\sin t,\;\cos t\right\rangle,\ \kappa=\tfrac{1}{16}"},
        key="A",
        sol=[r"$\mathbf r'=\langle -\sqrt7\sin t,\;-3\sin t,\;4\cos t\rangle$.",
             r"$|\mathbf r'|^{2}=7\sin^{2}t+9\sin^{2}t+16\cos^{2}t"
             r"=16\sin^{2}t+16\cos^{2}t=16$, so $|\mathbf r'|=4$ — constant. "
             r"(The $7+9=16$ is the whole design of the problem.)",
             r"$\mathbf T=\tfrac14\mathbf r'=\left\langle -\tfrac{\sqrt7}{4}\sin t,\,"
             r"-\tfrac34\sin t,\,\cos t\right\rangle$.",
             r"$|\mathbf T'|=\left|\left\langle -\tfrac{\sqrt7}{4}\cos t,"
             r"-\tfrac34\cos t,-\sin t\right\rangle\right|=1$, so $\kappa=\dfrac14$ — it "
             r"is a circle of radius $4$ in a tilted plane."],
        trap="Typing $\\sqrt{7/4}$ when you mean $\\dfrac{\\sqrt7}{4}$ (option B). The $4$ "
             "is <b>outside</b> the radical: it came from dividing by $|\\mathbf r'|$, not "
             "from anything under the root.",
        check=lambda: (speed(sqrt(7)*cos(t), 3*cos(t), 4*sin(t)),), want=(S(4),),
    ),
    dict(
        quiz="q4", id="Q4k", sec="14.5", title="14.5 · Alternative curvature formula",
        stem=r"Use $\kappa=\dfrac{|\mathbf a\times\mathbf v|}{|\mathbf v|^{3}}$ to find the "
             r"curvature of $\mathbf r(t)=\langle 2t^{2}+1,\,t,\,0\rangle$.",
        opts={"A": r"\dfrac{4}{(16t^{2}+1)^{3/2}}", "B": r"\dfrac{4}{(16t^{2}+1)^{1/2}}",
              "C": r"\dfrac{2}{(16t^{2}+1)^{3/2}}", "D": r"\dfrac{4}{16t^{2}+1}",
              "E": r"\dfrac{4t}{(16t^{2}+1)^{3/2}}", "F": r"\dfrac{4}{(4t^{2}+1)^{3/2}}"},
        key="A",
        sol=[r"$\mathbf v=\langle 4t,1,0\rangle$ and $\mathbf a=\langle 4,0,0\rangle$.",
             r"$\mathbf a\times\mathbf v=\langle 4,0,0\rangle\times\langle 4t,1,0\rangle"
             r"=\langle 0\cdot0-0\cdot1,\;0\cdot4t-4\cdot0,\;4\cdot1-0\cdot4t\rangle"
             r"=\langle 0,0,4\rangle$, so $|\mathbf a\times\mathbf v|=4$.",
             r"$|\mathbf v|=\sqrt{16t^{2}+1}$, so $|\mathbf v|^{3}=(16t^{2}+1)^{3/2}$.",
             r"$\kappa=\dfrac{4}{(16t^{2}+1)^{3/2}}$ — largest at $t=0$, the vertex of the "
             r"parabola $x=2y^{2}+1$."],
        trap="Cubing only the inside, or forgetting to cube at all. The denominator is the "
             "<b>speed</b> cubed, and the speed already carries a square root: "
             "$\\left(\\sqrt{u}\\right)^{3}=u^{3/2}$.",
        check=lambda: simplify(V(4, 0, 0).cross(V(4*t, 1, 0)).norm()
                               / V(4*t, 1, 0).norm()**3),
        want=4/(16*t**2 + 1)**Rational(3, 2),
    ),
    dict(
        quiz="q4", id="Q4l", sec="14.5", title="14.5 · Curvature of a graph y = f(x)",
        stem=r"Find the curvature of $y=e^{x}$ at the point $(0,1)$.",
        opts={"A": r"\dfrac{\sqrt2}{4}", "B": r"\dfrac{1}{2}", "C": r"1",
              "D": r"\dfrac{1}{\sqrt2}", "E": r"\dfrac{1}{4}", "F": r"2\sqrt2"},
        key="A",
        sol=[r"For a graph, $\kappa=\dfrac{|y''|}{\left(1+(y')^{2}\right)^{3/2}}$.",
             r"$y'=e^{x}$ and $y''=e^{x}$; at $x=0$ both equal $1$.",
             r"$\kappa=\dfrac{1}{(1+1^{2})^{3/2}}=\dfrac{1}{2^{3/2}}"
             r"=\dfrac{1}{2\sqrt2}=\dfrac{\sqrt2}{4}$."],
        trap="Using the $y$-coordinate in the formula, or forgetting the $3/2$ power and "
             "answering $\\tfrac12$. The exponent is $3/2$, not $1$ — it comes from "
             "$|\\mathbf v|^{3}$ with $|\\mathbf v|=\\sqrt{1+(y')^{2}}$.",
        check=lambda: 1/(1 + S(1)**2)**Rational(3, 2), want=sqrt(2)/4,
    ),

    # ======================================================== 15.1 ==========

    dict(
        quiz="q4", id="Q4m", sec="15.1", title="15.1 · Level curves of a surface",
        concept=True,
        stem=r"Describe the level curves of the surface $z=y-x^{2}$.",
        opts={"A": {"text": "Parabolas $y=x^{2}+z_0$ — all the same shape, "
                            "shifted vertically"},
              "B": {"text": "Circles $x^{2}+y^{2}=z_0$"},
              "C": {"text": "Lines $y-x=z_0$"},
              "D": {"text": "Hyperbolas $y^{2}-x^{2}=z_0$"},
              "E": {"text": "Ellipses $x^{2}+2y^{2}=z_0$"},
              "F": {"text": "Parabolas $x=y^{2}+z_0$, opening rightward"}},
        key="A",
        sol=[r"A level curve is what you get by setting $z$ to a constant $z_0$: "
             r"$y-x^{2}=z_0$, that is $y=x^{2}+z_0$.",
             r"Every level is the <b>same</b> parabola $y=x^{2}$, translated up by $z_0$.",
             r"Unlike a paraboloid's circles, these never close and never shrink — the "
             r"contour map is a family of identical nested parabolas, evenly spaced, so "
             r"the surface climbs at a steady rate in the $y$-direction."],
        trap="Assuming &ldquo;parabolic surface, therefore circular contours&rdquo; by "
             "analogy with $z=x^{2}+y^{2}$. Only a sum of two squares gives circles; "
             "$y$ appears here to the <b>first</b> power, and that is what makes the "
             "levels parabolas rather than closed loops.",
    ),
    dict(
        quiz="q4", id="Q4n", sec="15.1", title="15.1 · Domain of a polynomial",
        concept=True,
        stem=r"Find the domain of $f(x,y)=4x^{3}y-7xy^{2}+2y$.",
        opts={"A": {"text": "$\\mathbb R^{2}$"},
              "B": {"text": "$\\{(x,y):x\\ne y\\}$"},
              "C": {"text": "$\\{(x,y):xy>0\\}$"},
              "D": {"text": "$\\{(x,y):x\\ne0\\text{ and }y\\ne0\\}$"},
              "E": {"text": "$\\{(x,y):4x^{3}y-7xy^{2}+2y\\ge0\\}$"},
              "F": {"text": "$\\{(x,y):y>0\\}$"}},
        key="A",
        sol=[r"A polynomial in $x$ and $y$ is built from products and sums only.",
             r"There is no denominator to vanish, no even root to go negative, and no "
             r"logarithm to hit zero.",
             r"Every point of the plane works: the domain is $\mathbb R^{2}$."],
        trap="Reading the odd powers or the sign of the output as a constraint. Products "
             "and sums are fine everywhere; only division, even roots and logs ever "
             "restrict a domain. The <b>range</b> is a separate question entirely.",
    ),
    dict(
        quiz="q4", id="Q4o", sec="15.1", title="15.1 · Domain under a square root",
        stem=r"Find the domain of $f(x,y)=\sqrt{50-2x^{2}-2y^{2}}$.",
        opts={"A": r"\{(x,y):x^{2}+y^{2}\le25\}", "B": r"\{(x,y):x^{2}+y^{2}\le50\}",
              "C": r"\{(x,y):x^{2}+y^{2}\ge25\}", "D": r"\{(x,y):x^{2}+y^{2}<25\}",
              "E": r"\{(x,y):x^{2}+y^{2}\le5\}", "F": r"\mathbb R^{2}"},
        key="A",
        sol=[r"An even root needs its radicand non-negative: $50-2x^{2}-2y^{2}\ge0$.",
             r"Divide by $2$: $25-x^{2}-y^{2}\ge0$, that is $x^{2}+y^{2}\le25$.",
             r"A closed disc of radius $5$ — closed, because equality is allowed and "
             r"$\sqrt0=0$ is perfectly well defined."],
        trap="Forgetting to divide by the $2$ and answering $x^{2}+y^{2}\\le50$, or making "
             "the inequality strict. Strict belongs to logarithms and denominators, not to "
             "square roots. And the radius is $\\sqrt{25}=5$, not $25$.",
        check=lambda: (50 - 2*S(5)**2, 50 - 2*S(0)**2), want=(S(0), S(50)),
    ),
    dict(
        quiz="q4", id="Q4p", sec="15.1", title="15.1 · Domain of a composition",
        concept=True,
        stem=r"Find the domain of $f(x,y)=\cos\!\left(\dfrac{y+3}{x-5}\right)$.",
        opts={"A": {"text": "$\\{(x,y):x\\ne5\\}$"},
              "B": {"text": "$\\{(x,y):y\\ne-3\\}$"},
              "C": {"text": "$\\{(x,y):x\\ne5\\text{ and }y\\ne-3\\}$"},
              "D": {"text": "$\\{(x,y):-1\\le\\frac{y+3}{x-5}\\le1\\}$"},
              "E": {"text": "$\\mathbb R^{2}$"},
              "F": {"text": "$\\{(x,y):x>5\\}$"}},
        key="A",
        sol=[r"$\cos$ accepts every real input, so the outer function imposes nothing.",
             r"The only restriction lives in the fraction: $x-5\ne0$.",
             r"Domain: everything except the vertical line $x=5$."],
        trap="Restricting the argument to $[-1,1]$ (option D). That is the <b>range</b> of "
             "cosine, not its domain — it is the constraint you would impose for "
             "$\\arccos$, not $\\cos$. Note also that the numerator vanishing at $y=-3$ is "
             "harmless: it just makes $f=\\cos 0=1$.",
    ),
    dict(
        quiz="q4", id="Q4q", sec="15.1", title="15.1 · A plane: intercepts, domain, range",
        stem=r"For $f(x,y)=3x+6y-18$, which set of intercepts identifies its graph, and "
             r"what are the domain and range?",
        opts={"A": r"(6,0,0),\,(0,3,0),\,(0,0,-18);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "B": r"(3,0,0),\,(0,6,0),\,(0,0,18);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "C": r"(6,0,0),\,(0,3,0),\,(0,0,-18);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }z\ge-18",
              "D": r"(-6,0,0),\,(0,-3,0),\,(0,0,-18);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "E": r"(18,0,0),\,(0,18,0),\,(0,0,-18);\ \text{domain }\mathbb R^{2},\ "
                   r"\text{range }\mathbb R",
              "F": r"(6,0,0),\,(0,3,0),\,(0,0,-18);\ \text{domain }x,y\ge0,\ "
                   r"\text{range }\mathbb R"},
        key="A",
        sol=[r"$x$-intercept: set $y=z=0$, so $3x=18$ and $x=6$.",
             r"$y$-intercept: set $x=z=0$, so $6y=18$ and $y=3$. Note the coefficients and "
             r"the intercepts <b>swap</b> size: the bigger coefficient gives the smaller "
             r"intercept.",
             r"$z$-intercept: $f(0,0)=-18$.",
             r"A plane is defined for every $(x,y)$ and, being non-constant and linear, it "
             r"attains every real value: domain $\mathbb R^{2}$, range $\mathbb R$."],
        trap="Reading the intercepts straight off the coefficients as $(3,0,0)$ and "
             "$(0,6,0)$. You <b>divide</b> by the coefficient, you do not copy it. Option C "
             "makes the other classic error: a plane has no lowest point, so the range "
             "cannot be bounded below.",
        check=lambda: (S(18)/3, S(18)/6), want=(S(6), S(3)),
    ),
    dict(
        quiz="q4", id="Q4r", sec="15.1", title="15.1 · A surface with a missing variable",
        concept=True,
        stem=r"Describe the graph of $f(x,y)=y^{2}-4$, and give its domain and range.",
        opts={"A": {"text": "A parabolic cylinder — the parabola $z=y^{2}-4$ dragged "
                            "along the $x$-axis; domain $\\mathbb R^{2}$, range $z\\ge-4$"},
              "B": {"text": "A paraboloid opening upward; domain $\\mathbb R^{2}$, "
                            "range $z\\ge-4$"},
              "C": {"text": "A parabolic cylinder dragged along the $y$-axis; "
                            "domain $\\mathbb R^{2}$, range $z\\ge-4$"},
              "D": {"text": "A saddle; domain $\\mathbb R^{2}$, range $\\mathbb R$"},
              "E": {"text": "A plane; domain $\\mathbb R^{2}$, range $\\mathbb R$"},
              "F": {"text": "A parabolic cylinder; domain $|y|\\ge2$, range $z\\ge0$"}},
        key="A",
        sol=[r"$x$ does not appear, so the height never changes as you walk in the "
             r"$x$-direction: every cross-section $x=k$ is the same parabola $z=y^{2}-4$.",
             r"That sweeps out a <b>cylinder</b> — in the technical sense of a curve "
             r"dragged along a line, not a round tube. It is dragged along the axis of the "
             r"<b>missing</b> variable, here $x$.",
             r"$y$ is unrestricted, so the domain is $\mathbb R^{2}$. Since $y^{2}\ge0$, "
             r"$z=y^{2}-4\ge-4$, and every such value occurs: range $z\ge-4$."],
        trap="Calling it a paraboloid, or dragging it along the wrong axis (option C). A "
             "paraboloid curves in <b>both</b> directions ($z=x^{2}+y^{2}-4$); this one is "
             "flat along $x$, which is exactly what the missing variable means.",
    ),
    dict(
        quiz="q4", id="Q4s", sec="15.1", title="15.1 · Hemisphere · domain and range",
        stem=r"For $F(x,y)=\sqrt{36-x^{2}-y^{2}}$, give the graph, domain and range.",
        opts={"A": r"\text{upper hemisphere};\ x^{2}+y^{2}\le36;\ 0\le z\le6",
              "B": r"\text{full sphere};\ x^{2}+y^{2}\le36;\ -6\le z\le6",
              "C": r"\text{upper hemisphere};\ x^{2}+y^{2}<36;\ 0<z\le6",
              "D": r"\text{cone};\ \mathbb R^{2};\ z\ge0",
              "E": r"\text{paraboloid};\ x^{2}+y^{2}\le36;\ 0\le z\le36",
              "F": r"\text{upper hemisphere};\ \mathbb R^{2};\ 0\le z\le6",
              },
        key="A",
        sol=[r"Squaring: $z^{2}=36-x^{2}-y^{2}$, so $x^{2}+y^{2}+z^{2}=36$ — the sphere of "
             r"radius $6$.",
             r"But $z=\sqrt{\ \cdot\ }\ge0$, so only the <b>upper</b> half is the graph. A "
             r"function has one height per point; a whole sphere fails that.",
             r"Domain: $36-x^{2}-y^{2}\ge0$, the closed disc $x^{2}+y^{2}\le36$ of radius "
             r"$6$.",
             r"Range: the radicand runs over $[0,36]$, so $z=\sqrt{\ \cdot\ }$ runs over "
             r"$[0,6]$."],
        trap="Answering &ldquo;sphere&rdquo;, or letting the range run to $36$ instead of "
             "$6$ (option E) — you must take the square root of the largest radicand. The "
             "square root is non-negative <b>by definition</b>, and it is also what makes "
             "the domain a disc rather than the whole plane.",
        check=lambda: (36 - S(6)**2, sqrt(36 - S(0)**2)), want=(S(0), S(6)),
    ),
    dict(
        quiz="q4", id="Q4t", sec="15.1", title="15.1 · Matching level curves to a surface",
        concept=True,
        stem=r"A surface has one <b>peak</b> and, beside it along the $x$-axis, one "
             r"<b>pit</b>, flattening to zero far away. Which contour plot is it?",
        opts={"A": {"text": "Two nested families of closed loops, one left and one right "
                            "of the $y$-axis — values rising into one, falling into the "
                            "other"},
              "B": {"text": "One family of concentric circles about the origin"},
              "C": {"text": "Two nested families of closed loops, one above and one below "
                            "the $x$-axis"},
              "D": {"text": "Hyperbola-like curves asymptotic to two crossing lines"},
              "E": {"text": "Horizontal parallel lines"},
              "F": {"text": "Concentric ellipses elongated along $y$"}},
        key="A",
        sol=[r"A local maximum and a local minimum <b>both</b> show up as a nest of "
             r"<b>closed</b> level curves shrinking toward the extreme point. The picture "
             r"alone does not distinguish them — only the labelled values do.",
             r"The two features are separated along $x$, so the two nests sit left and "
             r"right in the $xy$-plane.",
             r"Option C is the same picture rotated: that is two features separated along "
             r"$y$. Concentric circles (B) means a single summit; crossing asymptotes (D) "
             r"is a saddle; parallel lines (E) means one variable is absent."],
        trap="Two things at once. First the <b>axis</b>: separation along $x$ on the "
             "surface means separation along $x$ on the map. Second, do not expect a pit "
             "to look different from a peak — it does not. Read the numbers on the "
             "contours, not the shape.",
    ),
    dict(
        quiz="q4", id="Q4u", sec="15.1", title="15.1 · Matching four surfaces",
        concept=True,
        stem=r"Match each function to its surface: (i) $\sin(x+y)$, "
             r"(ii) $\dfrac{1}{x^{2}+y^{2}}$, (iii) $\dfrac{1}{x+y}$, "
             r"(iv) $e^{-x^{2}-y^{2}}$.",
        opts={"A": {"text": "(i) parallel ridges and troughs · (ii) a spike to $+\\infty$ "
                            "at the origin · (iii) two sheets torn apart along the line "
                            "$y=-x$ · (iv) one bump at the origin decaying to $0$"},
              "B": {"text": "(i) one bump · (ii) a spike · (iii) parallel ridges · "
                            "(iv) two torn sheets"},
              "C": {"text": "(i) parallel ridges · (ii) one bump · (iii) a spike · "
                            "(iv) two torn sheets"},
              "D": {"text": "(i) two torn sheets · (ii) parallel ridges · (iii) a spike · "
                            "(iv) one bump"},
              "E": {"text": "(i) a spike · (ii) two torn sheets · (iii) one bump · "
                            "(iv) parallel ridges"},
              "F": {"text": "(i) parallel ridges · (ii) two torn sheets · (iii) a spike · "
                            "(iv) one bump"}},
        key="A",
        sol=[r"Read the <b>singularities and bounds</b> first, not the shape.",
             r"(i) $\sin(x+y)$ is bounded in $[-1,1]$ and depends only on $x+y$, so it is "
             r"constant along every line $x+y=c$ — parallel straight ridges and troughs.",
             r"(ii) $\dfrac{1}{x^{2}+y^{2}}\to+\infty$ as $(x,y)\to(0,0)$, is radially "
             r"symmetric, and is positive everywhere: a spike at a single <b>point</b>.",
             r"(iii) $\dfrac{1}{x+y}$ blows up on the whole <b>line</b> $y=-x$ and changes "
             r"sign across it — two sheets, $+\infty$ on one side, $-\infty$ on the other.",
             r"(iv) $e^{-x^{2}-y^{2}}$ has maximum $1$ at the origin and decays to $0$ in "
             r"every direction — a single smooth bump, never negative."],
        trap="Confusing (ii) and (iii). Both blow up, but $\\dfrac{1}{x^{2}+y^{2}}$ fails "
             "at a single <b>point</b> and keeps one sign, while $\\dfrac{1}{x+y}$ fails "
             "along an entire <b>line</b> and flips sign. Ask &ldquo;where is this "
             "undefined, and does it change sign there?&rdquo; and the picture follows.",
    ),

    # ======================================================== 15.2 ==========

    dict(
        quiz="q4", id="Q4v", sec="15.2", title="15.2 · Two-path test",
        concept=True,
        stem=r"Consider $\displaystyle\lim_{(x,y)\to(0,0)}\frac{xy}{x^{2}+3y^{2}}$.",
        opts={"A": {"text": "The limit does not exist: along $y=0$ it is $0$, along $y=x$ "
                            "it is $\\tfrac14$"},
              "B": {"text": "The limit is $0$"},
              "C": {"text": "The limit is $\\tfrac14$"},
              "D": {"text": "The limit is $\\tfrac13$"},
              "E": {"text": "The limit exists but depends on the direction of approach"},
              "F": {"text": "The limit is $\\infty$"}},
        key="A",
        sol=[r"Along the $x$-axis ($y=0$): the expression is $\dfrac{0}{x^{2}}=0$ for all "
             r"$x\ne0$, so the limit along that path is $0$.",
             r"Along the line $y=x$: $\dfrac{x^{2}}{x^{2}+3x^{2}}=\dfrac14$ for all "
             r"$x\ne0$.",
             r"Two paths, two values &rArr; <b>no limit</b>. In general, along $y=mx$ the "
             r"value is $\dfrac{m}{1+3m^{2}}$, so every slope gives a different answer."],
        trap="Concluding &ldquo;the limit is $0$&rdquo; from the axes alone. Checking the "
             "two axes is never enough — it is the <b>slanted</b> lines that break this "
             "one. Option E is also wrong as stated: if the value depends on direction, "
             "the limit does not exist at all.",
    ),
    dict(
        quiz="q4", id="Q4w", sec="15.2", title="15.2 · When lines are not enough",
        concept=True,
        stem=r"Consider $\displaystyle\lim_{(x,y)\to(0,0)}\frac{x^{3}y}{x^{6}+y^{2}}$.",
        opts={"A": {"text": "The limit does not exist: every line gives $0$, but $y=x^{3}$ "
                            "gives $\\tfrac12$"},
              "B": {"text": "The limit is $0$, since every line through the origin gives $0$"},
              "C": {"text": "The limit is $\\tfrac12$"},
              "D": {"text": "The limit is $1$"},
              "E": {"text": "The limit does not exist because the denominator vanishes"},
              "F": {"text": "The limit is $\\tfrac14$"}},
        key="A",
        sol=[r"Along $y=mx$: $\dfrac{x^{3}\cdot mx}{x^{6}+m^{2}x^{2}}"
             r"=\dfrac{mx^{2}}{x^{4}+m^{2}}\to\dfrac{0}{m^{2}}=0$ — every straight line "
             r"gives $0$.",
             r"Along the <b>curve</b> $y=x^{3}$: "
             r"$\dfrac{x^{3}\cdot x^{3}}{x^{6}+x^{6}}=\dfrac12$, constant.",
             r"So the limit does not exist. Matching the shape of the denominator — here "
             r"$x^{6}$ against $y^{2}$, so $y\sim x^{3}$ — is what tells you which curve "
             r"to try."],
        trap="Treating &ldquo;all lines agree&rdquo; as proof (option B). It never is. "
             "Agreeing on infinitely many paths still leaves infinitely many untried; only "
             "a squeeze, polar coordinates or continuity can <b>prove</b> a limit exists.",
    ),
    dict(
        quiz="q4", id="Q4x", sec="15.2", title="15.2 · A limit that does exist",
        stem=r"Evaluate $\displaystyle\lim_{(x,y)\to(0,0)}\frac{xy^{2}}{x^{2}+y^{2}}$.",
        opts={"A": r"0", "B": r"\tfrac12", "C": r"1",
              "D": r"\text{does not exist}", "E": r"\tfrac14", "F": r"\infty"},
        key="A",
        sol=[r"Squeeze it. Since $y^{2}\le x^{2}+y^{2}$, we have "
             r"$\dfrac{y^{2}}{x^{2}+y^{2}}\le1$.",
             r"Therefore $\left|\dfrac{xy^{2}}{x^{2}+y^{2}}\right|\le|x|$.",
             r"As $(x,y)\to(0,0)$, $|x|\to0$, so the expression is squeezed to $0$.",
             r"(Polar check: $\dfrac{r^{3}\cos\theta\sin^{2}\theta}{r^{2}}"
             r"=r\cos\theta\sin^{2}\theta\to0$ as $r\to0$, uniformly in $\theta$.)"],
        trap="Assuming that because the previous one failed, this must too. The "
             "<b>degrees</b> decide: the numerator here is degree $3$ and the denominator "
             "degree $2$, so in polar form a spare factor of $r$ survives and kills it. "
             "When numerator and denominator have equal degree, suspect it fails.",
        check=lambda: _polar_r_to_zero(), want=S(0),
    ),
    dict(
        quiz="q4", id="Q4y", sec="15.2", title="15.2 · Continuity and where it fails",
        concept=True,
        stem=r"Where is $f(x,y)=\dfrac{x-2y}{y-x^{3}}$ continuous?",
        opts={"A": {"text": "Everywhere except on the curve $y=x^{3}$"},
              "B": {"text": "Everywhere except at the origin"},
              "C": {"text": "Everywhere except on the line $x=2y$"},
              "D": {"text": "Everywhere on $\\mathbb R^{2}$"},
              "E": {"text": "Only where $y>x^{3}$"},
              "F": {"text": "Everywhere except on the parabola $y=x^{2}$"}},
        key="A",
        sol=[r"A quotient of polynomials is continuous wherever the denominator is nonzero.",
             r"$y-x^{3}=0$ exactly on the cubic $y=x^{3}$.",
             r"So $f$ is continuous on $\{(x,y):y\ne x^{3}\}$ — the whole plane with one "
             r"curve removed."],
        trap="Removing the zeros of the <b>numerator</b> too (option C). On the line "
             "$x=2y$ the function equals $0$, which is a perfectly good value, not a "
             "failure. Only the denominator can break continuity here.",
    ),
]


def _polar_r_to_zero():
    """x*y^2/(x^2+y^2) in polar is r*cos(th)*sin^2(th); r -> 0 kills it."""
    r, th = symbols("r th", positive=True)
    expr = simplify(((r*cos(th)) * (r*sin(th))**2)
                    / ((r*cos(th))**2 + (r*sin(th))**2))
    return simplify(expr.subs(r, 0))
