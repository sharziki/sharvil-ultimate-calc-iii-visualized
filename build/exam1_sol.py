"""Worked solutions for the official Exam 1 study guide's practice problems.

The instructor's page gives a stem and a final answer. It never shows the work.
This file supplies the missing middle: the steps, and the one thing a bare
answer can never give you — *why the wrong answer is tempting*.

Everything here is ours. Nothing in this file is attributed to the instructor
except the `answer` field, which `exam1_src.py` lifts verbatim from the page.

Two entries carry a `fix`. The published answers to Lesson 10, Problems 1 and 2
are wrong: both limits exist and both are 0. The squeeze is written out in the
solution, and the page renders the correction next to the official answer rather
than quietly replacing it — you are going to see the official answer again on
the real study guide, and you should know why it is wrong before you do.

`check` re-derives the answer with sympy at build time where the answer is a
value sympy can hold. Prose answers ("elliptic cone with axis along z") are not
checkable and carry no check; they are marked `prose=True` so the build can
count what it verified instead of implying it verified everything.
"""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, acos, atan, pi,
                   exp, log, symbols, diff, integrate, limit, simplify, solve,
                   Eq, oo)

t, s_, u_ = symbols("t s u", real=True)
x, y, z = symbols("x y z", real=True)
a_, c_, k_ = symbols("a c k", real=True)


def V(*c):
    return Matrix(list(c))


def cross(a, b):
    return V(*a).cross(V(*b))


