"""Worked solutions for Lessons 29-31 of the official guide.

Lesson 29  Green's Theorem            (§17.4)
Lesson 30  Curl and Divergence        (§17.5)
Lesson 31  Surface Integrals          (§17.6)

The instructor publishes a stem and a bare final answer. This file supplies the
missing middle: the set-up integral, the evaluation, and the specific wrong move
each problem invites.

Two things kill marks in this block and the `trap` fields hammer both:

  * **orientation** — Green's theorem and flux integrals are signed. A clockwise
    boundary, or a downward normal, flips the answer's sign. Green's theorem as
    stated requires the *counterclockwise* boundary; if the problem hands you a
    clockwise one you must negate.
  * **the surface element** — for a graph $z=g(x,y)$, $dS=\\sqrt{1+g_x^2+g_y^2}\\,dA$.
    Dropping that radical turns a surface integral into a plain double integral
    over the shadow, which is a different (usually smaller) number.

`check` re-derives each value with sympy from the stem. Two answers are prose
(a classification, an antiderivative potential) and carry no check rather than a
fake one.
"""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, acos, atan, pi,
                   exp, log, symbols, diff, integrate, limit, simplify, solve,
                   Eq, oo, Abs, sinh, cosh, atan2)

x, y, z = symbols("x y z", real=True)
r, th, ph, t, u, v = symbols("r theta phi t u v", real=True)
a_, b_ = symbols("a b", positive=True)


def V(*c):
    return Matrix(list(c))


def curl(F, vars=(x, y, z)):
    """curl of a 3-vector field given as a list of expressions."""
    X, Y, Z = vars
    Fx, Fy, Fz = F
    return V(diff(Fz, Y) - diff(Fy, Z),
             diff(Fx, Z) - diff(Fz, X),
             diff(Fy, X) - diff(Fx, Y))


def div(F, vars=(x, y, z)):
    return sum(diff(f, s) for f, s in zip(F, vars))


