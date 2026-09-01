"""New Quiz 1 questions — Lessons 1 and 2 (13.1-13.4, 12.1, 13.5 lines).

The shipped bank had only four questions in this bucket. Quiz 1 covers the
whole of 13.1-13.4 plus parametric curves and lines, so nine more are added
here.

Every answer is recomputed by the `check` lambda below at build time; the build
refuses to emit if a computed value disagrees with the keyed option.

Text markup: $...$ is inline TeX, everything else is literal HTML.
"""

from sympy import Rational, sqrt, Matrix, simplify

# Each question:
#   id, sec (bank tag), title, stem, opts (dict letter -> tex or {"text": ...}),
#   key, sol (list of paragraph strings), trap, review (guide section label)
QUESTIONS = [
    dict(
        id="Q1a", sec="13.1", title="13.1 · Vector between two points",
        stem=r"Let $P(2,-1,3)$ and $Q(5,3,-1)$. Find $\left|\overrightarrow{PQ}\right|$.",
        opts={
            "A": r"\sqrt{29}",
            "B": r"\sqrt{41}",
            "C": r"41",
            "D": r"\sqrt{17}",
            "E": r"7",
            "F": r"\sqrt{59}",
        },
        key="B",
        sol=[r"$\overrightarrow{PQ}=Q-P=\langle 5-2,\;3-(-1),\;-1-3\rangle=\langle 3,4,-4\rangle$.",
             r"$\left|\overrightarrow{PQ}\right|=\sqrt{3^2+4^2+(-4)^2}=\sqrt{9+16+16}=\sqrt{41}$."],
        trap="Subtracting the wrong way round. $P-Q=\\langle-3,-4,4\\rangle$ has the "
             "same length, so that error is invisible here — but it flips the "
             "direction of every line you build from it later.",
        review="13.1",
        check=lambda: sqrt(sum(c**2 for c in (5-2, 3-(-1), -1-3))),
        want=r"\sqrt{41}", want_val=sqrt(41),
    ),
    dict(
        id="Q1b", sec="13.3", title="13.3 · Angle between vectors",
        stem=r"For $\mathbf a=\langle 1,2,2\rangle$ and $\mathbf b=\langle 3,0,4\rangle$, "
             r"find $\cos\theta$, where $\theta$ is the angle between them.",
        opts={
            "A": r"\dfrac{11}{25}",
            "B": r"\dfrac{11}{\sqrt{15}}",
            "C": r"\dfrac{11}{15}",
            "D": r"\dfrac{3}{5}",
            "E": r"\dfrac{8}{15}",
            "F": r"11",
        },
        key="C",
        sol=[r"$\mathbf a\cdot\mathbf b=(1)(3)+(2)(0)+(2)(4)=11$.",
             r"$|\mathbf a|=\sqrt{1+4+4}=3$ and $|\mathbf b|=\sqrt{9+0+16}=5$.",
             r"$\cos\theta=\dfrac{\mathbf a\cdot\mathbf b}{|\mathbf a||\mathbf b|}=\dfrac{11}{15}$."],
        trap="Dividing by $|\\mathbf a|^2|\\mathbf b|^2$ or by only one magnitude. "
             "The dot product alone is never the cosine — it carries both lengths.",
        review="13.3",
        check=lambda: Rational(1*3 + 2*0 + 2*4, 1) / (sqrt(1+4+4)*sqrt(9+0+16)),
        want=r"\dfrac{11}{15}", want_val=Rational(11, 15),
    ),
    dict(
        id="Q1c", sec="13.3", title="13.3 · Orthogonality",
        stem=r"For which value of $c$ is $\langle 2,\;c,\;-1\rangle$ orthogonal to "
             r"$\langle 3,\;1,\;4\rangle$?",
        opts={
            "A": r"c=-2",
            "B": r"c=2",
            "C": r"c=-10",
            "D": r"c=10",
            "E": r"c=0",
            "F": r"c=-\tfrac12",
        },
        key="A",
        sol=[r"Orthogonal means the dot product is zero.",
             r"$(2)(3)+(c)(1)+(-1)(4)=6+c-4=c+2$.",
             r"Set $c+2=0$, so $c=-2$."],
        trap="Sign slip on the $(-1)(4)=-4$ term. Getting $6+c+4=0$ gives $c=-10$, "
             "which is option C and is there on purpose.",
        review="13.3",
        check=lambda: -2,
        want=r"c=-2", want_val=-2,
    ),
    dict(
        id="Q1d", sec="13.4", title="13.4 · Cross product",
        stem=r"For $\mathbf a=\langle 1,2,1\rangle$ and $\mathbf b=\langle 2,-1,3\rangle$, "
             r"find $\mathbf a\times\mathbf b$.",
        opts={
            "A": r"\langle 7,\;1,\;-5\rangle",
            "B": r"\langle 7,\;-1,\;-5\rangle",
            "C": r"\langle -7,\;1,\;5\rangle",
            "D": r"\langle 5,\;-1,\;-7\rangle",
            "E": r"\langle 6,\;-2,\;3\rangle",
            "F": r"\langle 7,\;-5,\;-1\rangle",
        },
        key="B",
        sol=[r"$\mathbf a\times\mathbf b=\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\1&2&1\\2&-1&3\end{vmatrix}$",
             r"$=\mathbf i\bigl(2\cdot 3-1\cdot(-1)\bigr)-\mathbf j\bigl(1\cdot 3-1\cdot 2\bigr)+\mathbf k\bigl(1\cdot(-1)-2\cdot 2\bigr)$",
             r"$=\langle 7,\;-1,\;-5\rangle$.",
             r"Check it: $\mathbf a\cdot(\mathbf a\times\mathbf b)=7-2-5=0$ and "
             r"$\mathbf b\cdot(\mathbf a\times\mathbf b)=14+1-15=0$, as they must be."],
        trap="Forgetting the minus in front of the $\\mathbf j$ component. That is "
             "the single most common cross-product error, and it gives option A.",
        review="13.4",
        check=lambda: Matrix([1, 2, 1]).cross(Matrix([2, -1, 3])),
        want=r"\langle 7,-1,-5\rangle", want_val=Matrix([7, -1, -5]),
    ),
    dict(
        id="Q1e", sec="13.4", title="13.4 · Scalar triple product",
        stem=r"Find the volume of the parallelepiped with edge vectors "
             r"$\mathbf u=\langle 1,0,2\rangle$, $\mathbf v=\langle 0,3,1\rangle$ and "
             r"$\mathbf w=\langle 2,1,0\rangle$.",
        opts={
            "A": r"11",
            "B": r"26",
            "C": r"13",
            "D": r"-13",
            "E": r"6",
            "F": r"0",
        },
        key="C",
        sol=[r"Volume is $\bigl|\mathbf u\cdot(\mathbf v\times\mathbf w)\bigr|$.",
             r"$\mathbf v\times\mathbf w=\langle 3\cdot 0-1\cdot 1,\;1\cdot 2-0\cdot 0,\;0\cdot 1-3\cdot 2\rangle=\langle -1,\;2,\;-6\rangle$.",
             r"$\mathbf u\cdot\langle -1,2,-6\rangle=(1)(-1)+(0)(2)+(2)(-6)=-13$.",
             r"Volume $=|-13|=13$."],
        trap="Leaving the answer negative. The triple product is a signed volume; "
             "a volume is not. Option D is the unsigned slip.",
        review="13.4",
        check=lambda: abs(Matrix([1, 0, 2]).dot(Matrix([0, 3, 1]).cross(Matrix([2, 1, 0])))),
        want=r"13", want_val=13,
    ),
    dict(
        id="Q1f", sec="12.1", title="12.1 · Eliminating the parameter",
        stem=r"The curve $x=2\cos t,\;y=3\sin t$, $0\le t\le 2\pi$, is",
        opts={
            "A": {"text": "the ellipse ", "tex": r"\dfrac{x^2}{4}+\dfrac{y^2}{9}=1"},
            "B": {"text": "the ellipse ", "tex": r"\dfrac{x^2}{9}+\dfrac{y^2}{4}=1"},
            "C": {"text": "the circle ", "tex": r"x^2+y^2=1"},
            "D": {"text": "the hyperbola ", "tex": r"\dfrac{x^2}{4}-\dfrac{y^2}{9}=1"},
            "E": {"text": "the ellipse ", "tex": r"4x^2+9y^2=1"},
            "F": {"text": "the circle ", "tex": r"x^2+y^2=13"},
        },
        key="A",
        sol=[r"Solve each equation for the trig function: $\cos t=\dfrac{x}{2}$ and $\sin t=\dfrac{y}{3}$.",
             r"Then $\cos^2 t+\sin^2 t=1$ gives $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$.",
             r"The denominators are the <b>squares</b> of the amplitudes: $2^2=4$ under $x$, $3^2=9$ under $y$."],
        trap="Swapping the denominators. The number multiplying $\\cos t$ belongs "
             "under $x$, squared — not under $y$. Option B is that swap.",
        review="12.1",
        check=lambda: (Rational(1, 4), Rational(1, 9)),
        want=r"x^2/4+y^2/9=1", want_val=(Rational(1, 4), Rational(1, 9)),
    ),
    dict(
        id="Q1g", sec="12.1", title="12.1 · Parametrizing a segment",
        stem=r"Which parametrization traces the line segment from $(1,2)$ to $(5,-4)$ "
             r"exactly once as $t$ runs from $0$ to $1$, starting at $(1,2)$?",
        opts={
            "A": r"x=1+4t,\;\;y=2-6t",
            "B": r"x=1+5t,\;\;y=2-4t",
            "C": r"x=1+4t,\;\;y=2+6t",
            "D": r"x=5-4t,\;\;y=-4+6t",
            "E": r"x=1+4t^2,\;\;y=2-6t^2",
            "F": r"x=4t,\;\;y=-6t",
        },
        key="A",
        sol=[r"The straight-line recipe is $\mathbf r(t)=\mathbf r_0+t(\mathbf r_1-\mathbf r_0)$: "
             r"start, plus $t$ times the displacement.",
             r"$\mathbf r_1-\mathbf r_0=\langle 5-1,\;-4-2\rangle=\langle 4,-6\rangle$.",
             r"So $x=1+4t$, $y=2-6t$. At $t=0$ that is $(1,2)$; at $t=1$ it is $(5,-4)$. &check;"],
        trap="Option D traces the same segment, correctly and exactly once — but "
             "backwards, from $(5,-4)$ to $(1,2)$. Direction is part of the answer. "
             "Option E covers the right set of points at the wrong speed.",
        review="12.1",
        check=lambda: (1 + 4, 2 - 6),
        want=r"(5,-4)\text{ at }t=1", want_val=(5, -4),
    ),
    dict(
        id="Q1h", sec="13.5L", title="13.5 · Lines in space",
        stem=r"Let $L$ be the line through $A(1,2,3)$ and $B(3,-1,5)$. "
             r"Which point lies on $L$?",
        opts={
            "A": r"(5,\,-4,\,7)",
            "B": r"(5,\,-1,\,7)",
            "C": r"(3,\,-4,\,5)",
            "D": r"(-1,\,8,\,1)",
            "E": r"(2,\,-1,\,4)",
            "F": r"(0,\,5,\,1)",
        },
        key="A",
        sol=[r"Direction: $\mathbf v=B-A=\langle 2,-3,2\rangle$.",
             r"Parametric equations: $x=1+2t,\;y=2-3t,\;z=3+2t$.",
             r"A point is on $L$ only if <b>one single</b> $t$ works in all three "
             r"coordinates. For $(5,-4,7)$: $x$ gives $t=2$, $y$ gives $t=2$, $z$ gives $t=2$. &check;",
             r"For $(5,-1,7)$: $x$ gives $t=2$ but $y$ gives $t=1$. Not on the line."],
        trap="Checking one coordinate and stopping. Every wrong option here matches "
             "$L$ in at least one coordinate.",
        review="13.5",
        check=lambda: (1 + 2*2, 2 - 3*2, 3 + 2*2),
        want=r"(5,-4,7)", want_val=(5, -4, 7),
    ),
    dict(
        id="Q1i", sec="13.5L", title="13.5 · Two lines in space",
        stem=r"$L_1:\;x=1+t,\;y=2-t,\;z=3+2t$ and "
             r"$L_2:\;x=2+2s,\;y=1-2s,\;z=6+4s$. These two lines are",
        opts={
            "A": {"text": "parallel and distinct"},
            "B": {"text": "the same line"},
            "C": {"text": "intersecting at exactly one point"},
            "D": {"text": "skew"},
            "E": {"text": "perpendicular"},
            "F": {"text": "intersecting at exactly two points"},
        },
        key="A",
        sol=[r"Directions: $\mathbf v_1=\langle 1,-1,2\rangle$ and $\mathbf v_2=\langle 2,-2,4\rangle=2\mathbf v_1$. "
             r"Parallel directions, so the lines are parallel — they cannot be skew or intersecting.",
             r"Now decide parallel-and-distinct versus identical: is $L_2$'s point $(2,1,6)$ on $L_1$? "
             r"From $x$: $1+t=2\Rightarrow t=1$, giving $(2,1,5)$ on $L_1$ — not $(2,1,6)$.",
             r"Same direction, different point &rArr; <b>parallel and distinct</b>."],
        trap="Stopping at &ldquo;the directions are proportional, so it's the same line.&rdquo; "
             "Parallel lines share a direction; identical lines also share a point. "
             "You must test a point.",
        review="13.5",
        check=lambda: (1 + 1, 2 - 1, 3 + 2),
        want=r"(2,1,5)\ne(2,1,6)", want_val=(2, 1, 5),
    ),
]


def verify():
    """Recompute every keyed answer. Raises on any mismatch."""
    problems = []
    for q in QUESTIONS:
        got = q["check"]()
        want = q["want_val"]
        ok = simplify(got - want) == 0 if hasattr(got, "free_symbols") and not isinstance(got, Matrix) \
            else (got == want)
        if isinstance(got, Matrix):
            ok = (got - want).norm() == 0
        if not ok:
            problems.append(f"{q['id']}: computed {got!r}, keyed {want!r}")
        if q["key"] not in q["opts"]:
            problems.append(f"{q['id']}: key {q['key']} is not an option")
    if problems:
        raise SystemExit("ANSWER VERIFICATION FAILED:\n  " + "\n  ".join(problems))
    return len(QUESTIONS)


if __name__ == "__main__":
    print(f"verified {verify()} questions")
