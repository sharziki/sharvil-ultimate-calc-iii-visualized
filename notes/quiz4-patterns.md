# Quiz 4 — MA 26100, Tue Sep 22 2026

Lessons 8–10 · **14.4 arc length · 14.5 curvature & TNB (to Thm 14.5) · 15.1 surfaces · 15.2 limits**

Everything below is the pattern set actually assigned in MyLab (14.4.9, .11, .13,
.23, .40, .42 · 14.5.11, .13, .15, .23 · 15.1.11, .15, .17, .19, .25, .28, .30,
.34, .35) plus the two 15.2 limit types the lesson plan adds.

The worked examples in *this* file use the homework's own numbers, because it is
a reference: you want to check your work against the problem you actually sat.
The **practice questions** in `quiz.html` deliberately do not — every one carries
different numbers, so drilling them exercises the method rather than your memory
of an answer you have already seen. `build/hwcheck.py` enforces that at build
time and refuses to emit on a collision.

---

## The one-page version

| Ask | Do this |
|---|---|
| Length of a curve | $L=\int_a^b\lvert\mathbf r'\rvert dt$. Simplify the speed **first** — it always collapses. |
| Speed | $\lvert\mathbf r'\rvert$. Factor the common power of $t$ out of the radical. |
| "Is $t$ arc length?" | Compute $\lvert\mathbf r'\rvert$. Equals $1$ for all $t$ → yes. Otherwise reparameterise. |
| Rewrite as $\mathbf r(s)$ | $s(t)=\int_a^t\lvert\mathbf r'\rvert du$, invert for $t$, substitute. |
| $\mathbf T$ | $\mathbf r'/\lvert\mathbf r'\rvert$. Must be unit — check the squares sum to 1. |
| $\kappa$ | $\lvert\mathbf T'\rvert/\lvert\mathbf r'\rvert$, or $\lvert\mathbf a\times\mathbf v\rvert/\lvert\mathbf v\rvert^3$ when told to. |
| Domain | Only three things restrict: denominators $\ne0$, even radicands $\ge0$, logs $>0$. |
| Range | Read the bounded piece: $x^2\ge0$, $\sqrt{\ }\ \ge0$, $\frac{1}{1+\cdot}\in(0,1]$. |
| Limit exists? | Two paths disagreeing kills it. All lines agreeing proves nothing — try $y=x^2$. |

---

## 14.4 · Arc length

### Type A — the speed collapses to $ct^n$
> 14.4.9, 14.4.23

$\mathbf r(t)=\langle 20t^2,\,-6,\,48t^2+5\rangle$ → $\mathbf r'=\langle40t,0,96t\rangle$,
$\lvert\mathbf r'\rvert=t\sqrt{1600+9216}=104t$, $L=\int_0^1 104t\,dt=\boxed{52}$.

Every constant component differentiates away. The design is always that the
radicand is a perfect square times $t^{2n}$.

- $\langle3t^3,-t^3,4t^3\rangle$: $\mathbf v=3t^2\langle3,-1,4\rangle$, speed $3\sqrt{26}\,t^2$, $L$ on $[0,6]$ is $216\sqrt{26}$.
- **Trap:** forgetting $\int_0^1 t\,dt=\tfrac12$ and answering the final speed.

### Type B — constant speed
> 14.4.11

$\langle3\cos t,3\sin t\rangle$ has speed $3$. $L=3\cdot(\text{parameter length})$.
On $0\le t\le\pi$: $3\pi$, half of $6\pi$.

### Type C — the $\sin t - t\cos t$ pair
> 14.4.13

$\mathbf r=\langle a\sin t-at\cos t,\;a\cos t+at\sin t\rangle$. Product rule makes
the non-$t$ terms cancel: $\mathbf r'=\langle at\sin t,\;at\cos t\rangle$, speed $at$.
With $a=4$ on $[0,\pi/2]$: $L=\int_0^{\pi/2}4t\,dt=\pi^2/2$.

**Recognise it by sight.** If your speed still has a loose $\sin$ or $\cos$ in it,
you dropped a product-rule term.

### Type D — is $t$ already arc length?
> 14.4.40 (no), 14.4.42 (yes)

The entire test is $\lvert\mathbf r'(t)\rvert=1$ **for every $t$**.

- $\left\langle\tfrac{1}{\sqrt2}\cos t,\tfrac{1}{\sqrt2}\cos t,\sin t\right\rangle$: speed$^2=\tfrac12\sin^2+\tfrac12\sin^2+\cos^2=1$. **Yes.**
- $\langle7t^2,8t^2,2\sqrt{14}t^2\rangle$ on $[1,4]$: speed $=26t\ne1$. **No.**