# pid -> dict(steps=[...], trap=str, check=callable|None, want=..., prose=bool)
SOL = {

# ------------------------------------------------------------ Lesson 1 ----
"L1P1": dict(
    steps=[
        r"The projection of $\vec u$ onto $\vec v$ is $\operatorname{proj}_{\vec v}\vec u=\dfrac{\vec u\cdot\vec v}{|\vec v|^2}\,\vec v$ — a vector *along* $\vec v$.",
        r"$\vec u\cdot\vec v=(2)(1)+(-1)(2)+(3)(2)=2-2+6=6$.",
        r"$|\vec v|^2=1+4+4=9$.",
        r"$\operatorname{proj}_{\vec v}\vec u=\frac{6}{9}\langle1,2,2\rangle=\frac{2}{3}\langle1,2,2\rangle=\left\langle\frac23,\frac43,\frac43\right\rangle$.",
    ],
    trap=r"Dividing by $|\vec v|$ instead of $|\vec v|^2$. That gives the scalar projection $\operatorname{comp}_{\vec v}\vec u=\frac{6}{3}=2$, which is a number, not a vector. Read which one the question wants.",
    check=lambda: (V(2, -1, 3).dot(V(1, 2, 2)) / V(1, 2, 2).dot(V(1, 2, 2))) * V(1, 2, 2),
    want=V(Rational(2, 3), Rational(4, 3), Rational(4, 3)),
),
"L1P2": dict(
    steps=[
        r"Two edge vectors from $P$: $\overrightarrow{PQ}=\langle-1,2,0\rangle$ and $\overrightarrow{PR}=\langle-1,0,3\rangle$.",
        r"$\overrightarrow{PQ}\times\overrightarrow{PR}=\langle 2\cdot3-0\cdot0,\;0\cdot(-1)-(-1)\cdot3,\;0-(-2)\rangle=\langle6,3,2\rangle$.",
        r"$|\langle6,3,2\rangle|=\sqrt{36+9+4}=7$ — that is the **parallelogram** area.",
        r"A triangle is half of it: $\text{area}=\frac72$.",
    ],
    trap=r"Forgetting the $\frac12$. The cross product's length is the parallelogram, and $7$ is sitting right there looking like an answer.",
    check=lambda: cross([-1, 2, 0], [-1, 0, 3]).norm() / 2, want=Rational(7, 2),
),
"L1P3": dict(
    steps=[
        r"$\vec u\times\vec v=\begin{vmatrix}\vec i&\vec j&\vec k\\3&-1&2\\1&4&-1\end{vmatrix}$.",
        r"$\vec i$: $(-1)(-1)-(2)(4)=1-8=-7$.",
        r"$\vec j$: $-\big[(3)(-1)-(2)(1)\big]=-(-5)=5$ — note the sign flip on the middle term.",
        r"$\vec k$: $(3)(4)-(-1)(1)=12+1=13$. So $\vec u\times\vec v=\langle-7,5,13\rangle$.",
    ],
    trap=r"The minus on the $\vec j$ component. Dropping it gives $\langle-7,-5,13\rangle$, and the sanity check catches it instantly: $\vec u\cdot(\vec u\times\vec v)$ must be $0$.",
    check=lambda: cross([3, -1, 2], [1, 4, -1]), want=V(-7, 5, 13),
),
"L1P4": dict(
    steps=[
        r"Orthogonal means the dot product vanishes.",
        r"$\langle2,c,-1\rangle\cdot\langle3,-6,c\rangle=6-6c-c=6-7c$.",
        r"$6-7c=0\Rightarrow c=\frac{6}{7}$.",
    ],
    trap=r"Missing that $c$ appears in **both** vectors, so the last term $(-1)(c)$ also carries a $c$. Treating it as a constant gives $c=1$.",
    check=lambda: solve(Eq(V(2, c_, -1).dot(V(3, -6, c_)), 0), c_)[0],
    want=Rational(6, 7),
),
"L1P5": dict(
    steps=[
        r"$\cos\theta=\dfrac{\vec u\cdot\vec v}{|\vec u||\vec v|}$.",
        r"$\vec u\cdot\vec v=0+1+0=1$, and $|\vec u|=|\vec v|=\sqrt2$.",
        r"$\cos\theta=\frac{1}{2}\Rightarrow\theta=\frac{\pi}{3}$.",
    ],
    trap=r"Answering $\frac{\pi}{6}$: $\cos^{-1}\!\frac12=\frac{\pi}{3}$, not $\frac{\pi}{6}$. $\frac{\pi}{6}$ is where the *sine* is $\frac12$.",
    check=lambda: acos(V(1, 1, 0).dot(V(0, 1, 1)) / (V(1, 1, 0).norm() * V(0, 1, 1).norm())),
    want=pi / 3,
),

# ------------------------------------------------------------ Lesson 2 ----
"L2P1": dict(
    steps=[
        r"Direction: $\vec v=\langle3-1,\,1-3,\,2-(-1)\rangle=\langle2,-2,3\rangle$.",
        r"Line: $\vec r(t)=\langle 1+2t,\;3-2t,\;-1+3t\rangle$.",
        r"Substitute into $x+y+z=6$: $(1+2t)+(3-2t)+(-1+3t)=3+3t=6\Rightarrow t=1$.",
        r"$\vec r(1)=\langle3,1,2\rangle$ — the second given point happens to lie on the plane.",
    ],
    trap=r"Sign errors in the direction vector. Notice the $x$ and $y$ parameters cancel, so the whole equation collapses to $3+3t$; if yours does not collapse, recheck $\vec v$.",
    # Derived from the two given points and the plane, not from the printed
    # answer: build the line, solve for t, evaluate.
    check=lambda: (lambda P, Q: (lambda r: list(r.subs(
        t, solve(Eq(r[0] + r[1] + r[2], 6), t)[0])))(P + t * (Q - P))
    )(V(1, 3, -1), V(3, 1, 2)),
    want=[3, 1, 2],
),
"L2P2": dict(
    steps=[
        r"Two vectors parallel to the plane give the normal through a cross product.",
        r"$\vec n=\langle1,0,3\rangle\times\langle2,1,0\rangle=\langle 0\cdot0-3\cdot1,\;3\cdot2-1\cdot0,\;1\cdot1-0\cdot2\rangle=\langle-3,6,1\rangle$.",
        r"Point-normal form at $(2,1,-1)$: $-3(x-2)+6(y-1)+1(z+1)=0$.",
        r"Expand: $-3x+6+6y-6+z+1=0\Rightarrow -3x+6y+z+1=0$.",
    ],
    trap=r"'Parallel to the vectors' does **not** mean the vectors are normals. They lie *in* the plane; their cross product is the normal.",
    check=lambda: cross([1, 0, 3], [2, 1, 0]), want=V(-3, 6, 1),
),
"L2P3": dict(
    steps=[
        r"Two equations, three unknowns — one free parameter, which is the line.",
        r"Let $y=-t$. Then $x+y=2$ gives $x=2+t$, and $y+z=3$ gives $z=3+t$.",
        r"$x=2+t,\;y=-t,\;z=3+t$.",
        r"Check the direction against $\vec n_1\times\vec n_2=\langle1,1,0\rangle\times\langle0,1,1\rangle=\langle1,-1,1\rangle$ — same direction, as it must be.",
    ],
    trap=r"Any parametrisation is correct; yours may look nothing like this one. Verify by plugging back into **both** plane equations rather than comparing to a printed answer.",
    check=lambda: cross([1, 1, 0], [0, 1, 1]), want=V(1, -1, 1),
),
"L2P4": dict(
    steps=[
        r"The angle between planes is the angle between normals: $\vec n_1=\langle1,1,1\rangle$, $\vec n_2=\langle1,-1,0\rangle$.",
        r"$\vec n_1\cdot\vec n_2=1-1+0=0$.",
        r"Zero dot product $\Rightarrow\theta=\frac{\pi}{2}$: the planes are perpendicular.",
    ],
    trap=r"Reading coefficients off a plane written as $x-y=0$ and forgetting the missing $z$ is a coefficient of $0$, not of $1$.",
    # Compute the angle the page actually prints, not just the dot product, so
    # the official-answer audit compares like for like.
    check=lambda: acos(V(1, 1, 1).dot(V(1, -1, 0))
                       / (V(1, 1, 1).norm() * V(1, -1, 0).norm())),
    want=pi / 2,
),
"L2P5": dict(
    steps=[
        r"Intersection needs a single point, so use **different** parameters $t$ and $s$ and solve all three components.",
        r"$x$: $1+t=3-s\Rightarrow t=2-s$.  $y$: $2t=s+1$.",
        r"Substitute: $2(2-s)=s+1\Rightarrow 4-2s=s+1\Rightarrow s=1$, hence $t=1$.",
        r"$z$: $3+t=2s+a\Rightarrow 3+1=2+a\Rightarrow a=2$.",
    ],
    trap=r"Using $t$ for both lines. Two lines can cross at a point they reach at different times; forcing one parameter finds only the cases where they arrive together, and reports skew for lines that do meet.",
    check=lambda: solve([Eq(1 + t, 3 - s_), Eq(2 * t, s_ + 1), Eq(3 + t, 2 * s_ + a_)],
                        [t, s_, a_])[a_],
    want=2,
),

# ---------------------------------------------------------- Lesson 3-4 ----
"L3-4P1": dict(
    steps=[
        r"Write it with the positive term first: $\dfrac{y^2}{4}-x^2-\dfrac{z^2}{9}=1$.",
        r"One positive square, two negative, equals $+1$ — that is the two-sheet signature.",
        r"Trace at $y=0$: $-x^2-\frac{z^2}{9}=1$, impossible. Nothing at the origin, so it cannot be one connected sheet.",
        r"**Hyperboloid of two sheets, axis along $y$** — the axis is always the variable whose square is positive.",
    ],
    trap=r"One sheet vs two sheets is decided by the count of minus signs, not by which variable is isolated. One minus = one sheet (connected); two minuses = two sheets.",
    prose=True,
),
"L3-4P2": dict(
    steps=[
        r"Complete the square in $x$ and $y$: $x^2+4x=(x+2)^2-4$ and $y^2-2y=(y-1)^2-1$.",
        r"$(x+2)^2-4+(y-1)^2-1+z^2=-4$.",
        r"$(x+2)^2+(y-1)^2+z^2=1$.",
        r"**Sphere**, centre $(-2,1,0)$, radius $1$.",
    ],
    trap=r"Moving the completion constants the wrong way. The $-4$ and $-1$ come out on the left, so they get **added** to the right: $-4+4+1=1$.",
    check=lambda: simplify((x + 2) ** 2 + (y - 1) ** 2 + z ** 2 - 1
                           - (x ** 2 + 4 * x + y ** 2 - 2 * y + z ** 2 + 4)),
    want=0,
),
"L3-4P3": dict(
    steps=[
        r"One variable ($z$) appears to the first power, the other two are squared with the **same** sign.",
        r"That is the paraboloid family. Both coefficients positive $\Rightarrow$ opens upward.",
        r"Traces $z=k>0$ are ellipses $4x^2+9y^2=k$; traces $x=0$ and $y=0$ are upward parabolas.",
        r"**Elliptic paraboloid opening upward.**",
    ],
    trap=r"Calling it a cone. A cone has $z^2$, not $z$; the first power is what makes it a paraboloid.",
    prose=True,
),
"L3-4P4": dict(
    steps=[
        r"Set $z=2$: $\dfrac{x^2}{4}+\dfrac{y^2}{9}-4=1$.",
        r"$\dfrac{x^2}{4}+\dfrac{y^2}{9}=5$.",
        r"Divide by $5$: $\dfrac{x^2}{20}+\dfrac{y^2}{45}=1$ — an **ellipse**.",
    ],
    trap=r"Stopping at $\frac{x^2}{4}+\frac{y^2}{9}=5$. A trace is named by its standard form, and the denominators change once you divide through.",
    # Substitute z=2 into the surface and read the ellipse's denominators off
    # the normalised form, rather than asserting 4*5 and 9*5.
    check=lambda: (lambda k: (4 * k, 9 * k))(
        solve(Eq((x ** 2 / 4 + y ** 2 / 9) - 2 ** 2, 1), x ** 2 / 4 + y ** 2 / 9)[0]),
    want=(20, 45),
),
"L3-4P5": dict(
    steps=[
        r"Rewrite as $x^2+\dfrac{y^2}{4}-\dfrac{z^2}{9}=0$ — equal to **zero**, not $1$.",
        r"Zero is the cone signature. Traces $z=k\ne0$ are ellipses that grow linearly with $|k|$; the trace $z=0$ is the single point at the origin (the vertex).",
        r"**Elliptic cone with axis along the $z$-axis.**",
    ],
    trap=r"Reading it as a hyperboloid. Same sign pattern — the right-hand side is the entire difference: $=1$ one sheet, $=-1$ two sheets, $=0$ the cone between them.",
    prose=True,
),

# ------------------------------------------------------------ Lesson 5 ----
"L5P1": dict(
    steps=[
        r"A vector function is continuous exactly where **every** component is.",
        r"$\sqrt{t-1}$ needs $t\ge1$.",
        r"$\ln(4-t)$ needs $4-t>0$, i.e. $t<4$.",
        r"$e^t$ is continuous everywhere. Intersect: $[1,4)$.",
    ],
    trap=r"The bracket types. $\sqrt{\;}$ allows equality (closed at $1$); $\ln$ never does (open at $4$).",
    prose=True,
),
"L5P2": dict(
    steps=[
        r"Componentwise.",
        r"$\lim_{t\to0}\frac{\sin 3t}{t}=3$ (the $\frac{\sin u}{u}$ limit with $u=3t$).",
        r"$\lim_{t\to0}e^{2t}=1$.",
        r"$\lim_{t\to0}\frac{t^2+1}{t+1}=1$. So the limit is $\langle3,1,1\rangle$.",
    ],
    trap=r"Writing $1$ for the first component out of reflex. $\frac{\sin 3t}{t}=3\cdot\frac{\sin 3t}{3t}\to3$.",
    check=lambda: [limit(sin(3 * t) / t, t, 0), limit(exp(2 * t), t, 0),
                   limit((t ** 2 + 1) / (t + 1), t, 0)],
    want=[3, 1, 1],
),
"L5P3": dict(
    steps=[
        r"$\frac{1}{t^2-4}$ needs $t\ne\pm2$.",
        r"$\sqrt t$ needs $t\ge0$ — which already kills $t=-2$.",
        r"$\cos t$ is everywhere continuous.",
        r"$[0,\infty)$ with $t=2$ removed: $[0,2)\cup(2,\infty)$.",
    ],
    trap=r"Reporting both $\pm2$ as holes. $t=-2$ is not a hole, it is outside the domain the square root already imposed.",
    prose=True,
),
"L5P4": dict(
    steps=[
        r"$x=2\cos t$, $y=2\sin t$ gives $x^2+y^2=4$, and $z=0$ throughout.",
        r"As $t$ runs $0\to2\pi$ the point goes once around, counterclockwise from $(2,0)$.",
        r"**A circle of radius 2 in the $xy$-plane, centred at the origin.**",
    ],
    trap=r"Calling it a helix. A helix needs $z$ to move; here $z\equiv0$.",
    prose=True,
),
"L5P5": dict(
    steps=[
        r"$\lim_{t\to0}\frac{e^t-1}{t}=1$ — this is $\frac{d}{dt}e^t$ at $0$.",
        r"$\lim_{t\to0}\frac{1-\cos t}{t^2}=\frac12$ (two applications of l'Hôpital, or the series $1-\cos t\approx\frac{t^2}{2}$).",
        r"$\left|t\sin\frac1t\right|\le|t|\to0$, so the third component is $0$ by the squeeze.",
        r"$\left\langle1,\frac12,0\right\rangle$.",
    ],
    trap=r"Declaring the third component undefined because $\sin\frac1t$ oscillates. Bounded times something going to zero still goes to zero.",
    check=lambda: [limit((exp(t) - 1) / t, t, 0), limit((1 - cos(t)) / t ** 2, t, 0),
                   limit(t * sin(1 / t), t, 0)],
    want=[1, Rational(1, 2), 0],
),

# ---------------------------------------------------------- Lesson 6-7 ----
"L6P1": dict(
    steps=[
        r"Position is the antiderivative of velocity: $\vec r(t)=\int\vec v(t)\,dt+\vec C$.",
        r"$\int\langle2t,3,-1\rangle dt=\langle t^2,\,3t,\,-t\rangle+\vec C$.",
        r"$\vec r(0)=\vec C=\langle1,-2,5\rangle$.",
        r"$\vec r(t)=\langle t^2+1,\;3t-2,\;-t+5\rangle$.",
    ],
    trap=r"Forgetting that $\vec C$ is a **vector** of three separate constants, not one scalar.",
    check=lambda: [integrate(2 * t, t) + 1, integrate(3, t) - 2, integrate(-1, t) + 5],
    want=[t ** 2 + 1, 3 * t - 2, 5 - t],
),
"L6P2": dict(
    steps=[
        r"$\vec r(1)=\langle1,3,1\rangle$ and $\vec r\,{}'(t)=\langle2t,2,3t^2\rangle$, so $\vec r\,{}'(1)=\langle2,2,3\rangle$.",
        r"Tangent line: $\langle1+2u,\;3+2u,\;1+3u\rangle$.",
        r"The $xz$-plane is $y=0$: $3+2u=0\Rightarrow u=-\frac32$.",
        r"$x=1+2(-\frac32)=-2$, $z=1+3(-\frac32)=-\frac72$. Point: $\left(-2,0,-\frac72\right)$.",
    ],
    trap=r"Using $t$ again for the tangent line. The line has its own parameter; reusing $t$ makes you solve on the curve instead of on its tangent.",
    # Build the tangent line from r(t) itself, solve y=0, evaluate x and z.
    check=lambda: (lambda r: (lambda L: [L[0].subs(u_, solve(Eq(L[1], 0), u_)[0]),
                                          L[2].subs(u_, solve(Eq(L[1], 0), u_)[0])])(
        r.subs(t, 1) + u_ * r.diff(t).subs(t, 1))
    )(Matrix([t ** 2, 2 * t + 1, t ** 3])),
    want=[-2, Rational(-7, 2)],
),
"L6P3": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle-\sin t,\cos t,1\rangle$, so $\vec r\,{}'(0)=\langle0,1,1\rangle$.",
        r"$|\vec r\,{}'(0)|=\sqrt{0+1+1}=\sqrt2$.",
        r"$\vec T(0)=\left\langle0,\frac{1}{\sqrt2},\frac{1}{\sqrt2}\right\rangle$.",
    ],
    trap=r"Skipping the normalisation. $\vec T$ is a **unit** vector by definition; $\vec r\,{}'$ alone is not one here.",
    check=lambda: (V(0, 1, 1) / V(0, 1, 1).norm()),
    want=V(0, 1 / sqrt(2), 1 / sqrt(2)),
),
"L6P4": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle e^t,\,-e^{-t},\,\sqrt2\rangle$; at $t=0$ this is $\langle1,-1,\sqrt2\rangle$.",
        r"Speed $=\sqrt{1+1+2}=\sqrt4=2$.",
    ],
    trap=r"Differentiating $e^{-t}$ to $e^{-t}$. The chain rule puts a minus in front, though here it squares away — the sign matters for direction, not for speed.",
    check=lambda: V(1, -1, sqrt(2)).norm(), want=2,
),
"L6P5": dict(
    steps=[
        r"$\vec r\,{}'=\langle1,2t,3t^2\rangle$ and $\vec r\,{}''=\langle0,2,6t\rangle$.",
        r"$\vec i$: $(2t)(6t)-(3t^2)(2)=12t^2-6t^2=6t^2$.",
        r"$\vec j$: $-\big[(1)(6t)-(3t^2)(0)\big]=-6t$.",
        r"$\vec k$: $(1)(2)-(2t)(0)=2$. So $\vec r\,{}'\times\vec r\,{}''=\langle6t^2,-6t,2\rangle$.",
    ],
    trap=r"This exact vector is the numerator of the curvature formula $\kappa=\frac{|\vec r\,{}'\times\vec r\,{}''|}{|\vec r\,{}'|^3}$ — recognise it and Lesson 8 gets shorter.",
    check=lambda: cross([1, 2 * t, 3 * t ** 2], [0, 2, 6 * t]),
    want=V(6 * t ** 2, -6 * t, 2),
),
"L6P6": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle-3\sin t,\;4\cos t,\;0\rangle$.",
        r"At $t=\frac{\pi}{2}$: $\langle-3,0,0\rangle$.",
        r"Speed $=3$.",
    ],
    trap=r"Assuming an ellipse is traversed at constant speed. It is not — the speed here is $\sqrt{9\sin^2t+16\cos^2t}$, which runs between $3$ and $4$. Only the circle has constant speed under this parametrisation.",
    check=lambda: V(-3 * sin(pi / 2), 4 * cos(pi / 2), 0).norm(), want=3,
),

