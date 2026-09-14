"""Worked solutions for Lessons 17-20 (Lagrange multipliers, double integrals
over rectangles and general regions, polar double integrals) of the official
MA 261 study guide."""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, acos, atan, pi,
                   exp, log, symbols, diff, integrate, limit, simplify, solve,
                   Eq, oo, Abs, sinh, cosh, atan2, Max, Min)

x, y, z = symbols("x y z", real=True)
r, th, ph, t, u, v = symbols("r theta phi t u v", real=True)
lam = symbols("lambda", real=True)


def V(*c):
    return Matrix(list(c))


def _lagrange(f, g, c, vars):
    """Solve grad f = lam * grad g, g = c. Return the list of values of f."""
    eqs = [Eq(diff(f, s), lam * diff(g, s)) for s in vars] + [Eq(g, c)]
    sols = solve(eqs, list(vars) + [lam], dict=True)
    return [simplify(f.subs(d)) for d in sols]


SOL = {

# ---------------------------------------------------------------- L17 -------

"L17P1": dict(
    steps=[
        r"The constraint $g(x,y)=x^2+2xy+4y^2=7$ is a closed curve (an ellipse), so $f$ attains a max and a min on it. Use Lagrange: $\nabla f=\lambda\nabla g$.",
        r"$\nabla f=\langle 2,\,-1\rangle$ and $\nabla g=\langle 2x+2y,\;2x+8y\rangle$, so the system is $2=\lambda(2x+2y)$, $-1=\lambda(2x+8y)$, $x^2+2xy+4y^2=7$.",
        r"Add twice the second equation to the first to kill $x$: $2+2(-1)=\lambda\big[(2x+2y)+2(2x+8y)\big]$ gives $0=\lambda(6x+18y)$. Since $\lambda\ne 0$ (else $\nabla f=\vec 0$, false), $x=-3y$.",
        r"Substitute into the constraint: $9y^2-6y^2+4y^2=7y^2=7$, so $y=\pm 1$ and $(x,y)=(-3,1)$ or $(3,-1)$.",
        r"Evaluate: $f(-3,1)=3-6-1=-4$ and $f(3,-1)=3+6+1=10$.",
        r"**Maximum value $=10$** (attained at $(3,-1)$; the minimum is $-4$).",
    ],
    trap=r"$\nabla g$ of the **cross term** is the usual casualty: $\partial_x(2xy)=2y$ and $\partial_y(2xy)=2x$, so $\nabla g=\langle 2x+2y,\,2x+8y\rangle$, **not** $\langle 2x+2y,\,8y\rangle$. Also, Lagrange hands you *critical values*, plural. The largest of the list is the answer, so you must evaluate $f$ at **every** solution point, not just the first one you find.",
    check=lambda: Max(*_lagrange(3 + 2*x - y, x**2 + 2*x*y + 4*y**2, 7, (x, y))),
    want=10,
),

"L17P2": dict(
    steps=[
        r"Constraint: the circle $g(x,y)=(x-1)^2+y^2=1$, centre $(1,0)$, radius $1$. $f$ is linear, so its extremes sit where the gradient of $f$ is normal to the circle.",
        r"Lagrange: $\langle 8,-6\rangle=\lambda\langle 2(x-1),\,2y\rangle$, i.e. $8=2\lambda(x-1)$ and $-6=2\lambda y$.",
        r"So $x-1=\dfrac{4}{\lambda}$ and $y=-\dfrac{3}{\lambda}$. Plug into the constraint: $\dfrac{16}{\lambda^2}+\dfrac{9}{\lambda^2}=1\Rightarrow \lambda^2=25,\ \lambda=\pm 5$.",
        r"$\lambda=5$: $(x,y)=\left(\tfrac95,-\tfrac35\right)$, $f=\tfrac{72}{5}+\tfrac{18}{5}=18$. $\lambda=-5$: $(x,y)=\left(\tfrac15,\tfrac35\right)$, $f=\tfrac85-\tfrac{18}{5}=-2$.",
        r"**Maximum value $=18$.**",
        r"Sanity check with geometry: $f=8x-6y$ at the centre $(1,0)$ is $8$, and $|\nabla f|=\sqrt{64+36}=10$, so on a radius-$1$ circle $f$ ranges over $8\pm 10=\{-2,18\}$. Same answer.",
    ],
    trap=r"The circle is **not** centred at the origin. Writing the constraint gradient as $\langle 2x,2y\rangle$ (forgetting the shift) is the standard wreck here; it must be $\langle 2(x-1),\,2y\rangle$. The shortcut $f_{\max}=f(\text{centre})+|\nabla f|\cdot R$ works **only** because $f$ is linear and the constraint is a circle; do not reach for it on an ellipse.",
    check=lambda: Max(*_lagrange(8*x - 6*y, (x - 1)**2 + y**2, 1, (x, y))),
    want=18,
),

"L17P3": dict(
    steps=[
        r"$f(x,y)=(x-2)^2+(y-4)^2$ is the **squared** distance from $(2,4)$; the constraint is the circle of radius $\sqrt5$ about the origin. So this is really a nearest/farthest point problem.",
        r"Lagrange: $\langle 2(x-2),\,2(y-4)\rangle=\lambda\langle 2x,\,2y\rangle$, i.e. $x-2=\lambda x$ and $y-4=\lambda y$.",
        r"Then $x(1-\lambda)=2$ and $y(1-\lambda)=4$, so $y=2x$ (dividing; note $\lambda\ne1$, since $\lambda=1$ would force $2=0$).",
        r"Constraint: $x^2+(2x)^2=5x^2=5\Rightarrow x=\pm1$, giving $(1,2)$ and $(-1,-2)$.",
        r"$f(1,2)=(1-2)^2+(2-4)^2=1+4=5$. $f(-1,-2)=(-3)^2+(-6)^2=9+36=45$.",
        r"**Maximum $45$, minimum $5$.** (Check: $|(2,4)|=\sqrt{20}=2\sqrt5$, so distances to the circle are $2\sqrt5\mp\sqrt5$, whose squares are $5$ and $45$.)",
    ],
    trap=r"Two traps. First, $f$ is the **squared** distance, so do not take a square root at the end and report $\sqrt{45}$ and $\sqrt5$. Second, the point $(2,4)$ lies *outside* the circle, so both critical points are genuine, one near and one far; the min is **not** $0$.",
    check=lambda: (lambda vals: [Max(*vals), Min(*vals)])(
        _lagrange((x - 2)**2 + (y - 4)**2, x**2 + y**2, 5, (x, y))),
    want=[45, 5],
),

"L17P4": dict(
    steps=[
        r"Constraint: the sphere $g=(x-1)^2+y^2+z^2=1$ of radius $1$ centred at $(1,0,0)$. $f=x+y+z$ is linear, so Lagrange with $\nabla f=\langle1,1,1\rangle$.",
        r"System: $1=2\lambda(x-1)$, $1=2\lambda y$, $1=2\lambda z$. Hence $x-1=y=z=\dfrac{1}{2\lambda}$.",
        r"Substitute: $3\left(\dfrac{1}{2\lambda}\right)^2=1\Rightarrow \dfrac{1}{2\lambda}=\pm\dfrac{1}{\sqrt3}$.",
        r"Taking the $+$ branch, $x=1+\tfrac{1}{\sqrt3},\ y=z=\tfrac{1}{\sqrt3}$, so $f=1+\tfrac{3}{\sqrt3}=1+\sqrt3$. The $-$ branch gives $1-\sqrt3$.",
        r"**Maximum $=1+\sqrt3$.**",
    ],
    trap=r"Same shifted-centre trap as before: $\nabla g=\langle 2(x-1),2y,2z\rangle$. And because the three partials give $x-1=y=z$ (not $x=y=z$), the symmetric guess $x=y=z=1/\sqrt3$ is wrong. The geometric check is $f(\text{centre})+|\nabla f|R=1+\sqrt3\cdot1$.",
    check=lambda: Max(*_lagrange(x + y + z, (x - 1)**2 + y**2 + z**2, 1, (x, y, z))),
    want=1 + sqrt(3),
),

"L17P5": dict(
    steps=[
        r"The constraint $x^2-xy+y^2=1$ is an ellipse (rotated $45^\circ$), a closed bounded curve, so a max and a min both exist.",
        r"Lagrange: $\langle1,1\rangle=\lambda\langle 2x-y,\;2y-x\rangle$, so $1=\lambda(2x-y)$ and $1=\lambda(2y-x)$.",
        r"Setting the two right sides equal: $2x-y=2y-x\Rightarrow 3x=3y\Rightarrow y=x$.",
        r"Constraint: $x^2-x^2+x^2=x^2=1$, so $(1,1)$ and $(-1,-1)$.",
        r"$f(1,1)=2$ and $f(-1,-1)=-2$, so $\boxed{M=2,\ m=-2}$.",
    ],
    trap=r"Differentiating the cross term $-xy$: $\partial_x=-y$, $\partial_y=-x$ — it is easy to drop a sign and get $2x+y$. Also, cancelling $\lambda$ from the two equations is legal here only because $\lambda\ne0$ (if $\lambda=0$ then $1=0$), so you should say so rather than divide blindly.",
    check=lambda: (lambda vals: [Max(*vals), Min(*vals)])(
        _lagrange(x + y, x**2 - x*y + y**2, 1, (x, y))),
    want=[2, -2],
),

# ---------------------------------------------------------------- L18 -------

"L18P1": dict(
    steps=[
        r"The integrand factors, $\sqrt{xy}=\sqrt{x}\,\sqrt{y}$, and the region is the rectangle $[0,4]\times[0,1]$, so the double integral splits into a product of single integrals.",
        r"$\displaystyle\int_0^1\!\!\int_0^4\sqrt{x}\sqrt{y}\,dx\,dy=\left(\int_0^4\sqrt{x}\,dx\right)\left(\int_0^1\sqrt{y}\,dy\right)$.",
        r"$\displaystyle\int_0^4 x^{1/2}dx=\tfrac23 x^{3/2}\Big|_0^4=\tfrac23\cdot 8=\tfrac{16}{3}$.",
        r"$\displaystyle\int_0^1 y^{1/2}dy=\tfrac23$.",
        r"Product: $\dfrac{16}{3}\cdot\dfrac23=\dfrac{32}{9}$.",
    ],
    trap=r"Read the differentials: $dx\,dy$ means the **inner** variable is $x$ (limits $0$ to $4$) and the outer is $y$ (limits $0$ to $1$). Pairing $x$ with $[0,1]$ gives $\tfrac23\cdot\tfrac{16}{3}$ by luck here, but on a non-symmetric integrand the same misreading is fatal. The split into a product is legal **only** because the integrand factors and the limits are constants.",
    check=lambda: integrate(sqrt(x*y), (x, 0, 4), (y, 0, 1)),
    want=Rational(32, 9),
),

"L18P2": dict(
    steps=[
        r"The base is the rectangle $R=[0,3]\times[0,2]$; the solid sits between the floor $z=1$ and the roof $z=e^{x+y}$. On $R$ we have $x+y\ge0$, so $e^{x+y}\ge1$ and the roof really is above the floor everywhere.",
        r"Volume $=\displaystyle\iint_R\big(e^{x+y}-1\big)\,dA=\int_0^2\!\!\int_0^3\big(e^{x}e^{y}-1\big)\,dx\,dy$.",
        r"$\displaystyle\iint_R e^{x}e^{y}\,dA=\left(\int_0^3 e^x dx\right)\left(\int_0^2 e^y dy\right)=(e^3-1)(e^2-1)$.",
        r"$\displaystyle\iint_R 1\,dA=\text{area}(R)=3\cdot2=6$.",
        r"Volume $=(e^3-1)(e^2-1)-6=e^5-e^3-e^2+1-6=e^5-e^3-e^2-5$.",
    ],
    trap=r"Forgetting to subtract the floor: integrating $e^{x+y}$ alone gives the volume under the surface down to $z=0$, not down to $z=1$. The correction is $-\text{area}(R)=-6$, and note $(e^3-1)(e^2-1)$ already contributes $+1$, so the constant is $1-6=-5$, not $-6$. Also $e^{x+y}=e^xe^y$ is what lets the integral factor; $e^{x+y}\ne e^x+e^y$.",
    check=lambda: integrate(exp(x + y) - 1, (x, 0, 3), (y, 0, 2)).expand(),
    want=exp(5) - exp(3) - exp(2) - 5,
),

"L18P3": dict(
    steps=[
        r"The four vertices give the rectangle $R=[-1,1]\times[0,5]$, of area $A=2\cdot5=10$.",
        r"Average value $=\dfrac{1}{A}\displaystyle\iint_R f\,dA=\dfrac{1}{10}\int_0^5\!\!\int_{-1}^{1}x^2y\,dx\,dy$.",
        r"$\displaystyle\int_{-1}^{1}x^2\,dx=\tfrac{x^3}{3}\Big|_{-1}^{1}=\tfrac23$ and $\displaystyle\int_0^5 y\,dy=\tfrac{25}{2}$.",
        r"$\displaystyle\iint_R x^2y\,dA=\tfrac23\cdot\tfrac{25}{2}=\tfrac{25}{3}$.",
        r"Average $=\dfrac{25/3}{10}=\dfrac{5}{6}$.",
    ],
    trap=r"Dividing by the wrong thing, or not dividing at all: the answer to an *average value* question is the integral **over the area**, here $10$. Second trap: $x^2$ is even, so $\int_{-1}^1 x^2dx=\tfrac23$, not $0$ — students who remember 'symmetric interval $\Rightarrow$ zero' from odd integrands kill this problem instantly.",
    check=lambda: integrate(x**2*y, (x, -1, 1), (y, 0, 5)) / ((1 - (-1))*(5 - 0)),
    want=Rational(5, 6),
),

"L18P4": dict(
    steps=[
        r"Innermost is $dz$ and the integrand $e^x$ is free of $z$, so the first integration is just multiplication by the height: $\displaystyle\int_0^{2-y}e^x\,dz=e^x(2-y)$.",
        r"The remaining limits are constants, so $\displaystyle\int_0^1\!\!\int_0^1 e^x(2-y)\,dx\,dy=\left(\int_0^1 e^x dx\right)\left(\int_0^1(2-y)\,dy\right)$.",
        r"$\displaystyle\int_0^1 e^x dx=e-1$.",
        r"$\displaystyle\int_0^1(2-y)\,dy=2-\tfrac12=\tfrac32$.",
        r"Value $=\dfrac32(e-1)$.",
    ],
    trap=r"The order is $dz\,dx\,dy$, so the $z$-limit $2-y$ belongs to the *innermost* integral and depends on the *outermost* variable — perfectly legal, but you must integrate $z$ first and carry $(2-y)$ outward. Attempting to do $dx$ first, or treating the upper limit as $2-x$, both break it. Once $z$ is gone the integral separates only because $e^x$ and $(2-y)$ live in different variables.",
    check=lambda: integrate(exp(x), (z, 0, 2 - y), (x, 0, 1), (y, 0, 1)),
    want=Rational(3, 2)*(exp(1) - 1),
),

"L18P5": dict(
    steps=[
        r"$R$ is a rectangle and the integrand splits as $\dfrac{x^2}{2+x^3}\cdot y$, so the integral is a product of two one-variable integrals.",
        r"$\displaystyle\iint_R\frac{x^2y}{2+x^3}\,dA=\left(\int_1^2\frac{x^2}{2+x^3}\,dx\right)\left(\int_0^4 y\,dy\right)$.",
        r"For the $x$-integral substitute $u=2+x^3$, $du=3x^2dx$, so $x^2dx=\tfrac{du}{3}$; as $x:1\to2$, $u:3\to10$.",
        r"$\displaystyle\int_3^{10}\frac{1}{3u}\,du=\tfrac13\big(\ln 10-\ln 3\big)$.",
        r"$\displaystyle\int_0^4 y\,dy=8$.",
        r"Value $=8\cdot\tfrac13(\ln10-\ln3)=\dfrac{8}{3}\big(\ln10-\ln3\big)=\dfrac83\ln\dfrac{10}{3}$.",
    ],
    trap=r"When you substitute $u=2+x^3$ you must **change the limits** to $u:3\to10$; leaving $1$ and $2$ gives $\tfrac13\ln\tfrac{2}{1}$, a completely different number. The other classic is losing the $\tfrac13$ from $du=3x^2\,dx$.",
    check=lambda: integrate(x**2*y/(2 + x**3), (x, 1, 2), (y, 0, 4)),
    want=Rational(8, 3)*(log(10) - log(3)),
),

# ---------------------------------------------------------------- L19 -------

"L19P1": dict(
    steps=[
        r"$e^{y^4}$ has no elementary antiderivative in $y$, so the inner integral as written is hopeless. That is the signal to **switch the order**.",
        r"Read off the region: $0\le x\le 27$ and $\sqrt[3]{x}\le y\le 3$. The curve $y=\sqrt[3]{x}$ is $x=y^3$, and at $x=27$, $y=3$.",
        r"Describe the same region with $y$ outer: $y$ runs $0\to3$, and for each $y$, $x$ runs from $0$ to $y^3$.",
        r"$\displaystyle\int_0^{27}\!\!\int_{\sqrt[3]{x}}^{3}4e^{y^4}\,dy\,dx=\int_0^3\!\!\int_0^{y^3}4e^{y^4}\,dx\,dy=\int_0^3 4y^3e^{y^4}\,dy$.",
        r"Substitute $u=y^4$, $du=4y^3dy$, limits $u:0\to81$: $\displaystyle\int_0^{81}e^u\,du=e^{81}-1$.",
        r"Value $=e^{81}-1$.",
    ],
    trap=r"Getting the new limits backwards. The old inner limit $y\ge\sqrt[3]{x}$ becomes $x\le y^3$, so the new inner range is $0\le x\le y^3$ — **not** $y^3\le x\le 27$. Sketch the region: it is the piece *above* the cube-root curve, i.e. to the *left* of $x=y^3$. The factor $4$ in the integrand is not decoration; it is exactly the $4y^3$ the substitution needs after the swap.",
    check=lambda: integrate(4*exp(y**4), (x, 0, y**3), (y, 0, 3)),
    want=exp(81) - 1,
),

"L19P2": dict(
    steps=[
        r"Sketch $R$: bounded below by $y=0$, above by $y=x$, on the right by $x=1$ — the triangle with vertices $(0,0),(1,0),(1,1)$.",
        r"$\dfrac{\sin x}{x}$ has no elementary antiderivative in $x$, so we must integrate in $y$ first (as instructed), which makes $x$ a constant.",
        r"$\displaystyle\iint_R\frac{\sin x}{x}\,dA=\int_0^1\!\!\int_0^{x}\frac{\sin x}{x}\,dy\,dx$.",
        r"Inner: $\dfrac{\sin x}{x}\cdot(x-0)=\sin x$. The offending $x$ in the denominator cancels — that is the whole point of the order.",
        r"$\displaystyle\int_0^1\sin x\,dx=-\cos x\Big|_0^1=1-\cos(1)$.",
    ],
    trap=r"Choosing $dy\,dx$ is not optional here: the other order gives $\int_y^1\frac{\sin x}{x}dx$, which cannot be evaluated in closed form. Also the inner limits are $0\le y\le x$ — a *variable* upper limit. Writing $\int_0^1$ for the inner $y$-integral turns the triangle into the unit square and gives $\int_0^1\frac{\sin x}{x}dx$, which is not elementary.",
    check=lambda: integrate(sin(x)/x, (y, 0, x), (x, 0, 1)),
    want=1 - cos(1),
),

"L19P3": dict(
    steps=[
        r"The base region $D$ is the triangle in the first quadrant cut off by $x+y=1$: vertices $(0,0),(1,0),(0,1)$. The roof is $z=2x\ge0$ there, so the volume is the plain double integral.",
        r"As a type-I region: $0\le x\le 1$ and $0\le y\le 1-x$.",
        r"$V=\displaystyle\iint_D 2x\,dA=\int_0^1\!\!\int_0^{1-x}2x\,dy\,dx$.",
        r"Inner: $2x(1-x)=2x-2x^2$.",
        r"$\displaystyle\int_0^1(2x-2x^2)\,dx=1-\tfrac23=\tfrac13$.",
    ],
    trap=r"Using $\int_0^1\int_0^1$ (the square) instead of the triangle: the hypotenuse $y=1-x$ must appear as the inner limit. Also note the integrand is $2x$, so the answer is **not** the triangle's area $\tfrac12$ times anything obvious; you have to actually integrate $2x(1-x)$.",
    check=lambda: integrate(2*x, (y, 0, 1 - x), (x, 0, 1)),
    want=Rational(1, 3),
),

"L19P4": dict(
    steps=[
        r"Read the region from the given order $dy\,dx$: $0\le x\le2$ and $x^2\le y\le 2x$ — the lens between the parabola $y=x^2$ and the line $y=2x$.",
        r"Find where the two curves meet: $x^2=2x\Rightarrow x=0$ or $x=2$, giving the corner points $(0,0)$ and $(2,4)$. So $y$ ranges over $[0,4]$ overall.",
        r"Now solve each boundary for $x$. From $y=2x$ we get $x=\dfrac{y}{2}$; from $y=x^2$ (with $x\ge0$) we get $x=\sqrt{y}$.",
        r"For a fixed $y\in[0,4]$, which is the left edge? Test $y=1$: the line gives $x=\tfrac12$, the parabola gives $x=1$. So $x$ runs from $\dfrac{y}{2}$ **up to** $\sqrt{y}$.",
        r"Reversed order: $\displaystyle\int_0^4\!\!\int_{y/2}^{\sqrt{y}}f(x,y)\,dx\,dy$.",
        r"Confidence check with a test integrand $f=xy$: the original order gives $\tfrac83$, and $\int_0^4\int_{y/2}^{\sqrt y}xy\,dx\,dy=\tfrac83$ as well.",
    ],
    trap=r"Inside the lens the parabola is the **right** boundary and the line is the **left** one (for $0<x<2$, $x^2<2x$ means the parabola sits *below* the line, which flips to *right of* when you read horizontally). Writing $\int_{\sqrt y}^{y/2}$ reverses the limits and negates the integral. Also $x=\sqrt y$, not $x=\pm\sqrt y$: the region lives in $x\ge0$.",
    right=r"$\displaystyle\int_0^4\!\!\int_{y/2}^{\sqrt{y}}f(x,y)\,dx\,dy$",
    fix=r"The official answer prints the inner limits as $\int_{\sqrt y}^{y/2}$, which is upside down. For $0<y<4$ we have $\tfrac{y}{2}<\sqrt{y}$ (at $y=1$: $0.5<1$), so the lower limit must be $y/2$ and the upper limit $\sqrt y$. As printed, the integral equals the negative of the original. Numerical check with $f(x,y)=xy$: the original iterated integral is $\tfrac83$, the correctly reversed one is $\tfrac83$, and the printed one is $-\tfrac83$.",
),

"L19P5": dict(
    steps=[
        r"$e^{x^2}$ has no elementary antiderivative, so the order must be reversed. Let $a=\sqrt{\ln 3}$ for short; the limits are $0\le y\le 2a$ and $\dfrac{y}{2}\le x\le a$.",
        r"Sketch: the region is the triangle with vertices $(0,0)$, $(a,0)$ and $(a,2a)$, bounded by the line $x=y/2$ (i.e. $y=2x$), the vertical line $x=a$, and the $x$-axis.",
        r"Reading it the other way: $x$ runs $0\to a$, and for each $x$, $y$ runs from $0$ to $2x$.",
        r"$\displaystyle\int_0^{2a}\!\!\int_{y/2}^{a}e^{x^2}\,dx\,dy=\int_0^{a}\!\!\int_0^{2x}e^{x^2}\,dy\,dx=\int_0^{a}2x\,e^{x^2}\,dx$.",
        r"Substitute $u=x^2$, $du=2x\,dx$, $u:0\to a^2=\ln3$: $\displaystyle\int_0^{\ln3}e^u\,du=e^{\ln3}-1=3-1=2$.",
        r"Value $=2$.",
    ],
    trap=r"The outer limit $2\sqrt{\ln3}$ and the inner $\sqrt{\ln3}$ are *different* numbers — reversing carelessly and writing $y$ from $0$ to $x$ (instead of $2x$) loses the factor of $2$ that the substitution needs, leaving a non-elementary integral. Also $e^{\ln 3}=3$, so the final answer is the clean $2$, not $e^{\ln 3}$ left unsimplified.",
    check=lambda: integrate(exp(x**2), (y, 0, 2*x), (x, 0, sqrt(log(3)))),
    want=2,
),

# ---------------------------------------------------------------- L20 -------

"L20P1": dict(
    steps=[
        r"Identify the region: $0\le x\le3$ and $0\le y\le\sqrt{9-x^2}$, i.e. $x^2+y^2\le9$ with $x,y\ge0$ — the **quarter** disk of radius $3$ in the first quadrant.",
        r"Polar: $x=r\cos\theta$, $y=r\sin\theta$, $\sqrt{x^2+y^2}=r$, and $dA=r\,dr\,d\theta$. The region is $0\le r\le3$, $0\le\theta\le\dfrac{\pi}{2}$.",
        r"$\displaystyle\int_0^3\!\!\int_0^{\sqrt{9-x^2}}\sqrt{x^2+y^2}\,dy\,dx=\int_0^{\pi/2}\!\!\int_0^3 r\cdot r\,dr\,d\theta=\int_0^{\pi/2}\!\!\int_0^3 r^2\,dr\,d\theta$.",
        r"Inner: $\dfrac{r^3}{3}\Big|_0^3=9$.",
        r"Outer: $9\cdot\dfrac{\pi}{2}=\dfrac{9\pi}{2}$.",
    ],
    trap=r"The integrand becomes $r^2$, not $r$: one factor of $r$ is $\sqrt{x^2+y^2}$ and the second is the **Jacobian** from $dA=r\,dr\,d\theta$. Dropping the Jacobian gives $\tfrac{9\pi}{4}$. Second trap: $\theta$ runs only to $\pi/2$ — the limits $x\in[0,3]$, $y\ge0$ give a quarter disk, not a half disk.",
    check=lambda: integrate(r*r, (r, 0, 3), (th, 0, pi/2)),
    want=9*pi/2,
),

"L20P2": dict(
    steps=[
        r"$R$ is the full disk of radius $2$ and the integrand depends only on $x^2+y^2$, so polar is the obvious move: $0\le r\le2$, $0\le\theta\le2\pi$.",
        r"$\displaystyle\iint_R e^{-(x^2+y^2)}\,dA=\int_0^{2\pi}\!\!\int_0^{2}e^{-r^2}\,r\,dr\,d\theta$.",
        r"Inner: substitute $u=r^2$, $du=2r\,dr$, so $\displaystyle\int_0^2 e^{-r^2}r\,dr=\tfrac12\int_0^4 e^{-u}du=\tfrac12\big(1-e^{-4}\big)$.",
        r"Outer: multiply by $\displaystyle\int_0^{2\pi}d\theta=2\pi$.",
        r"Value $=2\pi\cdot\tfrac12\big(1-e^{-4}\big)=\pi\big(1-e^{-4}\big)$.",
    ],
    trap=r"Without the Jacobian $r$, $\int e^{-r^2}dr$ is not elementary at all — the $r$ is exactly what makes the substitution work, so its absence should be an immediate alarm. Also $r$ goes to $2$, so $u=r^2$ goes to $4$, giving $e^{-4}$; writing $e^{-2}$ is the standard slip.",
    check=lambda: integrate(exp(-r**2)*r, (r, 0, 2), (th, 0, 2*pi)),
    want=pi*(1 - exp(-4)),
),

"L20P3": dict(
    steps=[
        r"Region: $0\le y\le1$ with $-\sqrt{1-y^2}\le x\le\sqrt{1-y^2}$, i.e. $x^2+y^2\le1$ with $y\ge0$ — the **upper half** of the unit disk.",
        r"In polar the half disk is $0\le r\le1$, $0\le\theta\le\pi$ (the full sweep of the upper half plane).",
        r"The integrand $(x^2+y^2)^{1/2}=r$, and $dA=r\,dr\,d\theta$, so $r\cdot r=r^2$.",
        r"$\displaystyle\int_0^1\!\!\int_{-\sqrt{1-y^2}}^{\sqrt{1-y^2}}(x^2+y^2)^{1/2}\,dx\,dy=\int_0^{\pi}\!\!\int_0^1 r^2\,dr\,d\theta$.",
        r"(Not asked for, but its value is $\dfrac{\pi}{3}$, and the original Cartesian integral evaluates to $\dfrac{\pi}{3}$ as well.)",
    ],
    trap=r"$\theta$ ranges over $[0,\pi]$, not $[0,\pi/2]$: $x$ takes **negative** values here, so the region covers the second quadrant too. And the integrand must pick up the Jacobian, $r\cdot r\,dr\,d\theta=r^2dr\,d\theta$; writing $\int_0^\pi\int_0^1 r\,dr\,d\theta$ is the most common wrong answer on this exact problem.",
    check=lambda: integrate(r*r, (r, 0, 1), (th, 0, pi)),
    want=pi/3,
),

"L20P4": dict(
    steps=[
        r"Region: $0\le y\le\sqrt{\pi}$, $0\le x\le\sqrt{\pi-y^2}$, i.e. $x^2+y^2\le\pi$ with $x,y\ge0$ — the quarter disk of radius $\sqrt{\pi}$.",
        r"$\sin(x^2+y^2)$ has no elementary antiderivative in Cartesian form, so polar is forced: $0\le r\le\sqrt{\pi}$, $0\le\theta\le\dfrac{\pi}{2}$.",
        r"$\displaystyle\int_0^{\sqrt\pi}\!\!\int_0^{\sqrt{\pi-y^2}}\sin(x^2+y^2)\,dx\,dy=\int_0^{\pi/2}\!\!\int_0^{\sqrt{\pi}}\sin(r^2)\,r\,dr\,d\theta$.",
        r"Inner: $u=r^2$, $du=2r\,dr$, $u:0\to\pi$, giving $\tfrac12\displaystyle\int_0^{\pi}\sin u\,du=\tfrac12\big(-\cos u\big)\Big|_0^{\pi}=\tfrac12(1+1)=1$.",
        r"Outer: $1\cdot\dfrac{\pi}{2}=\dfrac{\pi}{2}$.",
    ],
    trap=r"The radius is $\sqrt{\pi}$, so $u=r^2$ runs to $\pi$ — not to $\sqrt\pi$. Writing $\int_0^{\sqrt\pi}\sin u\,du$ is the killer here. As always, the Jacobian $r$ is what makes the $u$-substitution possible; without it the integral is non-elementary.",
    check=lambda: integrate(sin(r**2)*r, (r, 0, sqrt(pi)), (th, 0, pi/2)),
    want=pi/2,
),

"L20P5": dict(
    steps=[
        r"Region: $-3\le y\le3$ and $-\sqrt{9-y^2}\le x\le\sqrt{9-y^2}$ — the **entire** disk $x^2+y^2\le9$ of radius $3$.",
        r"Polar: $0\le r\le3$, $0\le\theta\le2\pi$, integrand $e^{x^2+y^2}=e^{r^2}$, and $dA=r\,dr\,d\theta$.",
        r"$\displaystyle\int_{-3}^{3}\!\int_{-\sqrt{9-y^2}}^{\sqrt{9-y^2}}e^{x^2+y^2}\,dx\,dy=\int_0^{2\pi}\!\!\int_0^{3}e^{r^2}r\,dr\,d\theta$.",
        r"Inner: $u=r^2$, $du=2r\,dr$, $u:0\to9$, so $\tfrac12\displaystyle\int_0^9 e^u\,du=\tfrac12\big(e^9-1\big)$.",
        r"Outer: $2\pi\cdot\tfrac12(e^9-1)=\pi\big(e^9-1\big)$.",
    ],
    trap=r"Both limits are symmetric, so $\theta$ sweeps the **full** $2\pi$; using $\pi$ (half disk) or $\pi/2$ halves or quarters the answer. And $u=r^2$ runs to $9$, giving $e^9$ — writing $e^3$ is the standard misfire. The $r$ from $dA$ is again mandatory.",
    check=lambda: integrate(exp(r**2)*r, (r, 0, 3), (th, 0, 2*pi)),
    want=pi*(exp(9) - 1),
),

}
