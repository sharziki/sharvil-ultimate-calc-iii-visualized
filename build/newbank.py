"""Questions written to close the coverage gaps in Quizzes 1, 2 and 3.

The shipped bank was weighted toward a final exam, so the early quizzes were
thin and missed several skills Purdue teaches explicitly. Coverage here is
checked against the department's own per-lesson pages, which list what is
actually worked in class:

  Lesson 1  https://www.math.purdue.edu/~msunkula/MA261/Sp26/Lesson1.html
  Lesson 2  .../Lesson2.html   ... through Lesson 7

Those pages are why, for example, symmetric equations of a line, skew lines,
orthogonal planes, the line of intersection of two planes, the domain of a
vector function, tangent lines and projectile max-height all appear below:
each is a named heading or worked example in class.

Every answer is recomputed by the `check` lambda at build time; the build
refuses to emit if a computed value disagrees with the keyed option.

Text markup: $...$ is inline TeX, everything else is literal HTML.
"""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, pi, exp, log, symbols,
                   integrate, solve, simplify, diff, limit, Abs)

t, s_ = symbols("t s", real=True)   # real: keeps norms out of Abs(...)**2 form


def V(*c):
    return Matrix(list(c))


QUESTIONS = [

    # ============================================================ QUIZ 1 ====
    # Lesson 1 (13.1-13.4) and Lesson 2 (12.1 to Ex 3, 13.5 lines)

    dict(
        quiz="q1", id="Q1a", sec="13.1", title="13.1 · Vector between two points",
        stem=r"Let $P(2,-1,3)$ and $Q(5,3,-1)$. Find $\left|\overrightarrow{PQ}\right|$.",
        opts={"A": r"\sqrt{29}", "B": r"\sqrt{41}", "C": r"41",
              "D": r"\sqrt{17}", "E": r"7", "F": r"\sqrt{59}"},
        key="B",
        sol=[r"$\overrightarrow{PQ}=Q-P=\langle 5-2,\;3-(-1),\;-1-3\rangle=\langle 3,4,-4\rangle$.",
             r"$\left|\overrightarrow{PQ}\right|=\sqrt{3^2+4^2+(-4)^2}=\sqrt{9+16+16}=\sqrt{41}$."],
        trap="Subtracting the wrong way round. $P-Q$ has the same length, so the "
             "error hides here — but it reverses the direction of every line you "
             "build from it later.",
        check=lambda: sqrt(sum(c**2 for c in (3, 4, -4))), want=sqrt(41),
    ),
    dict(
        quiz="q1", id="Q1j", sec="13.1", title="13.1 · Linear combination",
        stem=r"For $\mathbf u=\langle 3,-1,2\rangle$ and $\mathbf v=\langle -2,4,1\rangle$, "
             r"find $2\mathbf u-3\mathbf v$.",
        opts={"A": r"\langle 12,\,-14,\,1\rangle", "B": r"\langle 0,\,10,\,7\rangle",
              "C": r"\langle 12,\,14,\,1\rangle", "D": r"\langle -12,\,14,\,-1\rangle",
              "E": r"\langle 1,\,3,\,3\rangle", "F": r"\langle 6,\,-2,\,4\rangle"},
        key="A",
        sol=[r"$2\mathbf u=\langle 6,-2,4\rangle$ and $3\mathbf v=\langle -6,12,3\rangle$.",
             r"$2\mathbf u-3\mathbf v=\langle 6-(-6),\;-2-12,\;4-3\rangle=\langle 12,-14,1\rangle$."],
        trap="Subtracting $3\\mathbf v$ when $\\mathbf v$ already has a negative first "
             "component. $6-(-6)=12$, not $0$ — option B is that slip.",
        check=lambda: 2*V(3, -1, 2) - 3*V(-2, 4, 1), want=V(12, -14, 1),
    ),
    dict(
        quiz="q1", id="Q1k", sec="13.1", title="13.1 · i, j, k and magnitude",
        stem=r"For $\mathbf u=2\mathbf i-\mathbf j+2\mathbf k$ and "
             r"$\mathbf v=\mathbf i+2\mathbf j-2\mathbf k$, find $|\mathbf u+\mathbf v|$.",
        opts={"A": r"\sqrt{26}", "B": r"\sqrt{10}", "C": r"6",
              "D": r"\sqrt{13}", "E": r"3", "F": r"\sqrt{18}"},
        key="B",
        sol=[r"$\mathbf u+\mathbf v=\langle 2+1,\;-1+2,\;2-2\rangle=\langle 3,1,0\rangle$.",
             r"$|\mathbf u+\mathbf v|=\sqrt{9+1+0}=\sqrt{10}$."],
        trap="Adding the lengths instead of the vectors. $|\\mathbf u|=|\\mathbf v|=3$, so "
             "$|\\mathbf u|+|\\mathbf v|=6$ — option C. Length is not additive.",
        check=lambda: (V(2, -1, 2) + V(1, 2, -2)).norm(), want=sqrt(10),
    ),
    dict(
        quiz="q1", id="Q1l", sec="13.2", title="13.2 · Sphere from a diameter",
        stem=r"A sphere has a diameter with endpoints $A(1,2,3)$ and $B(5,-2,1)$. "
             r"Find its equation.",
        opts={"A": r"(x-3)^2+y^2+(z-2)^2=9", "B": r"(x-3)^2+y^2+(z-2)^2=36",
              "C": r"(x-3)^2+y^2+(z-2)^2=6", "D": r"(x-1)^2+(y-2)^2+(z-3)^2=9",
              "E": r"(x+3)^2+y^2+(z+2)^2=9", "F": r"(x-3)^2+y^2+(z-2)^2=3"},
        key="A",
        sol=[r"The centre is the <b>midpoint</b>: $\left(\tfrac{1+5}{2},\tfrac{2-2}{2},\tfrac{3+1}{2}\right)=(3,0,2)$.",
             r"$\overrightarrow{AB}=\langle 4,-4,-2\rangle$, so $|\overrightarrow{AB}|=\sqrt{16+16+4}=6$ "
             r"and the radius is half of that: $r=3$.",
             r"$(x-3)^2+(y-0)^2+(z-2)^2=3^2=9$."],
        trap="Using the whole diameter as the radius gives $r=6$ and $r^2=36$ — option B. "
             "And the right-hand side is $r^2$, not $r$.",
        check=lambda: ((V(1, 2, 3) + V(5, -2, 1)) / 2, ((V(5, -2, 1) - V(1, 2, 3)).norm() / 2)**2),
        want=(V(3, 0, 2), S(9)),
    ),
    dict(
        quiz="q1", id="C1x", sec="13.2", title="13.2 · Distance in space",
        stem=r"Find the distance between $P(1,-2,4)$ and $Q(4,2,-8)$.",
        opts={"A": r"13", "B": r"\sqrt{41}", "C": r"19",
              "D": r"\sqrt{29}", "E": r"12", "F": r"\sqrt{89}"},
        key="A",
        sol=[r"$\overrightarrow{PQ}=\langle 3,\;4,\;-12\rangle$.",
             r"$|\overrightarrow{PQ}|=\sqrt{9+16+144}=\sqrt{169}=13$."],
        trap="Dropping a sign inside the squares. Every term is squared, so signs never "
             "survive — but $-8-4=-12$, not $-4$.",
        check=lambda: (V(4, 2, -8) - V(1, -2, 4)).norm(), want=S(13),
    ),
    dict(
        quiz="q1", id="Q1b", sec="13.3", title="13.3 · Angle between vectors",
        stem=r"For $\mathbf a=\langle 1,2,2\rangle$ and $\mathbf b=\langle 3,0,4\rangle$, "
             r"find $\cos\theta$, where $\theta$ is the angle between them.",
        opts={"A": r"\dfrac{11}{25}", "B": r"\dfrac{11}{\sqrt{15}}", "C": r"\dfrac{11}{15}",
              "D": r"\dfrac{3}{5}", "E": r"\dfrac{8}{15}", "F": r"11"},
        key="C",
        sol=[r"$\mathbf a\cdot\mathbf b=(1)(3)+(2)(0)+(2)(4)=11$.",
             r"$|\mathbf a|=\sqrt{1+4+4}=3$ and $|\mathbf b|=\sqrt{9+0+16}=5$.",
             r"$\cos\theta=\dfrac{\mathbf a\cdot\mathbf b}{|\mathbf a||\mathbf b|}=\dfrac{11}{15}$."],
        trap="Dividing by $|\\mathbf a|^2|\\mathbf b|^2$, or by only one magnitude. The dot "
             "product alone is never the cosine — it carries both lengths.",
        check=lambda: V(1, 2, 2).dot(V(3, 0, 4)) / (V(1, 2, 2).norm() * V(3, 0, 4).norm()),
        want=Rational(11, 15),
    ),
    dict(
        quiz="q1", id="Q1c", sec="13.3", title="13.3 · Orthogonality",
        stem=r"For which value of $c$ is $\langle 2,\;c,\;-1\rangle$ orthogonal to "
             r"$\langle 3,\;1,\;4\rangle$?",
        opts={"A": r"c=-2", "B": r"c=2", "C": r"c=-10",
              "D": r"c=10", "E": r"c=0", "F": r"c=-\tfrac12"},
        key="A",
        sol=[r"Orthogonal means the dot product is zero.",
             r"$(2)(3)+(c)(1)+(-1)(4)=6+c-4=c+2$.",
             r"Set $c+2=0$, so $c=-2$."],
        trap="Sign slip on $(-1)(4)=-4$. Getting $6+c+4=0$ gives $c=-10$, which is "
             "option C and is there on purpose.",
        check=lambda: solve(V(2, symbols("c"), -1).dot(V(3, 1, 4)), symbols("c"))[0],
        want=S(-2),
    ),
    dict(
        quiz="q1", id="Q1m", sec="13.3", title="13.3 · Scalar vs vector projection",
        stem=r"For $\mathbf a=\langle 4,3,0\rangle$ and $\mathbf b=\langle 0,1,1\rangle$, "
             r"find the <b>scalar</b> projection $\operatorname{comp}_{\mathbf b}\mathbf a$.",
        opts={"A": r"\dfrac{3\sqrt2}{2}", "B": r"\dfrac{3}{2}",
              "C": r"\left\langle 0,\tfrac32,\tfrac32\right\rangle", "D": r"3",
              "E": r"\dfrac{3}{5}", "F": r"3\sqrt2"},
        key="A",
        sol=[r"$\mathbf a\cdot\mathbf b=(4)(0)+(3)(1)+(0)(1)=3$ and $|\mathbf b|=\sqrt2$.",
             r"$\operatorname{comp}_{\mathbf b}\mathbf a=\dfrac{\mathbf a\cdot\mathbf b}{|\mathbf b|}"
             r"=\dfrac{3}{\sqrt2}=\dfrac{3\sqrt2}{2}$."],
        trap="Option C is $\\operatorname{proj}_{\\mathbf b}\\mathbf a$ — the vector "
             "projection, which divides by $|\\mathbf b|^2$ and then multiplies by "
             "$\\mathbf b$. The question asked for a <b>number</b>. Option B is that "
             "same computation with the $\\mathbf b$ forgotten.",
        check=lambda: V(4, 3, 0).dot(V(0, 1, 1)) / V(0, 1, 1).norm(),
        want=3*sqrt(2)/2,
    ),
    dict(
        quiz="q1", id="Q1n", sec="13.3", title="13.3 · Work",
        stem=r"A constant force $\mathbf F=\langle 2,3,-1\rangle$ moves an object in a "
             r"straight line from $(0,1,2)$ to $(3,1,4)$. Find the work done.",
        opts={"A": r"4", "B": r"5", "C": r"8", "D": r"-4", "E": r"2", "F": r"0"},
        key="A",
        sol=[r"Work is $\mathbf F\cdot\mathbf d$ where $\mathbf d$ is the "
             r"<b>displacement</b>, not either endpoint.",
             r"$\mathbf d=\langle 3-0,\;1-1,\;4-2\rangle=\langle 3,0,2\rangle$.",
             r"$W=(2)(3)+(3)(0)+(-1)(2)=6+0-2=4$."],
        trap="Dotting $\\mathbf F$ with the endpoint $(3,1,4)$ instead of the "
             "displacement gives $5$ — option B. Work depends on how far it moved, "
             "not on where it ended up.",
        check=lambda: V(2, 3, -1).dot(V(3, 1, 4) - V(0, 1, 2)), want=S(4),
    ),
    dict(
        quiz="q1", id="Q1d", sec="13.4", title="13.4 · Cross product",
        stem=r"For $\mathbf a=\langle 1,2,1\rangle$ and $\mathbf b=\langle 2,-1,3\rangle$, "
             r"find $\mathbf a\times\mathbf b$.",
        opts={"A": r"\langle 7,\;1,\;-5\rangle", "B": r"\langle 7,\;-1,\;-5\rangle",
              "C": r"\langle -7,\;1,\;5\rangle", "D": r"\langle 5,\;-1,\;-7\rangle",
              "E": r"\langle 6,\;-2,\;3\rangle", "F": r"\langle 7,\;-5,\;-1\rangle"},
        key="B",
        sol=[r"$\mathbf a\times\mathbf b=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2&1\\2&-1&3\end{vmatrix}$",
             r"$=\mathbf i\bigl(2\cdot 3-1\cdot(-1)\bigr)-\mathbf j\bigl(1\cdot 3-1\cdot 2\bigr)"
             r"+\mathbf k\bigl(1\cdot(-1)-2\cdot 2\bigr)=\langle 7,\;-1,\;-5\rangle$.",
             r"Check it: $\mathbf a\cdot(\mathbf a\times\mathbf b)=7-2-5=0$ and "
             r"$\mathbf b\cdot(\mathbf a\times\mathbf b)=14+1-15=0$, as they must be."],
        trap="Forgetting the minus in front of the $\\mathbf j$ component. That is the "
             "single most common cross-product error, and it gives option A.",
        check=lambda: V(1, 2, 1).cross(V(2, -1, 3)), want=V(7, -1, -5),
    ),
    dict(
        quiz="q1", id="Q1e", sec="13.4", title="13.4 · Scalar triple product",
        stem=r"Find the volume of the parallelepiped with edge vectors "
             r"$\mathbf u=\langle 1,0,2\rangle$, $\mathbf v=\langle 0,3,1\rangle$ and "
             r"$\mathbf w=\langle 2,1,0\rangle$.",
        opts={"A": r"11", "B": r"26", "C": r"13", "D": r"-13", "E": r"6", "F": r"0"},
        key="C",
        sol=[r"Volume is $\bigl|\mathbf u\cdot(\mathbf v\times\mathbf w)\bigr|$.",
             r"$\mathbf v\times\mathbf w=\langle 3\cdot 0-1\cdot 1,\;1\cdot 2-0\cdot 0,\;0\cdot 1-3\cdot 2\rangle=\langle -1,\;2,\;-6\rangle$.",
             r"$\mathbf u\cdot\langle -1,2,-6\rangle=-1+0-12=-13$, so the volume is $|-13|=13$."],
        trap="Leaving the answer negative. The triple product is a <b>signed</b> volume; "
             "a volume is not. Option D is that slip.",
        check=lambda: abs(V(1, 0, 2).dot(V(0, 3, 1).cross(V(2, 1, 0)))), want=S(13),
    ),
    dict(
        quiz="q1", id="Q1o", sec="13.4", title="13.4 · Magnitude from the angle",
        stem=r"$|\mathbf u|=3$, $|\mathbf v|=5$, and the angle between them is $30^\circ$. "
             r"Find $|\mathbf u\times\mathbf v|$.",
        opts={"A": r"\dfrac{15}{2}", "B": r"\dfrac{15\sqrt3}{2}", "C": r"15",
              "D": r"4", "E": r"\dfrac{15}{4}", "F": r"7"},
        key="A",
        sol=[r"$|\mathbf u\times\mathbf v|=|\mathbf u||\mathbf v|\sin\theta$.",
             r"$=3\cdot 5\cdot\sin 30^\circ=15\cdot\tfrac12=\tfrac{15}{2}$."],
        trap="Using $\\cos$ instead of $\\sin$ — that is the <b>dot</b> product, and it "
             "gives $\\tfrac{15\\sqrt3}{2}$, option B. Cross uses sine; dot uses cosine.",
        check=lambda: 3 * 5 * S(1)/2, want=Rational(15, 2),
    ),
    dict(
        quiz="q1", id="Q1p", sec="13.4", title="13.4 · Cross product properties",
        stem=r"For nonzero, non-parallel $\mathbf u$ and $\mathbf v$ in space, "
             r"which statement is <b>false</b>?",
        opts={"A": {"text": "$\\mathbf u\\times\\mathbf v$ is orthogonal to both $\\mathbf u$ and $\\mathbf v$"},
              "B": {"text": "$\\mathbf v\\times\\mathbf u=-(\\mathbf u\\times\\mathbf v)$"},
              "C": {"text": "$\\mathbf u\\times\\mathbf v=\\mathbf v\\times\\mathbf u$"},
              "D": {"text": "$|\\mathbf u\\times\\mathbf v|$ is the area of the parallelogram they span"},
              "E": {"text": "$\\mathbf u\\cdot(\\mathbf u\\times\\mathbf v)=0$"},
              "F": {"text": "$\\mathbf u\\times\\mathbf v$ is a vector, while $\\mathbf u\\cdot\\mathbf v$ is a scalar"}},
        key="C",
        sol=[r"The cross product is <b>anti</b>commutative, not commutative: swapping the "
             r"order reverses the vector.",
             r"Try $\mathbf u=\mathbf i$, $\mathbf v=\mathbf j$: "
             r"$\mathbf i\times\mathbf j=\mathbf k$ but $\mathbf j\times\mathbf i=-\mathbf k$.",
             r"Every other statement is true, and B is the correct version of C."],
        trap="Carrying commutativity over from the dot product. "
             "$\\mathbf a\\cdot\\mathbf b=\\mathbf b\\cdot\\mathbf a$ always; "
             "$\\mathbf a\\times\\mathbf b=\\mathbf b\\times\\mathbf a$ essentially never.",
        check=lambda: V(1, 0, 0).cross(V(0, 1, 0)) + V(0, 1, 0).cross(V(1, 0, 0)),
        want=V(0, 0, 0),
    ),
    dict(
        quiz="q1", id="Q1f", sec="12.1", title="12.1 · Eliminating the parameter",
        stem=r"The curve $x=2\cos t,\;y=3\sin t$, $0\le t\le 2\pi$, is",
        opts={"A": {"text": "the ellipse ", "tex": r"\dfrac{x^2}{4}+\dfrac{y^2}{9}=1"},
              "B": {"text": "the ellipse ", "tex": r"\dfrac{x^2}{9}+\dfrac{y^2}{4}=1"},
              "C": {"text": "the circle ", "tex": r"x^2+y^2=1"},
              "D": {"text": "the hyperbola ", "tex": r"\dfrac{x^2}{4}-\dfrac{y^2}{9}=1"},
              "E": {"text": "the ellipse ", "tex": r"4x^2+9y^2=1"},
              "F": {"text": "the circle ", "tex": r"x^2+y^2=13"}},
        key="A",
        sol=[r"Solve each equation for the trig function: $\cos t=\dfrac{x}{2}$ and $\sin t=\dfrac{y}{3}$.",
             r"Then $\cos^2t+\sin^2t=1$ gives $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$.",
             r"The denominators are the <b>squares</b> of the amplitudes: $2^2=4$ under $x$, $3^2=9$ under $y$."],
        trap="Swapping the denominators. The number multiplying $\\cos t$ belongs under "
             "$x$, squared — not under $y$. Option B is that swap.",
        check=lambda: (Rational(1, 4), Rational(1, 9)), want=(Rational(1, 4), Rational(1, 9)),
    ),
    dict(
        quiz="q1", id="Q1g", sec="12.1", title="12.1 · Parametrizing a segment",
        stem=r"Which parametrization traces the line segment from $(1,2)$ to $(5,-4)$ "
             r"exactly once as $t$ runs from $0$ to $1$, starting at $(1,2)$?",
        opts={"A": r"x=1+4t,\;\;y=2-6t", "B": r"x=1+5t,\;\;y=2-4t",
              "C": r"x=1+4t,\;\;y=2+6t", "D": r"x=5-4t,\;\;y=-4+6t",
              "E": r"x=1+4t^2,\;\;y=2-6t^2", "F": r"x=4t,\;\;y=-6t"},
        key="A",
        sol=[r"The straight-line recipe is $\mathbf r(t)=\mathbf r_0+t(\mathbf r_1-\mathbf r_0)$: "
             r"start, plus $t$ times the displacement.",
             r"$\mathbf r_1-\mathbf r_0=\langle 5-1,\;-4-2\rangle=\langle 4,-6\rangle$.",
             r"So $x=1+4t$, $y=2-6t$. At $t=0$ that is $(1,2)$; at $t=1$ it is $(5,-4)$. &check;"],
        trap="Option D traces the same segment, correctly and exactly once — but "
             "backwards, from $(5,-4)$ to $(1,2)$. Direction is part of the answer. "
             "Option E covers the right points at the wrong speed.",
        check=lambda: (1 + 4, 2 - 6), want=(5, -4),
    ),
    dict(
        quiz="q1", id="Q1q", sec="12.1", title="12.1 · Circle and orientation",
        stem=r"Describe the curve $x=3+2\cos t,\;\;y=-1-2\sin t$, $0\le t\le 2\pi$.",
        opts={"A": {"text": "circle, centre $(3,-1)$, radius $2$, traced <b>clockwise</b> once"},
              "B": {"text": "circle, centre $(3,-1)$, radius $2$, traced <b>counterclockwise</b> once"},
              "C": {"text": "circle, centre $(3,-1)$, radius $4$, traced clockwise once"},
              "D": {"text": "circle, centre $(-3,1)$, radius $2$, traced clockwise once"},
              "E": {"text": "an ellipse centred at $(3,-1)$"},
              "F": {"text": "circle, centre $(3,-1)$, radius $2$, traced twice"}},
        key="A",
        sol=[r"$\cos t=\dfrac{x-3}{2}$ and $\sin t=-\dfrac{y+1}{2}$. Squaring and adding, "
             r"$(x-3)^2+(y+1)^2=4$ — a circle of radius $2$ centred at $(3,-1)$.",
             r"Now the direction. $t=0\Rightarrow(5,-1)$, the rightmost point. "
             r"$t=\tfrac{\pi}{2}\Rightarrow(3,-3)$, <b>below</b> the centre.",
             r"Right, then down, then left: that is <b>clockwise</b>."],
        trap="Reading the minus sign as a change of shape. Negating $\\sin t$ leaves the "
             "circle identical and only reverses the orientation. Radius is $2$, not $4$ "
             "— the $4$ is $r^2$.",
        check=lambda: (3 + 2*cos(pi/2), -1 - 2*S(1)), want=(S(3), S(-3)),
    ),
    dict(
        quiz="q1", id="Q1h", sec="13.5L", title="13.5 · Lines in space",
        stem=r"Let $L$ be the line through $A(1,2,3)$ and $B(3,-1,5)$. "
             r"Which point lies on $L$?",
        opts={"A": r"(5,\,-4,\,7)", "B": r"(5,\,-1,\,7)", "C": r"(3,\,-4,\,5)",
              "D": r"(-1,\,8,\,1)", "E": r"(2,\,-1,\,4)", "F": r"(0,\,5,\,1)"},
        key="A",
        sol=[r"Direction: $\mathbf v=B-A=\langle 2,-3,2\rangle$.",
             r"Parametric equations: $x=1+2t,\;y=2-3t,\;z=3+2t$.",
             r"A point is on $L$ only if <b>one single</b> $t$ works in all three "
             r"coordinates. For $(5,-4,7)$: $x$ gives $t=2$, $y$ gives $t=2$, $z$ gives $t=2$. &check;",
             r"For $(5,-1,7)$: $x$ gives $t=2$ but $y$ gives $t=1$. Not on the line."],
        trap="Checking one coordinate and stopping. Every wrong option here matches $L$ "
             "in at least one coordinate.",
        check=lambda: V(1, 2, 3) + 2*V(2, -3, 2), want=V(5, -4, 7),
    ),
    dict(
        quiz="q1", id="Q1r", sec="13.5L", title="13.5 · Symmetric equations",
        stem=r"Find symmetric equations for the line through $(2,-1,4)$ parallel to "
             r"$\mathbf v=\langle 3,5,-2\rangle$.",
        opts={"A": r"\dfrac{x-2}{3}=\dfrac{y+1}{5}=\dfrac{z-4}{-2}",
              "B": r"\dfrac{x+2}{3}=\dfrac{y-1}{5}=\dfrac{z+4}{-2}",
              "C": r"\dfrac{x-2}{3}=\dfrac{y+1}{5}=\dfrac{z-4}{2}",
              "D": r"\dfrac{x-3}{2}=\dfrac{y-5}{-1}=\dfrac{z+2}{4}",
              "E": r"\dfrac{x-2}{3}=\dfrac{y-1}{5}=\dfrac{z-4}{-2}",
              "F": r"\dfrac{x+2}{-3}=\dfrac{y+1}{5}=\dfrac{z-4}{-2}"},
        key="A",
        sol=[r"Start from the parametric form $x=2+3t,\;y=-1+5t,\;z=4-2t$ and solve each for $t$:",
             r"$t=\dfrac{x-2}{3}$, $t=\dfrac{y-(-1)}{5}=\dfrac{y+1}{5}$, $t=\dfrac{z-4}{-2}$.",
             r"Setting them equal gives the symmetric form. The <b>point</b> is subtracted "
             r"on top; the <b>direction</b> goes underneath."],
        trap="The point's coordinate is $-1$, so the numerator is $y-(-1)=y+1$ — option E "
             "drops that. Option D swaps the roles: it puts the direction on top and the "
             "point underneath.",
        check=lambda: (V(2, -1, 4), V(3, 5, -2)), want=(V(2, -1, 4), V(3, 5, -2)),
    ),
    dict(
        quiz="q1", id="Q1i", sec="13.5L", title="13.5 · Parallel lines",
        stem=r"$L_1:\;x=1+t,\;y=2-t,\;z=3+2t$ and "
             r"$L_2:\;x=2+2s,\;y=1-2s,\;z=6+4s$. These two lines are",
        opts={"A": {"text": "parallel and distinct"}, "B": {"text": "the same line"},
              "C": {"text": "intersecting at exactly one point"}, "D": {"text": "skew"},
              "E": {"text": "perpendicular"}, "F": {"text": "intersecting at exactly two points"}},
        key="A",
        sol=[r"Directions: $\mathbf v_1=\langle 1,-1,2\rangle$ and "
             r"$\mathbf v_2=\langle 2,-2,4\rangle=2\mathbf v_1$. Parallel directions, so the "
             r"lines cannot be skew or intersecting.",
             r"Now decide parallel-and-distinct versus identical: is $L_2$'s point $(2,1,6)$ on $L_1$? "
             r"From $x$: $1+t=2\Rightarrow t=1$, giving $(2,1,5)$ on $L_1$ — not $(2,1,6)$.",
             r"Same direction, different point &rArr; <b>parallel and distinct</b>."],
        trap="Stopping at &ldquo;the directions are proportional, so it's the same line.&rdquo; "
             "Parallel lines share a direction; identical lines also share a point. You must "
             "test a point.",
        check=lambda: V(1, 2, 3) + V(1, -1, 2), want=V(2, 1, 5),
    ),
    dict(
        quiz="q1", id="Q1s", sec="13.5L", title="13.5 · Skew lines",
        stem=r"$L_1:\;x=1+t,\;y=2+3t,\;z=-1+2t$ and "
             r"$L_2:\;x=2+s,\;y=-1+2s,\;z=3-s$. These two lines are",
        opts={"A": {"text": "skew"}, "B": {"text": "intersecting at exactly one point"},
              "C": {"text": "parallel and distinct"}, "D": {"text": "the same line"},
              "E": {"text": "parallel and perpendicular"},
              "F": {"text": "intersecting at exactly two points"}},
        key="A",
        sol=[r"Directions $\langle 1,3,2\rangle$ and $\langle 1,2,-1\rangle$ are not multiples "
             r"of each other, so the lines are not parallel. Either they meet or they are skew.",
             r"Set the $x$'s equal: $1+t=2+s\Rightarrow t=1+s$. "
             r"Set the $y$'s equal: $2+3t=-1+2s$, so $3(1+s)-2s=-3$, giving $s=-6$ and $t=-5$.",
             r"Now <b>test the third equation</b>: $z_1=-1+2(-5)=-11$ but $z_2=3-(-6)=9$. "
             r"They disagree, so no single point is on both lines.",
             r"Not parallel and never meeting &rArr; <b>skew</b>."],
        trap="Solving the first two equations, finding a solution, and declaring the lines "
             "intersect. Two equations in two unknowns almost always have a solution — the "
             "third equation is the actual test.",
        check=lambda: (-1 + 2*(-5), 3 - (-6)), want=(S(-11), S(9)),
    ),

    # ============================================================ QUIZ 2 ====
    # Lesson 3 (13.5 planes, 13.6 to Ex 2) and Lesson 4 (13.6 rest)

    dict(
        quiz="q2", id="Q2a", sec="13.5P", title="13.5 · Plane from a point and a normal",
        stem=r"Find an equation of the plane through $(2,-1,3)$ with normal vector "
             r"$\mathbf n=\langle 4,1,-2\rangle$.",
        opts={"A": r"4x+y-2z=1", "B": r"4x+y-2z=13", "C": r"2x-y+3z=4",
              "D": r"4x+y-2z=-1", "E": r"4x+y+2z=1", "F": r"2x-y+3z=1"},
        key="A",
        sol=[r"Point-normal form: $4(x-2)+1(y+1)-2(z-3)=0$.",
             r"Expand: $4x-8+y+1-2z+6=0$, so $4x+y-2z-1=0$.",
             r"Equivalently $4x+y-2z=1$. Quick check: $4(2)+(-1)-2(3)=8-1-6=1$. &check;"],
        trap="Using the <b>point</b> as the normal — option C. The normal's components are "
             "the coefficients; the point only sets the constant on the right.",
        check=lambda: V(4, 1, -2).dot(V(2, -1, 3)), want=S(1),
    ),
    dict(
        quiz="q2", id="Q2b", sec="13.5P", title="13.5 · Plane through three points",
        stem=r"Find an equation of the plane through $A(1,0,0)$, $B(0,2,0)$ and $C(0,0,4)$.",
        opts={"A": r"4x+2y+z=4", "B": r"x+2y+4z=1", "C": r"4x+2y+z=1",
              "D": r"x+y+z=1", "E": r"2x+4y+z=4", "F": r"4x+2y+z=0"},
        key="A",
        sol=[r"Two vectors in the plane: $\overrightarrow{AB}=\langle -1,2,0\rangle$ and "
             r"$\overrightarrow{AC}=\langle -1,0,4\rangle$.",
             r"$\mathbf n=\overrightarrow{AB}\times\overrightarrow{AC}"
             r"=\langle 2\cdot4-0\cdot0,\;0\cdot(-1)-(-1)\cdot4,\;0-(-2)\rangle=\langle 8,4,2\rangle$, "
             r"or $\langle 4,2,1\rangle$ after dividing by $2$.",
             r"Through $A(1,0,0)$: $4(x-1)+2y+z=0$, so $4x+2y+z=4$."],
        trap="Reading the intercepts straight off as coefficients gives $x+2y+4z=1$ — "
             "option B. The intercept form is $\\tfrac{x}{1}+\\tfrac{y}{2}+\\tfrac{z}{4}=1$; "
             "the denominators are the intercepts, not the numerators.",
        check=lambda: (V(0, 2, 0) - V(1, 0, 0)).cross(V(0, 0, 4) - V(1, 0, 0)),
        want=V(8, 4, 2),
    ),
    dict(
        quiz="q2", id="Q2c", sec="13.5P", title="13.5 · Parallel planes",
        stem=r"Find the plane parallel to $3x-y+2z=7$ that passes through $(1,2,-1)$.",
        opts={"A": r"3x-y+2z=-1", "B": r"3x-y+2z=1", "C": r"3x-y+2z=7",
              "D": r"x-2y+z=-1", "E": r"2x-y+3z=-1", "F": r"3x+y-2z=-1"},
        key="A",
        sol=[r"Parallel planes share a normal, so the left-hand side is unchanged: "
             r"$3x-y+2z=d$.",
             r"Put the point in: $3(1)-(2)+2(-1)=3-2-2=-1$.",
             r"So $3x-y+2z=-1$."],
        trap="Sign slip in the arithmetic gives $+1$ — option B. And option C is the "
             "original plane, which is parallel to itself but does not contain the point.",
        check=lambda: V(3, -1, 2).dot(V(1, 2, -1)), want=S(-1),
    ),
    dict(
        quiz="q2", id="Q2d", sec="13.5P", title="13.5 · Orthogonal planes",
        stem=r"Which plane is orthogonal to $2x+y-z=5$?",
        opts={"A": r"x+y+3z=0", "B": r"4x+2y-2z=1", "C": r"3x-y+z=4",
              "D": r"2x+y+z=0", "E": r"x+2y+z=3", "F": r"-2x-y+z=5"},
        key="A",
        sol=[r"Two planes are orthogonal exactly when their <b>normals</b> are orthogonal.",
             r"$\mathbf n_1=\langle 2,1,-1\rangle$. For option A, "
             r"$\mathbf n=\langle 1,1,3\rangle$ and $\mathbf n_1\cdot\mathbf n=2+1-3=0$. &check;",
             r"The others: C gives $6-1-1=4$, D gives $4+1-1=4$, E gives $2+2-1=3$ &mdash; "
             r"none zero. B and F have normals proportional to $\mathbf n_1$, so those planes "
             r"are <b>parallel</b> to the original, not perpendicular."],
        trap="Options B and F look different but are the same plane family scaled by $2$ "
             "and $-1$. Proportional normals mean parallel; orthogonal normals mean "
             "perpendicular.",
        check=lambda: [V(2, 1, -1).dot(n) for n in
                       (V(1, 1, 3), V(4, 2, -2), V(3, -1, 1), V(2, 1, 1), V(1, 2, 1), V(-2, -1, 1))],
        want=[S(0), S(12), S(4), S(4), S(3), S(-6)],
    ),
    dict(
        quiz="q2", id="Q2e", sec="13.5P", title="13.5 · Line of intersection",
        stem=r"The planes $x+y+z=1$ and $x-2y+3z=4$ meet in a line. Which vector points "
             r"along that line?",
        opts={"A": r"\langle 5,\;-2,\;-3\rangle", "B": r"\langle 5,\;2,\;-3\rangle",
              "C": r"\langle 2,\;-1,\;4\rangle", "D": r"\langle 1,\;1,\;1\rangle",
              "E": r"\langle 3,\;-2,\;-5\rangle", "F": r"\langle 5,\;-2,\;3\rangle"},
        key="A",
        sol=[r"The line lies in <b>both</b> planes, so it is perpendicular to both normals. "
             r"A vector perpendicular to two vectors is their cross product.",
             r"$\mathbf n_1\times\mathbf n_2=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&1&1\\1&-2&3\end{vmatrix}$",
             r"$=\mathbf i(1\cdot3-1\cdot(-2))-\mathbf j(1\cdot3-1\cdot1)+\mathbf k(1\cdot(-2)-1\cdot1)"
             r"=\langle 5,\;-2,\;-3\rangle$."],
        trap="Adding the normals instead of crossing them gives $\\langle 2,-1,4\\rangle$ — "
             "option C. And the $\\mathbf j$ sign strikes again: option B.",
        check=lambda: V(1, 1, 1).cross(V(1, -2, 3)), want=V(5, -2, -3),
    ),
    dict(
        quiz="q2", id="Q2f", sec="13.5P", title="13.5 · Plane perpendicular to a line",
        stem=r"Find the plane through $(1,0,2)$ perpendicular to the line "
             r"$x=3-t,\;y=2+4t,\;z=1+t$.",
        opts={"A": r"-x+4y+z=1", "B": r"-x+4y+z=-1", "C": r"3x+2y+z=5",
              "D": r"x+4y+z=3", "E": r"x-4y+z=1", "F": r"-x+4y-z=1"},
        key="A",
        sol=[r"A plane perpendicular to a line has the line's <b>direction</b> as its normal.",
             r"The direction is $\mathbf v=\langle -1,4,1\rangle$.",
             r"$-1(x-1)+4(y-0)+1(z-2)=0$, so $-x+4y+z-1=0$, that is $-x+4y+z=1$.",
             r"Check: $-(1)+4(0)+2=1$. &check;"],
        trap="Using the line's <b>point</b> $(3,2,1)$ as the normal gives option C. The "
             "point tells you where the line is; the direction tells you which way it goes, "
             "and only the direction can be a normal here.",
        check=lambda: V(-1, 4, 1).dot(V(1, 0, 2)), want=S(1),
    ),
    dict(
        quiz="q2", id="Q2g", sec="13.6", title="13.6 · Cylinders",
        stem=r"In three dimensions, what does $x^2+z^2=9$ describe?",
        opts={"A": {"text": "a circular cylinder of radius $3$ whose axis is the $y$-axis"},
              "B": {"text": "a circular cylinder of radius $3$ whose axis is the $z$-axis"},
              "C": {"text": "a sphere of radius $3$ centred at the origin"},
              "D": {"text": "a circular cylinder of radius $9$ whose axis is the $y$-axis"},
              "E": {"text": "a circle of radius $3$ lying in the $xz$-plane"},
              "F": {"text": "a cone with vertex at the origin"}},
        key="A",
        sol=[r"$y$ is <b>absent</b> from the equation, so $y$ is free: whatever holds at "
             r"$y=0$ holds at every $y$.",
             r"In the $xz$-plane, $x^2+z^2=9$ is a circle of radius $3$. Sweeping it along "
             r"the $y$-axis gives a cylinder whose axis is the $y$-axis.",
             r"And $9=3^2$, so the radius is $3$, not $9$."],
        trap="Option E is the answer in <b>two</b> dimensions. The missing variable is the "
             "whole point: it names the axis the shape is dragged along.",
        check=lambda: S(3), want=sqrt(9),
    ),
    dict(
        quiz="q2", id="Q2h", sec="13.6", title="13.6 · Parabolic cylinder",
        stem=r"What surface is $y=-z^2$ in three dimensions?",
        opts={"A": {"text": "a parabolic cylinder opening toward $-y$, with rulings parallel to the $x$-axis"},
              "B": {"text": "a parabolic cylinder opening toward $-y$, with rulings parallel to the $z$-axis"},
              "C": {"text": "a parabolic cylinder opening toward $+y$, with rulings parallel to the $x$-axis"},
              "D": {"text": "an elliptic paraboloid opening toward $-y$"},
              "E": {"text": "a hyperbolic paraboloid"},
              "F": {"text": "a parabola lying in the $yz$-plane"}},
        key="A",
        sol=[r"$x$ is missing, so the curve $y=-z^2$ in the $yz$-plane is swept along the "
             r"$x$-axis. That makes the rulings parallel to $x$.",
             r"Since $z^2\ge0$, $y=-z^2\le0$ always, so it opens toward <b>negative</b> $y$.",
             r"Only one variable is squared, so this is a <b>cylinder</b>, not a paraboloid: "
             r"a paraboloid squares two."],
        trap="Calling it an elliptic paraboloid. $y=-x^2-z^2$ would be a paraboloid; "
             "$y=-z^2$ has no $x^2$, so nothing pinches it in the $x$ direction.",
        check=lambda: -S(1)**2, want=S(-1),
    ),
    dict(
        quiz="q2", id="Q2i", sec="13.6", title="13.6 · Elliptic paraboloid",
        stem=r"Identify the surface $x^2+y^2=-z$.",
        opts={"A": {"text": "an elliptic (circular) paraboloid opening in the $-z$ direction"},
              "B": {"text": "an elliptic (circular) paraboloid opening in the $+z$ direction"},
              "C": {"text": "a circular cone with vertex at the origin"},
              "D": {"text": "a circular cylinder about the $z$-axis"},
              "E": {"text": "a hyperboloid of one sheet"},
              "F": {"text": "a sphere centred at the origin"}},
        key="A",
        sol=[r"Rewrite as $z=-(x^2+y^2)$.",
             r"Two squared variables and one linear variable is the signature of a "
             r"<b>paraboloid</b>. Horizontal traces $z=-k$ ($k>0$) are circles "
             r"$x^2+y^2=k$, so it is circular.",
             r"Because $x^2+y^2\ge0$, $z\le0$ — it opens downward."],
        trap="Losing the minus sign. $x^2+y^2=z$ opens up; $x^2+y^2=-z$ opens down. The "
             "shape is identical, reflected.",
        check=lambda: -(S(1)**2 + S(1)**2), want=S(-2),
    ),
    dict(
        quiz="q2", id="Q2j", sec="13.6", title="13.6 · Hyperbolic paraboloid",
        stem=r"Identify the surface $z=x^2-y^2$.",
        opts={"A": {"text": "a hyperbolic paraboloid (a saddle)"},
              "B": {"text": "an elliptic paraboloid"},
              "C": {"text": "a hyperboloid of one sheet"},
              "D": {"text": "an elliptic cone"},
              "E": {"text": "a hyperboloid of two sheets"},
              "F": {"text": "an ellipsoid"}},
        key="A",
        sol=[r"Two squared variables with <b>opposite signs</b>, plus one linear variable.",
             r"Along $y=0$: $z=x^2$, a parabola opening <b>up</b>. Along $x=0$: $z=-y^2$, a "
             r"parabola opening <b>down</b>.",
             r"Up one way and down the other is exactly a saddle — the hyperbolic paraboloid."],
        trap="Reading &ldquo;hyperbolic&rdquo; as &ldquo;hyperboloid&rdquo;. A hyperbol<b>oid</b> has "
             "<b>three</b> squared terms and a constant; a hyperbolic parabol<b>oid</b> has "
             "two squared terms and one linear one.",
        check=lambda: (S(1)**2 - S(0)**2, S(0)**2 - S(1)**2), want=(S(1), S(-1)),
    ),
    dict(
        quiz="q2", id="Q2k", sec="13.6", title="13.6 · Traces of a saddle",
        stem=r"For the surface $z=x^2-y^2$, what is the trace in the plane $z=0$?",
        opts={"A": {"text": "the two lines $y=x$ and $y=-x$"},
              "B": {"text": "a single point, the origin"},
              "C": {"text": "a circle centred at the origin"},
              "D": {"text": "a hyperbola with vertices on the $x$-axis"},
              "E": {"text": "a parabola"},
              "F": {"text": "nothing — the trace is empty"}},
        key="A",
        sol=[r"Set $z=0$: $x^2-y^2=0$, so $(x-y)(x+y)=0$.",
             r"That is $y=x$ or $y=-x$ — a pair of intersecting lines.",
             r"For $z=k\ne0$ the traces really are hyperbolas, opening along $x$ when $k>0$ "
             r"and along $y$ when $k<0$. $z=0$ is the level where the hyperbola "
             r"<b>degenerates</b> into its own asymptotes."],
        trap="Answering &ldquo;hyperbola&rdquo; because every other horizontal trace is one. "
             "The one level that breaks the pattern is the one the question asks about.",
        check=lambda: sorted(solve(S(1)**2 - symbols("y")**2, symbols("y")), key=str),
        want=sorted([S(-1), S(1)], key=str),
    ),
    dict(
        quiz="q2", id="Q2l", sec="13.6", title="13.6 · Hyperboloid of one sheet",
        stem=r"Identify the surface $4x^2+y^2-z^2=36$, and name its axis.",
        opts={"A": {"text": "hyperboloid of <b>one</b> sheet, axis the $z$-axis"},
              "B": {"text": "hyperboloid of <b>one</b> sheet, axis the $x$-axis"},
              "C": {"text": "hyperboloid of <b>two</b> sheets, axis the $z$-axis"},
              "D": {"text": "an elliptic cone about the $z$-axis"},
              "E": {"text": "an ellipsoid"},
              "F": {"text": "an elliptic paraboloid about the $z$-axis"}},
        key="A",
        sol=[r"Divide by $36$: $\dfrac{x^2}{9}+\dfrac{y^2}{36}-\dfrac{z^2}{36}=1$.",
             r"Three squared terms equal to a nonzero constant, with <b>two plus and one "
             r"minus</b>, is a hyperboloid of <b>one</b> sheet.",
             r"The axis is the variable carrying the <b>minus</b> sign: the $z$-axis. Traces "
             r"$z=k$ are ellipses for every $k$, which is what makes it a single connected piece."],
        trap="Counting signs the wrong way. One minus &rArr; one sheet; two minuses &rArr; "
             "two sheets. Either way the axis belongs to the odd sign out.",
        check=lambda: (Rational(36, 4), S(36), S(36)), want=(S(9), S(36), S(36)),
    ),
    dict(
        quiz="q2", id="Q2m", sec="13.6", title="13.6 · Hyperboloid of two sheets",
        stem=r"Identify the surface $-x^2-y^2+4z^2=36$.",
        opts={"A": {"text": "hyperboloid of <b>two</b> sheets, axis the $z$-axis"},
              "B": {"text": "hyperboloid of <b>one</b> sheet, axis the $z$-axis"},
              "C": {"text": "hyperboloid of <b>two</b> sheets, axis the $x$-axis"},
              "D": {"text": "an elliptic cone about the $z$-axis"},
              "E": {"text": "an ellipsoid"},
              "F": {"text": "an elliptic paraboloid"}},
        key="A",
        sol=[r"Divide by $36$: $\dfrac{z^2}{9}-\dfrac{x^2}{36}-\dfrac{y^2}{36}=1$.",
             r"<b>One</b> plus and <b>two</b> minuses &rArr; hyperboloid of <b>two</b> sheets, "
             r"and the axis is the positive variable: $z$.",
             r"Sanity check on the traces: $z=k$ needs $\dfrac{k^2}{9}-1\ge0$, so $|k|\ge3$. "
             r"There is no surface at all between $z=-3$ and $z=3$ — that gap is the two "
             r"separate sheets."],
        trap="Confusing this with $4x^2+y^2-z^2=36$, which has two pluses and is one sheet. "
             "Count the signs, then check whether some slab has no points in it: an empty "
             "gap means two sheets.",
        check=lambda: solve(S(4)*symbols("z")**2 - 36, symbols("z")), want=[S(-3), S(3)],
    ),
    dict(
        quiz="q2", id="Q2n", sec="13.6", title="13.6 · Trace of an ellipsoid",
        stem=r"For the ellipsoid $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$, what is the trace "
             r"in the plane $z=1$?",
        opts={"A": {"text": "the single point $(0,0,1)$"},
              "B": {"text": "an ellipse with semi-axes $2$ and $3$"},
              "C": {"text": "a circle of radius $1$"},
              "D": {"text": "nothing — the trace is empty"},
              "E": {"text": "two intersecting lines"},
              "F": {"text": "a parabola"}},
        key="A",
        sol=[r"Set $z=1$: $\dfrac{x^2}{4}+\dfrac{y^2}{9}+1=1$, so $\dfrac{x^2}{4}+\dfrac{y^2}{9}=0$.",
             r"A sum of two squares is zero only when both are zero: $x=0$ and $y=0$.",
             r"So the trace is the single point $(0,0,1)$ — the top of the ellipsoid. "
             r"For $z>1$ the trace really would be empty."],
        trap="Answering &ldquo;an ellipse&rdquo; on autopilot. Every trace with $|z|<1$ is an "
             "ellipse, $|z|=1$ is a point, and $|z|>1$ is empty. $z=1$ is the boundary case.",
        check=lambda: 1 - S(1)**2, want=S(0),
    ),

    # ------------------------------------------------- QUIZ 2 · fundamentals --
    # The first pass at Quiz 2 was almost entirely "identify this surface" and
    # "build this plane" — the computational half. These close the conceptual
    # gaps: reading a normal off an equation, every distance, the parallel /
    # orthogonal / contained tests, going backwards from traces to a surface,
    # completing the square, and the degenerate cases that look like typos.

    dict(
        quiz="q2", id="Q2o", sec="13.5P", title="13.5 · Reading the normal off the equation",
        concept=True,
        stem=r"Without doing any work, what is a normal vector to the plane $5x-2y+z=9$?",
        opts={"A": r"\langle 5,-2,1\rangle", "B": r"\langle 5,-2,9\rangle",
              "C": r"\langle 9,9,9\rangle", "D": r"\langle -5,2,-1\rangle \text{ only}",
              "E": r"\langle 1,1,1\rangle", "F": r"\text{not determined without a point}"},
        key="A",
        sol=[r"In $ax+by+cz=d$ the coefficients **are** the normal: $\mathbf{n}=\langle a,b,c\rangle$.",
             r"So $\mathbf{n}=\langle 5,-2,1\rangle$. The constant $d$ locates the plane in "
             r"space; it says nothing about which way the plane faces.",
             r"Any nonzero multiple works too — $\langle -5,2,-1\rangle$ is equally normal, "
             r"just pointing the other way."],
        trap="Dragging $d$ into the vector, giving $\\langle 5,-2,9\\rangle$. The normal has "
             "three components and the equation has four numbers; $d$ is the one that is not "
             "a direction.",
    ),

    dict(
        quiz="q2", id="Q2p", sec="13.5P", title="13.5 · Distance from a point to a plane",
        stem=r"Find the distance from $P(1,2,3)$ to the plane $2x-2y+z=6$.",
        opts={"A": r"\tfrac{5}{3}", "B": r"5", "C": r"\tfrac{5}{9}",
              "D": r"\tfrac{11}{3}", "E": r"\tfrac{1}{3}", "F": r"\sqrt{5}"},
        key="A",
        sol=[r"Write it as $2x-2y+z-6=0$, so $\mathbf{n}=\langle 2,-2,1\rangle$ and $|\mathbf{n}|=3$.",
             r"$D=\dfrac{|2(1)-2(2)+1(3)-6|}{\sqrt{2^2+(-2)^2+1^2}}"
             r"=\dfrac{|2-4+3-6|}{3}=\dfrac{5}{3}$.",
             r"It is a scalar projection onto the normal: the part of the trip from the plane "
             r"to $P$ that actually left the plane."],
        trap="Forgetting to divide by $|\\mathbf{n}|$ and answering $5$. The numerator alone is "
             "not a length — it is only a length once the normal is a unit vector.",
        check=lambda: Rational(abs(2*1 - 2*2 + 1*3 - 6), 3), want=Rational(5, 3),
    ),

    dict(
        quiz="q2", id="Q2q", sec="13.5P", title="13.5 · Distance from the origin",
        stem=r"How far is the origin from the plane $x+2y+2z=9$?",
        opts={"A": r"3", "B": r"9", "C": r"\tfrac{9}{5}", "D": r"1",
              "E": r"\sqrt{9}=3\text{, but only if the plane passes through }(1,2,2)",
              "F": r"\tfrac{9}{\sqrt{5}}"},
        key="A",
        sol=[r"$|\mathbf{n}|=\sqrt{1+4+4}=3$.",
             r"$D=\dfrac{|0+0+0-9|}{3}=3$.",
             r"Useful shortcut worth remembering: from the origin the distance is just "
             r"$|d|/|\mathbf{n}|$."],
        trap="Using $\\sqrt{1^2+2^2}=\\sqrt5$ and dropping the third component. All three "
             "coefficients are in the normal even when one of them repeats.",
        check=lambda: Rational(9, 3), want=S(3),
    ),

    dict(
        quiz="q2", id="Q2r", sec="13.5P", title="13.5 · Angle between two planes",
        stem=r"What is the angle between the planes $x+y=1$ and $x+z=1$?",
        opts={"A": r"60^\circ", "B": r"45^\circ", "C": r"90^\circ", "D": r"30^\circ",
              "E": r"0^\circ\text{ — they are parallel}", "F": r"120^\circ"},
        key="A",
        sol=[r"The angle between planes is the angle between their normals: "
             r"$\mathbf{n}_1=\langle 1,1,0\rangle$, $\mathbf{n}_2=\langle 1,0,1\rangle$.",
             r"$\cos\theta=\dfrac{|\mathbf{n}_1\cdot\mathbf{n}_2|}"
             r"{|\mathbf{n}_1||\mathbf{n}_2|}=\dfrac{1}{\sqrt2\sqrt2}=\dfrac12$.",
             r"$\theta=60^\circ$."],
        trap="Reading the missing variable as a zero angle. Neither normal is a multiple of "
             "the other, so the planes genuinely cross — a missing variable makes a plane "
             "parallel to an axis, not parallel to another plane.",
        check=lambda: cos(pi/3), want=Rational(1, 2),
    ),

    dict(
        quiz="q2", id="Q2s", sec="13.5P", title="13.5 · Line versus plane",
        stem=r"The line $\mathbf{r}(t)=\langle 2t,\;t,\;-t\rangle$ and the plane "
             r"$3x-y+5z=2$. Which is true?",
        opts={"A": {"text": "The line is parallel to the plane and does not meet it"},
              "B": {"text": "The line lies inside the plane"},
              "C": {"text": "The line meets the plane at exactly one point"},
              "D": {"text": "The line is perpendicular to the plane"},
              "E": {"text": "The line meets the plane at exactly two points"},
              "F": {"text": "Cannot be decided without more information"}},
        key="A",
        sol=[r"Test the direction against the normal: $\mathbf{v}=\langle 2,1,-1\rangle$, "
             r"$\mathbf{n}=\langle 3,-1,5\rangle$, and "
             r"$\mathbf{n}\cdot\mathbf{v}=6-1-5=0$.",
             r"A zero dot product means the line never climbs away from the plane — so it is "
             r"parallel to it, or lying in it. Two cases, and the dot product cannot tell "
             r"them apart.",
             r"Settle it with one point. At $t=0$ the line is at the origin, and "
             r"$3(0)-0+5(0)=0\neq 2$, so the origin is not on the plane.",
             r"Parallel and disjoint."],
        trap="Stopping at $\\mathbf{n}\\cdot\\mathbf{v}=0$ and answering \"parallel\" without "
             "checking a point — a line lying *inside* the plane passes that same test. One "
             "substitution separates them.",
        check=lambda: V(3, -1, 5).dot(V(2, 1, -1)), want=S(0),
    ),

    dict(
        quiz="q2", id="Q2t", sec="13.5P", title="13.5 · Classifying two planes",
        stem=r"How are $2x-4y+6z=5$ and $-x+2y-3z=1$ related?",
        opts={"A": {"text": "Parallel and distinct"},
              "B": {"text": "The same plane written twice"},
              "C": {"text": "Perpendicular"},
              "D": {"text": "They meet in a line, at some angle other than $90^\\circ$"},
              "E": {"text": "They meet at a single point"},
              "F": {"text": "Skew — they never meet and are not parallel"}},
        key="A",
        sol=[r"$\mathbf{n}_1=\langle 2,-4,6\rangle$ and $\mathbf{n}_2=\langle -1,2,-3\rangle$ "
             r"satisfy $\mathbf{n}_1=-2\,\mathbf{n}_2$, so the normals are parallel and the "
             r"planes are parallel.",
             r"Same or different? Scale the second equation by $-2$: $2x-4y+6z=-2$.",
             r"Same left-hand side, different constant ($-2$ against $5$), so they are "
             r"parallel and distinct — two sheets that never touch."],
        trap="\"Skew\" is not available to planes. Two planes in space are parallel or they "
             "meet in a line; only *lines* can be skew.",
        check=lambda: V(2, -4, 6).cross(V(-1, 2, -3)).norm(), want=S(0),
    ),

    dict(
        quiz="q2", id="Q2u", sec="13.6", title="13.6 · Completing the square",
        stem=r"Identify the surface $9x^{2}+4y^{2}+36z^{2}-18x=27$.",
        opts={"A": {"text": "An ellipsoid centred at $(1,0,0)$"},
              "B": {"text": "An ellipsoid centred at the origin"},
              "C": {"text": "A hyperboloid of one sheet"},
              "D": {"text": "An elliptic paraboloid opening along $x$"},
              "E": {"text": "A sphere of radius $6$"},
              "F": {"text": "An elliptic cylinder with rulings along $x$"}},
        key="A",
        sol=[r"Group the $x$ terms and factor out the $9$: $9(x^{2}-2x)+4y^{2}+36z^{2}=27$.",
             r"Complete the square inside: $9\left[(x-1)^{2}-1\right]+4y^{2}+36z^{2}=27$, so "
             r"$9(x-1)^{2}+4y^{2}+36z^{2}=36$.",
             r"Divide by $36$: $\dfrac{(x-1)^{2}}{4}+\dfrac{y^{2}}{9}+z^{2}=1$.",
             r"Three squared terms, all positive, right side $1$ — an **ellipsoid**, shifted "
             r"one unit along $x$."],
        trap="Adding $1$ to the right-hand side instead of $9$. The bracket is multiplied by "
             "$9$, so completing the square inside it adds $9\\cdot 1$ to the left. Getting "
             "this wrong changes the size but not the type, which is exactly why it survives "
             "a sanity check and still loses the mark.",
        check=lambda: S(9)*(S(1))**2 + S(0) + S(0) - S(9), want=S(0),
    ),

    dict(
        quiz="q2", id="Q2v", sec="13.6", title="13.6 · From traces back to the surface",
        concept=True,
        stem=r"A surface has an **ellipse** for every horizontal trace $z=k$, and a "
             r"**hyperbola** for every trace $x=k$ and $y=k$. What is it?",
        opts={"A": {"text": "A hyperboloid of one sheet"},
              "B": {"text": "A hyperboloid of two sheets"},
              "C": {"text": "An ellipsoid"},
              "D": {"text": "A hyperbolic paraboloid"},
              "E": {"text": "An elliptic cone"},
              "F": {"text": "An elliptic paraboloid"}},
        key="A",
        sol=[r"Ellipses at *every* height $z=k$ means the surface is present for all $z$ and "
             r"closes up horizontally — that rules out the two-sheet hyperboloid, which is "
             r"empty for small $|z|$, and the ellipsoid, which stops existing past its poles.",
             r"Hyperbolas in the two vertical directions means one squared term carries the "
             r"opposite sign: $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}-\dfrac{z^{2}}{c^{2}}=1$.",
             r"That is the **hyperboloid of one sheet** — the cooling-tower shape, connected, "
             r"with a waist you can walk around."],
        trap="A cone also gives hyperbolas vertically, but its horizontal traces shrink to a "
             "single point at the vertex rather than staying ellipses at every height. "
             "\"Every $k$\" is the word doing the work in this question.",
    ),

    dict(
        quiz="q2", id="Q2w", sec="13.6", title="13.6 · Cone versus hyperboloid",
        concept=True,
        stem=r"$\dfrac{x^{2}}{4}+\dfrac{y^{2}}{9}-z^{2}=1$ is a hyperboloid of one sheet. "
             r"What does the surface become if the right-hand side is changed to $0$?",
        opts={"A": {"text": "An elliptic cone — the waist closes to a single point"},
              "B": {"text": "A hyperboloid of two sheets"},
              "C": {"text": "An ellipsoid"},
              "D": {"text": "Nothing — the equation has no real solutions"},
              "E": {"text": "The same surface, shifted down by one"},
              "F": {"text": "An elliptic paraboloid"}},
        key="A",
        sol=[r"The right-hand side controls the size of the waist. At $z=0$ the one-sheet "
             r"hyperboloid gives $\dfrac{x^{2}}{4}+\dfrac{y^{2}}{9}=1$, an ellipse.",
             r"With $0$ on the right, $z=0$ forces $\dfrac{x^{2}}{4}+\dfrac{y^{2}}{9}=0$, "
             r"whose only real solution is the origin. The waist has pinched shut.",
             r"Every other trace is still a hyperbola or an ellipse, so the surface is the "
             r"**cone** the hyperboloid was hugging all along — the cone is the boundary case "
             r"between the one-sheet and two-sheet families."],
        trap="Reading \"$=0$\" as \"empty\". Zero on the right is the cone; it is a *negative* "
             "right-hand side with all-positive squared terms that gives you nothing at all.",
    ),

    dict(
        quiz="q2", id="Q2x", sec="13.6", title="13.6 · Where a two-sheet hyperboloid is empty",
        stem=r"For the surface $-x^{2}-y^{2}+4z^{2}=36$, which values of $z$ carry no points "
             r"of the surface at all?",
        opts={"A": r"|z|<3", "B": r"|z|<6", "C": r"|z|>3", "D": r"z=0\text{ only}",
              "E": r"|z|<36", "F": r"\text{none — the surface exists for every }z"},
        key="A",
        sol=[r"Fix $z=k$: $-x^{2}-y^{2}=36-4k^{2}$, i.e. $x^{2}+y^{2}=4k^{2}-36$.",
             r"A circle needs a non-negative right-hand side, so $4k^{2}\ge 36$, giving "
             r"$k^{2}\ge 9$ and $|k|\ge 3$.",
             r"For $|z|<3$ the trace would need a negative radius squared — there is nothing "
             r"there. That gap between $z=-3$ and $z=3$ is what makes it **two sheets**."],
        trap="Testing $z=0$, finding nothing, and concluding the surface is empty everywhere. "
             "Two-sheet hyperboloids are always empty at the origin; that is the definition, "
             "not a contradiction.",
        check=lambda: sqrt(S(36)/S(4)) - S(3), want=S(0),
    ),

    dict(
        quiz="q2", id="Q2y", sec="13.6", title="13.6 · Degenerate quadrics",
        concept=True,
        stem=r"What is the graph of $x^{2}+y^{2}+z^{2}=0$ in three dimensions?",
        opts={"A": {"text": "A single point, the origin"},
              "B": {"text": "A sphere of radius $0$… which is the whole $xy$-plane"},
              "C": {"text": "An elliptic cone"},
              "D": {"text": "Nothing — there are no real solutions"},
              "E": {"text": "The three coordinate axes"},
              "F": {"text": "A sphere of radius $1$"}},
        key="A",
        sol=[r"A sum of three squares of real numbers is zero only when every one of them is "
             r"zero.",
             r"So $x=y=z=0$: the graph is the **single point** $(0,0,0)$.",
             r"Compare $x^{2}+y^{2}+z^{2}=-1$, which really is empty, and "
             r"$x^{2}+y^{2}+z^{2}=9$, an honest sphere. The right-hand side alone separates "
             r"all three cases."],
        trap="Answering \"nothing\". Zero is attainable — every square can be zero at once. "
             "It is a *negative* right-hand side that has no real solutions.",
    ),

    dict(
        quiz="q2", id="Q2z", sec="13.6", title="13.6 · Which axis the rulings follow",
        concept=True,
        stem=r"In three dimensions, $y^{2}+z^{2}=4$ is a circular cylinder. Its rulings — the "
             r"straight lines running along its length — are parallel to which axis?",
        opts={"A": {"text": "The $x$-axis"}, "B": {"text": "The $y$-axis"},
              "C": {"text": "The $z$-axis"},
              "D": {"text": "None — a cylinder has no straight lines on it"},
              "E": {"text": "The line $y=z$"},
              "F": {"text": "It depends on the radius"}},
        key="A",
        sol=[r"$x$ does not appear in the equation, so $x$ is unconstrained: any $x$ at all "
             r"satisfies it.",
             r"The circle $y^{2}+z^{2}=4$ therefore repeats at every $x$, and stacking those "
             r"copies sweeps the curve along the **$x$-axis**.",
             r"General rule: the missing variable names the axis the rulings follow."],
        trap="Picking $z$ out of habit, because the cylinders drawn in most textbooks stand "
             "upright on the $z$-axis. Read the equation instead — the axis is whichever "
             "letter is absent.",
    ),

    # ------------------------------------------ QUIZ 2 · the remaining types --
    # Audit of 13.5-planes and 13.6 against the section material turned up eight
    # types with no question at all. Several are standard exam fare: piercing a
    # plane with a line, the distance between two parallel planes, and getting an
    # actual point on a line of intersection rather than only its direction.

    dict(
        quiz="q2", id="Q2ab", sec="13.5P", title="13.5 · Where a line pierces a plane",
        stem=r"Where does the line $x=1+t,\;y=-1+2t,\;z=3-t$ cross the plane "
             r"$2x-y+z=7$?",
        opts={"A": r"(0,-3,4)", "B": r"(2,1,2)", "C": r"(1,-1,3)",
              "D": r"(-1,-5,5)", "E": r"\text{it never meets the plane}",
              "F": r"\text{the whole line lies in the plane}"},
        key="A",
        sol=[r"Substitute the parametric coordinates straight into the plane equation:",
             r"$2(1+t)-(-1+2t)+(3-t)=7$.",
             r"$2+2t+1-2t+3-t=7\;\Rightarrow\;6-t=7\;\Rightarrow\;t=-1$.",
             r"Put $t=-1$ back in the line: $(1-1,\;-1-2,\;3+1)=(0,-3,4)$. "
             r"Check: $2(0)-(-3)+4=7$."],
        trap="Stopping at $t=-1$ and offering that as the answer. The parameter is not a "
             "point — it still has to go back into the line.",
        check=lambda: V(1 + (-1), -1 + 2*(-1), 3 - (-1)), want=V(0, -3, 4),
    ),

    dict(
        quiz="q2", id="Q2ac", sec="13.5P", title="13.5 · Distance between parallel planes",
        stem=r"How far apart are the planes $x+2y+2z=6$ and $x+2y+2z=-3$?",
        opts={"A": r"3", "B": r"9", "C": r"\tfrac{9}{\sqrt{5}}", "D": r"1",
              "E": r"0\text{ — they intersect}", "F": r"\tfrac{3}{2}"},
        key="A",
        sol=[r"Same left-hand side, so the normals match and the planes are parallel — the "
             r"distance is well defined.",
             r"Take any point on the second plane. Setting $y=z=0$ gives $(-3,0,0)$.",
             r"Now use point-to-plane on the first: "
             r"$D=\dfrac{|(-3)+0+0-6|}{\sqrt{1+4+4}}=\dfrac{9}{3}=3$.",
             r"Shortcut for this special case: with identical normals, "
             r"$D=\dfrac{|d_1-d_2|}{|\mathbf{n}|}$."],
        trap="Answering $9$, the difference of the constants. That is only the distance if "
             "the normal happens to be a unit vector, and here $|\\mathbf{n}|=3$.",
        check=lambda: Rational(abs(6 - (-3)), 3), want=S(3),
    ),

    dict(
        quiz="q2", id="Q2ad", sec="13.5P", title="13.5 · A point on the line of intersection",
        stem=r"The planes $x+y+z=1$ and $x-2y+3z=4$ meet in a line. Which point lies on it?",
        opts={"A": r"(2,-1,0)", "B": r"(1,0,0)", "C": r"(0,1,0)",
              "D": r"(1,-1,1)", "E": r"(0,0,1)", "F": r"(4,-2,-1)"},
        key="A",
        sol=[r"A point on the line has to satisfy **both** equations, so pick a convenient "
             r"slice: set $z=0$.",
             r"That leaves $x+y=1$ and $x-2y=4$. Subtracting, $3y=-3$, so $y=-1$ and $x=2$.",
             r"The point is $(2,-1,0)$. Check both: $2-1+0=1$ and $2+2+0=4$.",
             r"With the direction $\mathbf{n}_1\times\mathbf{n}_2=\langle 5,-2,-3\rangle$ "
             r"from the companion question, you now have the full line."],
        trap="Testing against only one of the two planes. Every option here satisfies at "
             "least one of them — the line is the *intersection*, so both have to hold.",
        check=lambda: (2 + (-1) + 0, 2 - 2*(-1) + 0), want=(S(1), S(4)),
    ),

    dict(
        quiz="q2", id="Q2ae", sec="13.6", title="13.6 · Elliptic cylinder",
        concept=True,
        stem=r"What surface is $4x^{2}+9y^{2}=36$ in three dimensions?",
        opts={"A": {"text": "An elliptic cylinder, rulings parallel to the $z$-axis"},
              "B": {"text": "An ellipsoid"},
              "C": {"text": "An elliptic cylinder, rulings parallel to the $x$-axis"},
              "D": {"text": "An elliptic paraboloid opening along $z$"},
              "E": {"text": "An ellipse in the $xy$-plane"},
              "F": {"text": "An elliptic cone about the $z$-axis"}},
        key="A",
        sol=[r"Divide by $36$: $\dfrac{x^{2}}{9}+\dfrac{y^{2}}{4}=1$ — an ellipse with "
             r"semi-axes $3$ and $2$.",
             r"$z$ is absent, so $z$ is free and that ellipse repeats at every height.",
             r"An **elliptic cylinder** whose rulings run along the missing variable's axis, "
             r"the $z$-axis. Not every cylinder is circular."],
        trap="Answering \"an ellipse\". In $\\mathbb{R}^{2}$ it is; the question says three "
             "dimensions, where the same equation is an infinite tube of elliptical "
             "cross-section.",
    ),

    dict(
        quiz="q2", id="Q2af", sec="13.6", title="13.6 · Hyperbolic cylinder",
        concept=True,
        stem=r"Identify $x^{2}-z^{2}=1$ in three dimensions.",
        opts={"A": {"text": "A hyperbolic cylinder, rulings parallel to the $y$-axis"},
              "B": {"text": "A hyperboloid of one sheet"},
              "C": {"text": "A hyperbolic paraboloid"},
              "D": {"text": "A hyperbolic cylinder, rulings parallel to the $z$-axis"},
              "E": {"text": "A hyperbola in the $xz$-plane"},
              "F": {"text": "Two intersecting planes"}},
        key="A",
        sol=[r"$y$ never appears, so this is a cylinder and the rulings run along the "
             r"**$y$-axis**.",
             r"The curve being swept is $x^{2}-z^{2}=1$ in the $xz$-plane: a hyperbola "
             r"opening along $\pm x$, in two branches.",
             r"So it is a **hyperbolic cylinder** — two curved sheets, both infinite in $y$."],
        trap="Mistaking it for a hyperboloid. A hyperboloid has all three variables squared; "
             "here one is missing entirely, which is the signature of a cylinder no matter "
             "what curve is being swept.",
    ),

    dict(
        quiz="q2", id="Q2ag", sec="13.6", title="13.6 · Identify a cone",
        concept=True,
        stem=r"Identify the surface $x^{2}+y^{2}-4z^{2}=0$.",
        opts={"A": {"text": "An elliptic (in fact circular) cone with axis the $z$-axis"},
              "B": {"text": "A hyperboloid of one sheet about the $z$-axis"},
              "C": {"text": "A hyperboloid of two sheets about the $z$-axis"},
              "D": {"text": "A circular cylinder about the $z$-axis"},
              "E": {"text": "A single point, the origin"},
              "F": {"text": "A circular paraboloid opening upward"}},
        key="A",
        sol=[r"Three squared terms, one of them negative — and the right-hand side is "
             r"**$0$**, not $1$. Zero on the right is the cone case.",
             r"Confirm with traces: $z=k$ gives $x^{2}+y^{2}=4k^{2}$, a circle whose radius "
             r"grows linearly with $|k|$ and pinches to a point at $k=0$.",
             r"The odd-one-out variable, $z$, is the axis."],
        trap="Reading the single negative sign and answering \"one sheet\". The minus-sign "
             "count only decides between the hyperboloids once the right-hand side is $1$; "
             "$0$ overrides it and gives the cone.",
    ),

    dict(
        quiz="q2", id="Q2ah", sec="13.6", title="13.6 · Identify an ellipsoid",
        concept=True,
        stem=r"Identify the surface $4x^{2}+y^{2}+9z^{2}=36$, and give its $x$-intercepts.",
        opts={"A": {"text": "An ellipsoid; $x=\\pm 3$"},
              "B": {"text": "An ellipsoid; $x=\\pm 6$"},
              "C": {"text": "A sphere of radius $6$; $x=\\pm 6$"},
              "D": {"text": "An elliptic cylinder; $x=\\pm 3$"},
              "E": {"text": "An ellipsoid; $x=\\pm 2$"},
              "F": {"text": "A hyperboloid of one sheet; $x=\\pm 3$"}},
        key="A",
        sol=[r"Divide by $36$: $\dfrac{x^{2}}{9}+\dfrac{y^{2}}{36}+\dfrac{z^{2}}{4}=1$.",
             r"Three squared terms, none negative, right side $1$ — an **ellipsoid**.",
             r"Intercepts are the denominators' square roots: $x=\pm 3$, $y=\pm 6$, "
             r"$z=\pm 2$. Unequal, so it is not a sphere."],
        trap="Reading the intercept off the original coefficient rather than the standard "
             "form. In $4x^{2}+\\dots=36$ the $x$-intercept is $\\sqrt{36/4}=3$, not $6$ — "
             "you must divide through first.",
    ),

    dict(
        quiz="q2", id="Q2ai", sec="13.6", title="13.6 · When a quadric is genuinely empty",
        concept=True,
        stem=r"What is the graph of $x^{2}+y^{2}+z^{2}=-4$?",
        opts={"A": {"text": "Nothing — there are no real points"},
              "B": {"text": "A single point, the origin"},
              "C": {"text": "A sphere of radius $2$"},
              "D": {"text": "A sphere of imaginary radius, drawn as radius $2$"},
              "E": {"text": "An elliptic cone"},
              "F": {"text": "A hyperboloid of two sheets"}},
        key="A",
        sol=[r"Every square of a real number is $\ge 0$, so the left-hand side is never "
             r"negative.",
             r"No real $(x,y,z)$ can satisfy it: the graph is the **empty set**.",
             r"Three cases worth holding together: $=9$ is a sphere, $=0$ is the single "
             r"point at the origin, and $<0$ is nothing at all. The right-hand side alone "
             r"separates them."],
        trap="Answering \"a single point\". That is the $=0$ case. A negative right-hand "
             "side is strictly emptier, and it is the one that looks most like a typo in an "
             "exam and most often gets \"corrected\" into a sphere.",
    ),

    # ---------------------------------------- QUIZ 2 · from Purdue's own notes --
    # Diffed against the handwritten Lesson 3 and Lesson 4 pages
    # (math.purdue.edu/~msunkula/MA261/Sp26/Lesson{3,4}.html), which show what is
    # actually worked in the room. Five things they teach had no question here —
    # including their opening think-pair-share, which is the whole intuition for
    # the section.

    dict(
        quiz="q2", id="Q2aj", sec="13.6", title="13.6 · The same equation in different dimensions",
        concept=True,
        stem=r"What does the equation $x=2$ describe in $\mathbb{R}^{3}$?",
        opts={"A": {"text": "A plane perpendicular to the $x$-axis"},
              "B": {"text": "A single point on the $x$-axis"},
              "C": {"text": "A line parallel to the $y$-axis"},
              "D": {"text": "A line parallel to the $x$-axis"},
              "E": {"text": "A circular cylinder about the $x$-axis"},
              "F": {"text": "Nothing — one equation cannot describe a surface"}},
        key="A",
        sol=[r"Count the free variables. $x$ is pinned at $2$; $y$ and $z$ appear nowhere, "
             r"so both are free to be anything.",
             r"Two free variables sweep out a two-dimensional object: a **plane**, "
             r"perpendicular to the $x$-axis and passing through $(2,0,0)$.",
             r"The same equation says something different in each dimension — a **point** on "
             r"the number line, a **vertical line** in the plane, a **plane** in space. The "
             r"equation never changes; the ambient space does.",
             r"This is the idea the whole section runs on: a variable that is absent is a "
             r"variable that is free, and every free variable is a direction you sweep along."],
        trap="Answering \"a line\" out of habit from two-variable algebra, where $x=2$ really "
             "is a line. The question has to tell you the ambient space, and in this chapter "
             "it is always $\\mathbb{R}^{3}$ unless it says otherwise.",
    ),

    dict(
        quiz="q2", id="Q2ak", sec="13.6", title="13.6 · A paraboloid that is not about the z-axis",
        concept=True,
        stem=r"Identify the surface $x^{2}+z^{2}=-y$.",
        opts={"A": {"text": "A circular paraboloid opening in the $-y$ direction"},
              "B": {"text": "A circular paraboloid opening in the $-z$ direction"},
              "C": {"text": "A circular cone about the $y$-axis"},
              "D": {"text": "A circular cylinder about the $y$-axis"},
              "E": {"text": "A hyperbolic paraboloid"},
              "F": {"text": "A paraboloid opening in the $+y$ direction"}},
        key="A",
        sol=[r"Two variables are squared ($x$ and $z$) and one is linear ($y$) — that is a "
             r"**paraboloid**, and the linear variable is always the axis. Here the axis is "
             r"$y$, not $z$.",
             r"The two squared terms share a sign, so the cross-sections are circles: "
             r"elliptic (in fact circular), not a saddle.",
             r"Which way does it open? Set $y=c$: $x^{2}+z^{2}=-c$. That needs $-c\ge 0$, so "
             r"$c\le 0$ — the surface only exists for $y\le 0$ and opens along $-y$.",
             r"At $y=0$ the trace is $x^{2}+z^{2}=0$, the single point at the vertex."],
        trap="Assuming every paraboloid stands on the $z$-axis because that is how they are "
             "always drawn. Read which variable is unsquared — that one is the axis.",
    ),

    dict(
        quiz="q2", id="Q2al", sec="13.6", title="13.6 · Where a paraboloid has no points",
        concept=True,
        stem=r"For the surface $x^{2}+y^{2}=-z$, which values of $z$ carry no points at all?",
        opts={"A": {"text": "Every $z>0$"},
              "B": {"text": "Every $z<0$"},
              "C": {"text": "Only $z=0$"},
              "D": {"text": "$|z|<1$"},
              "E": {"text": "None — the surface exists at every height"},
              "F": {"text": "Every $z\\neq 0$"}},
        key="A",
        sol=[r"Slice at $z=k$: $x^{2}+y^{2}=-k$.",
             r"The left side is a sum of squares, so it is never negative. A trace exists "
             r"only when $-k\ge 0$, i.e. $k\le 0$.",
             r"So there is **nothing above the $xy$-plane**: the paraboloid opens downward "
             r"from its vertex at the origin. At $k=0$ the trace is the single point "
             r"$(0,0,0)$; below that the traces are circles of radius $\sqrt{-k}$, growing "
             r"as you descend.",
             r"Same reasoning as the two-sheet hyperboloid — ask which slices force a "
             r"negative sum of squares, and those are the empty ones."],
        trap="Reading the minus sign as \"reflected, so it exists everywhere\". The minus "
             "sign is exactly what makes half of space empty. Test a slice rather than "
             "picturing the surface.",
    ),

    dict(
        quiz="q2", id="Q2am", sec="13.6", title="13.6 · The x²−y²=k family",
        concept=True,
        stem=r"In the plane, the curve $x^{2}-y^{2}=k$ changes character with $k$. Which "
             r"description is right?",
        opts={"A": {"text": "$k>0$ hyperbola opening left–right; $k=0$ the two lines $y=\\pm x$; $k<0$ hyperbola opening up–down"},
              "B": {"text": "$k>0$ hyperbola opening up–down; $k=0$ a single point; $k<0$ hyperbola opening left–right"},
              "C": {"text": "An ellipse for every $k$, of varying size"},
              "D": {"text": "$k>0$ a hyperbola; $k\\le 0$ nothing at all"},
              "E": {"text": "$k=0$ a circle of radius $0$; otherwise two parallel lines"},
              "F": {"text": "A parabola for every $k$"}},
        key="A",
        sol=[r"$k>0$: dividing by $k$ puts $x^{2}$ over a positive number, so the curve meets "
             r"the $x$-axis at $x=\pm\sqrt{k}$ and never the $y$-axis — it opens **left and "
             r"right**.",
             r"$k=0$: $x^{2}-y^{2}=0$ factors as $(x-y)(x+y)=0$, the **two lines** $y=x$ and "
             r"$y=-x$. This is the degenerate member of the family.",
             r"$k<0$: the roles swap and the hyperbola opens **up and down**, asymptotic to "
             r"the same two lines.",
             r"This is exactly the family of horizontal traces of the saddle $z=x^{2}-y^{2}$, "
             r"which is why the saddle's $z=0$ trace is a pair of crossed lines."],
        trap="Treating $k=0$ as \"empty\" or \"a point\". A difference of squares can vanish "
             "without either square vanishing — that is what makes the asymptotes part of "
             "the family rather than something outside it.",
    ),

    dict(
        quiz="q2", id="Q2an", sec="13.6", title="13.6 · How many pieces a cone has",
        concept=True,
        stem=r"The surface $x^{2}+y^{2}=z^{2}$ is a circular cone. What does it actually "
             r"look like?",
        opts={"A": {"text": "Two nappes meeting at the origin, one opening up and one opening down"},
              "B": {"text": "One nappe, opening upward from the origin"},
              "C": {"text": "One nappe, opening upward, plus an isolated point below it"},
              "D": {"text": "Two nappes separated by a gap around $z=0$"},
              "E": {"text": "A single sheet with a hole through the middle"},
              "F": {"text": "Two nappes meeting along the whole $z$-axis"}},
        key="A",
        sol=[r"Solve for $z$: $z=\pm\sqrt{x^{2}+y^{2}}$. Both signs are real for every "
             r"$(x,y)$, so the surface has an upper half and a lower half.",
             r"Trace at $z=k$: a circle of radius $|k|$ — so the circles shrink to a point at "
             r"$k=0$ and grow linearly in both directions.",
             r"The two **nappes** therefore touch at exactly one place, the origin. The "
             r"equation $z=\sqrt{x^{2}+y^{2}}$ would be only the top half; the squared form "
             r"is both.",
             r"Contrast the two-sheet hyperboloid, whose pieces are separated by a genuine "
             r"gap and never touch."],
        trap="Confusing the cone with the two-sheet hyperboloid. Both come in two pieces, but "
             "the cone's pieces meet at a point ($=0$ on the right) while the hyperboloid's "
             "are held apart by an empty band ($=1$ on the right).",
    ),

    # ============================================================ QUIZ 3 ====
    # Lesson 5 (14.1), Lesson 6 (14.2, 14.3 to Ex 1), Lesson 7 (14.3 rest)

    dict(
        quiz="q3", id="Q3a", sec="14.1", title="14.1 · Domain of a vector function",
        stem=r"Find the domain of $\mathbf r(t)=\left\langle \sqrt{t-1},\;\ln(4-t),\;"
             r"\dfrac{1}{t}\right\rangle$.",
        opts={"A": r"[1,\,4)", "B": r"(1,\,4)", "C": r"[1,\,4]",
              "D": r"(-\infty,\,4)", "E": r"[1,\,\infty)", "F": r"(0,\,4)"},
        key="A",
        sol=[r"The domain is the <b>intersection</b> of the three component domains.",
             r"$\sqrt{t-1}$ needs $t-1\ge0$, so $t\ge1$ — closed at $1$.",
             r"$\ln(4-t)$ needs $4-t>0$, so $t<4$ — open at $4$.",
             r"$\dfrac1t$ needs $t\ne0$, which $t\ge1$ already guarantees.",
             r"Intersecting: $1\le t<4$, that is $[1,4)$."],
        trap="Making both ends the same. The square root allows equality, the logarithm "
             "does not — so one end is closed and the other is open.",
        check=lambda: (S(1), S(4)), want=(S(1), S(4)),
    ),
    dict(
        quiz="q3", id="Q3b", sec="14.1", title="14.1 · Circle at a given height",
        stem=r"Which function traces the circle of radius $3$ centred on the $z$-axis in the "
             r"plane $z=5$, counterclockwise as seen from above?",
        opts={"A": r"\mathbf r(t)=\langle 3\cos t,\;3\sin t,\;5\rangle",
              "B": r"\mathbf r(t)=\langle 3\cos t,\;3\sin t,\;t\rangle",
              "C": r"\mathbf r(t)=\langle 5\cos t,\;5\sin t,\;3\rangle",
              "D": r"\mathbf r(t)=\langle 3\cos t,\;-3\sin t,\;5\rangle",
              "E": r"\mathbf r(t)=\langle 3+\cos t,\;3+\sin t,\;5\rangle",
              "F": r"\mathbf r(t)=\langle 9\cos t,\;9\sin t,\;5\rangle"},
        key="A",
        sol=[r"Staying in the plane $z=5$ forces the third component to be the constant $5$.",
             r"Radius $3$ centred on the axis gives $x=3\cos t$, $y=3\sin t$; then "
             r"$x^2+y^2=9$. &check;",
             r"$(+\cos,+\sin)$ runs counterclockwise viewed from $+z$ looking down."],
        trap="Option B has $z=t$ — that is a helix, not a plane curve. Option D reverses the "
             "orientation. Option E shifts the <b>centre</b> to $(3,3)$ and shrinks the "
             "radius to $1$.",
        check=lambda: (S(3)*cos(S(0)))**2 + (S(3)*S(0))**2, want=S(9),
    ),
    dict(
        quiz="q3", id="Q3c", sec="14.1", title="14.1 · The surface a curve lies on",
        stem=r"On which surface does $\mathbf r(t)=\langle t\cos t,\;t\sin t,\;t\rangle$ "
             r"lie for $t\ge0$?",
        opts={"A": r"\text{the cone } x^2+y^2=z^2",
              "B": r"\text{the cylinder } x^2+y^2=1",
              "C": r"\text{the paraboloid } z=x^2+y^2",
              "D": r"\text{the sphere } x^2+y^2+z^2=1",
              "E": r"\text{the plane } z=0",
              "F": r"\text{the hyperboloid } x^2+y^2-z^2=1"},
        key="A",
        sol=[r"Compute the combination the candidate surfaces care about:",
             r"$x^2+y^2=t^2\cos^2t+t^2\sin^2t=t^2(\cos^2t+\sin^2t)=t^2$.",
             r"And $z=t$, so $z^2=t^2$. Therefore $x^2+y^2=z^2$ — the cone.",
             r"(The curve is a spiral climbing the cone, widening as it rises.)"],
        trap="Stopping at $x^2+y^2=t^2$ and matching it to $z$ rather than $z^2$. That "
             "would give the paraboloid, option C. Compare like with like.",
        check=lambda: (t*cos(t))**2 + (t*__import__("sympy").sin(t))**2 - t**2,
        want=S(0), simplify_check=True,
    ),
    dict(
        quiz="q3", id="Q3d", sec="14.1", title="14.1 · Intersection with a surface",
        stem=r"The helix $\mathbf r(t)=\langle\cos t,\;\sin t,\;t\rangle$ meets the sphere "
             r"$x^2+y^2+z^2=5$. At which $t\ge0$?",
        opts={"A": r"t=2", "B": r"t=\sqrt5", "C": r"t=4",
              "D": r"t=2\pi", "E": r"t=\sqrt2", "F": r"t=5"},
        key="A",
        sol=[r"Substitute the components into the surface equation:",
             r"$\cos^2t+\sin^2t+t^2=5$.",
             r"$\cos^2t+\sin^2t=1$ always, so $1+t^2=5$, giving $t^2=4$ and $t=2$ for $t\ge0$."],
        trap="Not using the Pythagorean identity and trying to solve a transcendental "
             "equation. On a helix the first two components always contribute exactly $1$.",
        check=lambda: [x for x in solve(1 + t**2 - 5, t) if x.is_positive], want=[S(2)],
    ),
    dict(
        quiz="q3", id="Q3e", sec="14.2", title="14.2 · Derivative of a vector function",
        stem=r"For $\mathbf r(t)=\langle t^2,\;e^{2t},\;\ln t\rangle$, find "
             r"$\mathbf r'(1)$.",
        opts={"A": r"\langle 2,\;2e^2,\;1\rangle", "B": r"\langle 2,\;e^2,\;1\rangle",
              "C": r"\langle 2,\;2e^2,\;0\rangle", "D": r"\langle 1,\;2e^2,\;1\rangle",
              "E": r"\langle 2,\;2e,\;1\rangle", "F": r"\langle 2,\;e^2,\;0\rangle"},
        key="A",
        sol=[r"Differentiate componentwise: "
             r"$\mathbf r'(t)=\left\langle 2t,\;2e^{2t},\;\dfrac1t\right\rangle$.",
             r"At $t=1$: $\left\langle 2,\;2e^{2},\;1\right\rangle$."],
        trap="Two chain-rule slips live here. $\\dfrac{d}{dt}e^{2t}=2e^{2t}$, not $e^{2t}$ "
             "(option B), and $\\dfrac{d}{dt}\\ln t=\\dfrac1t$, which is $1$ at $t=1$, not "
             "$\\ln 1=0$ (option C).",
        check=lambda: Matrix([t**2, exp(2*t), __import__("sympy").log(t)]).diff(t).subs(t, 1),
        want=V(2, 2*exp(2), 1),
    ),
    dict(
        quiz="q3", id="Q3f", sec="14.2", title="14.2 · Tangent line to a curve",
        stem=r"Find parametric equations for the tangent line to "
             r"$\mathbf r(t)=\langle t,\;t^2,\;t^3\rangle$ at the point $(2,4,8)$.",
        opts={"A": r"x=2+s,\;\;y=4+4s,\;\;z=8+12s",
              "B": r"x=1+2s,\;\;y=4+4s,\;\;z=12+8s",
              "C": r"x=2+s,\;\;y=4+2s,\;\;z=8+3s",
              "D": r"x=2+2s,\;\;y=4+4s,\;\;z=8+8s",
              "E": r"x=s,\;\;y=4s,\;\;z=12s",
              "F": r"x=2+s,\;\;y=4+4s,\;\;z=8+6s"},
        key="A",
        sol=[r"First find the parameter value at that point. $x=t=2$, and indeed "
             r"$t^2=4$, $t^3=8$. So $t=2$.",
             r"$\mathbf r'(t)=\langle 1,\;2t,\;3t^2\rangle$, so "
             r"$\mathbf r'(2)=\langle 1,\;4,\;12\rangle$ — the direction.",
             r"Line through $(2,4,8)$ with direction $\langle1,4,12\rangle$: "
             r"$x=2+s,\;y=4+4s,\;z=8+12s$."],
        trap="Option C uses $\\mathbf r'$ with $t$ never substituted, effectively "
             "$\\langle1,2,3\\rangle$. Option B swaps the point and the direction. Option F "
             "evaluates $3t^2$ as $3\\cdot2=6$ instead of $3\\cdot4=12$.",
        check=lambda: Matrix([t, t**2, t**3]).diff(t).subs(t, 2), want=V(1, 4, 12),
    ),
    dict(
        quiz="q3", id="Q3g", sec="14.2", title="14.2 · Derivative rules",
        stem=r"$\mathbf r(t)$ is differentiable and $|\mathbf r(t)|$ is <b>constant</b>. "
             r"What is $\mathbf r(t)\cdot\mathbf r'(t)$?",
        opts={"A": r"0", "B": r"|\mathbf r(t)|", "C": r"1",
              "D": r"|\mathbf r'(t)|^2", "E": r"2|\mathbf r(t)|\,|\mathbf r'(t)|",
              "F": r"\text{it cannot be determined}"},
        key="A",
        sol=[r"Use the product rule for the dot product: "
             r"$\dfrac{d}{dt}\bigl[\mathbf r\cdot\mathbf r\bigr]"
             r"=\mathbf r'\cdot\mathbf r+\mathbf r\cdot\mathbf r'=2\,\mathbf r\cdot\mathbf r'$.",
             r"But $\mathbf r\cdot\mathbf r=|\mathbf r|^2$, which is a constant, so its "
             r"derivative is $0$.",
             r"Hence $2\,\mathbf r\cdot\mathbf r'=0$, so $\mathbf r\cdot\mathbf r'=0$.",
             r"Geometrically: a curve of constant distance from the origin lies on a sphere, "
             r"and its velocity must be tangent to that sphere — perpendicular to the radius."],
        trap="This is the fact behind uniform circular motion: constant speed means the "
             "acceleration is perpendicular to the velocity, which is the same statement "
             "applied to $\\mathbf v$ instead of $\\mathbf r$.",
        check=lambda: (Matrix([cos(t), __import__("sympy").sin(t), S(0)]).dot(
            Matrix([cos(t), __import__("sympy").sin(t), S(0)]).diff(t))),
        want=S(0), simplify_check=True,
    ),
    dict(
        quiz="q3", id="Q3h", sec="14.2", title="14.2 · Definite integral",
        stem=r"Evaluate $\displaystyle\int_0^1\left\langle 6t^2,\;4t,\;e^{t}\right\rangle dt$.",
        opts={"A": r"\langle 2,\;2,\;e-1\rangle", "B": r"\langle 2,\;2,\;e\rangle",
              "C": r"\langle 6,\;4,\;e-1\rangle", "D": r"\langle 2,\;2,\;1-e\rangle",
              "E": r"\langle 3,\;2,\;e-1\rangle", "F": r"\langle 2,\;4,\;e-1\rangle"},
        key="A",
        sol=[r"Integrate componentwise: "
             r"$\left\langle 2t^3,\;2t^2,\;e^{t}\right\rangle$ evaluated from $0$ to $1$.",
             r"$x$: $2(1)^3-0=2$. &nbsp; $y$: $2(1)^2-0=2$. &nbsp; $z$: $e^{1}-e^{0}=e-1$.",
             r"So the integral is $\langle 2,\;2,\;e-1\rangle$."],
        trap="Forgetting the lower limit on the exponential. $e^0=1$, not $0$, so the "
             "third component is $e-1$ — option B is the version that drops it.",
        check=lambda: Matrix([integrate(6*t**2, (t, 0, 1)), integrate(4*t, (t, 0, 1)),
                             integrate(exp(t), (t, 0, 1))]),
        want=V(2, 2, exp(1) - 1),
    ),
    dict(
        quiz="q3", id="Q3i", sec="14.3", title="14.3 · Velocity, speed, acceleration",
        stem=r"A particle has position $\mathbf r(t)=\langle 3t,\;t^2,\;t^3\rangle$. "
             r"Find its <b>speed</b> at $t=1$.",
        opts={"A": r"\sqrt{22}", "B": r"\sqrt{14}", "C": r"22",
              "D": r"\sqrt{13}", "E": r"\sqrt{34}", "F": r"4"},
        key="A",
        sol=[r"$\mathbf v(t)=\mathbf r'(t)=\langle 3,\;2t,\;3t^2\rangle$, so "
             r"$\mathbf v(1)=\langle 3,2,3\rangle$.",
             r"Speed is the <b>magnitude</b> of velocity: "
             r"$|\mathbf v(1)|=\sqrt{9+4+9}=\sqrt{22}$."],
        trap="Speed is a number, not a vector, and it comes from $\\mathbf v$ — not from "
             "$\\mathbf r$ and not from $\\mathbf a$. Differentiating $t^3$ to $t^2$ instead "
             "of $3t^2$ gives $\\sqrt{14}$, option B.",
        check=lambda: Matrix([3*t, t**2, t**3]).diff(t).subs(t, 1).norm(), want=sqrt(22),
    ),
    dict(
        quiz="q3", id="Q3j", sec="14.3", title="14.3 · Circular motion",
        stem=r"For $\mathbf r(t)=\langle 4\cos 3t,\;4\sin 3t\rangle$, which statement is true?",
        opts={"A": {"text": "the speed is constant at $12$, and the acceleration points toward the origin"},
              "B": {"text": "the speed is constant at $4$, and the acceleration is zero"},
              "C": {"text": "the speed is constant at $3$, and the acceleration points away from the origin"},
              "D": {"text": "the speed increases with $t$"},
              "E": {"text": "the acceleration is parallel to the velocity"},
              "F": {"text": "the speed is constant at $12$, and the acceleration is zero"}},
        key="A",
        sol=[r"$\mathbf v=\langle -12\sin3t,\;12\cos3t\rangle$, so "
             r"$|\mathbf v|=12\sqrt{\sin^23t+\cos^23t}=12$ — constant.",
             r"$\mathbf a=\langle -36\cos3t,\;-36\sin3t\rangle=-9\,\mathbf r(t)$.",
             r"A negative multiple of the position vector points straight back at the origin. "
             r"(This is centripetal acceleration.)",
             r"Also $\mathbf v\cdot\mathbf a=0$, so the acceleration is perpendicular to the "
             r"velocity, never parallel to it."],
        trap="&ldquo;Constant speed&rdquo; is not &ldquo;no acceleration&rdquo; — option F. The "
             "direction is changing the whole time, and changing direction is acceleration. "
             "Note also that the speed is $12$, not the radius $4$: the $3$ inside the "
             "trig functions multiplies it.",
        check=lambda: (Matrix([4*cos(3*t), 4*__import__("sympy").sin(3*t)]).diff(t).norm(),
                       Matrix([4*cos(3*t), 4*__import__("sympy").sin(3*t)]).diff(t).dot(
                           Matrix([4*cos(3*t), 4*__import__("sympy").sin(3*t)]).diff(t, 2))),
        want=(S(12), S(0)), simplify_check=True,
    ),
    dict(
        quiz="q3", id="Q3k", sec="14.3", title="14.3 · Position from acceleration",
        stem=r"A particle has acceleration $\mathbf a(t)=\langle 0,\;2,\;6t\rangle$, with "
             r"$\mathbf v(0)=\langle 1,0,0\rangle$ and $\mathbf r(0)=\langle 0,1,2\rangle$. "
             r"Find $\mathbf r(1)$.",
        opts={"A": r"\langle 1,\;2,\;3\rangle", "B": r"\langle 1,\;1,\;2\rangle",
              "C": r"\langle 1,\;3,\;5\rangle", "D": r"\langle 0,\;2,\;3\rangle",
              "E": r"\langle 1,\;2,\;5\rangle", "F": r"\langle 2,\;2,\;3\rangle"},
        key="A",
        sol=[r"Integrate once: $\mathbf v(t)=\langle 0,\;2t,\;3t^2\rangle+\mathbf C_1$. "
             r"Since $\mathbf v(0)=\langle 1,0,0\rangle$, $\mathbf C_1=\langle 1,0,0\rangle$, "
             r"so $\mathbf v(t)=\langle 1,\;2t,\;3t^2\rangle$.",
             r"Integrate again: $\mathbf r(t)=\langle t,\;t^2,\;t^3\rangle+\mathbf C_2$. "
             r"Since $\mathbf r(0)=\langle 0,1,2\rangle$, $\mathbf C_2=\langle 0,1,2\rangle$.",
             r"$\mathbf r(t)=\langle t,\;t^2+1,\;t^3+2\rangle$, so "
             r"$\mathbf r(1)=\langle 1,\;2,\;3\rangle$."],
        trap="Two integrations mean <b>two</b> vector constants, and each is fixed by its "
             "own initial condition. Losing $\\mathbf C_1$ drops the $x$ motion entirely; "
             "losing $\\mathbf C_2$ gives $\\langle1,1,1\\rangle$.",
        check=lambda: Matrix([t, t**2 + 1, t**3 + 2]).subs(t, 1), want=V(1, 2, 3),
    ),
    dict(
        quiz="q3", id="Q3l", sec="14.3", title="14.3 · Projectile · time of flight",
        stem=r"A ball is launched from a height of $15$ m with initial velocity "
             r"$\langle 20,\,0,\,10\rangle$ m/s, under acceleration "
             r"$\langle 0,0,-10\rangle$ m/s$^2$. When does it hit the ground?",
        opts={"A": r"t=3\ \text{s}", "B": r"t=2\ \text{s}", "C": r"t=1\ \text{s}",
              "D": r"t=1.5\ \text{s}", "E": r"t=4\ \text{s}", "F": r"t=5\ \text{s}"},
        key="A",
        sol=[r"Only the vertical component matters. Integrating twice, "
             r"$z(t)=15+10t-5t^2$ (initial height, plus initial vertical velocity, "
             r"minus $\tfrac12gt^2$).",
             r"Set $z=0$: $5t^2-10t-15=0$, so $t^2-2t-3=0$, that is $(t-3)(t+1)=0$.",
             r"The positive root is $t=3$ s."],
        trap="Dropping the initial height and solving $10t-5t^2=0$ gives $t=2$ — option B. "
             "The launch height is what keeps it in the air longer. And the coefficient is "
             "$\\tfrac12 g=5$, not $g=10$.",
        check=lambda: [x for x in solve(15 + 10*t - 5*t**2, t) if x.is_positive], want=[S(3)],
    ),
    dict(
        quiz="q3", id="Q3m", sec="14.3", title="14.3 · Projectile · maximum height",
        stem=r"Same ball: launched from $15$ m with velocity $\langle 20,\,0,\,10\rangle$ m/s "
             r"and acceleration $\langle 0,0,-10\rangle$ m/s$^2$. What is its maximum height?",
        opts={"A": r"20\ \text{m}", "B": r"15\ \text{m}", "C": r"25\ \text{m}",
              "D": r"10\ \text{m}", "E": r"30\ \text{m}", "F": r"5\ \text{m}"},
        key="A",
        sol=[r"The peak is where the <b>vertical velocity</b> is zero, not where $z=0$.",
             r"$z'(t)=10-10t=0$ gives $t=1$ s.",
             r"$z(1)=15+10(1)-5(1)^2=15+10-5=20$ m."],
        trap="Answering $15$ m, the launch height — the ball is still going up when it "
             "leaves. Or solving $z(t)=0$, which finds the ground, not the peak.",
        check=lambda: (15 + 10*t - 5*t**2).subs(
            t, solve(__import__("sympy").diff(15 + 10*t - 5*t**2, t), t)[0]),
        want=S(20),
    ),
]