# ------------------------------------------------------------ Lesson 8 ----
"L8P1": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle-3\sin t,\;3\cos t,\;4\rangle$.",
        r"$|\vec r\,{}'|=\sqrt{9\sin^2t+9\cos^2t+16}=\sqrt{9+16}=5$ — constant, the helix is traversed at constant speed.",
        r"$L=\int_0^{2\pi}5\,dt=10\pi$.",
    ],
    trap=r"Losing the Pythagorean identity. $9\sin^2+9\cos^2=9$; if your integrand still contains $t$, the collapse was missed.",
    check=lambda: integrate(sqrt(9 * sin(t) ** 2 + 9 * cos(t) ** 2 + 16), (t, 0, 2 * pi)),
    want=10 * pi,
),
"L8P2": dict(
    steps=[
        r"For the helix $\langle a\cos t,a\sin t,bt\rangle$, $\kappa=\dfrac{a}{a^2+b^2}$ — constant.",
        r"Here $a=2$, $b=1$: $\kappa=\dfrac{2}{4+1}=\dfrac25$.",
        r"By the cross-product formula: $\vec r\,{}'\times\vec r\,{}''=\langle2\sin t,-2\cos t,4\rangle$, whose length is $\sqrt{4+16}=2\sqrt5$, and $|\vec r\,{}'|^3=(\sqrt5)^3=5\sqrt5$. Ratio $=\frac{2\sqrt5}{5\sqrt5}=\frac25$.",
    ],
    trap=r"Using $\kappa=\frac1a$ — that is the **circle** of radius $a$. Climbing in $z$ straightens the curve, so the helix is always less curved than its shadow.",
    check=lambda: simplify(cross([-2 * sin(t), 2 * cos(t), 1],
                                 [-2 * cos(t), -2 * sin(t), 0]).norm()
                           / V(-2 * sin(t), 2 * cos(t), 1).norm() ** 3),
    want=Rational(2, 5),
),
"L8P3": dict(
    steps=[
        r"For a graph, $\kappa(x)=\dfrac{|f''(x)|}{\left[1+(f'(x))^2\right]^{3/2}}$.",
        r"$f'=3x^2$, $f''=6x$; at $x=0$ both the numerator and $f'$ vanish.",
        r"$\kappa(0)=\dfrac{0}{1^{3/2}}=0$.",
    ],
    trap=r"Assuming a curve that visibly bends must have $\kappa>0$ somewhere along it. $y=x^3$ is *flat to second order* at the origin — it is an inflection point, and curvature is exactly zero there.",
    check=lambda: (abs(diff(x ** 3, x, 2)) / (1 + diff(x ** 3, x) ** 2) ** Rational(3, 2)).subs(x, 0),
    want=0,
),
"L8P4": dict(
    steps=[
        r"$\vec r\,{}'=\langle3,4,0\rangle$, a constant vector: this is a straight line.",
        r"$|\vec r\,{}'|=5$.",
        r"$L=\int_1^5 5\,dt=5\cdot4=20$.",
    ],
    trap=r"Integrating from $0$ to $5$. The interval is $[1,5]$, which has length $4$, not $5$.",
    check=lambda: integrate(V(3, 4, 0).norm(), (t, 1, 5)), want=20,
),
"L8P5": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle5\cos t,\;3\cos t,\;-4\sin t\rangle$.",
        r"$|\vec r\,{}'|^2=25\cos^2t+9\cos^2t+16\sin^2t=34\cos^2t+16\sin^2t$.",
        r"Write $\sin^2t=1-\cos^2t$: $=16+18\cos^2t$.",
        r"$L=\displaystyle\int_0^{\pi}\sqrt{16+18\cos^2t}\,dt$ — an elliptic integral, which has no elementary antiderivative. Setting it up correctly *is* the answer.",
    ],
    trap=r"Hunting for a closed form. Most arc lengths do not have one; the exam asks you to set it up, so stop when the integral is right.",
    check=lambda: simplify(25 * cos(t) ** 2 + 9 * cos(t) ** 2 + 16 * sin(t) ** 2
                           - (16 + 18 * cos(t) ** 2)),
    want=0,
),

