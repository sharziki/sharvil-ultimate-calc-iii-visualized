"""The two halves of 13.6 the guide was missing.

Lesson 3 of MA 26100 Fall 2026 is "13.5 planes, 13.6 (to Ex 2)". In Briggs 3e
section 13.6 is *Cylinders and Quadric Surfaces*, and it opens with cylinders —
so "13.6 to Example 2" is largely the cylinder material. The guide's s136 went
straight to the six quadrics, leaving that first half untaught even though the
question bank tests it twice (a circular cylinder and a parabolic cylinder).

The identify-a-quadric algorithm also said "standard form first" and stopped,
never showing how to get there when the equation arrives shifted off the origin.

This module adds both and is consumed by *two* callers, because quizpage.py
reads guide.src.html directly rather than the patched guide:

    patch_guide.run()      -> guide.html
    quizpage.guide_parts() -> quiz.html

Both call augment(). One source of truth, same as guide_121.

Markup: $inline$ and $$display$$ TeX, everything else literal HTML.
"""

import sys

# ------------------------------------------------------------------ svg ----
# A curve in one coordinate plane, dragged along the missing axis.
# No TeX in here: the SVG is spliced in after M() has run, so $...$ would
# ship raw. Use entities, as guide_121 does. Left: the
# 2-D circle you would draw in a plane. Right: the same equation in space.

SVG = """
<svg viewBox="0 0 470 250" role="img" aria-label="Left panel: the circle x squared plus z squared equals nine drawn in the xz-plane. Right panel: the same equation in three dimensions, the circle swept along the y-axis into an infinite tube, with ruling lines parallel to the y-axis">
  <text class="sm" x="16" y="16">IN THE PLANE</text>
  <line class="s t1 mut" x1="24" y1="140" x2="212" y2="140"/>
  <line class="s t1 mut" x1="118" y1="46" x2="118" y2="234"/>
  <text class="sm mut" x="216" y="144">x</text>
  <text class="sm mut" x="110" y="40">z</text>
  <circle class="s t3 ac" cx="118" cy="140" r="66" fill="none"/>
  <text class="b c" x="146" y="86">x&#178; + z&#178; = 9</text>
  <text class="sm mut" x="24" y="226">a circle, radius 3</text>

  <line class="s t1 mut dash" x1="240" y1="12" x2="240" y2="238"/>

  <text class="sm" x="264" y="16">IN SPACE — y IS FREE</text>
  <line class="s t1 mut" x1="272" y1="176" x2="452" y2="176"/>
  <text class="sm mut" x="456" y="180">y</text>

  <ellipse class="s t3 ac" cx="318" cy="140" rx="20" ry="58" fill="none"/>
  <ellipse class="s t3 ac" cx="410" cy="140" rx="20" ry="58" fill="none"/>
  <line class="s t2 ac" x1="318" y1="82" x2="410" y2="82"/>
  <line class="s t2 ac" x1="318" y1="198" x2="410" y2="198"/>
  <line class="s t1 ac dash" x1="298" y1="140" x2="390" y2="140"/>
  <line class="s t1 ac dash" x1="338" y1="140" x2="430" y2="140"/>

  <text class="b c" x="286" y="228">same equation, no y</text>
  <text class="sm mut" x="286" y="244">rulings run along the y-axis</text>
</svg>
"""

# -------------------------------------------------------------- content ----

CYLINDERS = r"""<p class="say">Section 13.6 has <b>two halves</b>, and the first one is
    nearly free. A <b>cylinder</b> is what you get when a variable is <b>missing</b> from
    the equation. Missing means unconstrained: that coordinate may be anything at all, so
    the curve drawn in the other two variables is dragged along the whole missing axis.
    A cylinder in this course is not necessarily round &mdash; it is any curve times a line.</p>

    <div class="mathd"><span class="lbl">a missing variable is a swept axis</span>
    $$x^{2}+z^{2}=9\qquad\text{(no }y\text{)}$$</div>

    <p class="say">In the $xz$-plane that is a circle of radius $3$. In space, nothing
    constrains $y$, so every height $y=k$ gives the <em>same</em> circle. Stack them and you
    get an infinite tube whose axis is the $y$-axis.</p>

    <figure class="fig"><div class="box">SVGHERE
      <figcaption>The equation never mentions $y$, so $y$ is free. The circle repeats at
      every $y$ &mdash; the straight lines along the tube are the <b>rulings</b>, and they
      run parallel to the axis of the variable that went missing.</figcaption>
    </div></figure>

    <div class="algo"><h4>Algorithm &middot; name a cylinder</h4>
      <ol>
        <li><b>Spot the missing variable.</b> One of $x$, $y$, $z$ does not appear. If all
        three appear, it is not a cylinder &mdash; go to the quadric test below.</li>
        <li><b>Read the curve</b> formed by the two that remain, in their own coordinate
        plane: circle, ellipse, parabola, hyperbola, or a pair of lines.</li>
        <li><b>Sweep it</b> along the missing variable's axis. That axis is the direction of
        the rulings.</li>
        <li><b>Name it after the curve.</b> Circular, elliptic, parabolic or hyperbolic
        cylinder &mdash; then say which axis the rulings are parallel to. Both halves are
        expected in the answer.</li>
      </ol>
      <p class="tail">$y=-z^{2}$ has no $x$: a parabola in the $yz$-plane opening toward
      $-y$, swept along the $x$-axis. A <b>parabolic cylinder</b>, rulings parallel to the
      $x$-axis.</p>
    </div>

    <div class="trap"><h4>Trap</h4>
      <p>$x^{2}+z^{2}=9$ is a <b>circle</b> in two dimensions and a <b>tube</b> in three.
      The question decides which by telling you the ambient space, and 13.6 is a chapter
      about surfaces in $\mathbb{R}^{3}$ &mdash; so the answer is the tube. Answering
      &ldquo;a circle of radius 3&rdquo; is the single most common way to drop this
      question.</p>
    </div>

    """

