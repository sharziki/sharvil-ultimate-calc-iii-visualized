"""A 12.1 section for the guide.

Lesson 2 of MA 26100 Fall 2026 is "12.1 (to Ex 3), 13.5 lines". The guide was
built for the advanced-credit exam, which never touched 12.1, so it starts at
13.1 — leaving half of Quiz 1 uncovered. This adds it.

Markup: $inline$ and $$display$$ TeX, everything else literal HTML.
"""

SVG = """
<svg viewBox="0 0 470 250" role="img" aria-label="Left panel: an ellipse traced counterclockwise with tick marks at t equals 0, pi over 2, pi and 3 pi over 2, showing where the point is at each time. Right panel: the same ellipse traced twice as fast and in the opposite direction, showing that one curve has many parametrizations">
  <text class="sm" x="16" y="16">ONE CURVE</text>
  <line class="s t1 mut" x1="24" y1="140" x2="212" y2="140"/>
  <line class="s t1 mut" x1="118" y1="42" x2="118" y2="238"/>
  <ellipse class="s t3 ac" cx="118" cy="140" rx="72" ry="92" fill="none"/>
  <circle class="c" cx="190" cy="140" r="4.5" fill="currentColor"/>
  <text class="b c" x="196" y="136">t = 0</text>
  <circle class="c" cx="118" cy="48" r="4.5" fill="currentColor"/>
  <text class="b c" x="126" y="44">t = &#960;/2</text>
  <circle class="c" cx="46" cy="140" r="4.5" fill="currentColor"/>
  <text class="b c" x="10" y="158">t = &#960;</text>
  <circle class="c" cx="118" cy="232" r="4.5" fill="currentColor"/>
  <text class="b c" x="126" y="244">t = 3&#960;/2</text>
  <path class="s t3 ac" d="M172,86 A72,92 0 0,0 140,54" fill="none" marker-end="url(#arc)"/>

  <line class="s t1 mut dash" x1="240" y1="12" x2="240" y2="238"/>

  <text class="sm" x="264" y="16">SAME CURVE, DIFFERENT BUG</text>
  <line class="s t1 mut" x1="272" y1="140" x2="460" y2="140"/>
  <line class="s t1 mut" x1="366" y1="42" x2="366" y2="238"/>
  <ellipse class="s t3 vg" cx="366" cy="140" rx="72" ry="92" fill="none"/>
  <circle class="v" cx="438" cy="140" r="4.5" fill="currentColor"/>
  <text class="b v" x="410" y="132">t = 0</text>
  <path class="s t3 vg" d="M420,194 A72,92 0 0,1 388,226" fill="none" marker-end="url(#arv)"/>
</svg>
"""