# ------------------------------------------------------------ Lesson 9 ----
"L9P1": dict(
    steps=[
        r"A square root needs a non-negative radicand: $9-x^2-y^2\ge0$.",
        r"$x^2+y^2\le9$.",
        r"The **closed disk** of radius $3$ centred at the origin, boundary included.",
    ],
    trap=r"Writing a strict inequality. The boundary circle is fine — it just makes $f=0$ there. Strictness belongs to logs and denominators.",
    prose=True,
),
"L9P2": dict(
    steps=[
        r"Set $x^2+4y^2=k$. For $k<0$ there are no points; $k=0$ is the single point at the origin.",
        r"For $k>0$, divide: $\dfrac{x^2}{k}+\dfrac{y^2}{k/4}=1$.",
        r"**Ellipses** centred at the origin, twice as wide as they are tall (semi-axes $\sqrt k$ and $\sqrt k/2$).",
    ],
    trap=r"Calling them circles. The $4$ squashes the $y$-direction; equal denominators would be needed for circles.",
    prose=True,
),
"L9P3": dict(
    steps=[
        r"$y-x^2=k\Rightarrow y=x^2+k$.",
        r"**Parabolas** $y=x^2$, shifted vertically by $k$ — one for every real $k$, and they never intersect.",
    ],
    trap=r"Expecting closed curves. Level curves of a saddle-ish surface are unbounded; only bowl-shaped surfaces give loops.",
    prose=True,
),
"L9P4": dict(
    steps=[
        r"$\ln$ requires a **strictly** positive argument: $x+y-1>0$.",
        r"$x+y>1$: the open half-plane strictly above the line $y=1-x$, the line itself excluded.",
    ],
    trap=r"Including the line. At $x+y=1$ the log is $\ln 0$, undefined — this is the one place the boundary is genuinely out.",
    prose=True,
),
"L9P5": dict(
    steps=[
        r"$x^2+y^2+z^2=k$ with $k>0$ is a sphere of radius $\sqrt k$.",
        r"$k=0$ collapses to the origin; $k<0$ is empty.",
        r"**Concentric spheres** centred at the origin.",
    ],
    trap=r"A level *surface* of a three-variable function, not a level curve. One dimension up: $f(x,y,z)=k$ carves a surface out of space.",
    prose=True,
),