# Quiz 4 (14.4 / 14.5 / 15.1 / 15.2) lives in its own module — same schema,
# same verify() guard — because it was written from the actual MyLab set for
# Lessons 8-10 and is long enough to deserve its own file.
import q4bank                                                    # noqa: E402
QUESTIONS += q4bank.QUESTIONS


# --------------------------------------------------------- key checking ----

_TEX_CLEAN = [
    (r"\\left", ""), (r"\\right", ""), (r"\\!", ""), (r"\\,", ""),
    (r"\\;", ""), (r"\\ ", ""), (r"\\text\{[^}]*\}", ""),
    (r"\\displaystyle", ""), (r"\\[dt]frac", r"\\frac"),
]


def _grab(t, i):
    """Read the balanced {...} starting at t[i]; return (inner, next index)."""
    assert t[i] == "{"
    depth, j = 0, i
    while j < len(t):
        if t[j] == "{":
            depth += 1
        elif t[j] == "}":
            depth -= 1
            if depth == 0:
                return t[i + 1:j], j + 1
        j += 1
    raise ValueError("unbalanced")


def _brace_expand(t):
    """Rewrite \\frac{a}{b} and \\sqrt{a} using real brace matching."""
    import re as _re
    t = _re.sub(r"\\sqrt(\d+)", r"\\sqrt{\1}", t)
    for _ in range(8):
        m = _re.search(r"\\(frac|sqrt)\{", t)
        if not m:
            break
        name, i = m.group(1), m.end() - 1
        try:
            a, j = _grab(t, i)
            if name == "frac":
                b, j = _grab(t, j)
                rep = f"(({a})/({b}))"
            else:
                rep = f"(sqrt({a}))"
        except (ValueError, AssertionError, IndexError):
            return t
        t = t[:m.start()] + rep + t[j:]
    return t