HTML = r"""<article class="sec" id="s121">
    <div class="sec-h"><span class="sec-n">12.1</span><h3>Parametric equations</h3></div>
    <p class="say">A Cartesian equation tells you <b>where a curve is</b>. A parametrization
    tells you <b>how a point moves along it</b> &mdash; where it starts, which way it goes,
    how fast, and how many times round. Those extra facts are the whole reason the rest
    of this course uses parametrizations for everything: curves in space, surfaces,
    line integrals, flux. This is where they start.</p>

    <div class="mathd"><span class="lbl">a plane curve, parametrized</span>
    $$x=f(t),\qquad y=g(t),\qquad a\le t\le b$$</div>

    <p class="say">Think of $t$ as time and $(f(t),g(t))$ as the position of a bug. Sweep $t$
    from $a$ to $b$ and the bug draws the curve. Different bugs can draw the same picture.</p>

    <figure class="fig"><div class="box">SVGHERE
      <figcaption>Both bugs draw <b>the same ellipse</b>. The orange one goes
      counterclockwise once; the green one goes clockwise, twice as fast, twice around.
      They disagree about direction, speed, and how many laps. Eliminating the parameter keeps the picture and throws
      all three away &mdash; which is exactly the information line integrals care about.</figcaption>
    </div></figure>

    <div class="mathd v"><span class="lbl">the three you must know cold</span>
    $$\begin{aligned}
    \textsf{segment } P\to Q:&\quad \mathbf r(t)=P+t\,(Q-P),\qquad 0\le t\le 1\\[4pt]
    \textsf{circle, centre }(h,k)\textsf{, radius }R:&\quad x=h+R\cos t,\quad y=k+R\sin t,\qquad 0\le t\le 2\pi\\[4pt]
    \textsf{ellipse, semi-axes }a,b:&\quad x=h+a\cos t,\quad y=k+b\sin t,\qquad 0\le t\le 2\pi
    \end{aligned}$$</div>

    <p class="note">All three run <b>counterclockwise</b> as written, and all three start at
    the rightmost point when $t=0$. Swap $\sin$ and $\cos$, or negate one of them, and you
    change the starting point or the direction &mdash; never the picture.</p>

    <div class="algo"><h4>Algorithm &middot; eliminate the parameter</h4>
      <ol>
        <li><b>Look for the trig identity first.</b> If you see $\cos t$ and $\sin t$, solve each
        equation for the trig function and use $\cos^2t+\sin^2t=1$. Do not try to solve for $t$.</li>
        <li><b>Otherwise solve the easier equation for $t$</b> &mdash; usually the linear one &mdash;
        and substitute into the other.</li>
        <li><b>Carry the range across.</b> Ask what values $x$ and $y$ actually take as $t$ runs
        over its interval. The Cartesian equation on its own will usually describe <em>more</em>
        curve than you have.</li>
        <li><b>Say the direction out loud.</b> Plug in $t=a$, the midpoint, and $t=b$, and mark
        the three points in order. That is the orientation, and no Cartesian equation records it.</li>
      </ol>
      <p class="tail">Steps 3 and 4 are where the marks are. Step 1 and 2 are algebra you already have.</p>
    </div>

    <div class="ex"><h4>Worked example</h4>
      <p>Describe the curve $x=2\cos t,\;y=3\sin t$, $0\le t\le\pi$.</p>
      <div class="step"><span>identity</span><p>$\cos t=\dfrac{x}{2}$ and $\sin t=\dfrac{y}{3}$, so
      $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ &mdash; an ellipse with semi-axes $2$ and $3$.</p></div>
      <div class="step"><span>range</span><p>On $0\le t\le\pi$, $\sin t\ge 0$, so $y\ge 0$.
      Only the <b>upper half</b> of the ellipse.</p></div>
      <div class="step"><span>direction</span><p>$t=0\Rightarrow(2,0)$; $t=\tfrac{\pi}{2}\Rightarrow(0,3)$;
      $t=\pi\Rightarrow(-2,0)$. Right, up, left &mdash; counterclockwise.</p></div>
      <div class="step"><span>answer</span><p>The upper half of $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$,
      traced once counterclockwise from $(2,0)$ to $(-2,0)$.</p></div>
    </div>

    <div class="trap"><h4>Trap</h4>
      <p><b>&ldquo;Eliminate the parameter&rdquo; is a lossy operation.</b> $x=t,\;y=t^2$ and
      $x=t^2,\;y=t^4$ both give $y=x^2$, but the first is the whole parabola and the second is
      only its right half, traced in and back out. If a question mentions direction, a starting
      point, or a number of laps, the Cartesian equation cannot answer it &mdash; keep the
      parametrization.</p>
    </div>

    <p class="note">Where this reappears: <b>13.5</b> writes a line as $\mathbf r(t)=\mathbf r_0+t\mathbf v$,
    which is the segment recipe with the range removed. <b>14.1</b> is this section with a third
    coordinate bolted on. <b>17.2</b> integrates along one of these, and the orientation you were
    told to keep track of here is what decides the sign of the answer.</p>

    <div class="check"><h4>Check yourself</h4><ol>
    <li><p class="qt">Parametrize the segment from $(-1,4)$ to $(3,2)$ on $0\le t\le1$.</p>
      <details><summary>Answer</summary><div class="ans">$x=-1+4t,\;y=4-2t$. Start, plus $t$ times
      the displacement $\langle 4,-2\rangle$.</div></details></li>
    <li><p class="qt">What curve is $x=1+3\cos t,\;y=-2+3\sin t$, $0\le t\le 2\pi$?</p>
      <details><summary>Answer</summary><div class="ans">The circle of radius $3$ centred at
      $(1,-2)$, once counterclockwise from $(4,-2)$: $(x-1)^2+(y+2)^2=9$.</div></details></li>
    <li><p class="qt">$x=\sin t,\;y=\sin^2 t$. Cartesian equation, and how much of it?</p>
      <details><summary>Answer</summary><div class="ans">$y=x^2$, but only the arc with
      $-1\le x\le 1$, and the point retraces it back and forth forever.</div></details></li>
    <li><p class="qt">Two parametrizations give the same Cartesian equation. Name two things that
      can still differ.</p>
      <details><summary>Answer</summary><div class="ans">Orientation, speed, starting point, and
      how much of the curve is covered &mdash; any of these. Only the point set is shared.</div></details></li>
    </ol></div>
  </article>
"""


def html(M):
    """Render the section. M is build.py's TeX renderer."""
    return M(HTML).replace("SVGHERE", SVG)
