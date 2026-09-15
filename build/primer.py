"""From-zero primers: build the lesson up from things you already believe.

Not a summary and not a cheat sheet. The guide sections organise material for
someone who has seen it; this is for someone starting at zero the night before,
and it follows the one rule that reliably works:

    "When he stalls, suspect notation before concept. Strip to concrete numbers,
     run the procedure once by hand with actual digits, then reintroduce the
     symbols as shorthand for what he just did."

The difference between this and a cheat sheet is that **nothing is asserted**.
Every rule on the quiz gets derived from something already obvious:

  * slot-by-slot differentiation is *proved* from the limit definition, not
    stated as a convention
  * the derivative being tangent is argued from what a chord does as it shortens
  * speed being $|\\vec r\\,{}'|$ falls out of distance-over-time
  * arc length is not a new formula, it is distance = rate x time, summed
  * "acceleration leans inward" is two lines of algebra from $|\\vec v|$ constant
  * projectile motion is Newton plus the integrals you just derived

A formula you have watched appear is a formula you can rebuild at 8am when you
have forgotten it. That is the whole point of doing it this way.

Order inside each primer: one sentence, concrete digits, the derivation, the
symbols mapped back to the digits, the two jobs, the jingle last.
"""

PRIMERS = {
    "q3": dict(
        title="Build it from nothing",
        lede="Lessons 5&ndash;7 contain exactly one new idea, and every formula "
             "on the quiz can be re-derived from it in under a minute. "
             "Twenty minutes here and you are not memorising anything.",
        blocks=[

            # ---------------------------------------------------------- 1 ----
            dict(
                h="Step 0 · Two things you already have",
                body=[
                    "<p>You already know both halves of this chapter. They have "
                    "just never been introduced to each other.</p>",
                    "<p><b>A function</b> takes a number and hands you back a "
                    "number. $f(t) = t^2$: feed it 3, get 9.</p>",
                    "<p><b>A vector</b> is a list of numbers that means a "
                    "location or a direction. $\\langle 1, 3, 5\\rangle$ is "
                    "\"1 across, 3 back, 5 up\".</p>",
                    "<p class=\"twojobs\">Glue them: a <b>vector function</b> "
                    "takes a number and hands you back a <i>list</i>. Feed it a "
                    "time, get a position.</p>",
                    "<p>That is the only new object in Lessons 5&ndash;7. "
                    "Everything else is Calc I applied to it.</p>",
                ],
            ),

            # ---------------------------------------------------------- 2 ----
            dict(
                h="Step 1 · A bug, with actual numbers",
                body=[
                    "<p>No notation yet. A bug flies around. At time $t$ it is "
                    "at</p>",
                    "$$x = t^2, \\qquad y = 3t, \\qquad z = 5.$$",
                    "<p>Make a table, because a table is impossible to "
                    "misunderstand:</p>",
                    "<table class=\"pmap\"><tr><th>$t$</th><th>$x=t^2$</th>"
                    "<th>$y=3t$</th><th>$z=5$</th><th>where it is</th></tr>"
                    "<tr><td>0</td><td>0</td><td>0</td><td>5</td><td>$(0,0,5)$</td></tr>"
                    "<tr><td>1</td><td>1</td><td>3</td><td>5</td><td>$(1,3,5)$</td></tr>"
                    "<tr><td>2</td><td>4</td><td>6</td><td>5</td><td>$(4,6,5)$</td></tr>"
                    "<tr><td>3</td><td>9</td><td>9</td><td>5</td><td>$(9,9,5)$</td></tr></table>",
                    "<p>Join those dots and you get a curve. <b>The curve is the "
                    "trail; the function is the flight.</b> Two different bugs "
                    "can trace the same trail at different speeds, which is why "
                    "the function carries more information than the picture.</p>",
                    "<p>Notice $z$ never moves. The bug stays at height 5 the "
                    "whole time, so the trail lies flat in a horizontal plane. "
                    "You just read a geometric fact off a slot &mdash; that is "
                    "most of what 14.1 asks you to do.</p>",
                ],
            ),

            # ---------------------------------------------------------- 3 ----
            dict(
                h="Step 2 · Derive the derivative (do not take my word for it)",
                body=[
                    "<p>How fast is the bug going at $t=1$? You know how to "
                    "answer this for <i>one</i> function: the derivative is the "
                    "limit of rise over run. Do the same thing and watch what "
                    "happens.</p>",
                    "<p>Between time $t$ and a moment $h$ later, the bug moves "
                    "from $\\vec r(t)$ to $\\vec r(t+h)$. The <b>change</b> is "
                    "the subtraction:</p>",
                    "$$\\vec r(t+h) - \\vec r(t).$$",
                    "<p>Subtracting two triples means subtracting each slot "
                    "&mdash; that is just what subtracting vectors <i>is</i>. So "
                    "the change is</p>",
                    "$$\\big\\langle\\, x(t+h)-x(t),\\;\\; y(t+h)-y(t),\\;\\; "
                    "z(t+h)-z(t) \\,\\big\\rangle.$$",
                    "<p>Now divide by $h$. Dividing a vector by a number divides "
                    "each slot, so each slot becomes its own rise-over-run:</p>",
                    "$$\\left\\langle\\, \\frac{x(t+h)-x(t)}{h},\\;\\; "
                    "\\frac{y(t+h)-y(t)}{h},\\;\\; \\frac{z(t+h)-z(t)}{h} "
                    "\\,\\right\\rangle.$$",
                    "<p>Finally let $h \\to 0$. A point in space is close to "
                    "another exactly when it is close in <i>all three</i> "
                    "coordinates, so the limit of a triple is the triple of the "
                    "limits &mdash; and each of those is an ordinary Calc I "
                    "derivative.</p>",
                    "<p class=\"twojobs\">$$\\vec r\\,{}'(t) = \\big\\langle "
                    "x'(t),\\; y'(t),\\; z'(t) \\big\\rangle$$ "
                    "<b>Slot by slot is not a convention. It is forced.</b> "
                    "There was never an opportunity for the slots to interact.</p>",
                    "<p>Which is why the same is true of limits, integrals and "
                    "continuity: every one of them is built out of subtracting, "
                    "dividing and taking limits, and all three go slot by slot. "
                    "<b>That single argument covers most of Lesson 5 and all of "
                    "Lesson 6.</b></p>",
                    "<p>For the bug: $x'=2t$, $y'=3$, $z'=0$. At $t=1$ the "
                    "velocity is $\\langle 2,3,0\\rangle$.</p>",
                ],
            ),

            # ---------------------------------------------------------- 4 ----
            dict(
                h="Step 3 · Why that arrow points along the curve",
                body=[
                    "<p>Worth thirty seconds, because it is the reason the word "
                    "<i>tangent</i> shows up everywhere.</p>",
                    "<p>$\\vec r(t+h) - \\vec r(t)$ is the arrow <b>from where "
                    "the bug is now to where it will be</b>. It cuts across the "
                    "curve like a chord across a circle.</p>",
                    "<p>Dividing by a positive number $h$ stretches or shrinks "
                    "that arrow but <b>cannot rotate it</b>. So the direction "
                    "survives the division untouched.</p>",
                    "<p>Now shrink $h$. The far endpoint slides back toward the "
                    "near one, and the chord pivots until it is just grazing the "
                    "curve.</p>",
                    "<p class=\"twojobs\">So $\\vec r\\,{}'$ points <b>exactly "
                    "the way the bug is heading</b>, and its length says how "
                    "fast. Direction and magnitude in one object &mdash; that is "
                    "what \"velocity\" means.</p>",
                ],
            ),

            # ---------------------------------------------------------- 5 ----
            dict(
                h="Step 4 · Speed, and why arc length is not a new formula",
                body=[
                    "<p>The length of $\\vec r(t+h)-\\vec r(t)$ is (nearly) the "
                    "<b>distance travelled</b> in those $h$ seconds. Divide by "
                    "$h$ and you have distance over time.</p>",
                    "<p class=\"twojobs\"><b>Speed $= |\\vec r\\,{}'(t)|$.</b> "
                    "Not a definition handed down &mdash; it is "
                    "distance&nbsp;/&nbsp;time, in the limit.</p>",
                    "<p>For the bug: $|\\langle 2t,3,0\\rangle| = "
                    "\\sqrt{4t^2+9}$, which at $t=1$ is $\\sqrt{13}$.</p>",
                    "<p>And now arc length for free. If you travel at speed "
                    "$|\\vec r\\,{}'|$ for a tiny time $dt$, you cover "
                    "$|\\vec r\\,{}'|\\,dt$ of ground. Add up every tiny piece:</p>",
                    "$$L = \\int_a^b \\big|\\vec r\\,{}'(t)\\big|\\,dt.$$",
                    "<p>That is <b>distance = rate &times; time, summed</b>. If "
                    "you ever blank on it, rebuild it from that sentence in five "
                    "seconds.</p>",
                ],
            ),

            # ---------------------------------------------------------- 6 ----
            dict(
                h="Step 5 · Unit tangent: direction with the size stripped off",
                body=[
                    "<p>Sometimes you want <i>only</i> the heading, with speed "
                    "thrown away. Dividing any vector by its own length always "
                    "gives length 1 &mdash; same trick as 13.1.</p>",
                    "$$\\vec T(t) = \\frac{\\vec r\\,{}'(t)}{|\\vec r\\,{}'(t)|}$$",
                    "<p>Check it at $t=1$: $\\vec r\\,{}' = \\langle 2,3,0\\rangle$ "
                    "has length $\\sqrt{13}$, so $\\vec T = \\left\\langle "
                    "\\tfrac{2}{\\sqrt{13}}, \\tfrac{3}{\\sqrt{13}}, 0 "
                    "\\right\\rangle$, whose length is "
                    "$\\sqrt{\\tfrac{4}{13}+\\tfrac{9}{13}} = 1$. Good.</p>",
                    "<p class=\"twojobs\"><b>$\\vec T$ is a signpost, not a "
                    "speedometer.</b> If a question asks for $\\vec T$ and your "
                    "answer does not have length 1, you skipped the division.</p>",
                ],
            ),

            # ---------------------------------------------------------- 7 ----
            dict(
                h="Step 6 · Why acceleration leans into the bend",
                body=[
                    "<p>This is the one result that looks like it needs "
                    "intuition and actually needs two lines of algebra.</p>",
                    "<p>Suppose the speed never changes &mdash; a car going "
                    "round a roundabout at a steady 30. Then "
                    "$|\\vec v|$ is constant, so $|\\vec v|^2$ is constant, and "
                    "$|\\vec v|^2 = \\vec v \\cdot \\vec v$.</p>",
                    "<p>Differentiate both sides. The left is a constant, so it "
                    "gives 0. The right uses the product rule for dot products, "
                    "which is the ordinary product rule:</p>",
                    "$$0 = \\frac{d}{dt}(\\vec v \\cdot \\vec v) = \\vec v\\,{}' "
                    "\\cdot \\vec v + \\vec v \\cdot \\vec v\\,{}' = "
                    "2\\,\\vec a \\cdot \\vec v.$$",
                    "<p>So $\\vec a \\cdot \\vec v = 0$: <b>acceleration is "
                    "perpendicular to velocity</b> whenever speed is constant.</p>",
                    "<p class=\"twojobs\">Which makes physical sense. "
                    "Acceleration along your direction of travel would speed you "
                    "up or slow you down. If your speed is not changing, all of "
                    "it must be spent <b>turning</b> &mdash; pointing sideways, "
                    "into the bend.</p>",
                    "<p>Circular motion is exactly this case, which is why "
                    "$\\vec r = \\langle a\\cos t, a\\sin t\\rangle$ always has "
                    "$\\vec a$ aimed at the centre. Differentiate it twice and "
                    "you get $\\vec a = -\\vec r$ &mdash; literally pointing "
                    "back at the origin.</p>",
                ],
            ),

            # ---------------------------------------------------------- 8 ----
            dict(
                h="Step 7 · Projectiles are Newton plus the integrals you just built",
                body=[
                    "<p>Purdue's Lesson 7 does projectile motion, and none of it "
                    "is new. Gravity pulls down at a constant rate and nothing "
                    "pushes sideways:</p>",
                    "$$\\vec a(t) = \\langle 0,\\,0,\\,-9.8\\rangle.$$",
                    "<p>Integrating undoes differentiating, slot by slot for the "
                    "same reason as before. Once:</p>",
                    "$$\\vec v(t) = \\langle 0,0,-9.8t\\rangle + \\vec C, "
                    "\\qquad \\text{and at } t=0 \\text{ this is } \\vec C, "
                    "\\text{ so } \\vec C = \\vec v(0).$$",
                    "<p>Twice, the same way, giving "
                    "$\\vec r(t) = \\langle 0,0,-4.9t^2\\rangle + t\\,\\vec v(0) "
                    "+ \\vec r(0)$.</p>",
                    "<p class=\"twojobs\">The constant of integration is a "
                    "<b>vector</b> &mdash; three separate constants &mdash; and "
                    "the initial condition is what pins it down. Every $t$ dies "
                    "at $t=0$, so whatever survives <i>is</i> $\\vec C$.</p>",
                    "<p>Now every projectile question is just reading the $z$ "
                    "slot, because only $z$ has gravity in it:</p>",
                    "<ul>"
                    "<li><b>Max height</b> &mdash; height stops rising when "
                    "$z' = 0$. Solve for $t$, put it back in $z$.</li>"
                    "<li><b>Time of flight</b> &mdash; it lands when $z = 0$.</li>"
                    "<li><b>How far</b> &mdash; take that landing time and read "
                    "the $x$ and $y$ slots, which stayed linear.</li></ul>",
                    "<p>Same three questions every time.</p>",
                ],
            ),

            # ---------------------------------------------------------- 9 ----
            dict(
                h="Every symbol on the quiz, mapped to the bug",
                body=[
                    "<p>Now the notation is just shorthand for moves you have "
                    "already made:</p>",
                    "<table class=\"pmap\"><tr><th>Symbol</th><th>Out loud</th>"
                    "<th>The bug</th></tr>"
                    "<tr><td>$\\vec r(t)$</td><td><b>position</b> &mdash; where it is</td>"
                    "<td>$\\langle t^2, 3t, 5\\rangle$</td></tr>"
                    "<tr><td>$\\vec r\\,{}'(t)=\\vec v(t)$</td>"
                    "<td><b>velocity</b> &mdash; heading and how fast</td>"
                    "<td>$\\langle 2t, 3, 0\\rangle$</td></tr>"
                    "<tr><td>$|\\vec v(t)|$</td><td><b>speed</b> &mdash; one number</td>"
                    "<td>$\\sqrt{4t^2+9}$</td></tr>"
                    "<tr><td>$\\vec r\\,{}''(t)=\\vec a(t)$</td>"
                    "<td><b>acceleration</b> &mdash; how the heading changes</td>"
                    "<td>$\\langle 2,0,0\\rangle$</td></tr>"
                    "<tr><td>$\\vec T(t)$</td><td><b>unit tangent</b> &mdash; heading only</td>"
                    "<td>$\\vec v/|\\vec v|$</td></tr>"
                    "<tr><td>$\\int \\vec r\\,dt$</td><td><b>undo a derivative</b>, "
                    "plus a vector constant</td><td>slot by slot</td></tr></table>",
                    "<p><b>The arrow on top only ever means \"this is a list of "
                    "three, not one\".</b> The prime is still a derivative. $t$ "
                    "is still time. There is no third meaning hiding anywhere.</p>",
                ],
            ),

            # --------------------------------------------------------- 10 ----
            dict(
                h="The one distinction the quiz will punish",
                body=[
                    "<p class=\"twojobs\"><b>Velocity is a vector. Speed is its "
                    "length.</b> Velocity knows which way you are going; speed "
                    "is a single number that has forgotten.</p>",
                    "<p>So \"find the speed at $t = \\pi/2$\" means "
                    "differentiate, substitute, <b>then take the square root of "
                    "the sum of the squares</b>. If your answer to a speed "
                    "question still has angle brackets around it, you stopped one "
                    "step early. That is the single most common lost mark in "
                    "14.3.</p>",
                ],
            ),

            # --------------------------------------------------------- 11 ----
            dict(
                h="The jingle — now that it means something",
                body=[
                    "<p class=\"jingle\">Slot by slot, then reassemble.<br>"
                    "Prime once for velocity, twice for acceleration.<br>"
                    "<b>Speed is the length</b> &mdash; take the root or lose "
                    "the mark.<br>"
                    "The constant is a vector; $t=0$ finds it.</p>",
                ],
            ),

            # --------------------------------------------------------- 12 ----
            dict(
                h="You are ready when you can rebuild these, not recall them",
                body=[
                    "<ul class=\"ready\">"
                    "<li>Why differentiating goes slot by slot &mdash; the "
                    "subtract, divide, take-the-limit argument</li>"
                    "<li>Why $\\vec r\\,{}'$ points along the curve (the chord "
                    "that pivots)</li>"
                    "<li>Why speed is $|\\vec r\\,{}'|$, and why arc length is "
                    "just rate &times; time summed</li>"
                    "<li>Why $\\vec a \\perp \\vec v$ when speed is constant "
                    "&mdash; the $\\vec v\\cdot\\vec v$ trick</li>"
                    "<li>How to build $\\vec T$ from $\\vec v$, and why its "
                    "length is 1</li>"
                    "<li>How to get position from acceleration, and why "
                    "$\\vec C$ has three components</li>"
                    "<li>The three projectile questions and which slot answers "
                    "each</li>"
                    "<li>Why a domain question is \"where is every slot defined "
                    "at once\"</li>"
                    "</ul>",
                    "<p>Anything there you cannot derive out loud in a sentence "
                    "is exactly what the problems below are for. Start with the "
                    "official ones.</p>",
                ],
            ),
        ],
    ),
}