# ----------------------------------------------------------- Lesson 10 ----
"L10P1": dict(
    steps=[
        r"Try paths first. Along $y=0$: $0$. Along $x=0$: $0$. Along $y=x^2$: $\frac{x^3\cdot x^2}{x^4+x^4}=\frac{x}{2}\to0$. Every path gives $0$, which is a signal to stop hunting and start proving.",
        r"Squeeze. By AM–GM, $x^4+y^2\ge 2x^2|y|$, so for $(x,y)\ne(0,0)$:",
        r"$$\left|\frac{x^3y}{x^4+y^2}\right|\le\frac{|x|^3|y|}{2x^2|y|}=\frac{|x|}{2}.$$",
        r"$\frac{|x|}{2}\to0$, so the limit **exists and equals $0$**.",
    ],
    trap=r"A finite pile of paths never proves a limit exists — but it also never proves it fails. When every path you try agrees, switch to a bound.",
    right=r"$0$",
    fix=r"The official answer says the limit does not exist. It does: the AM–GM squeeze above bounds the expression by $\frac{|x|}{2}$. (Compare $\frac{x^2y}{x^4+y^2}$, which genuinely fails along $y=x^2$ — one power of $x$ away.)",
    check=lambda: limit(limit((x ** 3 * y) / (x ** 4 + y ** 2), y, x ** 2), x, 0),
    want=0,
),
"L10P2": dict(
    steps=[
        r"Every path gives $0$: along $y=mx$, $\frac{3x^2(mx)}{x^2(1+m^2)}=\frac{3mx}{1+m^2}\to0$.",
        r"Squeeze, and this one is immediate: $x^2\le x^2+y^2$, so $\dfrac{x^2}{x^2+y^2}\le1$ and",
        r"$$\left|\frac{3x^2y}{x^2+y^2}\right|\le 3|y|.$$",
        r"$3|y|\to0$ as $(x,y)\to(0,0)$, so the limit **exists and equals $0$**.",
    ],
    trap=r"Degree counting is the fast check: the numerator is degree $3$, the denominator degree $2$. Numerator degree strictly larger $\Rightarrow$ the quotient is squeezed to $0$. Only equal degrees can produce a path-dependent limit.",
    right=r"$0$",
    fix=r"The official answer says the limit does not exist. It does: it is $0$, by the one-line bound $\left|\frac{3x^2y}{x^2+y^2}\right|\le3|y|$. The classic DNE example is $\frac{xy}{x^2+y^2}$ — numerator and denominator both degree $2$.",
    check=lambda: limit(limit((3 * x ** 2 * y) / (x ** 2 + y ** 2), y, k_ * x), x, 0),
    want=0,
),
"L10P3": dict(
    steps=[
        r"Split it: $\dfrac{x^4-y^4}{x^2+y^2}-\dfrac{2k(x^2+y^2)}{x^2+y^2}$.",
        r"First piece factors: $\dfrac{(x^2-y^2)(x^2+y^2)}{x^2+y^2}=x^2-y^2\to0$.",
        r"Second piece is exactly $2k$, for every $(x,y)\ne(0,0)$.",
        r"Limit $=-2k$. Set $-2k=6\Rightarrow k=-3$.",
    ],
    trap=r"Losing the sign. The term enters as $-2k(x^2+y^2)$, so the limit is $-2k$, and $k=3$ would give $-6$.",
    check=lambda: solve(Eq(-2 * k_, 6), k_)[0], want=-3,
),
"L10P4": dict(
    steps=[
        r"Substitute $u=x^2+y^2$. As $(x,y)\to(0,0)$, $u\to0^+$.",
        r"The expression is $\dfrac{\sin u}{u}$.",
        r"$\lim_{u\to0}\frac{\sin u}{u}=1$.",
    ],
    trap=r"The substitution is legitimate here precisely because $x$ and $y$ only ever appear in the combination $x^2+y^2$. It is not legitimate in general.",
    check=lambda: limit(sin(u_) / u_, u_, 0), want=1,
),
"L10P5": dict(
    steps=[
        r"Polar coordinates: $x=r\cos\theta$, $y=r\sin\theta$, and $(x,y)\to(0,0)$ is exactly $r\to0^+$.",
        r"$\dfrac{r^3(\cos^3\theta-\sin^3\theta)}{r^2}=r(\cos^3\theta-\sin^3\theta)$.",
        r"$|\cos^3\theta-\sin^3\theta|\le2$, so the whole thing is $\le 2r\to0$ **uniformly in $\theta$**.",
        r"The limit is $0$.",
    ],
    trap=r"Polar only settles it when the $\theta$ factor is bounded and the $r$ factor goes to zero on its own. If $\theta$ survives in the limit, polar has told you it does **not** exist.",
    check=lambda: limit((x ** 3 - y ** 3) / (x ** 2 + y ** 2), x, 0).subs(y, 0),
    want=0,
),

# ----------------------------------------------------------- Lesson 11 ----
"L11P1": dict(
    steps=[
        r"Read the order right: $f_{yxz}$ means differentiate by $y$, then $x$, then $z$.",
        r"$f_y=-x\sin(xy)+2yz\,e^{y^2z}$.",
        r"$f_{yx}=-\sin(xy)-xy\cos(xy)$ — the $e^{y^2z}$ term has no $x$ and dies here.",
        r"$f_{yxz}=0$: what is left has no $z$ in it at all. Evaluating at $(0,1,1)$ is not even needed.",
    ],
    trap=r"Grinding through the $\ln(z^3)$ term. It has no $x$ and no $y$, so it is annihilated by the very first derivative.",
    check=lambda: diff(cos(x * y) + exp(y ** 2 * z) + log(z ** 3), y, x, z),
    want=0,
),
"L11P2": dict(
    steps=[
        r"$f_x=3x^2y^2+y\cos(xy)$.",
        r"$f_{xy}=6x^2y+\cos(xy)-xy\sin(xy)$ (product rule on $y\cos(xy)$).",
        r"At $(0,0)$: $0+\cos0-0=1$.",
    ],
    trap=r"Evaluating at $(0,0)$ **before** differentiating. $f(x,0)=0$ for all $x$, so that route reports $0$ — you must differentiate symbolically first, then substitute.",
    check=lambda: diff(x ** 3 * y ** 2 + sin(x * y), x, y).subs({x: 0, y: 0}),
    want=1,
),
"L11P3": dict(
    steps=[
        r"Hold $y$ constant: $f_x=e^{x^2y}\cdot 2xy$.",
        r"At $(1,2)$: $e^{2}\cdot2\cdot1\cdot2=4e^2$.",
    ],
    trap=r"Differentiating the exponent as if $y$ were a variable too. In $f_x$, $y$ is a constant — that is the entire content of 'partial'.",
    check=lambda: diff(exp(x ** 2 * y), x).subs({x: 1, y: 2}), want=4 * exp(2),
),
"L11P4": dict(
    steps=[
        r"$f_x=2x\ln y$, so $f_{xy}=\dfrac{2x}{y}$.",
        r"The other order: $f_y=\dfrac{x^2}{y}$, so $f_{yx}=\dfrac{2x}{y}$.",
        r"They agree — as Clairaut guarantees, since both mixed partials are continuous on $y>0$.",
    ],
    trap=r"Believing Clairaut always applies. It needs continuity of the mixed partials; the standard counterexample $\frac{xy(x^2-y^2)}{x^2+y^2}$ has $f_{xy}(0,0)\ne f_{yx}(0,0)$.",
    check=lambda: [simplify(diff(x ** 2 * log(y), x, y)), simplify(diff(x ** 2 * log(y), y, x))],
    want=[2 * x / y, 2 * x / y],
),
"L11P5": dict(
    steps=[
        r"For $f=\arctan\frac{y}{x}$: $f_x=\dfrac{-y}{x^2+y^2}$ and $f_y=\dfrac{x}{x^2+y^2}$.",
        r"At $(1,1)$: $f_x=-\frac12$, $f_y=\frac12$.",
        r"$f_x+f_y=0$.",
    ],
    trap=r"Dropping the inner derivative $\frac{\partial}{\partial x}\frac{y}{x}=-\frac{y}{x^2}$. The $\frac{1}{1+(y/x)^2}$ factor then has to be cleared of its fractions to reach $x^2+y^2$.",
    check=lambda: (diff(atan(y / x), x) + diff(atan(y / x), y)).subs({x: 1, y: 1}),
    want=0,
),