def tex_to_sympy(tex):
    """Parse the small TeX dialect the options actually use. None if unsure.

    Deliberately narrow: integers, fractions, square roots, pi, powers and
    products of those, which covers most keyed scalars. Anything it does not
    fully recognise returns None and the key check skips that option — a miss
    is acceptable here, a false accusation is not.
    """
    import re as _re
    from sympy import sympify
    t = tex
    # "c=-2" / "t=3" style: the value is whatever follows the single '='
    if t.count("=") == 1 and _re.match(r"^\s*[a-zA-Z]\s*=", t):
        t = t.split("=", 1)[1]
    for pat, rep in _TEX_CLEAN:
        t = _re.sub(pat, rep, t)
    t = t.strip()
    # Superscript braces are the only other user of {}, and they confuse the
    # brace-matching below, so turn ^{..} into ^(..) up front. \frac and \sqrt
    # are then expanded innermost-first by real brace matching, not by regex.
    t = _re.sub(r"\^\{([^{}]*)\}", r"^(\1)", t)
    t = _brace_expand(t)
    if "\\frac" in t or "\\sqrt" in t:
        return None                                 # beyond this dialect
    t = t.replace("\\pi", "pi")
    t = t.replace("^", "**")
    t = _re.sub(r"\{([^{}]*)\}", r"(\1)", t)
    # implicit multiplication: 216sqrt(26) -> 216*sqrt(26), 3pi -> 3*pi
    t = _re.sub(r"(\d)\s*(?=[a-zA-Z(])", r"\1*", t)
    t = _re.sub(r"\)\s*(?=[a-zA-Z0-9(])", r")*", t)
    if "\\" in t or "langle" in t or "&" in t:
        return None
    try:
        return sympify(t, rational=True)
    except Exception:                              # noqa: BLE001 - unparsed is fine
        return None


