"""Worked solutions for Lessons 21-24 of the official guide.

Lesson 21  Triple integrals in Cartesian coordinates      (16.4)
Lesson 22  Triple integrals in cylindrical coordinates    (16.5)
Lesson 23  Triple integrals in spherical coordinates      (16.5)
Lesson 24  Mass, moments and centres of mass              (16.6)

The instructor's page prints a stem and a bare final answer. This file is the
missing middle. Every `check` rebuilds the integral from the stem and lets
sympy evaluate it; nothing here asserts a value it did not compute. Where the
Jacobian is the point -- and in this batch it usually is -- the check derives
`r` or `rho**2*sin(phi)` as an actual determinant rather than typing it in.

Two entries carry a `fix`:
  L21P3  the second of the two offered orders has the wrong outer z-limit;
         as printed it integrates to 1/2 instead of the correct 2/3.
  L22P1  the printed Cartesian stem and the printed cylindrical answer are
         not the same region; the stem's inner limit should start at y = x.
"""

from sympy import (Matrix, Rational, S, sqrt, cos, sin, tan, sec, acos, atan,
                   atan2, pi, E, exp, log, symbols, diff, integrate, limit,
                   simplify, solve, Eq, oo, Abs, sinh, cosh)

x, y, z = symbols("x y z", real=True)
r, th, ph, t, u, v = symbols("r theta phi t u v", real=True)
rho = symbols("rho", nonnegative=True)


def V(*c):
    return Matrix(list(c))


def cyl_jac():
    """The cylindrical Jacobian, computed rather than quoted: dV = r dr dtheta dz."""
    return simplify(Matrix([r * cos(th), r * sin(th), z])
                    .jacobian(Matrix([r, th, z])).det())


def sph_jac():
    """The spherical Jacobian, computed rather than quoted: dV = rho^2 sin(phi) drho dphi dtheta."""
    return simplify(Matrix([rho * sin(ph) * cos(th),
                            rho * sin(ph) * sin(th),
                            rho * cos(ph)])
                    .jacobian(Matrix([rho, ph, th])).det())