CSS = """
/* ---- from-zero primer ------------------------------------------------- */
.primer{margin-top:26px;border:1px solid var(--rule);border-left:3px solid var(--veg);
  border-radius:3px;background:var(--card);overflow:hidden;max-width:86ch}
.primer-h{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding:16px 20px 0}
.primer-h h3{font-size:22px;font-weight:800;letter-spacing:-.022em}
.primer-h .mins{font:500 10.5px/1 var(--mono);letter-spacing:.12em;
  text-transform:uppercase;color:var(--veg);border:1px solid var(--veg);
  border-radius:2px;padding:5px 8px}
.primer-lede{padding:9px 20px 0;font-size:17px;line-height:1.55;color:var(--ink-2)}
.primer-toggle{margin:14px 20px 18px;cursor:pointer;border:1px solid var(--veg);
  background:var(--veg);color:var(--paper);border-radius:2px;padding:10px 15px;
  font:600 13px/1 var(--disp)}
.primer-body{padding:0 20px 20px;border-top:1px solid var(--rule);margin-top:2px}
.primer-body[hidden]{display:none}
.pblock{padding-top:22px}
.pblock h4{font:700 10.5px/1.5 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--contour)}
.pblock p{margin-top:10px;font-size:17px;line-height:1.62;color:var(--ink-2)}
.pblock p b{color:var(--ink);font-weight:600}
.pblock ul{margin:10px 0 0;padding-left:20px;font-size:17px;line-height:1.6;color:var(--ink-2)}
.pblock li{margin-top:6px}
.pblock li b{color:var(--ink)}
.pblock .katex{color:var(--ink)}
.twojobs{margin-top:12px!important;background:var(--paper-2);
  border-left:2px solid var(--contour);padding:11px 14px;border-radius:2px}
.jingle{margin-top:12px!important;background:var(--paper-2);
  border-left:2px solid var(--revise);padding:13px 16px;border-radius:2px;
  font-size:17.5px!important;line-height:1.75!important}
.ready{list-style:none;padding-left:0!important}
.ready li{position:relative;padding-left:26px}
.ready li::before{content:"";position:absolute;left:4px;top:11px;width:9px;height:9px;
  border:1px solid var(--ink-3);border-radius:2px}
table.pmap{width:100%;border-collapse:collapse;margin-top:12px;font-size:16px}
table.pmap th,table.pmap td{border:1px solid var(--rule);padding:9px 11px;
  text-align:left;vertical-align:middle;color:var(--ink-2)}
table.pmap th{font-family:var(--disp);font-size:11.5px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--ink);background:var(--paper-2)}
/* A header cell may be a variable name ($t$, $x=t^2$). Uppercasing rendered
   maths turns t into T and silently changes what the symbol means. */
table.pmap th .katex{text-transform:none;font-size:15px}
table.pmap td:first-child{white-space:nowrap}
table.pmap td b{color:var(--ink)}
@media (max-width:760px){
  .primer-h{padding:14px 15px 0}
  .primer-h h3{font-size:20px}
  .primer-lede,.primer-body{padding-left:15px;padding-right:15px}
  .primer-toggle{margin-left:15px;margin-right:15px}
  .pblock p,.pblock ul{font-size:16.5px}
  table.pmap{font-size:14px}
  table.pmap th,table.pmap td{padding:7px 8px}
}
"""