# ----------------------------------------------------------- Lesson 12 ----
"L12P1": dict(
    steps=[
        r"Chain rule: $\frac{dz}{dt}=\frac{\partial z}{\partial x}\frac{dx}{dt}+\frac{\partial z}{\partial y}\frac{dy}{dt}=2xy(2t)+x^2(3t^2)$.",
        r"At $t=1$: $x=1$, $y=1$, so $=2(1)(1)(2)+1(3)=4+3=7$.",
        r"Sanity check by substituting first: $z=(t^2)^2t^3=t^7$, $\frac{dz}{dt}=7t^6=7$ at $t=1$. Same.",
        r"$\dfrac{dz}{dt}\Big|_{t=1}=7$.",
    ],
    trap=r"Substituting first is fine here and often faster — but the exam wants the tree diagram, and for a general $f$ you cannot substitute at all.",
    check=lambda: diff((t ** 2) ** 2 * t ** 3, t).subs(t, 1), want=7,
),
"L12P2": dict(
    steps=[
        r"Write $F=xz^2+y^2z-2$, so the surface is $F=0$.",
        r"$F_x=z^2$ and $F_z=2xz+y^2$.",
        r"$\dfrac{\partial z}{\partial x}=-\dfrac{F_x}{F_z}=-\dfrac{z^2}{2xz+y^2}$.",
        r"At $(1,1,1)$: $-\dfrac{1}{2+1}=-\dfrac13$.",
    ],
    trap=r"The minus sign in $-F_x/F_z$. It is not optional and it is the single most-dropped symbol in 15.4.",
    check=lambda: (-diff(x * z ** 2 + y ** 2 * z - 2, x) / diff(x * z ** 2 + y ** 2 * z - 2, z)).subs({x: 1, y: 1, z: 1}),
    want=Rational(-1, 3),
),
"L12P3": dict(
    steps=[
        r"$\frac{\partial w}{\partial s}=w_x x_s+w_y y_s+w_z z_s=(y)(1)+(x+z)(t)+(y)(1)$.",
        r"At $s=1,t=0$: $x=1$, $y=0$, $z=1$, so $=0+(2)(0)+0=0$.",
        r"Or substitute first: $w=st(s+t)+st(s-t)=2s^2t$, $w_s=4st=0$ at $(1,0)$.",
        r"$\dfrac{\partial w}{\partial s}=0$.",
    ],
    trap=r"Missing that $y$ multiplies **two** branches ($w=xy+yz$ feeds $y$ into both terms), so $y_s$ appears once with coefficient $x+z$.",
    check=lambda: diff(2 * s_ ** 2 * t, s_).subs({s_: 1, t: 0}), want=0,
),
"L12P4": dict(
    steps=[
        r"$F=\sin(xy)-e^{2z}$, so $F_x=y\cos(xy)$ and $F_z=-2e^{2z}$.",
        r"At $\left(1,\frac{\pi}{2},0\right)$: $F_x=\frac{\pi}{2}\cos\frac{\pi}{2}=0$ and $F_z=-2$.",
        r"$\dfrac{\partial z}{\partial x}=-\dfrac{0}{-2}=0$.",
    ],
    trap=r"$\cos\frac{\pi}{2}=0$ is what kills this one. Check the point before doing any algebra — sometimes it collapses the whole expression.",
    check=lambda: (-diff(sin(x * y) - exp(2 * z), x) / diff(sin(x * y) - exp(2 * z), z)).subs({x: 1, y: pi / 2, z: 0}),
    want=0,
),
"L12P5": dict(
    steps=[
        r"$\frac{\partial z}{\partial r}=f_x\frac{\partial x}{\partial r}+f_y\frac{\partial y}{\partial r}$.",
        r"$\frac{\partial x}{\partial r}=\cos\theta$ and $\frac{\partial y}{\partial r}=\sin\theta$ (with $\theta$ held fixed).",
        r"$\dfrac{\partial z}{\partial r}=f_x\cos\theta+f_y\sin\theta$.",
        r"Worth noticing: that is $\nabla f\cdot\langle\cos\theta,\sin\theta\rangle$ — the directional derivative straight outward. Lesson 13 in disguise.",
    ],
    trap=r"Writing $\frac{\partial z}{\partial\theta}$ by mistake; that one is $-f_x r\sin\theta+f_y r\cos\theta$, and the factors of $r$ are the tell.",
    prose=True,
),
"L12P6": dict(
    steps=[
        r"$F=x^2+y^2+z^2-3xyz$, so $F_x=2x-3yz$ and $F_z=2z-3xy$.",
        r"At $(1,1,1)$: $F_x=2-3=-1$ and $F_z=2-3=-1$.",
        r"$F_z=-1\ne0$, so the implicit function theorem applies and $z$ really is a function of $(x,y)$ near this point.",
        r"$\dfrac{\partial z}{\partial x}=-\dfrac{-1}{-1}=-1$.",
    ],
    trap=r"Skipping the $F_z\ne0$ check. When $F_z=0$ the surface has a vertical tangent plane there and $\frac{\partial z}{\partial x}$ does not exist — which is exactly what the 'or explain why not' is fishing for.",
    check=lambda: (-diff(x ** 2 + y ** 2 + z ** 2 - 3 * x * y * z, x)
                   / diff(x ** 2 + y ** 2 + z ** 2 - 3 * x * y * z, z)).subs({x: 1, y: 1, z: 1}),
    want=-1,
),

# ----------------------------------------------------------- Lesson 13 ----
"L13P1": dict(
    steps=[
        r"$\nabla f=\langle 2xy,\;x^2-6y\rangle$; at $(2,1)$ that is $\langle4,\,4-6\rangle=\langle4,-2\rangle$.",
        r"Normalise the direction: $|\langle3,4\rangle|=5$, so $\hat u=\left\langle\frac35,\frac45\right\rangle$.",
        r"$D_{\hat u}f=\langle4,-2\rangle\cdot\left\langle\frac35,\frac45\right\rangle=\frac{12-8}{5}=\frac45$.",
    ],
    trap=r"Dotting with $\langle3,4\rangle$ unnormalised, which gives $4$ — five times too big. The directional derivative is only a rate if the direction has length $1$.",
    check=lambda: V(4, -2).dot(V(3, 4) / 5), want=Rational(4, 5),
),
"L13P2": dict(
    steps=[
        r"$f=x\sqrt{yz}$, so $f_x=\sqrt{yz}$, $f_y=\dfrac{xz}{2\sqrt{yz}}$, $f_z=\dfrac{xy}{2\sqrt{yz}}$.",
        r"At $(4,1,4)$: $\sqrt{yz}=2$, so $\nabla f=\left\langle2,\;\frac{16}{4},\;\frac{4}{4}\right\rangle=\langle2,4,1\rangle$.",
        r"Maximum rate $=|\nabla f|=\sqrt{4+16+1}=\sqrt{21}$.",
        r"It occurs in the direction of $\nabla f$ itself, $\langle2,4,1\rangle$.",
    ],
    trap=r"Giving the maximum rate as a vector or the direction as a number. The rate is $|\nabla f|$; the direction is $\nabla f$ (or its unit version).",
    check=lambda: V(2, 4, 1).norm(), want=sqrt(21),
),
"L13P3": dict(
    steps=[
        r"$\nabla f=\left\langle e^{-y},\;-xe^{-y}\right\rangle$; at $(1,2)$: $\left\langle e^{-2},\,-e^{-2}\right\rangle$.",
        r"Steepest **decrease** is $-\nabla f=\left\langle-e^{-2},\,e^{-2}\right\rangle$, i.e. the direction $\langle-1,1\rangle$.",
        r"The rate of decrease is $|\nabla f|=e^{-2}\sqrt{2}$.",
    ],
    trap=r"Reporting the rate as negative. 'Rate of decrease' is already signed by the word; the magnitude $\sqrt2\,e^{-2}$ is the number wanted.",
    check=lambda: V(exp(-2), -exp(-2)).norm(), want=sqrt(2) * exp(-2),
),
"L13P4": dict(
    steps=[
        r"$\nabla f=\langle2x,4y,6z\rangle$; at $(1,1,1)$: $\langle2,4,6\rangle$.",
        r"$\hat u=\dfrac{\langle1,-1,0\rangle}{\sqrt2}$.",
        r"$D_{\hat u}f=\dfrac{2-4+0}{\sqrt2}=\dfrac{-2}{\sqrt2}=-\sqrt2$.",
    ],
    trap=r"Rationalising carelessly: $\frac{-2}{\sqrt2}=-\sqrt2$, not $-\frac{\sqrt2}{2}$.",
    check=lambda: simplify(V(2, 4, 6).dot(V(1, -1, 0) / sqrt(2))), want=-sqrt(2),
),
"L13P5": dict(
    steps=[
        r"$\hat u=\left\langle\frac35,\frac45\right\rangle$.",
        r"$D_{\hat u}f=\langle4,-3\rangle\cdot\left\langle\frac35,\frac45\right\rangle=\frac{12-12}{5}=0$.",
        r"Zero is meaningful: $\langle3,4\rangle$ is perpendicular to $\nabla f$, so this direction runs **along the level curve** through $(2,3)$.",
    ],
    trap=r"Treating $0$ as a computational accident. A zero directional derivative always means you are moving tangent to the level curve.",
    check=lambda: V(4, -3).dot(V(3, 4) / 5), want=0,
),