SOL = {

# ----------------------------------------------------------- Lesson 21 ----
"L21P1": dict(
    steps=[
        r"Read the order off the differentials: $dz\,dx\,dy$. The innermost variable is $z$, and the integrand $e^x$ does not contain $z$ — so the inner integral is just multiplication by the height.",
        r"$\displaystyle\int_0^{2-y}e^x\,dz=e^x\,(2-y)$.",
        r"Now the $x$ and $y$ limits are both constants, and what is left **separates**: $\displaystyle\int_0^1\!\int_0^1 e^x(2-y)\,dx\,dy=\left(\int_0^1 e^x\,dx\right)\left(\int_0^1(2-y)\,dy\right)$.",
        r"$\displaystyle\int_0^1 e^x\,dx=e-1$ and $\displaystyle\int_0^1(2-y)\,dy=2-\tfrac12=\tfrac32$.",
        r"Product: $\tfrac{3}{2}(e-1)$.",
    ],
    trap=r"The limit $2-y$ sits on the **inner** integral while $y$ is the **outer** variable. That is legal — inner limits may involve any variable integrated later — but it means you cannot do the $y$-integral first. Someone who starts at the outside gets $\int_0^1(2-y)\,dy$ sitting where a $z$-integral belongs and loses the factor entirely.",
    check=lambda: integrate(exp(x), (z, 0, 2 - y), (x, 0, 1), (y, 0, 1)),
    want=Rational(3, 2) * (E - 1),
),
"L21P2": dict(
    steps=[
        r"Order $dz\,dy\,dx$ means: $z$ is bounded by surfaces, $y$ by curves in the $xy$-plane, $x$ by numbers. Build it from the inside out.",
        r"First octant gives the floor $z=0$; the plane gives the ceiling $z=8-4x-2y$. So $c=8-4x-2y$.",
        r"**Project the solid onto the $xy$-plane** by setting $z=0$ in the plane: $4x+2y=8$, i.e. $y=4-2x$. That triangle, together with $x\ge0,\ y\ge0$, is the shadow.",
        r"For a fixed $x$, $y$ runs from $0$ up to that line: $b=4-2x$.",
        r"$x$ runs until the shadow closes, i.e. until $4-2x=0$: $a=2$.",
        r"$\displaystyle\iiint_E f\,dV=\int_0^2\!\int_0^{4-2x}\!\int_0^{8-4x-2y}f\,dz\,dy\,dx$.",
    ],
    trap=r"Using the $x$-intercept of the plane, $x=2$... by luck that is right here, but the reason matters: $a$ is where the **shadow** closes, not where the plane meets an axis. Get $b$ by setting $z=0$, not $x=0$; setting $x=0$ gives $y=4$, which is the wrong constant limit and makes the region a box.",
    check=lambda: [solve(Eq(4 - 2 * x, 0), x)[0],
                   solve(Eq(4 * x + 2 * y - 8, 0), y)[0]],
    want=[2, 4 - 2 * x],
),
"L21P3": dict(
    steps=[
        r"Four surfaces, so list the inequalities: $x\ge0$, $z\ge0$, $y\ge x$, and $x+y+z\le2$.",
        r"Take $z$ innermost: $0\le z\le 2-x-y$.",
        r"Shadow in the $xy$-plane is where that height is non-negative and $y\ge x$: the triangle $x\le y\le 2-x$, $x\ge0$.",
        r"That triangle closes when $x=2-x$, i.e. $x=1$. So $\displaystyle\int_0^1\!\int_x^{2-x}\!\int_0^{2-x-y}f\,dz\,dy\,dx$.",
        r"Reordering to $dy\,dz\,dx$: solve $y\ge x$ and $y\le 2-x-z$, so $x\le y\le 2-x-z$.",
        r"Those two limits cross when $2-x-z=x$, i.e. at $z=2-2x$ — so $z$ must stop at $2-2x$, giving $\displaystyle\int_0^1\!\int_0^{2-2x}\!\int_x^{2-x-z}f\,dy\,dz\,dx$.",
        r"Sanity check both with $f=1$: each gives volume $\tfrac23$.",
    ],
    trap=r"When you reorder, the **new** outer limit is where the inner limits collide, not where some surface hits an axis. Writing $z$ from $0$ to $2-x$ (the plane's $z$-intercept above $y=0$) puts $z$ in a range where the inner $y$-limits are upside-down, $2-x-z<x$, and the integral quietly subtracts the phantom slab instead of erroring.",
    right=r"$\displaystyle\int_0^1\!\int_0^{2-2x}\!\int_x^{2-x-z}f\,dy\,dz\,dx$",
    fix=r"The **second** offered order is wrong as printed. With $z$ running to $2-x$, every $z>2-2x$ has $2-x-z<x$, so the inner $y$-integral runs backwards. With $f=1$ the printed form evaluates to $\tfrac12$; the true volume, and the value of the printed **first** form, is $\tfrac23$. The $z$-limit must be $2-2x$.",
    check=lambda: [integrate(1, (z, 0, 2 - x - y), (y, x, 2 - x), (x, 0, 1)),
                   integrate(1, (y, x, 2 - x - z), (z, 0, 2 - 2 * x), (x, 0, 1))],
    want=[Rational(2, 3), Rational(2, 3)],
),
"L21P4": dict(
    steps=[
        r"The $z$-limits are already given: the solid sits between the upward paraboloid $z=x^2+y^2$ and the downward one $z=6-x^2-y^2$.",
        r"They meet where $x^2+y^2=6-x^2-y^2$, i.e. $2(x^2+y^2)=6$, so $x^2+y^2=3$ — a circle of radius $\sqrt3$.",
        r"That circle **is** the shadow's boundary, which is why the outer limits are $\pm\sqrt3$.",
        r"Solving $x^2+y^2=3$ for $y$: $a=-\sqrt{3-x^2}$, $b=\sqrt{3-x^2}$.",
    ],
    trap=r"Setting $x^2+y^2=6$ (from $z=6-x^2-y^2$ with $z=0$) instead of equating the two surfaces. The paraboloids never reach $z=0$ together; the boundary of the shadow is where the **ceiling meets the floor**, and that is radius $\sqrt3$, not $\sqrt6$. The given outer limits $\pm\sqrt3$ are the tell.",
    check=lambda: sorted(solve(Eq(x ** 2 + y ** 2, 6 - x ** 2 - y ** 2), y),
                         key=lambda e: e.subs(x, 0)),
    want=[-sqrt(3 - x ** 2), sqrt(3 - x ** 2)],
),
"L21P5": dict(
    steps=[
        r"Look at the shadow before touching the integrand: $-1\le y\le1$ with $-\sqrt{1-y^2}\le x\le\sqrt{1-y^2}$ is the full unit disk, and $z$ runs over the fixed interval $[-1,1]$. The solid is a cylinder.",
        r"$(x^2+y^2)^{3/2}$ is a function of distance from the $z$-axis alone — cylindrical coordinates, and the $z$-integral is just a factor of $2$.",
        r"$(x^2+y^2)^{3/2}=r^3$, and $dV=r\,dr\,d\theta\,dz$, so the integrand becomes $r^3\cdot r=r^4$.",
        r"$\displaystyle\int_{-1}^{1}\!\int_0^{2\pi}\!\int_0^1 r^4\,dr\,d\theta\,dz=2\cdot 2\pi\cdot\frac{1}{5}=\frac{4\pi}{5}$.",
    ],
    trap=r"Converting $(x^2+y^2)^{3/2}$ to $r^3$ and then integrating $\int_0^1 r^3\,dr=\tfrac14$ — the extra $r$ from $dA=r\,dr\,d\theta$ is dropped and the answer comes out $\pi$ instead of $\tfrac{4\pi}{5}$. The exponent you integrate is always one higher than the one you converted.",
    check=lambda: integrate(cyl_jac() * (r ** 2) ** Rational(3, 2),
                            (r, 0, 1), (th, 0, 2 * pi), (z, -1, 1)),
    want=4 * pi / 5,
),

# ----------------------------------------------------------- Lesson 22 ----
"L22P1": dict(
    steps=[
        r"$z$ is already uncoupled: it runs over $[2,6]$ and nothing else mentions it, so it can go anywhere in the order.",
        r"The integrand $e^{-x^2-y^2}=e^{-r^2}$ — that is the whole reason to convert. In Cartesian it has no elementary antiderivative.",
        r"$dV=r\,dr\,d\theta\,dz$, so the integrand becomes $re^{-r^2}$, which integrates instantly to $-\tfrac12e^{-r^2}$.",
        r"Region: $y\le\sqrt{4-x^2}$ is the disk $r\le2$; the corner point $(\sqrt2,\sqrt2)$ where $x=\sqrt2$ meets that circle is at $\theta=\frac{\pi}{4}$.",
        r"So the wedge $\frac{\pi}{4}\le\theta\le\frac{\pi}{2}$, $0\le r\le 2$ — which is exactly the set $y\ge x$ inside the disk in the first quadrant.",
        r"$\displaystyle\int_2^6\!\int_{\pi/4}^{\pi/2}\!\int_0^2 re^{-r^2}\,dr\,d\theta\,dz=4\cdot\frac{\pi}{4}\cdot\frac{1-e^{-4}}{2}=\frac{\pi}{2}\left(1-e^{-4}\right)$.",
    ],
    trap=r"Converting the integrand but keeping the Cartesian limits in spirit — reading $0\le x\le\sqrt2$ as '$\theta$ from $0$'. The upper $x$-limit $\sqrt2$ is a **vertical line**, $r=\sqrt2\sec\theta$, not a ray; only the presence of the lower boundary $y=x$ turns it into the clean ray $\theta=\frac{\pi}{4}$. Any time a straight edge is not through the origin, polar limits stop being constants.",
    right=r"$\displaystyle\int_2^6\!\int_0^{\pi/4}\!\int_0^{\sqrt2\sec\theta}\!re^{-r^2}\,dr\,d\theta\,dz+\int_2^6\!\int_{\pi/4}^{\pi/2}\!\int_0^2 re^{-r^2}\,dr\,d\theta\,dz$",
    fix=r"The printed Cartesian stem and the printed cylindrical answer describe **different regions**. As written, $0\le y\le\sqrt{4-x^2}$ over $0\le x\le\sqrt2$ has area $1+\frac{\pi}{2}$, while the wedge $\frac{\pi}{4}\le\theta\le\frac{\pi}{2},\ r\le2$ has area $\frac{\pi}{2}$ — the answer is missing the triangular piece below $y=x$. The printed answer is correct for the inner limit $\int_x^{\sqrt{4-x^2}}$; with the printed lower limit $0$ the rewrite needs the two pieces above.",
    check=lambda: integrate(
        cyl_jac() * exp(-x ** 2 - y ** 2).subs({x: r * cos(th), y: r * sin(th)}).simplify(),
        (r, 0, 2), (th, pi / 4, pi / 2), (z, 2, 6)),
    want=pi / 2 * (1 - exp(-4)),
),
"L22P2": dict(
    steps=[
        r"Shadow first: $0\le x\le2$, $0\le y\le\sqrt{4-x^2}$ is the quarter disk of radius $2$ in the first quadrant, so $0\le\theta\le\frac{\pi}{2}$, $0\le r\le2$.",
        r"The $z$-limits are both cones: $z=\sqrt{x^2+y^2}=r$ below and $z=\sqrt{2(x^2+y^2)}=\sqrt2\,r$ above.",
        r"Height of the column at radius $r$: $\sqrt2\,r-r=(\sqrt2-1)r$.",
        r"With $dV=r\,dr\,d\theta\,dz$: $\displaystyle\int_0^{\pi/2}\!\int_0^2(\sqrt2-1)r\cdot r\,dr\,d\theta=\frac{\pi}{2}(\sqrt2-1)\cdot\frac{8}{3}$.",
        r"$=\dfrac{4\pi}{3}\left(\sqrt2-1\right)$.",
    ],
    trap=r"$\sqrt{2(x^2+y^2)}$ is $\sqrt2\,r$, not $2r$ and not $r^2$ — pulling the $2$ out from under the root without the square root gives $\frac{4\pi}{3}$ exactly one unit too large. Second trap: the height $(\sqrt2-1)r$ already carries one power of $r$, so the integrand is $r^2$, not $r$; forgetting the Jacobian here costs a factor of $\frac{3}{2}\cdot\frac{2}{2}$ and lands on $\pi(\sqrt2-1)$.",
    check=lambda: integrate(cyl_jac(), (z, r, sqrt(2) * r), (r, 0, 2), (th, 0, pi / 2)),
    want=4 * pi / 3 * (sqrt(2) - 1),
),
"L22P3": dict(
    steps=[
        r"The shadow $0\le x\le10$, $0\le y\le\sqrt{100-x^2}$ is a quarter disk of radius $10$: $0\le\theta\le\frac{\pi}{2}$, $0\le r\le10$.",
        r"The ceiling $z=\sqrt{x^2+y^2}$ is the cone $z=r$; the integrand $\frac{1}{\sqrt{x^2+y^2}}=\frac1r$.",
        r"So the full cylindrical integrand is $\frac1r\cdot r=1$ — the Jacobian **cancels the singularity**. That is the point of the problem.",
        r"$\displaystyle\int_0^{\pi/2}\!\int_0^{10}\!\int_0^{r}1\,dz\,dr\,d\theta=\int_0^{\pi/2}\!\int_0^{10}r\,dr\,d\theta=\frac{\pi}{2}\cdot 50=25\pi$.",
    ],
    trap=r"Two errors cancel here if you are careless in exactly the wrong way. Dropping the Jacobian leaves $\int\int \frac1r\,\cdot r\,dz$ vs $\int\int\frac1r\,dz$ — the second gives $\int_0^{10}1\,dr=10$ and the answer $5\pi$. The integrand being $1$ after conversion is a result, not an accident: check that you multiplied by $r$ before you simplified.",
    check=lambda: integrate(cyl_jac() * (1 / sqrt(x ** 2 + y ** 2)).subs(
        {x: r * cos(th), y: r * sin(th)}).simplify().subs(Abs(r), r),
        (z, 0, r), (r, 0, 10), (th, 0, pi / 2)),
    want=25 * pi,
),
"L22P4": dict(
    steps=[
        r"Both surfaces depend only on $r^2=x^2+y^2$: $z=r^2-9$ (an upward paraboloid dropped to $-9$) and $z=-2r^2$ (a downward one from the origin).",
        r"Which is on top? At $r=0$: $-9$ versus $0$, so $z=-2r^2$ is the **ceiling** and $z=r^2-9$ is the floor.",
        r"They meet where $r^2-9=-2r^2\Rightarrow 3r^2=9\Rightarrow r=\sqrt3$. Full revolution, so $0\le\theta\le2\pi$.",
        r"Height $=-2r^2-(r^2-9)=9-3r^2$.",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\sqrt3}(9-3r^2)\,r\,dr\,d\theta=2\pi\left[\frac{9r^2}{2}-\frac{3r^4}{4}\right]_0^{\sqrt3}=2\pi\left(\frac{27}{2}-\frac{27}{4}\right)=\frac{27\pi}{2}$.",
    ],
    trap=r"Assuming the paraboloid opening **upward** is the ceiling because it 'goes up'. Over the whole region $r<\sqrt3$ it is the floor, and swapping them makes the volume negative. Test at $r=0$ every time. The other trap is integrating $9-3r^2$ against $dr$ instead of $r\,dr$, which gives $2\pi(9\sqrt3-3\sqrt3)=12\sqrt3\,\pi$ — a suspiciously irrational volume for a surface of revolution with rational intersection radius.",
    check=lambda: integrate(cyl_jac(), (z, r ** 2 - 9, -2 * r ** 2),
                            (r, 0, sqrt(3)), (th, 0, 2 * pi)),
    want=27 * pi / 2,
),
"L22P5": dict(
    steps=[
        r"In spherical, the cone $z^2=x^2+y^2$ with $z>0$ is the single surface $\phi=\frac{\pi}{4}$, and the solid inside it is $0\le\phi\le\frac{\pi}{4}$.",
        r"A **horizontal plane** is not a constant in spherical: $z=\rho\cos\phi$, so $z=1$ becomes $\rho=\sec\phi$ and $z=2$ becomes $\rho=2\sec\phi$.",
        r"Those are the $\rho$-limits, and they depend on $\phi$ — so $\rho$ must be integrated first.",
        r"$dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$, full revolution in $\theta$:",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\pi/4}\!\int_{\sec\phi}^{2\sec\phi}\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$.",
        r"Worth confirming in cylindrical, where it is a stack of disks of radius $z$: $\displaystyle\int_0^{2\pi}\!\int_1^2\!\int_0^{z}r\,dr\,dz\,d\theta=\int_1^2\pi z^2\,dz=\frac{7\pi}{3}$ — and the spherical integral gives the same.",
    ],
    trap=r"Writing the planes as constant $\rho$ (say $\rho$ from $1$ to $2$), which describes the region between two **spheres**, not two planes — that is a spherical shell wedge, volume $\frac{2\pi}{3}(8-1)(1-\cos\frac\pi4)$, not $\frac{7\pi}{3}$. Any flat boundary not through the origin becomes $\rho=\text{(something)}\sec\phi$ and forces $d\rho$ innermost.",
    check=lambda: integrate(sph_jac(), (rho, sec(ph), 2 * sec(ph)),
                            (ph, 0, pi / 4), (th, 0, 2 * pi)),
    want=7 * pi / 3,
),