JS = r"""
(function(){
  "use strict";
  /* Open by default the first time you land on a quiz — someone arriving cold
     should not have to go looking for it. Collapse once and that sticks. */
  var K="ma261-primer", st={};
  try{ st=JSON.parse(localStorage.getItem(K)||"{}"); }catch(e){ st={}; }
  document.querySelectorAll(".primer").forEach(function(p){
    var id=p.dataset.quiz, body=p.querySelector(".primer-body"),
        btn=p.querySelector(".primer-toggle");
    function paint(open){
      body.hidden=!open;
      btn.textContent=open?"Hide this":"Never studied this? Start here \u2014 20 min";
    }
    paint(st[id]!==0);
    btn.addEventListener("click",function(){
      var open=body.hidden;
      paint(open); st[id]=open?1:0;
      try{ localStorage.setItem(K,JSON.stringify(st)); }catch(e){}
      if(!open) p.scrollIntoView({block:"start",behavior:"smooth"});
    });
  });
})();
"""


def html(stop_id, M):
    """The primer block for one quiz, or "" when there isn't one."""
    p = PRIMERS.get(stop_id)
    if not p:
        return ""
    blocks = "".join(
        f'<div class="pblock"><h4>{M(b["h"])}</h4>'
        + "".join(M(x) for x in b["body"]) + "</div>"
        for b in p["blocks"])
    return (
        f'<div class="primer" data-quiz="{stop_id}">'
        f'<div class="primer-h"><h3>{p["title"]}</h3>'
        f'<span class="mins">from zero &middot; nothing assumed</span></div>'
        f'<p class="primer-lede">{M(p["lede"])}</p>'
        f'<button class="primer-toggle" type="button"></button>'
        f'<div class="primer-body">{blocks}</div></div>')


def texts(stop_id):
    """Every TeX-bearing string, so the build can prime KaTeX in one call."""
    p = PRIMERS.get(stop_id)
    if not p:
        return []
    out = [p["lede"]]
    for b in p["blocks"]:
        out.append(b["h"])
        out.extend(b["body"])
    return out