# ----------------------------------------------------------- Lesson 14 ----
"L14P1": dict(
    steps=[
        r"Solve for $z$: $z=-2x^2+4x-y^3-2$.",
        r"Parallel to the $xy$-plane means the tangent plane is horizontal: $z_x=0$ and $z_y=0$.",
        r"$z_x=-4x+4=0\Rightarrow x=1$; $z_y=-3y^2=0\Rightarrow y=0$.",
        r"$z=-2+4-0-2=0$. The point is $(1,0,0)$.",
    ],
    trap=r"Reporting only $(x,y)$. The question asks for points on the **surface**, so the $z$-coordinate has to be computed.",
    check=lambda: [solve(Eq(-4 * x + 4, 0), x)[0], solve(Eq(-3 * y ** 2, 0), y)[0],
                   (-2 * x ** 2 + 4 * x - y ** 3 - 2).subs({x: 1, y: 0})],
    want=[1, 0, 0],
),
"L14P2": dict(
    steps=[
        r"$z_x=2x+2y$ and $z_y=2x$; at $(1,1)$: $z_x=4$, $z_y=2$.",
        r"$z=3+4(x-1)+2(y-1)$.",
        r"Expand: $z=4x+2y-3$, i.e. $4x+2y-z=3$.",
    ],
    trap=r"Leaving off $f(a,b)=3$. The tangent plane has to pass through the point of tangency; without the constant it passes through the origin instead.",
    check=lambda: [diff(x ** 2 + 2 * x * y, x).subs({x: 1, y: 1}),
                   diff(x ** 2 + 2 * x * y, y).subs({x: 1, y: 1})],
    want=[4, 2],
),
"L14P3": dict(
    steps=[
        r"$f(3,4)=5$. $f_x=\dfrac{x}{\sqrt{x^2+y^2}}=\frac35$, $f_y=\dfrac{y}{\sqrt{x^2+y^2}}=\frac45$.",
        r"$L(x,y)=5+\frac35(x-3)+\frac45(y-4)$.",
        r"At $(3.1,3.9)$: $\Delta x=0.1$, $\Delta y=-0.1$.",
        r"$L=5+0.6(0.1)+0.8(-0.1)=5+0.06-0.08=4.98$.",
    ],
    trap=r"Sign of $\Delta y$. Moving from $4$ to $3.9$ is $-0.1$; getting that backwards gives $5.02$, and both look plausible.",
    # Build the linearisation from f and its partials at (3,4), then evaluate
    # it at (3.1, 3.9).
    check=lambda: (lambda f, a, b, at: (f.subs(at)
                                        + diff(f, x).subs(at) * (a - 3)
                                        + diff(f, y).subs(at) * (b - 4))
                   )(sqrt(x ** 2 + y ** 2), Rational(31, 10), Rational(39, 10),
                     {x: 3, y: 4}),
    want=Rational(249, 50),
),
"L14P4": dict(
    steps=[
        r"$dz=f_x\,dx+f_y\,dy$.",
        r"$f_x=3x^2y^2$ and $f_y=2x^3y$.",
        r"$dz=3x^2y^2\,dx+2x^3y\,dy$.",
    ],
    trap=r"Writing $\Delta z$ for $dz$. The differential is the linear estimate; $\Delta z$ is the true change, and they differ by higher-order terms.",
    check=lambda: [diff(x ** 3 * y ** 2, x), diff(x ** 3 * y ** 2, y)],
    want=[3 * x ** 2 * y ** 2, 2 * x ** 3 * y],
),
"L14P5": dict(
    steps=[
        r"Write the surface as a level set: $F(x,y,z)=x^2+y^2-z=0$.",
        r"$\nabla F=\langle2x,\;2y,\;-1\rangle$.",
        r"At $(1,2,5)$: $\langle2,4,-1\rangle$.",
    ],
    trap=r"Reading $\langle f_x,f_y,-1\rangle$ and the sign on the last slot. Both $\langle2,4,-1\rangle$ and $\langle-2,-4,1\rangle$ are normal; the form that comes out of $\nabla F$ is the one asked for.",
    check=lambda: V(diff(x ** 2 + y ** 2 - z, x), diff(x ** 2 + y ** 2 - z, y),
                    diff(x ** 2 + y ** 2 - z, z)).subs({x: 1, y: 2}),
    want=V(2, 4, -1),
),