COMPLETE_SQUARE = r"""<div class="algo"><h4>Algorithm &middot; complete the square into standard form</h4>
      <ol>
        <li><b>Group by variable</b> and move the bare constant to the right-hand side.</li>
        <li><b>Factor out</b> the coefficient of each squared term, so the bracket opens
        with a bare $x^{2}$, $y^{2}$ or $z^{2}$.</li>
        <li><b>Complete each square</b> by adding $(b/2)^{2}$ <em>inside</em> the bracket.
        Because the bracket is multiplied by that factored-out coefficient, what you must
        add to the other side is $a\cdot(b/2)^{2}$, not $(b/2)^{2}$. This is where the
        arithmetic goes wrong.</li>
        <li><b>Divide</b> so the right side is $1$ (or $0$).</li>
        <li><b>Now count the minus signs</b> with the algorithm above. Shifting a surface
        never changes what it is &mdash; only where it sits.</li>
      </ol>
    </div>

    <div class="mathd v"><span class="lbl">worked &middot; $4x^{2}-y^{2}+z^{2}+8x=0$</span>
    $$\begin{aligned}
    4(x^{2}+2x)-y^{2}+z^{2}&=0\\[2pt]
    4(x^{2}+2x+1)-y^{2}+z^{2}&=0+4\cdot 1\\[2pt]
    4(x+1)^{2}-y^{2}+z^{2}&=4\\[2pt]
    (x+1)^{2}-\tfrac{y^{2}}{4}+\tfrac{z^{2}}{4}&=1
    \end{aligned}$$</div>

    <p class="say">One minus sign, right side $1$: a <b>hyperboloid of one sheet</b>, axis
    the $y$-axis, centred at $(-1,0,0)$. The $+8x$ only moved it one unit along $x$; the
    surface was never anything else.</p>

    """

# Extra check-yourself items appended to the section's existing list.
CHECKS = r"""<li><p class="qt">In space, what is $x^{2}+z^{2}=9$?</p><details><summary>Answer</summary><div class="ans">No $y$, so $y$ is free: a <b>circular cylinder</b> of radius $3$ with rulings parallel to the <b>$y$-axis</b>. In the plane it would be a circle; in $\mathbb{R}^{3}$ it is a tube.</div></details></li>
    <li><p class="qt">Identify $y=-z^{2}$ in three dimensions.</p><details><summary>Answer</summary><div class="ans">No $x$: a <b>parabolic cylinder</b>, the parabola $y=-z^{2}$ in the $yz$-plane opening toward $-y$, swept along the <b>$x$-axis</b>.</div></details></li>
    <li><p class="qt">Put $9x^{2}+4y^{2}+36z^{2}-18x=27$ into standard form and identify it.</p><details><summary>Answer</summary><div class="ans">$9(x^{2}-2x)=9(x-1)^{2}-9$, so $9(x-1)^{2}+4y^{2}+36z^{2}=36$, i.e. $\tfrac{(x-1)^{2}}{4}+\tfrac{y^{2}}{9}+z^{2}=1$. No minus signs &rarr; an <b>ellipsoid</b> centred at $(1,0,0)$.</div></details></li>
    """


def augment(sec_html, M):
    """Insert cylinders and completing-the-square into the s136 markup.

    `sec_html` is either the whole <article id="s136"> element (patch_guide) or
    its inner HTML (quizpage) — both contain every anchor used here. Raises via
    sys.exit if the guide source moves out from under it, matching the rest of
    the build's fail-loudly contract.
    """
    def one(hay, needle, repl, why):
        if hay.count(needle) != 1:
            sys.exit(f"guide_136: {why} — found {hay.count(needle)} anchors, expected 1")
        return hay.replace(needle, repl, 1)

    h = sec_html

    # Briggs calls 13.6 "Cylinders and Quadric Surfaces"; say so now that the
    # section actually covers both.
    h = one(h, "<h3>Quadric surfaces</h3>",
            "<h3>Cylinders &amp; quadric surfaces</h3>",
            "section title")

    # Order matters. Both remaining inserts anchor on markup that the cylinder
    # block itself contains (it ends with its own .trap), so do them while the
    # section still has exactly one of each.

    # Standard form belongs with the algorithm that demands it.
    h = one(h, '<div class="trap">', M(COMPLETE_SQUARE) + '<div class="trap">',
            "trap anchor")

    # Three more self-checks on exactly the two new skills. Anchor on the list
    # head — the existing items all open with "Identify", so that is not unique.
    h = one(h, '<div class="check"><h4>Check yourself</h4><ol>',
            '<div class="check"><h4>Check yourself</h4><ol>\n    ' + M(CHECKS),
            "check list")

    # Cylinders go last but read first: they lead in Briggs and in Lesson 3.
    cyl = M(CYLINDERS).replace("SVGHERE", SVG)
    h = one(h, '<p class="say">Every quadric is decided by',
            cyl + '<p class="say">Now the other half. Every quadric is decided by',
            "quadric lede")

    return h