SOL = {

# ====================================================== Lesson 29 — Green ====

"L29P1": dict(
    steps=[
        r"Green's Theorem converts a **counterclockwise** closed line integral into a double integral: $\oint_C P\,dx+Q\,dy=\iint_R\left(\dfrac{\partial Q}{\partial x}-\dfrac{\partial P}{\partial y}\right)dA$.",
        r"Read off $P=x$ and $Q=x^2+y^2$. The orientation is already CCW, so no sign flip is needed.",
        r"$\dfrac{\partial Q}{\partial x}=2x$ and $\dfrac{\partial P}{\partial y}=0$, so the integrand is just $2x$.",
        r"$R$ is the rectangle $0\le x\le2$, $0\le y\le3$ — a genuine rectangle, so the limits are constants and the order does not matter.",
        r"$\displaystyle\iint_R 2x\,dA=\int_0^3\!\!\int_0^2 2x\,dx\,dy=\int_0^3\left[x^2\right]_0^2 dy=\int_0^3 4\,dy=12$.",
    ],
    trap=r"Trying to parametrize all four sides by hand. That is four integrals, and the $\int x\,dx$ pieces on the top and bottom edges cancel in a way that is easy to botch — one sign slip on the *return* edges (which run right-to-left and top-to-bottom) and you get $0$ or $24$. Green's theorem exists precisely to make the orientation bookkeeping automatic; use it. Also note $P=x$ contributes **nothing**, since $P_y=0$ — the whole answer comes from $Q$.",
    check=lambda: integrate(diff(x**2 + y**2, x) - diff(x, y), (x, 0, 2), (y, 0, 3)),
    want=S(12),
),

"L29P2": dict(
    steps=[
        r"$P=\cos^3(x)$, $Q=e^{x}$. Neither has an elementary-looking line integral, which is the hint that Green's Theorem is the intended route.",
        r"$\dfrac{\partial Q}{\partial x}=e^{x}$, $\dfrac{\partial P}{\partial y}=0$ (there is no $y$ in $\cos^3 x$ at all), so $Q_x-P_y=e^{x}$.",
        r"Describe the triangle. The two slanted sides are $y=x$ (from $(0,0)$ to $(1,1)$) and $y=2-x$ (from $(1,1)$ to $(2,0)$), with the base $y=0$.",
        r"Integrating in $x$ first avoids splitting the region: for each $y\in[0,1]$, $x$ runs from the left edge $x=y$ to the right edge $x=2-y$.",
        r"$\displaystyle\int_0^1\!\!\int_{y}^{2-y}e^{x}\,dx\,dy=\int_0^1\left(e^{2-y}-e^{y}\right)dy$.",
        r"$=\left[-e^{2-y}-e^{y}\right]_0^1=(-e-e)-(-e^2-1)=e^2-2e+1$.",
    ],
    trap=r"Integrating $dy$ first. Then you **must** split at $x=1$, because the upper boundary changes formula from $y=x$ to $y=2-x$ there: $\int_0^1\!\int_0^x+\int_1^2\!\int_0^{2-x}$. Students who write a single $\int_0^2\!\int_0^{x}$ silently integrate over a region that is not the triangle. Going $dx$ first needs no split. (Note $e^2-2e+1=(e-1)^2$, a useful sanity check that it is positive.)",
    check=lambda: integrate(diff(exp(x), x) - diff(cos(x)**3, y), (x, y, 2 - y), (y, 0, 1)),
    want=exp(2) - 2 * exp(1) + 1,
),

"L29P3": dict(
    steps=[
        r"$P=y$, $Q=2x$, and the square is traversed CCW, so Green's Theorem applies directly.",
        r"$\dfrac{\partial Q}{\partial x}-\dfrac{\partial P}{\partial y}=2-1=1$.",
        r"The integrand collapsed to the constant $1$, so the double integral is literally the **area** of $R$.",
        r"$R$ is the square $-1\le x\le1$, $-1\le y\le1$, whose side length is $2$, so its area is $4$.",
        r"$\displaystyle\oint_C y\,dx+2x\,dy=\iint_R 1\,dA=\text{area}(R)=4$.",
    ],
    trap=r"Computing $P_x-Q_y$ instead of $Q_x-P_y$. That gives $0-0=0$ here, a clean-looking wrong answer. The derivative always hits the *other* variable: $Q$ gets $\partial_x$, $P$ gets $\partial_y$. Second trap: the vertices $(\pm1,\pm1)$ describe a square of side $2$, not side $1$ — its area is $4$, not $1$.",
    check=lambda: integrate(diff(2 * x, x) - diff(y, y), (x, -1, 1), (y, -1, 1)),
    want=S(4),
),

"L29P4": dict(
    steps=[
        r"Write the integral as $\oint_C P\,dx+Q\,dy$ with $P=y^3$ and $Q=-x^3$ — the minus sign in front of $x^3\,dy$ belongs to $Q$.",
        r"$\dfrac{\partial Q}{\partial x}=-3x^2$, $\dfrac{\partial P}{\partial y}=3y^2$, so $Q_x-P_y=-3x^2-3y^2=-3(x^2+y^2)$.",
        r"$R$ is the unit disk and the integrand depends only on $x^2+y^2$, so polar is the obvious move: $x^2+y^2=r^2$ and $dA=r\,dr\,d\theta$.",
        r"$\displaystyle\iint_R -3(x^2+y^2)\,dA=\int_0^{2\pi}\!\!\int_0^1 -3r^2\cdot r\,dr\,d\theta=\int_0^{2\pi}\!\!\int_0^1 -3r^3\,dr\,d\theta$.",
        r"$=2\pi\cdot\left(-\dfrac{3}{4}\right)=-\dfrac{3\pi}{2}$.",
    ],
    trap=r"Two sign traps stacked. First, forgetting that $Q=-x^3$, which makes $Q_x=+3x^2$ and hands you $+\frac{3\pi}{2}$ — the right magnitude, wrong sign. Second, forgetting the polar Jacobian: $-3r^2\,dr\,d\theta$ instead of $-3r^3\,dr\,d\theta$ gives $-2\pi$. The answer is negative, and it *should* be: the field circulates clockwise while $C$ runs counterclockwise.",
    check=lambda: integrate((diff(-x**3, x) - diff(y**3, y)).subs({x: r * cos(th), y: r * sin(th)}).simplify() * r,
                            (r, 0, 1), (th, 0, 2 * pi)),
    want=-3 * pi / 2,
),

"L29P5": dict(
    steps=[
        r"Green's Theorem run **backwards**: pick $P,Q$ with $Q_x-P_y=1$, and the double integral becomes the area. The symmetric choice is $P=-\tfrac{y}{2}$, $Q=\tfrac{x}{2}$, giving the area formula $A=\tfrac12\oint_C x\,dy-y\,dx$.",
        r"Parametrize the ellipse CCW: $x=a\cos t$, $y=b\sin t$, $0\le t\le2\pi$.",
        r"Then $dx=-a\sin t\,dt$ and $dy=b\cos t\,dt$.",
        r"$x\,dy-y\,dx=(a\cos t)(b\cos t)\,dt-(b\sin t)(-a\sin t)\,dt=ab(\cos^2t+\sin^2t)\,dt=ab\,dt$.",
        r"$A=\dfrac12\displaystyle\int_0^{2\pi}ab\,dt=\dfrac12\cdot ab\cdot 2\pi=\pi ab$.",
        r"Sanity check: setting $a=b=R$ gives $\pi R^2$, the circle.",
    ],
    trap=r"Dropping the $\tfrac12$. The area formula is $\tfrac12\oint x\,dy-y\,dx$ — the half is there because *each* of $x\,dy$ and $-y\,dx$ separately already integrates to the full area, and you are averaging them, not adding them. Forgetting it doubles the answer to $2\pi ab$. The other trap is parametrizing clockwise ($y=-b\sin t$), which returns $-\pi ab$; area must come out positive, so a negative result means your orientation was backwards.",
    check=lambda: Rational(1, 2) * integrate(
        (a_ * cos(t)) * (b_ * cos(t)) - (b_ * sin(t)) * (-a_ * sin(t)), (t, 0, 2 * pi)),
    want=pi * a_ * b_,
),

# ============================================ Lesson 30 — Curl and Divergence ====

"L30P1": dict(
    steps=[
        r"$\operatorname{curl}\vec F=\nabla\times\vec F=\left\langle \dfrac{\partial R}{\partial y}-\dfrac{\partial Q}{\partial z},\;\dfrac{\partial P}{\partial z}-\dfrac{\partial R}{\partial x},\;\dfrac{\partial Q}{\partial x}-\dfrac{\partial P}{\partial y}\right\rangle$ for $\vec F=\langle P,Q,R\rangle$.",
        r"Here $P=xy$, $Q=\sin z$, $R=\cos y$.",
        r"First component: $R_y-Q_z=\dfrac{\partial}{\partial y}(\cos y)-\dfrac{\partial}{\partial z}(\sin z)=-\sin y-\cos z$.",
        r"Second component: $P_z-R_x=\dfrac{\partial}{\partial z}(xy)-\dfrac{\partial}{\partial x}(\cos y)=0-0=0$.",
        r"Third component: $Q_x-P_y=\dfrac{\partial}{\partial x}(\sin z)-\dfrac{\partial}{\partial y}(xy)=0-x=-x$.",
        r"$\operatorname{curl}\vec F=\langle-\sin y-\cos z,\,0,\,-x\rangle$.",
    ],
    trap=r"The **middle component's sign**. Expanding the determinant $\begin{vmatrix}\vec i&\vec j&\vec k\\\partial_x&\partial_y&\partial_z\\P&Q&R\end{vmatrix}$, the $\vec j$ entry carries a minus from cofactor expansion: it is $-(R_x-P_z)=P_z-R_x$, **not** $R_x-P_z$. Write the middle slot as $P_z-R_x$ and the sign takes care of itself. (Here it is $0$ either way, which is exactly why the habit must be built on a problem where it does not bite.) Second trap: $\operatorname{curl}$ of a vector field is a **vector**, while $\operatorname{div}$ is a scalar — never report a single number here.",
    check=lambda: curl([x * y, sin(z), cos(y)]),
    want=V(-sin(y) - cos(z), 0, -x),
),

"L30P2": dict(
    steps=[
        r"$\operatorname{div}(\nabla f)=\nabla^2 f=f_{xx}+f_{yy}+f_{zz}$, the Laplacian. So take second partials, not first.",
        r"$f=xy^2z^3$. Gradient: $\nabla f=\langle y^2z^3,\;2xyz^3,\;3xy^2z^2\rangle$.",
        r"$f_{xx}=\dfrac{\partial}{\partial x}(y^2z^3)=0$ — $f$ is linear in $x$.",
        r"$f_{yy}=\dfrac{\partial}{\partial y}(2xyz^3)=2xz^3$.",
        r"$f_{zz}=\dfrac{\partial}{\partial z}(3xy^2z^2)=6xy^2z$.",
        r"$\nabla^2 f=0+2xz^3+6xy^2z$. At $(2,-1,1)$: $2(2)(1)^3+6(2)(-1)^2(1)=4+12=16$.",
    ],
    trap=r"Evaluating at the point **too early**. If you plug $(2,-1,1)$ into $\nabla f$ and then try to differentiate, you are differentiating constants and get $0$. Differentiate fully, *then* substitute. The other trap is $y^2$ at $y=-1$: $(-1)^2=+1$, not $-1$, so the $6xy^2z$ term is $+12$; a dropped square gives $4-12=-8$.",
    check=lambda: sum(diff(x * y**2 * z**3, s, 2) for s in (x, y, z)).subs({x: 2, y: -1, z: 1}),
    want=S(16),
),

"L30P3": dict(
    steps=[
        r"Label $P=e^{yz}-y\sin(xy)$, $Q=zxe^{yz}-x\sin(xy)$, $R=xye^{yz}$, and compute the three components of $\nabla\times\vec F$.",
        r"$R_y=\dfrac{\partial}{\partial y}\!\left(xye^{yz}\right)=xe^{yz}+xyze^{yz}$, and $Q_z=\dfrac{\partial}{\partial z}\!\left(zxe^{yz}-x\sin(xy)\right)=xe^{yz}+xyze^{yz}$. First component $R_y-Q_z=0$.",
        r"$P_z=\dfrac{\partial}{\partial z}\!\left(e^{yz}-y\sin(xy)\right)=ye^{yz}$, and $R_x=\dfrac{\partial}{\partial x}\!\left(xye^{yz}\right)=ye^{yz}$. Second component $P_z-R_x=0$.",
        r"$Q_x=ze^{yz}-\sin(xy)-xy\cos(xy)$ (product rule on $x\sin(xy)$), and $P_y=ze^{yz}-\sin(xy)-xy\cos(xy)$ (product rule on $y\sin(xy)$). Third component $Q_x-P_y=0$.",
        r"So $\operatorname{curl}\vec F=\vec 0$ everywhere.",
        r"$\vec F$ is defined and smooth on all of $\mathbb R^3$, which is simply connected, so $\operatorname{curl}\vec F=\vec0$ **implies** $\vec F$ is conservative: there is a potential $\varphi$ with $\nabla\varphi=\vec F$.",
        r"Indeed $\varphi=xe^{yz}+\cos(xy)$ works: $\varphi_x=e^{yz}-y\sin(xy)$, $\varphi_y=xze^{yz}-x\sin(xy)$, $\varphi_z=xye^{yz}$. Consequence: $\int_C\vec F\cdot d\vec r$ is path-independent and $\oint_C\vec F\cdot d\vec r=0$ on any closed curve.",
    ],
    trap=r"Stating the converse without the **domain** hypothesis. $\operatorname{curl}\vec F=\vec0$ alone does not make a field conservative — the standard counterexample $\vec F=\left\langle\frac{-y}{x^2+y^2},\frac{x}{x^2+y^2},0\right\rangle$ has zero curl but a nonzero loop integral, because its domain has the $z$-axis punched out. You get the conclusion here only because this $\vec F$ is smooth on all of $\mathbb R^3$. The computational trap is $\partial_y\big(y\sin(xy)\big)$: it needs the product rule, $\sin(xy)+xy\cos(xy)$, not just $xy\cos(xy)$.",
    prose=True,
),

"L30P4": dict(
    steps=[
        r"Test with the curl. $P=yz$, $Q=xz$, $R=xy$.",
        r"$R_y-Q_z=x-x=0$; $\;P_z-R_x=y-y=0$; $\;Q_x-P_y=z-z=0$. So $\operatorname{curl}\vec F=\vec 0$, and since $\vec F$ is a polynomial field on all of $\mathbb R^3$ (simply connected), $\vec F$ **is conservative**.",
        r"Now build $\varphi$ with $\nabla\varphi=\vec F$. Start from $\varphi_x=yz$ and integrate in $x$, treating $y,z$ as constants: $\varphi=xyz+g(y,z)$ — the 'constant' of integration may depend on the other variables.",
        r"Differentiate that in $y$: $\varphi_y=xz+g_y(y,z)$. Match against $Q=xz$, so $g_y=0$ and $g=h(z)$.",
        r"Differentiate in $z$: $\varphi_z=xy+h'(z)$. Match against $R=xy$, so $h'(z)=0$ and $h$ is a genuine constant.",
        r"$\varphi=xyz+C$, and one checks $\nabla(xyz)=\langle yz,xz,xy\rangle=\vec F$.",
    ],
    trap=r"Writing the first antiderivative as $\varphi=xyz+C$ with a **numeric** constant. At that stage the unknown is a whole function $g(y,z)$, because anything free of $x$ dies under $\partial_x$. Collapsing it to a number too early means you never actually verify $\varphi_y=Q$ and $\varphi_z=R$ — on a field where the components do *not* fit together, that shortcut produces a 'potential' for a non-conservative field. Also: test with $\operatorname{curl}$, not $\operatorname{div}$. Here $\operatorname{div}\vec F=0$ too, but that says the field is incompressible, an entirely different statement.",
    prose=True,
),

"L30P5": dict(
    steps=[
        r"$\operatorname{div}\vec F=\nabla\cdot\vec F=P_x+Q_y+R_z$ — each component differentiated with respect to its **own** variable, summed to a scalar.",
        r"$P=e^{xy}$, so $P_x=ye^{xy}$ (chain rule: $\partial_x(xy)=y$).",
        r"$Q=e^{yz}$, so $Q_y=ze^{yz}$.",
        r"$R=e^{xz}$, so $R_z=xe^{xz}$.",
        r"$\operatorname{div}\vec F=ye^{xy}+ze^{yz}+xe^{xz}$.",
        r"For the identity, let $\vec G=\langle G_1,G_2,G_3\rangle$. Then $\operatorname{curl}\vec G=\langle \partial_yG_3-\partial_zG_2,\;\partial_zG_1-\partial_xG_3,\;\partial_xG_2-\partial_yG_1\rangle$.",
        r"$\operatorname{div}(\operatorname{curl}\vec G)=\left(G_{3yx}-G_{2zx}\right)+\left(G_{1zy}-G_{3xy}\right)+\left(G_{2xz}-G_{1yz}\right)$.",
        r"By Clairaut's theorem the mixed partials commute ($G_{3yx}=G_{3xy}$, etc.), so the six terms cancel in pairs and $\operatorname{div}(\operatorname{curl}\vec G)=0$ for every $\vec G$ with continuous second partials.",
    ],
    trap=r"Dropping the chain-rule factor. $\partial_x e^{xy}=ye^{xy}$, not $e^{xy}$ — the answer $e^{xy}+e^{yz}+e^{xz}$ is the single most common version of this and it is wrong in all three terms. Watch which variable owns which exponent: the third component is $e^{xz}$ and gets $\partial_z$, producing $x e^{xz}$, not $z e^{xz}$. For the identity, the cancellation needs **continuous** second partials (Clairaut); it is a theorem, not algebra, and the practical payoff is that a field with $\operatorname{div}\vec H\ne0$ can never be written as $\operatorname{curl}$ of anything.",
    check=lambda: div([exp(x * y), exp(y * z), exp(x * z)]),
    want=y * exp(x * y) + z * exp(y * z) + x * exp(x * z),
),

# ============================================ Lesson 31 — Surface Integrals ====

"L31P1": dict(
    steps=[
        r"Solve for $z$ to get the surface as a graph: $z=g(x,y)=10-2x-5y$.",
        r"For a graph, $dS=\sqrt{1+g_x^2+g_y^2}\;dA$. Here $g_x=-2$, $g_y=-5$, so $dS=\sqrt{1+4+25}\,dA=\sqrt{30}\,dA$ — a **constant**, as it must be for a plane.",
        r"Find the shadow $D$. The first octant needs $x\ge0$, $y\ge0$, and $z\ge0$, and the last of these is $10-2x-5y\ge0$, i.e. $2x+5y\le10$.",
        r"$D$ is the triangle with legs along the axes: $x$-intercept $x=5$, $y$-intercept $y=2$. Its area is $\tfrac12(5)(2)=5$.",
        r"$\displaystyle\text{Area}=\iint_D\sqrt{30}\,dA=\sqrt{30}\cdot\text{area}(D)=5\sqrt{30}$.",
        r"Explicitly: $\displaystyle\int_0^5\!\!\int_0^{(10-2x)/5}\sqrt{30}\,dy\,dx=5\sqrt{30}$.",
    ],
    trap=r"Reporting $5$ — the area of the **shadow** — by forgetting the $\sqrt{1+g_x^2+g_y^2}$ factor. A tilted plane is always larger than its projection, so the stretch factor is $\ge1$ and your answer must exceed the shadow's area. The other trap is the shadow's shape: the first octant condition $z\ge0$ is what bounds $D$, giving the triangle $2x+5y\le10$ with intercepts $x=5$, $y=2$. Students who integrate over $0\le x\le5$, $0\le y\le2$ (the full rectangle) double the answer to $10\sqrt{30}$.",
    check=lambda: integrate(sqrt(1 + diff(10 - 2 * x - 5 * y, x)**2 + diff(10 - 2 * x - 5 * y, y)**2),
                            (y, 0, (10 - 2 * x) / 5), (x, 0, 5)),
    want=5 * sqrt(30),
),

"L31P2": dict(
    steps=[
        r"This is the 2D flux (outward-normal) line integral, and the problem hands you the formula: $\text{Flux}=\displaystyle\int_C P\,dy-Q\,dx$ with $\vec F=\langle P,Q\rangle$.",
        r"Along the curve, $P=x=3\cos t$ and $Q=y=2\sin t$.",
        r"Differentiate the parametrization: $dx=-3\sin t\,dt$ and $dy=2\cos t\,dt$.",
        r"$P\,dy-Q\,dx=(3\cos t)(2\cos t)\,dt-(2\sin t)(-3\sin t)\,dt=6\cos^2t\,dt+6\sin^2t\,dt=6\,dt$.",
        r"$\displaystyle\int_{-\pi}^{\pi}6\,dt=6(2\pi)=12\pi$.",
        r"Cross-check with the divergence form of Green's Theorem: $\operatorname{div}\vec F=1+1=2$, and the ellipse $\frac{x^2}{9}+\frac{y^2}{4}=1$ encloses area $\pi(3)(2)=6\pi$, so the flux is $2\cdot6\pi=12\pi$. ✓",
    ],
    trap=r"Computing $\int P\,dx+Q\,dy$ — the **circulation** — instead of $\int P\,dy-Q\,dx$. For this field that gives $\int(-9\cos t\sin t+4\sin t\cos t)dt=0$, a plausible-looking but wrong answer. Flux swaps the differentials *and* inserts a minus sign; circulation does not. The second trap is the parameter range: $-\pi\le t\le\pi$ is a full $2\pi$ sweep traversed counterclockwise, so the outward normal convention holds and the flux is positive — halving it to $6\pi$ means you read the range as a half-loop.",
    check=lambda: integrate((3 * cos(t)) * diff(2 * sin(t), t) - (2 * sin(t)) * diff(3 * cos(t), t),
                            (t, -pi, pi)),
    want=12 * pi,
),

"L31P3": dict(
    steps=[
        r"$\iint_S 1\,dS$ is the **surface area** of $S$. The surface is the graph $z=g(x,y)=x^2+y^2$.",
        r"$g_x=2x$, $g_y=2y$, so $dS=\sqrt{1+4x^2+4y^2}\;dA$.",
        r"The shadow: $z\le4$ means $x^2+y^2\le4$, the disk of radius $2$.",
        r"Polar, since both the integrand and the region depend only on $x^2+y^2=r^2$: $dS=\sqrt{1+4r^2}\;r\,dr\,d\theta$ — note **both** the radical and the Jacobian $r$.",
        r"$\displaystyle\iint_S dS=\int_0^{2\pi}\!\!\int_0^2\sqrt{1+4r^2}\;r\,dr\,d\theta$.",
        r"Inner integral by $u=1+4r^2$, $du=8r\,dr$: $\displaystyle\int_0^2 r\sqrt{1+4r^2}\,dr=\left[\frac{(1+4r^2)^{3/2}}{12}\right]_0^2=\frac{17^{3/2}-1}{12}=\frac{17\sqrt{17}-1}{12}$.",
        r"Multiply by $\int_0^{2\pi}d\theta=2\pi$: $\;\dfrac{2\pi(17\sqrt{17}-1)}{12}=\dfrac{\pi}{6}\left(17\sqrt{17}-1\right)$.",
    ],
    trap=r"The radius of the shadow. $z=4$ on $z=x^2+y^2$ means $r^2=4$, so $r$ runs to $\mathbf{2}$, not $4$ — using $r\le4$ gives $\frac{\pi}{6}(65\sqrt{65}-1)$. The second trap is losing one of the two $r$'s: $\sqrt{1+4r^2}\,r\,dr\,d\theta$ carries the surface radical *and* the polar Jacobian, and dropping the Jacobian leaves an integral with no elementary $u$-substitution, which should tip you off that something is missing.",
    check=lambda: integrate(sqrt(1 + 4 * r**2) * r, (r, 0, 2), (th, 0, 2 * pi)),
    want=pi * (17 * sqrt(17) - 1) / 6,
),

"L31P4": dict(
    steps=[
        r"For an **upward**-oriented graph $z=g(x,y)$, $\displaystyle\iint_S\vec F\cdot d\vec S=\iint_D\left(-P\,g_x-Q\,g_y+R\right)dA$. Note this formula already has the $\sqrt{1+g_x^2+g_y^2}$ built in — it cancels against the normalization of $\hat n$, so do **not** multiply by it again.",
        r"Here $g=4-x^2-y^2$, so $g_x=-2x$ and $g_y=-2y$; and $\vec F=\langle x,y,z\rangle$ with $z$ evaluated *on the surface*: $R=4-x^2-y^2$.",
        r"Integrand: $-x(-2x)-y(-2y)+(4-x^2-y^2)=2x^2+2y^2+4-x^2-y^2=x^2+y^2+4$.",
        r"The shadow $D$ is where $z\ge0$: $4-x^2-y^2\ge0$, the disk $x^2+y^2\le4$ of radius $2$.",
        r"Polar: $\displaystyle\int_0^{2\pi}\!\!\int_0^2\left(r^2+4\right)r\,dr\,d\theta=\int_0^{2\pi}\!\!\int_0^2\left(r^3+4r\right)dr\,d\theta$.",
        r"$\displaystyle\int_0^2\left(r^3+4r\right)dr=\left[\frac{r^4}{4}+2r^2\right]_0^2=4+8=12$, and times $2\pi$ gives $24\pi$.",
    ],
    trap=r"Leaving $z$ as the free variable $z$ instead of substituting the surface, $z=4-x^2-y^2$. The flux integral lives *on* the surface, so every appearance of $z$ in $\vec F$ must be replaced. The second trap is the sign pattern: it is $\langle-g_x,-g_y,1\rangle$ for **upward** — the two tangential terms get minus signs and the $\vec k$ slot gets $+1$. If the problem had said downward you would negate the whole thing, giving $-24\pi$. Third: do not tack on an extra $\sqrt{1+4x^2+4y^2}$; that factor is only for $dS$ in a scalar surface integral, never for $d\vec S$ in this form.",
    check=lambda: integrate(
        ((-(x) * diff(4 - x**2 - y**2, x) - (y) * diff(4 - x**2 - y**2, y) + (4 - x**2 - y**2))
         ).subs({x: r * cos(th), y: r * sin(th)}).simplify() * r,
        (r, 0, 2), (th, 0, 2 * pi)),
    want=24 * pi,
),

"L31P5": dict(
    steps=[
        r"The cone is the graph $z=g(x,y)=\sqrt{x^2+y^2}$.",
        r"$g_x=\dfrac{x}{\sqrt{x^2+y^2}}$ and $g_y=\dfrac{y}{\sqrt{x^2+y^2}}$, so $g_x^2+g_y^2=\dfrac{x^2+y^2}{x^2+y^2}=1$.",
        r"Therefore $dS=\sqrt{1+1}\,dA=\sqrt{2}\,dA$ — constant, because a cone has the same slope everywhere.",
        r"The shadow: $z\le3$ means $\sqrt{x^2+y^2}\le3$, the disk of radius $3$, whose area is $9\pi$.",
        r"$\displaystyle\iint_S dS=\int_0^{2\pi}\!\!\int_0^3\sqrt2\;r\,dr\,d\theta=\sqrt2\cdot 9\pi=9\pi\sqrt2$.",
    ],
    trap=r"Writing $dS=\sqrt{1+x^2+y^2}\,dA$ by squaring the *function* instead of its partials. The radical needs $g_x^2+g_y^2$, and for this cone those partials are the components of a **unit** vector, so their squares sum to exactly $1$ and the factor is the clean $\sqrt2$. The other trap: the apex $(0,0,0)$ makes $g_x,g_y$ undefined there, but it is a single point of measure zero and the improper integral converges — the $\sqrt2$ still holds. And do not confuse this with the *lateral* cone formula $\pi r\ell$: here $r=3$, $\ell=3\sqrt2$, giving $9\pi\sqrt2$, which agrees. ✓",
    check=lambda: integrate(sqrt(1 + (diff(sqrt(x**2 + y**2), x)**2 + diff(sqrt(x**2 + y**2), y)**2).subs(
        {x: r * cos(th), y: r * sin(th)}).simplify()) * r, (r, 0, 3), (th, 0, 2 * pi)),
    want=9 * pi * sqrt(2),
),

"L31P6": dict(
    steps=[
        r"$S$ is a flat horizontal disk at height $z=1$, oriented **upward**, so the unit normal is simply $\hat n=\vec k=\langle0,0,1\rangle$ and $d\vec S=\langle0,0,1\rangle\,dA$ (the graph $z=g=1$ has $g_x=g_y=0$, so $dS=dA$).",
        r"Dot the field with the normal: $\vec F\cdot\hat n=\langle y,-x,1\rangle\cdot\langle0,0,1\rangle=1$. Only the $\vec k$-component of $\vec F$ survives.",
        r"$\displaystyle\iint_S\vec F\cdot d\vec S=\iint_{x^2+y^2\le1}1\,dA=\text{area of the unit disk}=\pi$.",
        r"Explicitly in polar: $\displaystyle\int_0^{2\pi}\!\!\int_0^1 1\cdot r\,dr\,d\theta=2\pi\cdot\tfrac12=\pi$.",
    ],
    trap=r"Trying to integrate the $y$ and $-x$ components. They are entirely tangential to a horizontal disk and contribute **nothing** to flux — this field swirls *within* the plane $z=1$ and never crosses it. (Its curl is $\langle0,0,-2\rangle$, so its *circulation* around the boundary is $-2\pi$, a completely different number that this problem is baiting you toward.) The second trap is orientation: 'oriented upward' fixes $\hat n=+\vec k$; downward would give $-\pi$. Third, the disk has radius $1$, so its area is $\pi$, not $2\pi$.",
    check=lambda: integrate(V(r * sin(th), -r * cos(th), 1).dot(V(0, 0, 1)) * r, (r, 0, 1), (th, 0, 2 * pi)),
    want=pi,
),

}
