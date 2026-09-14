"""Worked solutions for Lessons 25-28 (vector fields, line integrals, FTLI)
of the official MA 261 study guide."""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, acos, atan, pi,
                   exp, log, symbols, diff, integrate, limit, simplify, solve,
                   Eq, oo, Abs, sinh, cosh, atan2)

x, y, z = symbols("x y z", real=True)
r, th, ph, t, u, v = symbols("r theta phi t u v", real=True)


def V(*c):
    return Matrix(list(c))


# A nonzero placeholder for y, so sympy's antiderivative of -y*sin(xy)
# does not split into a Piecewise around the degenerate case y = 0.
_yp = symbols("y_p", positive=True)


def _potential_of_exp_sin():
    r"""Derive a potential for F = <e^{yz}-y sin(xy), zx e^{yz}-x sin(xy), xy e^{yz}>
    by antidifferentiating the first component in x, then confirming that the
    gradient of the result really is F before handing it back."""
    F = V(exp(_yp*z) - _yp*sin(x*_yp),
          z*x*exp(_yp*z) - x*sin(x*_yp),
          x*_yp*exp(_yp*z))
    phi = integrate(F[0], x)                      # constant of integration g(y,z)
    phi = phi + integrate(simplify(F[1] - diff(phi, _yp)), _yp)
    phi = phi + integrate(simplify(F[2] - diff(phi, z)), z)
    grad = V(diff(phi, x), diff(phi, _yp), diff(phi, z))
    assert simplify(grad - F) == Matrix.zeros(3, 1), "not a potential"
    return simplify(phi.subs(_yp, y))


def _potential_of_sin_y():
    r"""Derive a potential for F = <sin y, x cos y>, then pin the free additive
    constant by matching the instructor's normalization phi(0, 0) = 1."""
    F = V(sin(y), x*cos(y))
    assert simplify(diff(F[0], y) - diff(F[1], x)) == 0, "not conservative"
    phi = integrate(F[0], x)
    phi = phi + integrate(simplify(F[1] - diff(phi, y)), y)
    assert simplify(V(diff(phi, x), diff(phi, y)) - F) == Matrix.zeros(2, 1)
    C = solve(Eq(phi.subs([(x, 0), (y, 0)]) + u, 1), u)[0]
    return simplify(phi + C)


def _ftli(F, start, end, var=(x, y, z)):
    """Fundamental Theorem of Line Integrals, done honestly.

    Derives the potential from F by successive antidifferentiation, *asserts*
    that its gradient really is F (so a wrong potential cannot slip through),
    then returns phi(end) - phi(start). Writing the potential down from memory
    and evaluating it would verify only the arithmetic.
    """
    a, b, c = var
    phi = integrate(F[0], a)
    phi = phi + integrate(simplify(F[1] - diff(phi, b)), b)
    phi = phi + integrate(simplify(F[2] - diff(phi, c)), c)
    grad = V(diff(phi, a), diff(phi, b), diff(phi, c))
    assert simplify(grad - F) == Matrix.zeros(3, 1), "not a potential for F"
    sub = lambda P: phi.subs(list(zip(var, P)))
    return simplify(sub(end) - sub(start))