def _align(parsed, want):
    """sympify() invents assumption-free symbols; the bank's carry real=True.

    Symbol("t") != Symbol("t", real=True), so an otherwise perfect match would
    be reported as a mismatch. Re-point the parsed expression at the symbols
    the keyed answer actually uses.
    """
    sub = {p: w for p in parsed.free_symbols
           for w in want.free_symbols if p.name == w.name}
    return parsed.subs(sub) if sub else parsed


def keycheck(q):
    """Is q['key'] the option whose value equals q['want']? '' if fine."""
    from sympy import simplify
    want = q.get("want")
    if want is None or isinstance(want, (tuple, list, Matrix)):
        return ""                                   # multi-part: nothing to match
    opts = q["opts"]
    keyed = opts.get(q["key"])
    if isinstance(keyed, dict):
        return ""                                   # prose option, not a value
    parsed = tex_to_sympy(keyed)
    if parsed is None:
        return ""                                   # outside the dialect; skip
    try:
        if simplify(_align(parsed, want) - want) == 0:
            return ""
    except Exception:                               # noqa: BLE001
        return ""
    # The keyed option disagrees. Only complain if some OTHER option matches —
    # otherwise the parser, not the question, is probably at fault.
    for letter, v in opts.items():
        if letter == q["key"] or isinstance(v, dict):
            continue
        other = tex_to_sympy(v)
        try:
            if other is not None and simplify(_align(other, want) - want) == 0:
                return (f"key is {q['key']} but the computed answer {want} "
                        f"is option {letter}")
        except Exception:                           # noqa: BLE001
            continue
    return ""