# --------------------------------------------------------- Lesson 15-16 ----
"L15P1": dict(
    steps=[
        r"$f_x=2xy=0$ and $f_y=x^2-1+6y=0$.",
        r"$f_x=0$ splits into two cases: $x=0$ **or** $y=0$.",
        r"$x=0$: $-1+6y=0\Rightarrow y=\frac16$, giving $\left(0,\frac16\right)$.",
        r"$y=0$: $x^2-1=0\Rightarrow x=\pm1$, giving $(1,0)$ and $(-1,0)$.",
    ],
    trap=r"Dividing $2xy=0$ by $x$. That silently discards the $x=0$ branch — and here it is a whole critical point.",
    # Actually solve the gradient system; the earlier version sorted a list of
    # the answers I had already written down, which verified nothing.
    check=lambda: sorted(solve([diff(x ** 2 * y - y + 3 * y ** 2, x),
                                diff(x ** 2 * y - y + 3 * y ** 2, y)], [x, y])),
    want=sorted([(S(-1), S(0)), (S(0), Rational(1, 6)), (S(1), S(0))]),
),
"L15P2": dict(
    steps=[
        r"$f_x=2x+y+3=0$ and $f_y=x+2y-3=0$.",
        r"Solve: $y=-3-2x$, then $x+2(-3-2x)-3=0\Rightarrow-3x-9=0\Rightarrow x=-3$, $y=3$.",
        r"$f_{xx}=2$, $f_{yy}=2$, $f_{xy}=1$, so $D=4-1=3>0$.",
        r"$D>0$ and $f_{xx}=2>0$: **local minimum** at $(-3,3)$.",
    ],
    trap=r"Squaring $f_{xy}$ is required: $D=f_{xx}f_{yy}-(f_{xy})^2$. Using $f_{xy}$ unsquared gives $3$ here too, by coincidence — the habit will fail you elsewhere.",
    check=lambda: solve([Eq(2 * x + y + 3, 0), Eq(x + 2 * y - 3, 0)], [x, y]),
    want={x: -3, y: 3},
),
"L15P3": dict(
    steps=[
        r"Interior: $f_x=2x-2=0\Rightarrow x=1$, $f_y=2y=0\Rightarrow y=0$. Inside the disk, and $f(1,0)=1-2+0+4=3$.",
        r"Boundary $x^2+y^2=4$: substitute $y^2=4-x^2$, so $f=x^2-2x+(4-x^2)+4=8-2x$ with $x\in[-2,2]$.",
        r"That is linear and decreasing: max $12$ at $x=-2$, min $4$ at $x=2$.",
        r"Compare everything: $M=12$, $m=3$, so $M+m=15$.",
    ],
    trap=r"Ignoring the interior critical point because the boundary already gave a max and a min. The absolute minimum here is *inside*, at $(1,0)$.",
    # Interior critical point plus the boundary extremes, all computed.
    check=lambda: (lambda f: (lambda vals: max(vals) + min(vals))(
        [f.subs(solve([diff(f, x), diff(f, y)], [x, y], dict=True)[0])]
        + [simplify(f.subs({x: 2 * cos(u_), y: 2 * sin(u_)})).subs(u_, c)
           for c in (0, pi)])
    )(x ** 2 - 2 * x + y ** 2 + 4),
    want=15,
),
"L15P4": dict(
    steps=[
        r"$f_x=y-3x^2=0$ and $f_y=x-2y=0$, so $x=2y$ and $y=3x^2$.",
        r"$y=3(2y)^2=12y^2\Rightarrow y(1-12y)=0\Rightarrow y=0$ or $y=\frac1{12}$.",
        r"Critical points: $(0,0)$ and $\left(\frac16,\frac1{12}\right)$.",
        r"$f_{xx}=-6x$, $f_{yy}=-2$, $f_{xy}=1$, so $D=12x-1$. At $(0,0)$: $D=-1<0$, **saddle**. At $\left(\frac16,\frac1{12}\right)$: $D=1>0$ and $f_{xx}=-1<0$, **local maximum**.",
    ],
    trap=r"$D$ depends on $x$ here, so it must be re-evaluated at each point. A single computed $D$ cannot classify two different critical points.",
    # Solve for the critical points and evaluate the discriminant at each.
    check=lambda: (lambda f: [simplify((diff(f, x, 2) * diff(f, y, 2)
                                        - diff(f, x, y) ** 2).subs(c))
                              for c in solve([diff(f, x), diff(f, y)], [x, y], dict=True)]
                   )(x * y - x ** 3 - y ** 2),
    want=[-1, 1],
),
"L15P5": dict(
    steps=[
        r"$f_x=2x=0$ and $f_y=-2y=0$, so the only critical point is $(0,0)$.",
        r"$f_{xx}=2$, $f_{yy}=-2$, $f_{xy}=0$.",
        r"$D=(2)(-2)-0=-4<0$, so $(0,0)$ is a **saddle point**.",
        r"The geometry backs it up: along $y=0$ the surface is $x^2$ (a valley), along $x=0$ it is $-y^2$ (a ridge). This is the standard saddle.",
    ],
    trap=r"$D<0$ is the one case that is fully decisive with no second test needed. Do not go looking at $f_{xx}$ afterwards; its sign is irrelevant when $D<0$.",
    check=lambda: diff(x ** 2 - y ** 2, x, 2) * diff(x ** 2 - y ** 2, y, 2)
                  - diff(x ** 2 - y ** 2, x, y) ** 2,
    want=-4,
),
"L15P6": dict(
    steps=[
        r"Interior: $f_x=4y-2x=0$ and $f_y=4x-4y=0$ give $x=y$ and $x=2y$, so only $(0,0)$ — a corner, not interior. No interior critical point.",
        r"Edge $y=0$: $f=2-x^2$ on $x\in[0,2]$, running from $2$ down to $-2$.",
        r"Edge $y=1$: $f=4x-x^2$ on $[0,2]$, running from $0$ up to $4$ at $x=2$.",
        r"Edge $x=0$: $f=2-2y^2\in[0,2]$. Edge $x=2$: $f=-2y^2+8y-2$, from $-2$ at $y=0$ to $4$ at $y=1$.",
        r"Absolute max $=4$ at $(2,1)$; absolute min $=-2$ at $(2,0)$.",
    ],
    trap=r"Forgetting the four **corners**. Both extremes here happen to be corner points, which the edge parametrisations only catch at their endpoints.",
    # Sweep the four edges (endpoints and interior critical points) and take
    # the extremes, instead of evaluating f at the two answers I expected.
    check=lambda: (lambda f: (lambda v: [max(v), min(v)])(
        [f.subs({x: a, y: b})
         for a in (0, 2) for b in (0, 1)]
        + [f.subs({x: a, y: b})
           for a in (0, 2)
           for b in [r for r in solve(diff(f.subs(x, a), y), y)
                     if r.is_real and 0 <= r <= 1]]
        + [f.subs({x: a, y: b})
           for b in (0, 1)
           for a in [r for r in solve(diff(f.subs(y, b), x), x)
                     if r.is_real and 0 <= r <= 2]])
    )(4 * x * y - x ** 2 - 2 * y ** 2 + 2),
    want=[4, -2],
),
}


# ---------------------------------------------------------------------------
# One problem is present in the published HTML but commented out, so it does
# not render on the instructor's page. The skill is squarely on the syllabus
# (13.5, distance from a point to a plane), so it is restored here — flagged,
# not smuggled in.
EXTRA = [
    dict(
        pid="L2X1", lesson="L2", after=2,
        stem=r"Find the distance from the point $(1,-2,3)$ to the plane $2x-y+2z=4$.",
        answer=r"$2$",
        steps=[
            r"$D=\dfrac{|ax_0+by_0+cz_0-d|}{\sqrt{a^2+b^2+c^2}}$ with $\vec n=\langle2,-1,2\rangle$.",
            r"Numerator: $|2(1)-(-2)+2(3)-4|=|2+2+6-4|=6$.",
            r"Denominator: $\sqrt{4+1+4}=3$.",
            r"$D=\dfrac63=2$.",
        ],
        trap=r"Forgetting to move $d$ to the same side. The formula measures $ax+by+cz-d$, so a plane written as $2x-y+2z=4$ contributes $-4$, not $+4$.",
        note="Commented out on the official page, so it does not appear there. "
             "The skill is still on the syllabus, so it is restored here.",
        check=lambda: abs(2 * 1 - (-2) + 2 * 3 - 4) / sqrt(4 + 1 + 4),
        want=2,
    ),
]


def _same(got, want):
    """Structural equality that knows sympy: recurses into lists and matrices."""
    if isinstance(got, Matrix) or isinstance(want, Matrix):
        g, w = Matrix(got), Matrix(want)
        return g.shape == w.shape and simplify(g - w) == Matrix.zeros(*g.shape)
    if isinstance(got, dict) or isinstance(want, dict):
        if set(got) != set(want):
            return False
        return all(_same(got[k], want[k]) for k in got)
    if isinstance(got, (list, tuple)) or isinstance(want, (list, tuple)):
        if len(got) != len(want):
            return False
        return all(_same(g, w) for g, w in zip(got, want))
    return simplify(S(got) - S(want)) == 0


def all_solutions():
    """The Exam 1 bank plus the Exam 2 / Final banks, as one dict.

    Kept in separate files because Exam 1 is hand-written and the later guides
    were produced in parallel passes, but every consumer — the page builder,
    verify(), and the official-answer audit — sees one merged bank held to one
    standard.
    """
    import exam2_sol
    merged = dict(SOL)
    clash = set(merged) & set(exam2_sol.SOL)
    if clash:
        import sys
        sys.exit(f"exam1_sol: duplicate solution ids across banks: {sorted(clash)}")
    merged.update(exam2_sol.SOL)
    return merged


def verify():
    """Recompute every checkable answer; die on a mismatch.

    Returns (checked, prose) counts so the build can report honestly how much
    of the bank is machine-verified rather than merely asserted.
    """
    import sys
    checked = prose = 0
    for pid, sol in all_solutions().items():
        fn = sol.get("check")
        if fn is None:
            prose += 1
            continue
        got = fn()
        if not _same(got, sol["want"]):
            sys.exit(f"solutions: {pid} check failed — computed {got!r}, "
                     f"expected {sol['want']!r}")
        checked += 1
    for e in EXTRA:
        if not _same(e["check"](), e["want"]):
            sys.exit(f"exam1_sol: {e['pid']} check failed")
        checked += 1
    return checked, prose


if __name__ == "__main__":
    c, p = verify()
    print(f"{c} answers recomputed and matched, {p} prose answers unchecked")
    print(f"{len(SOL)} solutions written, {sum(1 for s in SOL.values() if 'fix' in s)} "
          f"corrections to the official answers")