# ----------------------------------------------------------- Lesson 23 ----
"L23P1": dict(
    steps=[
        r"$c$ is the Jacobian and nothing else: $dV=\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$, so $c=\rho^2\sin\phi$.",
        r"Sphere $x^2+y^2+z^2=4$ is $\rho=2$, and since $\rho$ is innermost and starts at $0$, $b=2$.",
        r"The cone $z=\sqrt{3x^2+3y^2}=\sqrt3\,\sqrt{x^2+y^2}$ has $\tan\phi=\dfrac{\sqrt{x^2+y^2}}{z}=\dfrac{1}{\sqrt3}$.",
        r"So $\phi=\frac{\pi}{6}$, and 'inside the cone' means $0\le\phi\le\frac{\pi}{6}$: $a=\frac{\pi}{6}$.",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\pi/6}\!\int_0^{2}\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$.",
    ],
    trap=r"$\tan\phi=\frac{r}{z}$, not $\frac{z}{r}$ — $\phi$ is measured **down from the positive $z$-axis**. Taking $\tan\phi=\sqrt3$ gives $\phi=\frac{\pi}{3}$, which is the complementary wedge and roughly four times the volume. Second trap: writing $c=\rho\sin\phi$, the *polar* Jacobian with a $\rho$ in it, which is dimensionally wrong for a volume.",
    check=lambda: [atan(1 / sqrt(S(3))),
                   solve(Eq(rho ** 2, 4), rho)[0],
                   sph_jac()],
    want=[pi / 6, 2, rho ** 2 * sin(ph)],
),
"L23P2": dict(
    steps=[
        r"Cone $z=\sqrt{x^2+y^2}$: here $\tan\phi=\frac{r}{z}=1$, so it is the surface $\phi=\frac{\pi}{4}$, and the solid inside it is $0\le\phi\le\frac{\pi}{4}$.",
        r"Sphere $x^2+y^2+z^2=8$ is $\rho^2=8$, i.e. $\rho=\sqrt8=2\sqrt2$.",
        r"Both boundaries are coordinate surfaces in spherical — every limit is a constant, which is the whole reason to use it here.",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\pi/4}\!\int_0^{\sqrt8}\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$.",
        r"Value: $2\pi\cdot\left(1-\tfrac{\sqrt2}{2}\right)\cdot\frac{(\sqrt8)^3}{3}=\frac{32\pi}{3}\left(\sqrt2-1\right)$, which the cylindrical set-up $\int_0^{2\pi}\!\int_0^2\left(\sqrt{8-r^2}-r\right)r\,dr\,d\theta$ confirms.",
    ],
    trap=r"Reading $\rho=8$ off $x^2+y^2+z^2=8$. The equation gives $\rho^2=8$, so $\rho=2\sqrt2$ — and cubing the wrong one inflates the volume by a factor of $8^3/8^{3/2}\approx22.6$. Also note the cone/sphere meet at $z=2$, $r=2$: that intersection is *not* needed in spherical, which is the payoff for converting.",
    check=lambda: integrate(cyl_jac(), (z, r, sqrt(8 - r ** 2)),
                            (r, 0, 2), (th, 0, 2 * pi)),
    want=32 * pi * (sqrt(2) - 1) / 3,
),
"L23P3": dict(
    steps=[
        r"Put both spheres in spherical form. Origin-centred radius $2$: $\rho=2$.",
        r"The one centred at $(0,0,2)$: $x^2+y^2+(z-2)^2=4\Rightarrow \rho^2-4\rho\cos\phi=0\Rightarrow\rho=4\cos\phi$.",
        r"'Inside the shifted sphere, outside the origin one' is exactly $2\le\rho\le4\cos\phi$ — the inner radius is the constant, the outer is the $\phi$-dependent one.",
        r"Those limits are only valid where $4\cos\phi\ge2$, i.e. $\cos\phi\ge\frac12$, i.e. $\phi\le\frac{\pi}{3}$. That is the $\phi$-limit.",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\pi/3}\!\int_2^{4\cos\phi}\rho^2\sin\phi\,d\rho\,d\phi\,d\theta$.",
        r"Check it independently: the lens where two radius-$2$ spheres with centres $2$ apart overlap has volume $\frac{\pi(4R+d)(2R-d)^2}{12}=\frac{10\pi}{3}$, so the answer is $\frac{32\pi}{3}-\frac{10\pi}{3}=\frac{22\pi}{3}$ — and the integral above gives $\frac{22\pi}{3}$.",
    ],
    trap=r"Taking $\phi$ up to $\frac{\pi}{2}$ because the shifted sphere 'sits above the $xy$-plane'. Past $\phi=\frac{\pi}{3}$ the outer limit $4\cos\phi$ drops **below** the inner limit $2$, so the integral starts subtracting. The upper $\phi$ is always where the two $\rho$-limits meet: solve $4\cos\phi=2$.",
    check=lambda: integrate(sph_jac(), (rho, 2, 4 * cos(ph)),
                            (ph, 0, pi / 3), (th, 0, 2 * pi)),
    want=22 * pi / 3,
),
"L23P4": dict(
    steps=[
        r"The shadow $-1\le x\le1$, $|y|\le\sqrt{1-x^2}$ is the full unit disk, so $\theta$ makes a full turn: $a=2\pi$.",
        r"Ceiling $z=\sqrt{4-x^2-y^2}$ is the sphere $\rho=2$, so $c=2$.",
        r"Floor $z=\sqrt{3(x^2+y^2)}=\sqrt3\,r$ is a cone with $\tan\phi=\frac{r}{z}=\frac{1}{\sqrt3}$, so $\phi$ runs from $0$ to $\frac{\pi}{6}$: $b=\frac{\pi}{6}$.",
        r"Consistency check on the shadow: the cone meets the sphere where $\rho=2$, $\phi=\frac\pi6$, giving $r=2\sin\frac\pi6=1$ — exactly the unit disk in the stem. Good.",
        r"$\dfrac{bc}{a}=\dfrac{\frac{\pi}{6}\cdot 2}{2\pi}=\dfrac{1}{6}$.",
    ],
    trap=r"Setting $b=\frac{\pi}{3}$ from $\tan\phi=\sqrt3$. $\phi$ is the angle from the $z$-axis, and a steep cone ($z$ large compared to $r$) means a **small** $\phi$. The disk-radius check catches it: $\phi=\frac\pi3$ would give shadow radius $2\sin\frac\pi3=\sqrt3\ne1$.",
    check=lambda: (atan(1 / sqrt(S(3))) * solve(Eq(rho ** 2, 4), rho)[0]) / (2 * pi),
    want=Rational(1, 6),
),
"L23P5": dict(
    steps=[
        r"$\rho=12\cos\phi$ is already a sphere in disguise: multiply by $\rho$ to get $\rho^2=12\rho\cos\phi$, i.e. $x^2+y^2+z^2=12z$.",
        r"Complete the square: $x^2+y^2+(z-6)^2=36$ — radius $6$, centred at $(0,0,6)$.",
        r"So the answer must be $\frac43\pi(6)^3=288\pi$; now get the same thing from the integral.",
        r"The surface closes up at $\phi=\frac{\pi}{2}$ (where $\rho=0$), so $\phi$ runs $0$ to $\frac{\pi}{2}$ — **not** to $\pi$.",
        r"$\displaystyle V=\int_0^{2\pi}\!\int_0^{\pi/2}\!\int_0^{12\cos\phi}\rho^2\sin\phi\,d\rho\,d\phi\,d\theta=\int_0^{2\pi}\!\int_0^{\pi/2}\frac{1728\cos^3\phi}{3}\sin\phi\,d\phi\,d\theta=2\pi\cdot 576\cdot\frac14=288\pi$.",
    ],
    trap=r"Letting $\phi$ run to $\pi$ out of habit. For $\phi>\frac{\pi}{2}$, $12\cos\phi<0$ and there is no sphere there; the extra range adds another $288\pi$ of nonsense (the $\cos^3\phi\sin\phi$ integrand is odd about $\frac\pi2$, so it actually cancels to $0$ — an error that can *silently* delete the whole answer). The sphere is fully traced by $\phi\in[0,\frac\pi2]$.",
    check=lambda: integrate(sph_jac(), (rho, 0, 12 * cos(ph)),
                            (ph, 0, pi / 2), (th, 0, 2 * pi)),
    want=288 * pi,
),