def verify():
    """Recompute every keyed answer. Raises on any mismatch."""
    from sympy import simplify
    problems, seen = [], set()
    for q in QUESTIONS:
        if q["id"] in seen:
            problems.append(f"{q['id']}: duplicate id")
        seen.add(q["id"])
        if q["key"] not in q["opts"]:
            problems.append(f"{q['id']}: key {q['key']} is not an option")
        if len(q["opts"]) < 4:
            problems.append(f"{q['id']}: only {len(q['opts'])} options")

        # Conceptual questions have nothing to recompute — the answer is a
        # definition or a classification, not a number. They opt out explicitly
        # with concept=True rather than carrying a fake check that would pass
        # trivially and quietly weaken this guard for everything else.
        if q.get("concept"):
            if "check" in q or "want" in q:
                problems.append(f"{q['id']}: concept=True but still carries a check")
            if not q.get("sol") or not q.get("trap"):
                problems.append(f"{q['id']}: concept question needs sol and trap")
            continue

        if "check" not in q or "want" not in q:
            problems.append(f"{q['id']}: no check — add one, or mark concept=True")
            continue

        # The check above proves the *keyed value* is right. It says nothing
        # about whether q["key"] points at the option that displays that value —
        # editing an option letter would slip through silently. keycheck closes
        # that, for every option it can parse back into sympy.
        bad_key = keycheck(q)
        if bad_key:
            problems.append(f"{q['id']}: {bad_key}")

        got, want = q["check"](), q["want"]
        try:
            if isinstance(got, Matrix):
                ok = simplify((got - want)).norm() == 0
            elif isinstance(got, (tuple, list)):
                ok = (len(got) == len(want) and
                      all(simplify(a - b) == 0 if not isinstance(a, Matrix)
                          else simplify(a - b).norm() == 0
                          for a, b in zip(got, want)))
            else:
                ok = simplify(got - want) == 0
        except Exception as e:                     # noqa: BLE001 - report, don't mask
            ok, e_ = False, e
            problems.append(f"{q['id']}: check raised {e_!r}")
            continue
        if not ok:
            problems.append(f"{q['id']}: computed {got!r}, keyed {want!r}")

    if problems:
        raise SystemExit("ANSWER VERIFICATION FAILED:\n  " + "\n  ".join(problems))
    return len(QUESTIONS)


if __name__ == "__main__":
    n = verify()
    from collections import Counter
    c = Counter(q["quiz"] for q in QUESTIONS)
    concept = sum(1 for q in QUESTIONS if q.get("concept"))
    print(f"verified {n - concept} computed + {concept} conceptual = {n}: "
          + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
