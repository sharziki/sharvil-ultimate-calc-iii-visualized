"""Worked solutions for Lessons 34 and 36 (Stokes' Theorem, Divergence Theorem)
of the official MA 261 final exam study guide."""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, acos, atan, pi,
                   exp, log, symbols, diff, integrate, limit, simplify, solve,
                   Eq, oo, Abs, sinh, cosh, atan2)

x, y, z = symbols("x y z", real=True)
r, th, ph, t, u, v = symbols("r theta phi t u v", real=True)


def V(*c):
    return Matrix(list(c))


def curl(F):
    """curl of a 3-vector field written in x, y, z."""
    return V(diff(F[2], y) - diff(F[1], z),
             diff(F[0], z) - diff(F[2], x),
             diff(F[1], x) - diff(F[0], y))


def div(F):
    return diff(F[0], x) + diff(F[1], y) + diff(F[2], z)


# ----------------------------------------------------------------- L34 checks

def _l34p1():
    # Cap the triangle with the plane piece x + y + z = 1, i.e. z = 1 - x - y.
    # Upward normal: n dS = <-z_x, -z_y, 1> dA = <1, 1, 1> dA.
    C = curl(V(y**2, x, z**2))
    f = C.dot(V(1, 1, 1)).subs(z, 1 - x - y)
    return integrate(integrate(f, (y, 0, 1 - x)), (x, 0, 1))


def _l34p2():
    # C bounds the flat disk x^2 + y^2 <= 4 in the plane z = 3, n = <0,0,1>.
    C = curl(V(-y**2, x, z**2))
    f = C.dot(V(0, 0, 1)).subs(z, 3)
    f = f.subs({x: r*cos(th), y: r*sin(th)}) * r        # polar Jacobian
    return integrate(integrate(f, (r, 0, 2)), (th, 0, 2*pi))


def _l34p3():
    # Stokes backwards: replace the hemisphere by its boundary circle
    # x^2 + y^2 = 4 in z = 0, counterclockwise from above.
    rt = V(2*cos(t), 2*sin(t), S(0))
    F = V(y*z, x*z, x*y).subs([(x, rt[0]), (y, rt[1]), (z, rt[2])])
    return integrate(F.dot(diff(rt, t)), (t, 0, 2*pi))


def _l34p4():
    # Use the paraboloid itself, z = 1 - x^2 - y^2: n dS = <2x, 2y, 1> dA.
    C = curl(V(x*z, y*z, x*y))
    f = C.dot(V(2*x, 2*y, S(1))).subs(z, 1 - x**2 - y**2)
    f = f.subs({x: r*cos(th), y: r*sin(th)}) * r
    return integrate(integrate(f, (r, 0, 1)), (th, 0, 2*pi))


def _l34p5():
    # z = 9 - x^2 - y^2, upward: n dS = <2x, 2y, 1> dA over the disk r <= 3.
    C = curl(V(-y**3, x**3, -z**3))
    f = C.dot(V(2*x, 2*y, S(1))).subs(z, 9 - x**2 - y**2)
    f = f.subs({x: r*cos(th), y: r*sin(th)}) * r
    return integrate(integrate(f, (r, 0, 3)), (th, 0, 2*pi))


# ----------------------------------------------------------------- L36 checks

def _l36p1():
    D = div(V(x**3, y**3, z**3))
    D = simplify(D.subs({x: r*sin(ph)*cos(th),
                         y: r*sin(ph)*sin(th),
                         z: r*cos(ph)}))
    f = D * r**2 * sin(ph)                    # spherical Jacobian
    return integrate(integrate(integrate(f, (r, 0, 1)), (ph, 0, pi)),
                     (th, 0, 2*pi))


def _l36p2():
    D = div(V(x*y, y**2, y*z))
    return integrate(integrate(integrate(D, (x, 0, 1)), (y, 0, 1)), (z, 0, 1))


def _l36p3():
    D = div(V(x, y, z))                       # = 3
    f = D * r**2 * sin(ph)
    return integrate(integrate(integrate(f, (r, 0, 2)), (ph, 0, pi/2)),
                     (th, 0, 2*pi))


def _l36p4():
    D = div(V(x**2*z, y**2*z, z**2))
    D = D.subs({x: r*cos(th), y: r*sin(th)})
    f = D * r                                 # cylindrical Jacobian
    return integrate(integrate(integrate(f, (z, 0, 3)), (r, 0, 2)),
                     (th, 0, 2*pi))