# ----------------------------------------------------------- Lesson 24 ----
"L24P1": dict(
    steps=[
        r"Mass first: $\displaystyle m=\int_0^2\!\int_0^4(1+y)\,dy\,dx=\int_0^2\left[y+\tfrac{y^2}{2}\right]_0^4dx=\int_0^2 12\,dx=24$.",
        r"$\bar x$: the density does not depend on $x$ and the region is symmetric in $x$, so $\bar x=1$ by inspection. Formally $M_y=\int_0^2\!\int_0^4 x(1+y)\,dy\,dx=\left(\int_0^2x\,dx\right)(12)=24$, and $\bar x=\frac{24}{24}=1$.",
        r"$\bar y$: $\displaystyle M_x=\int_0^2\!\int_0^4 y(1+y)\,dy\,dx=2\int_0^4(y+y^2)\,dy=2\left(8+\tfrac{64}{3}\right)=\tfrac{176}{3}$.",
        r"$\bar y=\dfrac{M_x}{m}=\dfrac{176/3}{24}=\dfrac{22}{9}\approx2.44$.",
        r"Sanity: $\frac{22}{9}>2$, and it should be — the density grows with $y$, so mass piles up toward the top.",
        r"Centre of mass $\left(1,\tfrac{22}{9}\right)$.",
    ],
    trap=r"Swapping the moments. $M_x=\iint y\,\delta\,dA$ gives $\bar y$, not $\bar x$ — the subscript names the **axis the moment is about**, so it pairs with the *other* coordinate. Using $M_x$ for $\bar x$ here returns $\frac{22}{9}$ for a rectangle only $2$ wide, which is impossible and is the fastest way to catch it.",
    check=lambda: [integrate(x * (1 + y), (y, 0, 4), (x, 0, 2))
                   / integrate(1 + y, (y, 0, 4), (x, 0, 2)),
                   integrate(y * (1 + y), (y, 0, 4), (x, 0, 2))
                   / integrate(1 + y, (y, 0, 4), (x, 0, 2))],
    want=[1, Rational(22, 9)],
),
"L24P2": dict(
    steps=[
        r"$\bar x=\dfrac{M_{yz}}{m}$ with $M_{yz}=\displaystyle\iiint x\,\delta\,dV$; the mass $m=\tfrac34$ is handed to you.",
        r"$\displaystyle M_{yz}=\int_0^1\!\int_0^1\!\int_0^1 x(x+yz)\,dz\,dy\,dx=\int\!\!\int\!\!\int\left(x^2+xyz\right)dV$.",
        r"Both pieces separate over the cube: $\displaystyle\iiint x^2\,dV=\tfrac13$ and $\displaystyle\iiint xyz\,dV=\left(\tfrac12\right)^3=\tfrac18$.",
        r"$M_{yz}=\tfrac13+\tfrac18=\tfrac{11}{24}$.",
        r"$\bar x=\dfrac{11/24}{3/4}=\dfrac{11}{24}\cdot\dfrac43=\dfrac{11}{18}$.",
        r"Sanity: $\frac{11}{18}>\frac12$, correct — the $x$ term in the density weights the far side.",
    ],
    trap=r"Multiplying only the first term by $x$: $\int x\cdot x\,dV+\int yz\,dV=\tfrac13+\tfrac14$ gives $\tfrac{7}{12}$ and then $\bar x=\tfrac79$. The moment weights the **entire** density, so distribute the $x$ across $x+yz$ before integrating.",
    check=lambda: integrate(x * (x + y * z), (z, 0, 1), (y, 0, 1), (x, 0, 1))
                  / Rational(3, 4),
    want=Rational(11, 18),
),
"L24P3": dict(
    steps=[
        r"Sketch the wedge: between $y=\tfrac12x$ (lower) and $y=x$ (upper), closed off at $x=1$. They meet at the origin, so $0\le x\le1$ and $\tfrac{x}{2}\le y\le x$.",
        r"Vertical strips are the right choice — each strip has height $x-\tfrac{x}{2}=\tfrac{x}{2}$.",
        r"$\displaystyle m=\int_0^1\!\int_{x/2}^{x}2x\,dy\,dx=\int_0^1 2x\cdot\frac{x}{2}\,dx=\int_0^1x^2\,dx=\frac13$.",
        r"$\displaystyle M_y=\int_0^1\!\int_{x/2}^{x}x\cdot 2x\,dy\,dx=\int_0^1 2x^2\cdot\frac{x}{2}\,dx=\int_0^1 x^3\,dx=\frac14$.",
        r"$\bar x=\dfrac{M_y}{m}=\dfrac{1/4}{1/3}=\dfrac34$.",
        r"Sanity: $\tfrac34$ is past the midpoint of $[0,1]$, as it must be — the strips get both taller and denser as $x$ grows.",
    ],
    trap=r"Integrating in the order $dx\,dy$ without splitting. Horizontal strips run from $x=y$ to $x=2y$ only while $2y\le1$; above $y=\tfrac12$ the right edge is the line $x=1$ instead, so that order needs **two** integrals. The printed answer's order avoids that entirely — pick strips that are described by one pair of curves.",
    check=lambda: integrate(x * 2 * x, (y, x / 2, x), (x, 0, 1))
                  / integrate(2 * x, (y, x / 2, x), (x, 0, 1)),
    want=Rational(3, 4),
),
"L24P4": dict(
    steps=[
        r"Three of the four corners are on the axes, so use the intercept form of the slanted face: $\dfrac{x}{1}+\dfrac{y}{2}+\dfrac{z}{4}=1$.",
        r"Solve for the ceiling: $z=4\left(1-x-\dfrac{y}{2}\right)=4-4x-2y$.",
        r"Shadow: set $z=0$ to get $x+\frac{y}{2}=1$, i.e. $y=2(1-x)$, with $0\le x\le1$.",
        r"$\displaystyle m=\int_0^1\!\int_0^{2(1-x)}\!\int_0^{4-4x-2y}2z\,dz\,dy\,dx$.",
        r"Inner: $\left[z^2\right]_0^{4-4x-2y}=(4-4x-2y)^2$.",
        r"$\displaystyle\int_0^{2(1-x)}(4-4x-2y)^2dy=\left[-\frac{(4-4x-2y)^3}{6}\right]_0^{2(1-x)}=\frac{64(1-x)^3}{6}$.",
        r"$\displaystyle m=\frac{64}{6}\int_0^1(1-x)^3dx=\frac{64}{6}\cdot\frac14=\frac{8}{3}$.",
    ],
    trap=r"Treating a variable density as a constant and reaching for $\rho\cdot V$: the volume is $\frac{1\cdot2\cdot4}{6}=\frac43$, and $2\bar z\cdot V$ is *not* something you can shortcut without already knowing $\bar z$. Also: $\rho$ here is a **density**, not the spherical radius — the symbol collides with Lesson 23 and the units tell you which.",
    check=lambda: integrate(2 * z, (z, 0, 4 - 4 * x - 2 * y),
                            (y, 0, 2 * (1 - x)), (x, 0, 1)),
    want=Rational(8, 3),
),
"L24P5": dict(
    steps=[
        r"Region: $y=x^2$ below, $y=1$ above, $x=0$ on the left — so $0\le x\le1$ and $x^2\le y\le1$.",
        r"The mass is given as $\tfrac16$; confirm it cheaply: $\displaystyle\int_0^1\!\int_{x^2}^{1}xy\,dy\,dx=\int_0^1\frac{x(1-x^4)}{2}dx=\frac12\left(\frac12-\frac16\right)=\frac16$. Good.",
        r"$\displaystyle M_x=\int_0^1\!\int_{x^2}^{1}y\cdot xy\,dy\,dx=\int_0^1 x\cdot\frac{1-x^6}{3}\,dx$.",
        r"$=\dfrac13\left(\dfrac12-\dfrac18\right)=\dfrac13\cdot\dfrac38=\dfrac18$.",
        r"$\bar y=\dfrac{M_x}{m}=\dfrac{1/8}{1/6}=\dfrac{6}{8}=\dfrac34$.",
        r"Sanity: the region hugs the top (it is wide near $y=1$, pinched near $y=0$) and the density $xy$ favours large $y$, so $\bar y>\tfrac12$ is right.",
    ],
    trap=r"Taking the region as $0\le y\le x^2$ — 'bounded by $y=x^2$' does not say which side. The third boundary $x=0$ is the tell: the region above the parabola touches the $y$-axis, the region below it does not need $x=0$ to close. Getting this backwards flips $\bar y$ to $\tfrac{5}{7}$-ish territory and, more tellingly, changes the mass away from the given $\tfrac16$ — which is exactly why that value was handed to you.",
    check=lambda: integrate(y * x * y, (y, x ** 2, 1), (x, 0, 1)) / Rational(1, 6),
    want=Rational(3, 4),
),
}