SOL = {

# ===================== L25  Vector Fields  §17.1 =====================

"L25P1": dict(
    steps=[
        r"We want $\varphi$ with $\nabla\varphi=\vec F$, so **start with the component that is easiest to antidifferentiate** and then patch it up.",
        r"Integrate the first component in $x$, holding $y,z$ fixed: $\varphi=\displaystyle\int\big(e^{yz}-y\sin(xy)\big)\,dx = xe^{yz}+\cos(xy)+g(y,z)$.",
        r"The sign is the whole game here: $\dfrac{d}{dx}\cos(xy)=-y\sin(xy)$, so the antiderivative of $-y\sin(xy)$ is $+\cos(xy)$.",
        r"Now differentiate that candidate in $y$: $\varphi_y = xze^{yz}-x\sin(xy)+g_y$.",
        r"Compare with the given second component $zxe^{yz}-x\sin(xy)$: they already match, so $g_y=0$.",
        r"Differentiate in $z$: $\varphi_z = xye^{yz}+g_z$, and the third component is $xye^{yz}$, so $g_z=0$ too. Hence $g$ is a constant.",
        r"$\varphi = xe^{yz}+\cos(xy)$ (any additive constant is also a potential).",
    ],
    trap=r"Writing $\int -y\sin(xy)\,dx = -\cos(xy)$. The $-y$ out front is exactly the inner derivative, so the two minus signs cancel and you get $+\cos(xy)$. Getting this backwards still passes a careless $\varphi_x$ check if you also flip the sign when differentiating.",
    check=_potential_of_exp_sin,
    want=x*exp(y*z) + cos(x*y),
),

"L25P2": dict(
    steps=[
        r"$C$ is the level curve $g(x,y)=a$ of $g(x,y)=x^2-2y^2$.",
        r"Key fact: the gradient of $g$ is **normal to every level curve of $g$**, hence orthogonal to the tangent of $C$ at each point.",
        r"$\nabla g=\langle g_x,g_y\rangle = \langle 2x,\,-4y\rangle$.",
        r"So $\vec F=\langle 2x,-4y\rangle$ is orthogonal to $\vec T$ at every $(x_0,y_0)$ on $C$ (and so is any scalar multiple of it).",
        r"Sanity check by hand: implicit differentiation of $x^2-2y^2=a$ gives $2x-4y\,y'=0$, so $\vec T\parallel\langle 4y,2x\rangle$, and $\langle 2x,-4y\rangle\cdot\langle 4y,2x\rangle = 8xy-8xy=0$.",
    ],
    trap=r"Dropping the minus sign and answering $\langle 2x,4y\rangle$ — that is $\nabla(x^2+2y^2)$, the normal to an **ellipse**, not to this hyperbola. The other classic miss is handing back the tangent $\langle 4y,2x\rangle$ instead of the normal.",
    check=lambda: V(diff(x**2 - 2*y**2, x), diff(x**2 - 2*y**2, y)),
    want=V(2*x, -4*y),
),

"L25P3": dict(
    steps=[
        r"Counterclockwise rotation means the field is tangent to circles centered at the origin, pointing in the direction of increasing angle.",
        r"Parametrize a circle the counterclockwise way: $\vec r(t)=\langle\cos t,\sin t\rangle$.",
        r"The direction of travel is $\vec r\,{}'(t)=\langle-\sin t,\cos t\rangle$.",
        r"Rewrite that at the point itself, using $x=\cos t$, $y=\sin t$: the tangent direction is $\langle -y,\,x\rangle$.",
        r"Spot-check the description: above the $x$-axis take $(0,1)$, giving $\langle-1,0\rangle$ (points left); below take $(0,-1)$, giving $\langle1,0\rangle$ (points right). Matches.",
        r"$\vec F=\langle -y,\,x\rangle$.",
    ],
    trap=r"Answering $\langle y,-x\rangle$, which is the same picture run **clockwise**. Always test one concrete point above the $x$-axis rather than trusting the sign pattern; $\langle y,-x\rangle$ gives $\langle1,0\rangle$ at $(0,1)$, pointing right, which is the wrong rotation.",
    check=lambda: diff(V(cos(t), sin(t)), t).subs([(sin(t), y), (cos(t), x)]),
    want=V(-y, x),
),

"L25P4": dict(
    steps=[
        r"$\operatorname{div}(\nabla f)$ is the **Laplacian** $f_{xx}+f_{yy}+f_{zz}$ — a scalar, not a vector.",
        r"$\nabla f=\langle y^2z^3,\;2xyz^3,\;3xy^2z^2\rangle$.",
        r"Take the matching partial of each component: $f_{xx}=\partial_x(y^2z^3)=0$, $f_{yy}=\partial_y(2xyz^3)=2xz^3$, $f_{zz}=\partial_z(3xy^2z^2)=6xy^2z$.",
        r"So $\operatorname{div}(\nabla f)=0+2xz^3+6xy^2z$.",
        r"At $(2,-1,1)$: $2(2)(1)^3+6(2)(-1)^2(1)=4+12=16$.",
    ],
    trap=r"Two traps. First, differentiating the wrong slot — you must take $\partial_x$ of the **first** component, $\partial_y$ of the second, $\partial_z$ of the third, not all three of one component. Second, $(-1)^2=+1$: plugging $y=-1$ into $6xy^2z$ gives $+12$, and writing $-12$ turns $16$ into $-8$.",
    check=lambda: sum(diff(x*y**2*z**3, w, 2) for w in (x, y, z)).subs(
        [(x, 2), (y, -1), (z, 1)]),
    want=S(16),
),

# ============ L26  Line Integrals of Functions  §17.2 ============

"L26P1": dict(
    steps=[
        r"Scalar line integral: $\displaystyle\int_C f\,ds=\int_a^b f(\vec r(t))\,|\vec r\,{}'(t)|\,dt$.",
        r"Here $\vec r\,{}'(t)=\langle1,1\rangle$, so $|\vec r\,{}'(t)|=\sqrt{2}$ and $ds=\sqrt2\,dt$.",
        r"On $C$ we have $x=t$, $y=t$, so $f(\vec r(t))=\sin(2\pi t)+t^2$.",
        r"Set up: $\displaystyle\int_0^1\big(\sin(2\pi t)+t^2\big)\sqrt2\,dt$.",
        r"$\displaystyle\int_0^1\sin(2\pi t)\,dt=\Big[-\frac{\cos(2\pi t)}{2\pi}\Big]_0^1=-\frac{1}{2\pi}+\frac{1}{2\pi}=0$ — a full period integrates away.",
        r"$\displaystyle\int_0^1 t^2\,dt=\frac13$, so the value is $\sqrt2\cdot\frac13=\frac{\sqrt2}{3}$.",
    ],
    trap=r"Forgetting the $|\vec r\,{}'|=\sqrt2$ factor and reporting $\tfrac13$. The parametrization $\langle t,t\rangle$ is not unit speed even though it looks tame — $ds\ne dt$ here.",
    check=lambda: integrate((sin(2*pi*t) + t*t)*sqrt(2), (t, 0, 1)),
    want=sqrt(2)/3,
),

"L26P2": dict(
    steps=[
        r"$\vec r\,{}'(t)=\langle-\sin t,\cos t,1\rangle$, so $|\vec r\,{}'(t)|=\sqrt{\sin^2t+\cos^2t+1}=\sqrt2$.",
        r"The helix has **constant speed** $\sqrt2$, so $ds=\sqrt2\,dt$.",
        r"On $C$, $xy=\cos t\sin t$.",
        r"Set up: $\displaystyle\int_0^{\pi/2}\cos t\,\sin t\,\sqrt2\,dt$.",
        r"Substitute $u=\sin t$: $\displaystyle\sqrt2\int_0^1 u\,du=\sqrt2\cdot\frac12=\frac{\sqrt2}{2}$.",
    ],
    trap=r"Reading the first two components as a unit circle and concluding $|\vec r\,{}'|=1$. The $z=t$ component contributes a $1$ under the radical, making the speed $\sqrt2$; dropping it halves-by-$\sqrt2$ the answer to $\tfrac12$.",
    check=lambda: integrate(cos(t)*sin(t)*sqrt(2), (t, 0, pi/2)),
    want=sqrt(2)/2,
),

"L26P3": dict(
    steps=[
        r"Parametrize the segment from $(1,0)$ to $(5,3)$ as $\vec r(t)=\langle1,0\rangle+t\langle4,3\rangle=\langle1+4t,\;3t\rangle$, $0\le t\le1$.",
        r"$\vec r\,{}'(t)=\langle4,3\rangle$, so $|\vec r\,{}'(t)|=\sqrt{16+9}=5$ and $ds=5\,dt$ (the length of the segment, spread over $t\in[0,1]$).",
        r"The integrand simplifies beautifully: $x-y=(1+4t)-3t=1+t$, so $\dfrac{1}{(x-y)^2}=\dfrac{1}{(1+t)^2}$.",
        r"Set up: $\displaystyle\int_0^1\frac{5}{(1+t)^2}\,dt$.",
        r"$=5\Big[-\frac{1}{1+t}\Big]_0^1 = 5\Big(-\frac12+1\Big)=\frac52$.",
    ],
    trap=r"Using $dx$ instead of $ds$. If you parametrize by $x$ with $y=\tfrac34(x-1)$ you must carry $ds=\sqrt{1+(3/4)^2}\,dx=\tfrac54\,dx$; dropping that factor gives $2$ instead of $\tfrac52$. Also note the line never crosses $x=y$, so the integrand stays finite.",
    check=lambda: integrate(5/((1 + 4*t) - 3*t)**2, (t, 0, 1)),
    want=Rational(5, 2),
),

"L26P4": dict(
    steps=[
        r"The circle has radius $2$, so $\vec r(t)=\langle2\cos t,\,2\sin t\rangle$.",
        r"**Pick the range that gives $x\ge0$, not $y\ge0$**: $x=2\cos t\ge0$ forces $-\tfrac\pi2\le t\le\tfrac\pi2$ (the right half).",
        r"$\vec r\,{}'(t)=\langle-2\sin t,2\cos t\rangle$, so $|\vec r\,{}'(t)|=2$ and $ds=2\,dt$.",
        r"Set up: $\displaystyle\int_{-\pi/2}^{\pi/2}(2\cos t)(2)\,dt=4\int_{-\pi/2}^{\pi/2}\cos t\,dt$.",
        r"$=4\big[\sin t\big]_{-\pi/2}^{\pi/2}=4(1-(-1))=8$.",
    ],
    trap=r"Taking $0\le t\le\pi$ out of habit. That traces the **upper** half ($y\ge0$), over which $\int x\,ds=0$ by symmetry — a suspiciously clean wrong answer. The condition is $x\ge0$, so center the interval on $t=0$.",
    check=lambda: integrate(2*cos(t)*2, (t, -pi/2, pi/2)),
    want=S(8),
),

"L26P5": dict(
    steps=[
        r"Arc length is $\displaystyle L=\int_a^b|\vec r\,{}'(t)|\,dt$.",
        r"$\vec r\,{}'(t)=\langle-4\sin t,\,4\cos t,\,3\rangle$.",
        r"$|\vec r\,{}'(t)|=\sqrt{16\sin^2t+16\cos^2t+9}=\sqrt{16+9}=5$ — constant speed, the hallmark of a circular helix.",
        r"Set up: $\displaystyle L=\int_0^{2\pi}5\,dt=5(2\pi)=10\pi$.",
    ],
    trap=r"Adding the radius and the pitch coordinate as if speed were $4+3=7$, or forgetting the $3$ entirely and getting $8\pi$ (the circumference of the shadow circle). The helix is strictly longer than its projection because of the climb.",
    check=lambda: integrate(
        sqrt(sum(c**2 for c in diff(V(4*cos(t), 4*sin(t), 3*t), t))),
        (t, 0, 2*pi)),
    want=10*pi,
),

# ========= L27  Line Integrals of Vector Fields  §17.2 =========

"L27P1": dict(
    steps=[
        r"Work is $\displaystyle W=\int_C\vec F\cdot d\vec r=\int_a^b\vec F(\vec r(t))\cdot\vec r\,{}'(t)\,dt$.",
        r"Find the $t$-range from the endpoints: $(2,0)$ is $t=0$ and $(0,3)$ is $t=\tfrac\pi2$, so we travel a **quarter** of the ellipse.",
        r"On $C$: $\vec F(\vec r(t))=\langle-y,x\rangle=\langle-3\sin t,\,2\cos t\rangle$ and $\vec r\,{}'(t)=\langle-2\sin t,\,3\cos t\rangle$.",
        r"Dot them: $6\sin^2t+6\cos^2t=6$ — the integrand is constant.",
        r"Set up: $\displaystyle W=\int_0^{\pi/2}6\,dt=6\cdot\frac{\pi}{2}=3\pi$.",
    ],
    trap=r"Reaching for Green's theorem. $C$ is an open quarter-arc, not a closed curve, so Green does not apply; and $\vec F=\langle-y,x\rangle$ is **not** conservative ($P_y=-1\ne1=Q_x$), so the path genuinely matters and FTLI is off the table. You must integrate along this arc.",
    check=lambda: integrate(
        V(-3*sin(t), 2*cos(t)).dot(diff(V(2*cos(t), 3*sin(t)), t)),
        (t, 0, pi/2)),
    want=3*pi,
),

"L27P2": dict(
    steps=[
        r"Flux uses the stated formula $\displaystyle\int_C P\,dy-Q\,dx$ with $P=x$, $Q=y$ — note $dy$ pairs with $P$, not with $Q$.",
        r"From $\vec r(t)=\langle3\cos t,2\sin t\rangle$: $dx=-3\sin t\,dt$ and $dy=2\cos t\,dt$.",
        r"Substitute: $P\,dy-Q\,dx=(3\cos t)(2\cos t)\,dt-(2\sin t)(-3\sin t)\,dt$.",
        r"$=6\cos^2t+6\sin^2t=6$, constant again.",
        r"Set up: $\displaystyle\int_{-\pi}^{\pi}6\,dt=6(2\pi)=12\pi$.",
        r"Cross-check with the divergence form: $\operatorname{div}\vec F=2$ and the ellipse encloses area $\pi(3)(2)=6\pi$, so the flux is $2\cdot6\pi=12\pi$.",
    ],
    trap=r"Computing circulation $\int P\,dx+Q\,dy$ instead of flux. With this field that swap gives $\int(-6\sin t\cos t+6\sin t\cos t)\,dt=0$, so the mistake produces a clean $0$ and looks deliberate. Keep the pairing $P\,dy-Q\,dx$ straight.",
    check=lambda: integrate(
        3*cos(t)*diff(2*sin(t), t) - 2*sin(t)*diff(3*cos(t), t),
        (t, -pi, pi)),
    want=12*pi,
),

"L27P3": dict(
    steps=[
        r"Parametrize the segment: $\vec r(t)=\langle2t,3t,4t\rangle$, $0\le t\le1$, so $\vec r\,{}'(t)=\langle2,3,4\rangle$.",
        r"Evaluate the field **on the curve**, remembering the components are shifted: $\vec F=\langle y,z,x\rangle=\langle3t,\,4t,\,2t\rangle$.",
        r"Dot: $\vec F\cdot\vec r\,{}'=6t+12t+8t=26t$.",
        r"Set up: $\displaystyle W=\int_0^1 26t\,dt=26\cdot\frac12=\frac{26}{2}=13$.",
    ],
    trap=r"Substituting $\vec F=\langle2t,3t,4t\rangle$, i.e. reading $\langle y,z,x\rangle$ as $\langle x,y,z\rangle$. That gives $\int_0^1 29t\,dt$ and the wrong number. The cyclic shift is the entire content of this problem. (Also: $\vec F=\langle y,z,x\rangle$ is **not** conservative, since $P_y=1$ but $Q_x=0$, so you must integrate.)",
    check=lambda: integrate(
        V(3*t, 4*t, 2*t).dot(diff(V(2*t, 3*t, 4*t), t)), (t, 0, 1)),
    want=Rational(26, 2),
),

"L27P4": dict(
    steps=[
        r"The problem says 'a smooth curve' without naming it, which is the signal that $\vec F$ must be **conservative** — otherwise the answer would not be well defined.",
        r"Hunt for $\varphi$: integrate the first component in $x$, $\displaystyle\int ye^z\,dx = xye^z+g(y,z)$.",
        r"Match the second component: $\varphi_y=xe^z+g_y$ must equal $e^y+xe^z$, so $g_y=e^y$ and $g=e^y+h(z)$.",
        r"Match the third: $\varphi_z=xye^z+h'(z)$ must equal $xye^z$, so $h$ is constant. Take $\varphi=xye^z+e^y$.",
        r"FTLI: $\displaystyle\int_C\vec F\cdot\vec T\,ds=\int_C\vec F\cdot d\vec r=\varphi(-1,1,1)-\varphi(0,0,0)$.",
        r"$\varphi(-1,1,1)=(-1)(1)e^1+e^1=-e+e=0$ and $\varphi(0,0,0)=0+e^0=1$.",
        r"Value $=0-1=-1$.",
    ],
    trap=r"Evaluating $\varphi$ at the **start** minus the end. FTLI is end minus start, and here that sign error hands you $+1$. Second trap: forgetting the $e^y$ piece because it does not appear in $\varphi_x$ — it is exactly what makes $\varphi(0,0,0)=1$ rather than $0$.",
    check=lambda: ((x*y*exp(z) + exp(y)).subs([(x, -1), (y, 1), (z, 1)])
                   - (x*y*exp(z) + exp(y)).subs([(x, 0), (y, 0), (z, 0)])),
    want=S(-1),
),

"L27P5": dict(
    steps=[
        r"Again the curve is unspecified, so test for conservativity: with $P=2xy-yz$, $Q=x^2-xz$, $R=-xy$ we get $P_y=2x-z=Q_x$, $P_z=-y=R_x$, $Q_z=-x=R_y$. All three match, so $\vec F$ is conservative.",
        r"Build $\varphi$: $\displaystyle\int(2xy-yz)\,dx = x^2y-xyz+g(y,z)$.",
        r"Check $\varphi_y=x^2-xz+g_y$ against $Q=x^2-xz$: $g_y=0$. Check $\varphi_z=-xy+g_z$ against $R=-xy$: $g_z=0$. So $\varphi=x^2y-xyz$.",
        r"FTLI: value $=\varphi(3,2,-1)-\varphi(2,1,0)$.",
        r"$\varphi(3,2,-1)=9(2)-(3)(2)(-1)=18+6=24$.",
        r"$\varphi(2,1,0)=4(1)-0=4$.",
        r"Value $=24-4=20$.",
    ],
    trap=r"Sign-slipping on $-xyz$ at the endpoint with $z=-1$: $-(3)(2)(-1)=+6$, so $\varphi(3,2,-1)=24$, not $12$. Writing $18-6$ gives $8$ and is the single most common wrong answer here.",
    check=lambda: _ftli(V(2*x*y - y*z, x**2 - x*z, -x*y), (2, 1, 0), (3, 2, -1)),
    want=S(20),
),

# ===== L28  Fundamental Theorem of Line Integrals  §17.3 =====

"L28P1": dict(
    steps=[
        r"The path is only described as 'a smooth curve', so the integral had better be path-independent — first verify $\vec F$ is conservative.",
        r"With $P=2xy-yz$, $Q=x^2-xz$, $R=-xy$: $P_y=2x-z=Q_x$, $P_z=-y=R_x$, $Q_z=-x=R_y$. Conservative.",
        r"Find the potential: $\displaystyle\varphi=\int(2xy-yz)\,dx = x^2y-xyz+g(y,z)$, and both $\varphi_y=x^2-xz$ and $\varphi_z=-xy$ already match, so $g$ is constant.",
        r"$\varphi(x,y,z)=x^2y-xyz$.",
        r"FTLI: $\displaystyle\int_C\vec F\cdot d\vec r=\varphi(3,2,-1)-\varphi(2,1,0)=(18+6)-(4-0)$.",
        r"$=24-4=20$.",
    ],
    trap=r"Trying to parametrize. No curve was given, so any attempt to build one is wasted work — and if you accidentally pick a path while $\vec F$ were **not** conservative, the answer would be meaningless. Confirm the mixed partials first, then use endpoints only. Watch $-xyz$ at $z=-1$, which contributes $+6$.",
    check=lambda: _ftli(V(2*x*y - y*z, x**2 - x*z, -x*y), (2, 1, 0), (3, 2, -1)),
    want=S(20),
),

"L28P2": dict(
    steps=[
        r"Antidifferentiate the first component in $x$: $\displaystyle\varphi=\int\big(e^{yz}-y\sin(xy)\big)\,dx$.",
        r"Term by term, $\int e^{yz}\,dx = xe^{yz}$ (as $x$ varies, $e^{yz}$ is a constant) and $\int -y\sin(xy)\,dx = \cos(xy)$.",
        r"So $\varphi = xe^{yz}+\cos(xy)+g(y,z)$.",
        r"Test against the second component: $\varphi_y = xze^{yz}-x\sin(xy)+g_y$, and we need $zxe^{yz}-x\sin(xy)$, so $g_y=0$.",
        r"Test against the third: $\varphi_z = xye^{yz}+g_z$, and we need $xye^{yz}$, so $g_z=0$.",
        r"Therefore $\varphi = xe^{yz}+\cos(xy)$, up to an additive constant.",
    ],
    trap=r"Differentiating $e^{yz}$ with respect to $y$ and writing $ze^{yz}$ without the $x$ that the antiderivative introduced. The $x$ in $xe^{yz}$ must be carried through, and it is exactly what makes $\varphi_y=xze^{yz}$ match the printed $zxe^{yz}$.",
    check=_potential_of_exp_sin,
    want=x*exp(y*z) + cos(x*y),
),

"L28P3": dict(
    steps=[
        r"First confirm a potential exists: $P=\sin y$, $Q=x\cos y$, and $P_y=\cos y=Q_x$. Conservative on all of $\mathbb R^2$.",
        r"Integrate $P$ in $x$: $\displaystyle\varphi=\int\sin y\,dx = x\sin y+g(y)$.",
        r"Differentiate in $y$: $\varphi_y=x\cos y+g'(y)$, which must equal $Q=x\cos y$, so $g'(y)=0$ and $g$ is any constant.",
        r"The family of potentials is $\varphi=x\sin y+C$. The printed choice takes $C=1$: $\varphi = x\sin y+1$.",
    ],
    trap=r"Rejecting the '$+1$' as a typo. **Potentials are only determined up to an additive constant**, so $x\sin y$, $x\sin y+1$, and $x\sin y-7$ are all correct; on a multiple-choice list the constant is there precisely to see whether you know that. The real error to avoid is $\varphi=-x\cos y$, from mistakenly antidifferentiating $\sin y$ in $y$ instead of $x$.",
    check=_potential_of_sin_y,
    want=x*sin(y) + 1,
),

"L28P4": dict(
    steps=[
        r"$\int_C\vec F\cdot\vec T\,ds$ is just $\int_C\vec F\cdot d\vec r$ rewritten, since $d\vec r=\vec T\,ds$.",
        r"No specific curve is given, so check conservativity: with $P=ye^z$, $Q=e^y+xe^z$, $R=xye^z$ we get $P_y=e^z=Q_x$, $P_z=ye^z=R_x$, $Q_z=xe^z=R_y$. Conservative.",
        r"Potential: $\displaystyle\int ye^z\,dx = xye^z+g(y,z)$; then $\varphi_y=xe^z+g_y = e^y+xe^z$ forces $g_y=e^y$, and $\varphi_z=xye^z+h'(z)=xye^z$ forces $h'=0$.",
        r"$\varphi = xye^z+e^y$.",
        r"FTLI: $\varphi(-1,1,1)-\varphi(0,0,0) = \big((-1)(1)e+e\big)-\big(0+1\big)$.",
        r"$=0-1=-1$.",
    ],
    trap=r"Seeing $\vec T\,ds$ and thinking you must compute $|\vec r\,{}'|$ and a unit tangent. You never do — $\vec T\,ds=d\vec r$, the speed cancels, and the whole problem collapses to two endpoint evaluations. The second trap is $\varphi(0,0,0)=0$: the $e^y$ term makes it $e^0=1$.",
    check=lambda: ((x*y*exp(z) + exp(y)).subs([(x, -1), (y, 1), (z, 1)])
                   - (x*y*exp(z) + exp(y)).subs([(x, 0), (y, 0), (z, 0)])),
    want=S(-1),
),

"L28P5": dict(
    steps=[
        r"The integrand is already a gradient, $\nabla\varphi$ with $\varphi(x,y,z)=x^2y-xyz$, so FTLI applies immediately and no conservativity test is needed.",
        r"$\displaystyle\int_C\nabla\varphi\cdot d\vec r = \varphi(\text{end})-\varphi(\text{start})$, independent of the path.",
        r"$\varphi(2,1,-1)=2^2(1)-(2)(1)(-1)=4+2=6$.",
        r"$\varphi(1,0,0)=1^2(0)-(1)(0)(0)=0$.",
        r"Value $=6-0=6$.",
    ],
    trap=r"Expanding $\nabla(x^2y-xyz)=\langle2xy-yz,\,x^2-xz,\,-xy\rangle$ and then grinding out a line integral along some invented path. All that work is discarded by FTLI. Within the evaluation, the sign trap is $-xyz$ at $z=-1$, which **adds** $2$; writing $4-2=2$ is the common wrong answer.",
    # The field IS a gradient here, so build F by differentiating the stated
    # potential, then recover the potential from F — the round trip is the check.
    check=lambda: _ftli(V(diff(x**2*y - x*y*z, x), diff(x**2*y - x*y*z, y),
                          diff(x**2*y - x*y*z, z)), (1, 0, 0), (2, 1, -1)),
    want=S(6),
),

}