def _l36p5():
    D = div(V(x, y, z))                       # = 3
    f = D * r**2 * sin(ph)
    return integrate(integrate(integrate(f, (r, 1, 2)), (ph, 0, pi)),
                     (th, 0, 2*pi))


SOL = {

# =========================================================== L34 Stokes' Thm

"L34P1": dict(
    steps=[
        r"Stokes' Theorem says $\oint_C \vec F\cdot d\vec r=\iint_S \operatorname{curl}(\vec F)\cdot d\vec S$ for **any** surface $S$ with $\partial S=C$. The point of the whole theorem here is that the line integral is three separate segments, each needing its own parametrization, while the surface integral is one flat triangle. Convert.",
        r"$\operatorname{curl}(\vec F)=\left\langle \dfrac{\partial}{\partial y}(z^2)-\dfrac{\partial}{\partial z}(x),\; \dfrac{\partial}{\partial z}(y^2)-\dfrac{\partial}{\partial x}(z^2),\; \dfrac{\partial}{\partial x}(x)-\dfrac{\partial}{\partial y}(y^2)\right\rangle=\langle 0,0,1-2y\rangle$.",
        r"The three vertices $(1,0,0),(0,1,0),(0,0,1)$ all satisfy $x+y+z=1$, so take $S$ to be the flat triangle in that plane: $z=g(x,y)=1-x-y$ over the shadow triangle $D:\ x\ge0,\ y\ge0,\ x+y\le1$.",
        r"For a graph $z=g(x,y)$ with **upward** normal, $d\vec S=\langle -g_x,-g_y,1\rangle\,dA=\langle 1,1,1\rangle\,dA$. Counterclockwise viewed from above is exactly the orientation that pairs with the upward normal, so no sign flip.",
        r"$\operatorname{curl}(\vec F)\cdot\langle 1,1,1\rangle=(0)(1)+(0)(1)+(1-2y)(1)=1-2y$, and note the $z$'s have vanished, so no substitution of the plane is even needed.",
        r"$\displaystyle\iint_D (1-2y)\,dA=\int_0^1\!\!\int_0^{1-x}(1-2y)\,dy\,dx=\int_0^1\Big[y-y^2\Big]_0^{1-x}dx=\int_0^1 \big[(1-x)-(1-x)^2\big]\,dx$.",
        r"$\displaystyle=\int_0^1 (x-x^2)\,dx=\tfrac12-\tfrac13=\dfrac{1}{6}$.",
    ],
    trap=r"Two traps stacked. First, people write $d\vec S=\langle -g_x,-g_y,1\rangle\,dA$ but then also multiply by $\sqrt{1+g_x^2+g_y^2}=\sqrt3$ — that factor belongs to $dS$ (scalar surface area), **not** to $d\vec S$, and including both double-counts. Second, the shadow region is the triangle $x+y\le 1$ in the first quadrant, **not** the unit square: the inner limit is $y:0\to 1-x$, and using $0\to1$ turns $\tfrac16$ into $0$.",
    check=lambda: _l34p1(),
    want=Rational(1, 6),
),

"L34P2": dict(
    steps=[
        r"$C$ is a circle sitting in a horizontal plane, so the cheapest surface to span it with is the flat disk in that same plane — the normal is constant and the surface integral collapses to a plain double integral.",
        r"$\operatorname{curl}(\vec F)=\left\langle \dfrac{\partial}{\partial y}(z^2)-\dfrac{\partial}{\partial z}(x),\; \dfrac{\partial}{\partial z}(-y^2)-\dfrac{\partial}{\partial x}(z^2),\; \dfrac{\partial}{\partial x}(x)-\dfrac{\partial}{\partial y}(-y^2)\right\rangle=\langle 0,0,1+2y\rangle$.",
        r"Take $S:\ x^2+y^2\le 4,\ z=3$. Counterclockwise from above $\Rightarrow$ upward normal $\vec n=\langle0,0,1\rangle$ and $d\vec S=\langle0,0,1\rangle\,dA$.",
        r"$\operatorname{curl}(\vec F)\cdot\vec n=1+2y$, so $\displaystyle\iint_S\operatorname{curl}(\vec F)\cdot d\vec S=\iint_{x^2+y^2\le4}(1+2y)\,dA$.",
        r"In polar, $\displaystyle\int_0^{2\pi}\!\!\int_0^2 (1+2r\sin\theta)\,r\,dr\,d\theta$. The $2r\sin\theta$ piece integrates to $0$ because $\int_0^{2\pi}\sin\theta\,d\theta=0$ (the disk is symmetric about $y=0$ and $y$ is odd).",
        r"What is left is $\displaystyle\iint_{x^2+y^2\le4}1\,dA=\text{area}=\pi(2)^2=4\pi$.",
    ],
    trap=r"The sign on $-y^2$. Since $\dfrac{\partial}{\partial y}(-y^2)=-2y$, the $k$-component is $1-(-2y)=1+2y$, not $1-2y$. Either way the $y$-term dies by symmetry, so this particular problem forgives it — but only by luck, and the same slip elsewhere does not cancel. Also note $z=3$ is irrelevant to the answer: the curl has no $z$ in it, so the height of the plane never enters.",
    check=lambda: _l34p2(),
    want=4*pi,
),

"L34P3": dict(
    steps=[
        r"Here Stokes is run in the **other** direction: a curved surface integral is traded for a line integral. $\partial S$ is where the hemisphere meets $z=0$, namely the circle $x^2+y^2=4$ in the $xy$-plane. Upward normal on $S$ pairs with counterclockwise traversal of that circle seen from above.",
        r"Parametrize $\vec r(t)=\langle 2\cos t,\,2\sin t,\,0\rangle$, $0\le t\le 2\pi$, so $\vec r\,{}'(t)=\langle -2\sin t,\,2\cos t,\,0\rangle$.",
        r"On $C$ we have $z=0$, so $\vec F=\langle yz,xz,xy\rangle=\langle 0,\,0,\,4\cos t\sin t\rangle$ — the first two components are killed by $z=0$.",
        r"$\vec F\cdot\vec r\,{}'(t)=0\cdot(-2\sin t)+0\cdot(2\cos t)+4\cos t\sin t\cdot 0=0$ identically, since $\vec r\,{}'$ has no $k$-component while $\vec F$ has only a $k$-component.",
        r"$\displaystyle\oint_C\vec F\cdot d\vec r=\int_0^{2\pi}0\,dt=0$, hence $\displaystyle\iint_S\operatorname{curl}(\vec F)\cdot d\vec S=0$.",
        r"Sanity check the fast way: $\operatorname{curl}\langle yz,xz,xy\rangle=\langle x-x,\;y-y,\;z-z\rangle=\vec 0$, because $\vec F=\nabla(xyz)$ is conservative. A zero curl makes **every** such flux zero.",
    ],
    trap=r"Trying to parametrize the hemisphere and grind out $\iint\operatorname{curl}(\vec F)\cdot d\vec S$ in spherical coordinates. It works, but it is minutes of work for a field whose curl is $\vec 0$. Also: the boundary is the equator circle at $z=0$, not the whole sphere and not the point at the top — a hemisphere with $z\ge0$ has exactly one boundary curve.",
    check=lambda: _l34p3(),
    want=S(0),
),

"L34P4": dict(
    steps=[
        r"$C$ is where $z=1-x^2-y^2$ meets $z=0$: setting $z=0$ gives $x^2+y^2=1$, the unit circle in the $xy$-plane. Stokes lets us span it with either the paraboloid cap or the flat disk; both are legal, so pick deliberately.",
        r"$\operatorname{curl}(\vec F)=\left\langle \dfrac{\partial}{\partial y}(xy)-\dfrac{\partial}{\partial z}(yz),\; \dfrac{\partial}{\partial z}(xz)-\dfrac{\partial}{\partial x}(xy),\; \dfrac{\partial}{\partial x}(yz)-\dfrac{\partial}{\partial y}(xz)\right\rangle=\langle x-y,\;x-y,\;0\rangle$.",
        r"**Cheap route.** Use the flat disk $S:\ x^2+y^2\le1,\ z=0$ with $\vec n=\langle0,0,1\rangle$. Then $\operatorname{curl}(\vec F)\cdot\vec n=0$ because the curl has no $k$-component, and the integral is $0$ on sight.",
        r"**Honest route**, to confirm the choice of surface did not smuggle anything in: on the paraboloid, $d\vec S=\langle 2x,2y,1\rangle\,dA$ over $x^2+y^2\le1$, and $\operatorname{curl}(\vec F)\cdot\langle2x,2y,1\rangle=2x(x-y)+2y(x-y)=2(x^2-y^2)$.",
        r"$\displaystyle\iint_{x^2+y^2\le1}2(x^2-y^2)\,dA=\int_0^{2\pi}\!\!\int_0^1 2r^2(\cos^2\theta-\sin^2\theta)\,r\,dr\,d\theta=2\Big(\int_0^1 r^3dr\Big)\Big(\int_0^{2\pi}\cos 2\theta\,d\theta\Big)$.",
        r"$\int_0^{2\pi}\cos2\theta\,d\theta=0$, so the value is $0$ — same as the flat disk, as Stokes guarantees.",
    ],
    trap=r"Reaching for the paraboloid because the problem named it. Stokes only cares about the boundary curve, so you may replace the cap with the flat disk it bounds and the $k$-component-free curl kills the integral instantly. The other trap is the boundary itself: 'above the $xy$-plane' means $C$ is $x^2+y^2=1$ at $z=0$, not a curve on the paraboloid at some other height.",
    check=lambda: _l34p4(),
    want=S(0),
),

"L34P5": dict(
    steps=[
        r"$\operatorname{curl}(\vec F)=\left\langle \dfrac{\partial}{\partial y}(-z^3)-\dfrac{\partial}{\partial z}(x^3),\; \dfrac{\partial}{\partial z}(-y^3)-\dfrac{\partial}{\partial x}(-z^3),\; \dfrac{\partial}{\partial x}(x^3)-\dfrac{\partial}{\partial y}(-y^3)\right\rangle=\langle 0,\,0,\,3x^2+3y^2\rangle$.",
        r"Two ways to finish. Direct: $S$ is $z=9-x^2-y^2$ with upward normal, so $d\vec S=\langle 2x,2y,1\rangle\,dA$ over the shadow disk $x^2+y^2\le9$ (set $z=0$ to get radius $3$).",
        r"$\operatorname{curl}(\vec F)\cdot\langle2x,2y,1\rangle=0\cdot 2x+0\cdot 2y+(3x^2+3y^2)(1)=3(x^2+y^2)$, so the messy $\langle2x,2y\rangle$ part contributes nothing.",
        r"Polar: $\displaystyle\iint_{x^2+y^2\le9}3(x^2+y^2)\,dA=\int_0^{2\pi}\!\!\int_0^3 3r^2\cdot r\,dr\,d\theta=2\pi\cdot 3\cdot\frac{3^4}{4}=\frac{243\pi}{2}$.",
        r"Cross-check with Stokes on the boundary circle $x^2+y^2=9$, $z=0$: $\vec r(t)=\langle3\cos t,3\sin t,0\rangle$, $\vec F=\langle -27\sin^3t,\,27\cos^3 t,\,0\rangle$, and $\vec F\cdot\vec r\,{}'=81(\sin^4t+\cos^4t)$, whose integral over $[0,2\pi]$ is $81\cdot\frac{3\pi}{2}=\frac{243\pi}{2}$. Same value.",
    ],
    trap=r"Forgetting the polar Jacobian: the integrand is $3r^2$ and $dA=r\,dr\,d\theta$, so you integrate $3r^3$. Dropping the extra $r$ gives $2\pi\cdot 3\cdot 9=54\pi$ instead of $\tfrac{243\pi}{2}$. Second trap: the shadow radius is $3$, not $9$ — $z=9-x^2-y^2$ hits $z=0$ at $x^2+y^2=9$, i.e. $r=3$.",
    check=lambda: _l34p5(),
    want=Rational(243, 2)*pi,
),

# ====================================================== L36 Divergence Theorem

"L36P1": dict(
    steps=[
        r"$S$ is **closed** with outward normal, which is exactly the hypothesis of the Divergence Theorem: $\displaystyle\iint_S\vec F\cdot d\vec S=\iiint_E \operatorname{div}(\vec F)\,dV$. Going the other way, parametrizing a sphere and dotting with a normal, is far worse.",
        r"$\operatorname{div}(\vec F)=\dfrac{\partial}{\partial x}(x^3)+\dfrac{\partial}{\partial y}(y^3)+\dfrac{\partial}{\partial z}(z^3)=3x^2+3y^2+3z^2=3\rho^2$ in spherical coordinates.",
        r"$E$ is the solid unit ball, so spherical coordinates with $0\le\rho\le1$, $0\le\phi\le\pi$, $0\le\theta\le2\pi$ and $dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$.",
        r"$\displaystyle\iiint_E 3\rho^2\,dV=\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_0^1 3\rho^2\cdot\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$ — note the integrand is $3\rho^4\sin\phi$.",
        r"The three factors separate: $\displaystyle\Big(\int_0^{2\pi}d\theta\Big)\Big(\int_0^{\pi}\sin\phi\,d\phi\Big)\Big(\int_0^1 3\rho^4 d\rho\Big)=(2\pi)(2)\left(\frac35\right)=\frac{12\pi}{5}$.",
    ],
    trap=r"Writing $dV=\rho^2\sin\phi$ and then integrating $3\rho^2$ as if it were $3\rho^2\cdot\rho\sin\phi$ or just $3\rho^2\,d\rho$. The full integrand is $3\rho^4\sin\phi$; dropping either the $\rho^2$ of $dV$ or the $\sin\phi$ changes the answer to $2\pi$ or $\tfrac{4\pi}{3}$-type garbage. Also $\int_0^{\pi}\sin\phi\,d\phi=2$, not $0$ — students who reflexively write $0$ for a sine integral lose the whole thing.",
    check=lambda: _l36p1(),
    want=Rational(12, 5)*pi,
),

"L36P2": dict(
    steps=[
        r"The cube has six faces, so the direct flux computation is six separate double integrals with six different normals. The Divergence Theorem replaces all of it with one triple integral over $[0,1]^3$.",
        r"$\operatorname{div}(\vec F)=\dfrac{\partial}{\partial x}(xy)+\dfrac{\partial}{\partial y}(y^2)+\dfrac{\partial}{\partial z}(yz)=y+2y+y=4y$.",
        r"$\displaystyle\iint_S\vec F\cdot d\vec S=\iiint_{[0,1]^3}4y\,dV=\int_0^1\!\!\int_0^1\!\!\int_0^1 4y\,dx\,dy\,dz$.",
        r"The region is a box and the integrand depends only on $y$, so it factors: $\displaystyle\Big(\int_0^1 dx\Big)\Big(\int_0^1 4y\,dy\Big)\Big(\int_0^1 dz\Big)=1\cdot 2\cdot 1$.",
        r"Flux $=2$.",
    ],
    trap=r"Differentiating the wrong variable in each slot. $\operatorname{div}$ takes $\partial_x$ of the **first** component, $\partial_y$ of the second, $\partial_z$ of the third: $\partial_x(xy)=y$ and $\partial_z(yz)=y$, so the three terms are $y+2y+y=4y$, not $x+2y+y$. A secondary trap is assuming the answer must be $0$ by symmetry — $y$ is not symmetric on $[0,1]$, only on an interval centered at the origin.",
    check=lambda: _l36p2(),
    want=S(2),
),

"L36P3": dict(
    steps=[
        r"The hemisphere alone is not closed, but the problem already glued the flat disk on, so $S=\partial E$ where $E$ is the solid half-ball $x^2+y^2+z^2\le4,\ z\ge0$. Outward normal on both pieces means the Divergence Theorem applies as stated.",
        r"$\operatorname{div}\langle x,y,z\rangle=1+1+1=3$, a constant — which is why the flux reduces to $3\,\text{Vol}(E)$.",
        r"$\displaystyle\iint_S\vec F\cdot d\vec S=\iiint_E 3\,dV=3\cdot\text{Vol}(E)$.",
        r"$E$ is half of a ball of radius $2$: $\text{Vol}(E)=\tfrac12\cdot\tfrac43\pi(2)^3=\tfrac{16\pi}{3}$. In spherical this is $\int_0^{2\pi}\!\!\int_0^{\pi/2}\!\!\int_0^2 \rho^2\sin\phi\,d\rho\,d\phi\,d\theta$, with $\phi$ stopping at $\pi/2$ because $z\ge0$.",
        r"Flux $=3\cdot\dfrac{16\pi}{3}=16\pi$.",
    ],
    trap=r"Letting $\phi$ run to $\pi$ and getting $32\pi$. For the upper half-ball $\phi\in[0,\pi/2]$ — $\phi=\pi/2$ is the equator, $\phi=\pi$ is the south pole. The second trap is applying the theorem to the hemisphere alone: it is not closed, so you would need the disk anyway. Here the disk happens to contribute $0$, since on $z=0$ the outward normal is $\langle0,0,-1\rangle$ and $\vec F\cdot\vec n=-z=0$, but that is a fact you must state, not one you may assume.",
    check=lambda: _l36p3(),
    want=16*pi,
),

"L36P4": dict(
    steps=[
        r"The boundary is a can: top disk, bottom disk, and curved side, each with a different normal. One triple integral over the solid beats three surface integrals.",
        r"$\operatorname{div}(\vec F)=\dfrac{\partial}{\partial x}(x^2z)+\dfrac{\partial}{\partial y}(y^2z)+\dfrac{\partial}{\partial z}(z^2)=2xz+2yz+2z$.",
        r"The solid is a cylinder, so cylindrical coordinates: $x=r\cos\theta$, $y=r\sin\theta$, $0\le r\le2$, $0\le\theta\le2\pi$, $0\le z\le3$, $dV=r\,dz\,dr\,d\theta$.",
        r"$\displaystyle\iiint_E(2xz+2yz+2z)\,dV=\int_0^{2\pi}\!\!\int_0^2\!\!\int_0^3\big(2rz\cos\theta+2rz\sin\theta+2z\big)\,r\,dz\,dr\,d\theta$.",
        r"The first two terms vanish: $\int_0^{2\pi}\cos\theta\,d\theta=\int_0^{2\pi}\sin\theta\,d\theta=0$, i.e. $x$ and $y$ are odd over a disk centered on the axis.",
        r"What survives is $\displaystyle\int_0^{2\pi}\!\!\int_0^2\!\!\int_0^3 2z\,r\,dz\,dr\,d\theta=\Big(\int_0^3 2z\,dz\Big)\Big(\iint_{r\le2}dA\Big)=9\cdot 4\pi=36\pi$.",
    ],
    trap=r"Justifying the death of $2xz$ and $2yz$ with the wrong symmetry. The $z$-interval $[0,3]$ is **not** symmetric about $0$, so nothing cancels in $z$; the cancellation is in $\theta$, because $\int_0^{2\pi}\cos\theta\,d\theta=\int_0^{2\pi}\sin\theta\,d\theta=0$ over the full disk. Beware also that this problem will not punish a dropped Jacobian: $\int_0^2 r\,dr=\int_0^2 dr=2$, so omitting the $r$ still lands on $36\pi$ here. That is a coincidence of the radius being $2$, and it will not save you on the next cylinder.",
    check=lambda: _l36p4(),
    want=36*pi,
),

"L36P5": dict(
    steps=[
        r"$E$ is a spherical shell $1\le\rho\le2$. Its boundary is **two** spheres, and 'outward' for the solid means outward on $\rho=2$ but pointing *toward the origin* on $\rho=1$. The Divergence Theorem handles that bookkeeping for free.",
        r"$\operatorname{div}\langle x,y,z\rangle=3$.",
        r"$\displaystyle\iint_S\vec F\cdot d\vec S=\iiint_E 3\,dV=3\cdot\text{Vol}(E)$, and $\text{Vol}(E)=\tfrac43\pi(2^3-1^3)=\tfrac{28\pi}{3}$.",
        r"As a spherical integral: $\displaystyle\int_0^{2\pi}\!\!\int_0^{\pi}\!\!\int_1^2 3\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$, where $\int_1^2 3\rho^2 d\rho=2^3-1^3=7$, $\int_0^{\pi}\sin\phi\,d\phi=2$, $\int_0^{2\pi}d\theta=2\pi$.",
        r"Flux $=7\cdot 2\cdot 2\pi=28\pi$, matching $3\cdot\dfrac{28\pi}{3}$.",
    ],
    trap=r"Setting the inner limit to $\rho=0$ and getting $32\pi$ — the ball of radius $1$ is **not** part of $E$, it is a hole. Equally common is computing the two spheres separately and adding them with the same sign: on the inner sphere the outward-from-$E$ normal is $-\hat\rho$, so its flux is $-4\pi$, and $32\pi+(-4\pi)=28\pi$. Adding $+4\pi$ gives $36\pi$.",
    check=lambda: _l36p5(),
    want=28*pi,
),

}