### Type E — reparameterise by arc length
> 14.4.40

1. Direction vector length: $\lvert\langle7,8,2\sqrt{14}\rangle\rvert=\sqrt{49+64+56}=13$.
2. $s(t)=\int_1^t 26u\,du=13(t^2-1)$, so $t^2=1+\frac{s}{13}$.
3. Substitute: $\mathbf r(s)=\left(1+\frac{s}{13}\right)\langle7,8,2\sqrt{14}\rangle
   =\left\langle 7+\frac{7s}{13},\,8+\frac{8s}{13},\,2\sqrt{14}+\frac{2\sqrt{14}s}{13}\right\rangle$.
4. Upper limit: $s(4)=13(16-1)=195$.

**Trap that cost a try:** writing the third component over $14$ instead of $13$.
*Every* component is divided by the same constant — the length of the direction
vector, never the component's own coefficient.

---

## 14.5 · Unit tangent and curvature

$$\mathbf T=\frac{\mathbf r'}{\lvert\mathbf r'\rvert}\qquad
\kappa=\frac{\lvert\mathbf T'\rvert}{\lvert\mathbf r'\rvert}
=\frac{\lvert\mathbf a\times\mathbf v\rvert}{\lvert\mathbf v\rvert^{3}}
\qquad\text{graph }y=f(x):\ \kappa=\frac{\lvert y''\rvert}{(1+(y')^2)^{3/2}}$$

### Type A — a line
> 14.5.11

$\langle2t+2,4t-8,5t+14\rangle$: $\mathbf r'=\langle2,4,5\rangle$ constant,
$\lvert\mathbf r'\rvert=\sqrt{45}=3\sqrt5$.
$\mathbf T=\left\langle\frac{2\sqrt5}{15},\frac{4\sqrt5}{15},\frac{\sqrt5}{3}\right\rangle$,
and $\kappa=\boxed{0}$ — **a straight line has no curvature.** Free mark.

### Type B — a helix
> 14.5.13

$\langle\sqrt3 t,3\sin t,3\cos t\rangle$: speed $\sqrt{3+9}=2\sqrt3$.
$\mathbf T=\left\langle\tfrac12,\tfrac{\sqrt3}{2}\cos t,-\tfrac{\sqrt3}{2}\sin t\right\rangle$,
$\lvert\mathbf T'\rvert=\tfrac{\sqrt3}{2}$, $\kappa=\tfrac{\sqrt3/2}{2\sqrt3}=\tfrac14$.

**Trap that cost a try:** the third component is $-\tfrac{\sqrt3}{2}\sin t$, not
$\cos t$. $\frac{d}{dt}(3\cos t)=-3\sin t$. This is the single most common lost
mark in the section.

### Type C — a circle in a tilted plane
> 14.5.15

$\langle\sqrt{19}\cos t,9\cos t,10\sin t\rangle$:
$\lvert\mathbf r'\rvert^2=19\sin^2+81\sin^2+100\cos^2=100$. The $19+81=100$ is
the whole point of the numbers.
$\mathbf T=\left\langle-\tfrac{\sqrt{19}}{10}\sin t,-\tfrac{9}{10}\sin t,\cos t\right\rangle$,
$\kappa=\tfrac{1}{10}$ — a circle of radius $10$.

**Trap that cost two tries:** $\sqrt{19}/10$ is **not** $\sqrt{19/10}$. In MyLab,
build the fraction first, then put $\sqrt{19}$ in the numerator.

### Type D — the alternative formula
> 14.5.23

$\mathbf r=\langle3+t^2,t,0\rangle$: $\mathbf v=\langle2t,1,0\rangle$,
$\mathbf a=\langle2,0,0\rangle$, $\mathbf a\times\mathbf v=\langle0,0,2\rangle$.
$$\kappa=\frac{2}{(4t^2+1)^{3/2}}$$
The denominator is the **speed cubed**, and the speed already has a root:
$(\sqrt u)^3=u^{3/2}$.

---

## 15.1 · Surfaces, domains, ranges, level curves

### Level curves
> 15.1.11

Set $z=z_0$ and read the plane curve.

| Surface | Level curves $z=z_0$ |
|---|---|
| $z=x^2+y^2$ | circles $x^2+y^2=z_0$, radius $\sqrt{z_0}$, crowding as you climb |
| $z=x^2+4y^2$ | ellipses |
| $z=x^2-y^2$ | hyperbolas, asymptotic to $y=\pm x$ |
| $z=ax+by$ | parallel lines |
| $z=1-x^2$ | parallel lines (no $y$) |

Do not confuse level curves (horizontal slices, drawn in the $xy$-plane) with
traces in the $xz$- or $yz$-planes.

### Domains — only three things ever restrict
> 15.1.15, .17, .19

| Form | Restriction |
|---|---|
| polynomial, e.g. $9xy+5x+4y$ | none: $\mathbb R^2$ |
| $\sqrt{12-3x^2-3y^2}$ | radicand $\ge0$ → $x^2+y^2\le4$ (**closed** disc; divide by the 3) |
| $\sin\!\left(\frac{x-6}{y-8}\right)$ | only the fraction: $y\ne8$. Sine eats every real. |
| $\ln(\cdot)$ | strictly $>0$ |
| $\frac{1}{x-y}$ | $x\ne y$ |

Radicals give **closed** conditions ($\le,\ge$); logs and denominators give
**strict** ones. A trig function outside never restricts — $[-1,1]$ is sine's
*range*, not its domain.

### Sketch + domain + range
> 15.1.25, .28, .30

| $f$ | Graph | Domain | Range |
|---|---|---|---|
| $5x+4y-20$ | plane, intercepts $(4,0,0)$, $(0,5,0)$, $(0,0,-20)$ | $\mathbb R^2$ | $\mathbb R$ |
| $1-x^2$ | parabolic **cylinder**, flat along $y$ | $\mathbb R^2$ | $z\le1$ |
| $\sqrt{1-x^2-y^2}$ | **upper** hemisphere | $x^2+y^2\le1$ | $0\le z\le1$ |

- Intercepts **divide** by the coefficient: $5x=20\Rightarrow x=4$. Big coefficient, small intercept.
- A missing variable means a cylinder, never a paraboloid.
- A square root is never negative, so a whole sphere is never a function's graph.

### Matching surfaces and contours
> 15.1.34, .35

Read **singularities and bounds** before shape.

| Function | Tell | Picture |
|---|---|---|
| $\cos xy$ | bounded in $[-1,1]$, oscillates forever | rippled sheet |
| $\ln(x^2+y^2)$ | $\to-\infty$ at one **point** | funnel at the origin |
| $\frac{1}{x-y}$ | blows up along a whole **line** $y=x$, sign flip | two torn sheets |
| $\frac{1}{1+x^2+y^2}$ | denominator never zero, max $1$ | one smooth bump |

Contours: each local max is its own nest of closed loops. Two peaks separated
along $y$ → two nests stacked **along $y$**. Concentric circles = one summit.
Crossing asymptotes = saddle. Parallel lines = a variable is missing.

---

## 15.2 · Limits

**To kill a limit:** exhibit two paths with different values.
**To prove one:** squeeze, or polar coordinates. Paths never prove existence.

| Limit at $(0,0)$ | Verdict | Why |
|---|---|---|
| $\frac{xy}{x^2+y^2}$ | DNE | $y=0$ → $0$; $y=x$ → $\tfrac12$. Along $y=mx$: $\frac{m}{1+m^2}$. |
| $\frac{x^2-y^2}{x^2+y^2}$ | DNE | $y=0$ → $1$; $x=0$ → $-1$ |
| $\frac{x^2y}{x^4+y^2}$ | DNE | every **line** gives 0, but $y=x^2$ gives $\tfrac12$ |
| $\frac{x^2y}{x^2+y^2}$ | $=0$ | $\left\lvert\cdot\right\rvert\le\lvert y\rvert$; polar $r\cos^2\theta\sin\theta\to0$ |

Match the path to the denominator: $x^4$ against $y^2$ is telling you to try
$y=x^2$. Continuity: a rational function is continuous wherever the
**denominator** is nonzero — $\frac{x+y}{x^2-y}$ fails only on $y=x^2$; numerator
zeros are just zeros.

---

## What to do the night before

1. Recompute all four $\kappa$ types cold (line = 0, helix, tilted circle, $\mathbf a\times\mathbf v$).
2. Reparameterise one curve by arc length end to end, including the new upper limit.
3. Say out loud, for six functions, which of the three things restricts the domain.
4. Two-path any limit that has matching even powers upstairs and downstairs.
5. Drill mode on the Quiz 4 tab until every question comes back clean twice.
