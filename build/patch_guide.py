"""Patch guide.html for the Fall 2026 semester.

The guide was written for the advanced-credit exam. This:
  - retitles it and drops the test-out framing
  - inserts a 12.1 section (Lesson 2, never needed for the test-out)
  - badges every section and every rail entry with the quiz that tests it
  - replaces the "Exam map" reference section with the real Fall 2026 calendar

Reads build/guide.src.html (untouched original) and writes ../guide.html.
"""
import re
import sys
from pathlib import Path

import course
import guide_121

ROOT = Path(__file__).resolve().parent.parent


def sid_to_stops():
    """guide section id -> [stop labels], in calendar order."""
    out = {}
    for s in course.STOPS:
        for ln in s["lessons"]:
            if ln not in course.LESSONS:
                continue
            for sid in course.LESSONS[ln][1]:
                out.setdefault(sid, [])
                if s["label"] not in out[sid]:
                    out[sid].append(s["label"])
    # An exam covers everything before it; only badge a section with an exam
    # when no quiz tests it, otherwise every badge would read "Quiz 3, Midterm 1".
    for sid, labels in out.items():
        quizzes = [l for l in labels if l.startswith("Quiz")]
        # Exam-only section: name the first exam that tests it. The final is
        # comprehensive, so listing it as well would add nothing to any badge.
        out[sid] = quizzes if quizzes else labels[:1]
    return out


SHORT = {"Quiz 1": "Q1", "Quiz 2": "Q2", "Quiz 3": "Q3", "Quiz 4": "Q4",
         "Quiz 5": "Q5", "Quiz 6": "Q6", "Quiz 7": "Q7", "Quiz 8": "Q8",
         "Quiz 9": "Q9", "Quiz 10": "Q10", "Midterm 1": "M1",
         "Midterm 2": "M2", "Final Exam": "Final"}

STOP_ID = {s["label"]: s["id"] for s in course.STOPS}

RAIL = [
    ("u1", "Unit 1 · Vectors &amp; curves", None, None),
    ("s131", "13.1", "Vectors", None), ("s132", "13.2", "Space, distance, spheres", None),
    ("s133", "13.3", "Dot product", None), ("s133b", "13.3b", "Scalar vs vector projection", None),
    ("s134", "13.4", "Cross product", None),
    ("s121", "12.1", "Parametric equations", None),
    ("s135", "13.5", "Lines &amp; planes", None), ("s135b", "13.5b", "Every distance formula", None),
    ("s136", "13.6", "Quadric surfaces", None),
    ("s141", "14.1", "Vector functions", None), ("s142", "14.2", "Derivatives &amp; integrals", None),
    ("s143", "14.3", "Motion · T, N, B", None), ("s144", "14.4", "Arc length &amp; curvature", None),
    ("u2", "Unit 2 · Partial derivatives", None, None),
    ("s151", "15.1", "Surfaces &amp; level curves", None), ("s152", "15.2", "Limits &amp; continuity", None),
    ("s153", "15.3", "Partial derivatives", None), ("s154", "15.4", "Chain rule", None),
    ("s155", "15.5", "Gradient &amp; directional", None), ("s156", "15.6", "Tangent planes", None),
    ("s157", "15.7", "Max &amp; min", None), ("s158", "15.8", "Lagrange multipliers", None),
    ("u3", "Unit 3 · Multiple integrals", None, None),
    ("s161", "16.1", "Double integrals", None), ("s162", "16.2", "General regions", None),
    ("s163", "16.3", "Polar", None), ("s164", "16.4", "Triple integrals", None),
    ("s165c", "16.5a", "Cylindrical", None), ("s165s", "16.5b", "Spherical", None),
    ("s166", "16.6", "Mass, centroid, inertia", None), ("s167", "16.7", "Jacobian · bonus", None),
    ("u4", "Unit 4 · Vector calculus", None, None),
    ("s171", "17.1", "Vector fields", None), ("s172", "17.2", "Line integrals", None),
    ("s173", "17.3", "Conservative fields", None), ("s174", "17.4", "Green's theorem", None),
    ("s175", "17.5", "Curl &amp; divergence", None), ("s176p", "17.6a", "Parametric surfaces", None),
    ("s176a", "17.6b", "Surface area", None), ("s176f", "17.6c", "Surface integrals &amp; flux", None),
    ("s177", "17.7", "Stokes' theorem", None), ("s178", "17.8", "Divergence theorem", None),
    ("u5", "Reference", None, None),
    ("rexam", "R.1", "Fall 2026 map", None), ("rchoose", "R.2", "Which theorem?", None),
    ("rcoord", "R.3", "Coordinates", None), ("rsheet", "R.4", "Formula sheet", None),
    ("rtraps", "R.5", "Traps", None), ("rcheck", "R.6", "Self-check", None),
]

EXTRA_CSS = """
/* --- Fall 2026 quiz badges --- */
.rail a.s{grid-template-columns:38px 1fr auto}
.rail a.s u{font:700 9px/1 var(--mono);text-decoration:none;letter-spacing:.06em;
  color:var(--ink-3);border:1px solid var(--rule);border-radius:2px;padding:3px 4px;
  white-space:nowrap;align-self:center}
.rail a.s.on u,.rail a.s:hover u{color:var(--contour);border-color:var(--contour)}
.sec-h .qz{font:700 9.5px/1 var(--mono);letter-spacing:.11em;text-transform:uppercase;
  text-decoration:none;color:var(--paper);background:var(--contour);
  border-radius:2px;padding:5px 7px;margin-left:auto;white-space:nowrap;align-self:center}
.sec-h .qz.m{background:var(--water)}
.sec-h .qz.n{background:none;color:var(--ink-3);border:1px solid var(--rule)}
.sec-h .qz:hover{filter:brightness(1.12)}
.sec-h{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.cal{width:100%;border-collapse:collapse;font-size:15px;margin-top:16px}
.cal th{font:700 10px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);
  text-align:left;padding:0 12px 8px 0;border-bottom:1.5px solid var(--ink);white-space:nowrap}
.cal td{padding:9px 12px 9px 0;border-bottom:1px solid var(--rule-2);vertical-align:top;color:var(--ink-2)}
.cal td:first-child{color:var(--ink);font-weight:600;font-family:var(--disp);white-space:nowrap}
.cal tr.ex td{background:color-mix(in srgb,var(--water) 8%,transparent)}
.cal a{color:var(--contour)}
.calwrap{overflow-x:auto}
guidefooter{display:block}
.gfoot{margin:64px auto 0;max-width:1200px;padding:22px 32px 90px;
  border-top:1px solid var(--rule);font:400 13px/1.7 var(--mono);color:var(--ink-3)}
.gfoot a{color:var(--contour)}
"""


def build_rail(badges):
    out = []
    for row in RAIL:
        sid, a, b = row[0], row[1], row[2]
        if b is None:
            out.append(f'      <a class="u" href="#{sid}">{a}</a>')
            continue
        labels = badges.get(sid, [])
        if labels:
            short = " ".join(SHORT[l] for l in labels)
            href = STOP_ID[labels[0]]
            tag = f'<u>{short}</u>'
        else:
            tag = "<u>&mdash;</u>" if sid.startswith("s") else ""
        out.append(f'      <a class="s" href="#{sid}"><i>{a}</i>{b}{tag}</a>')
    return "\n".join(out)


def calendar_table():
    rows = []
    for s in course.STOPS:
        lessons = (", ".join(str(l) for l in s["lessons"]) if len(s["lessons"]) <= 6
                   else f'{s["lessons"][0]}&ndash;{s["lessons"][-1]}')
        secs = s["secs_label"]
        cls = ' class="ex"' if s["kind"] == "exam" else ""
        rows.append(
            f'<tr{cls}><td>{s["label"]}</td><td>{s["when"]}</td>'
            f'<td>{lessons}</td><td>{secs}</td>'
            f'<td><a href="/quiz.html#{s["id"]}">study it</a></td></tr>')
    skips = "".join(f"<li><b>{w}</b> &mdash; {t}</li>" for w, t in course.NO_QUIZ_WEEKS)
    grades = "".join(f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>'
                     for a, b, c in course.GRADING)
    dates = "".join(f"<li><b>{d}</b> &mdash; {w}</li>" for d, w in course.DEADLINES)
    return f"""
    <p class="say">Purdue splits MA 26100 into <b>37 lessons</b>. Ten recitation quizzes,
    two evening midterms and a final are laid on top of them &mdash; and the boundaries do
    not fall on chapter breaks. Everything below is transcribed from the department's own
    Fall&nbsp;2026 calendar, read {course.VERIFIED}.</p>
    <div class="calwrap"><table class="cal">
      <thead><tr><th>Stop</th><th>When</th><th>Lessons</th><th>Sections</th><th></th></tr></thead>
      <tbody>{"".join(rows)}</tbody>
    </table></div>
    <p class="note"><b>Three windows have no quiz.</b> Lessons 14&ndash;16 (tangent planes,
    max/min) land between Quiz&nbsp;5 and Midterm&nbsp;1. Lessons 29&ndash;30 (Green's theorem,
    curl and divergence) land between Quiz&nbsp;9 and Midterm&nbsp;2. Lessons 34&ndash;37
    (Stokes, divergence theorem) land after the last quiz and are on the final only. Nothing
    forces you to learn those on schedule, which is exactly why they are where grades go.</p>
    <div class="algo"><h4>Weeks with no quiz</h4><ol>{skips}</ol>
      <p class="tail">The two lowest quiz scores are dropped, and there are no make-ups
      &mdash; the drops <em>are</em> the make-up policy.</p></div>
    <p class="note"><b>16.7 (change of variables / the Jacobian) is not on the lesson plan
    at all</b> &mdash; the calendar goes 16.6 &rarr; 17.1. It is kept here as background,
    badged as a bonus, and no quiz or exam requires it.</p>
    <div class="calwrap"><table class="cal">
      <thead><tr><th>Component</th><th>Weight</th><th>Detail</th></tr></thead>
      <tbody>{grades}</tbody>
    </table></div>
    <div class="algo"><h4>Dates that are not about material</h4><ol>{dates}</ol>
      <p class="tail">Calculators are allowed on nothing &mdash; not quizzes, not
      midterms, not the final.</p></div>
"""


def run(M, MM, coverage_chips):
    # Read the pristine source and write the patched copy, so the build is
    # repeatable — patching guide.html in place would only work once.
    src = Path(__file__).resolve().parent / "guide.src.html"
    p = ROOT / "guide.html"
    h = src.read_text(encoding="utf-8")
    orig = len(h)
    badges = sid_to_stops()

    def sub1(pat, repl, why, flags=0):
        nonlocal h
        h2, n = re.subn(pat, repl, h, count=1, flags=flags)
        if n != 1:
            sys.exit(f"patch_guide: {why} — matched {n} times, expected 1")
        h = h2

    # ---- head -------------------------------------------------------------
    sub1(r"<title>[^<]*</title>",
         "<title>Calculus III, drawn &middot; MA 26100 Fall 2026</title>", "title")
    h = h.replace(
        'content="Purdue MA 26100 in four units — 41 figures, 12 you can spin, '
        '41 algorithms, 86 self-checks."',
        'content="Purdue MA 26100 Fall 2026 — all 37 lessons in four units, every '
        'section badged with the quiz that tests it."')
    h = h.replace('content="Sharvil · Ultimate Calc III Visualized"',
                  'content="Calculus III, drawn · MA 26100 Fall 2026"')

    # ---- chrome -----------------------------------------------------------
    sub1(r'<a class="sitenav" href="/">.*?</a>',
         '<a class="sitenav" href="/">&larr; Semester map</a>', "sitenav", re.S)

    sub1(r'@media \(prefers-reduced-motion:reduce\)\{\*\{animation:none!important;'
         r'transition:none!important\}\}',
         EXTRA_CSS + "\n@media (prefers-reduced-motion:reduce){*{animation:none!important;"
         "transition:none!important}}", "extra css")

    # ---- hero -------------------------------------------------------------
    sub1(r'<p class="eyebrow">Purdue MA 26100 · Briggs 3e, Ch\. 13–17 · all 37 lessons</p>',
         '<p class="eyebrow">Purdue MA 26100 &middot; Fall 2026 &middot; Briggs 3e '
         '&middot; all 37 lessons</p>', "hero eyebrow")
    sub1(r'<p class="hero-sub">.*?</p>',
         '<p class="hero-sub">One long walk over a hilly landscape. That\'s the whole '
         'course &mdash; and every section below is badged with the quiz that tests it, '
         'so you always know what is next.</p>', "hero sub", re.S)
    sub1(r'<div class="hero-meta">.*?</div>',
         '<div class="hero-meta">\n'
         '      <span class="chip"><b>37</b> lessons &middot; Ch. 12&ndash;17</span>\n'
         '      <span class="chip"><b>10</b> quizzes &middot; 3 exams</span>\n'
         '      <span class="chip"><b>41</b> figures &middot; 12 you can spin</span>\n'
         '      <span class="chip"><b>86</b> check-yourself questions</span>\n'
         '      <span class="chip">every formula gets a <b>reason</b></span>\n'
         '    </div>', "hero chips", re.S)

    # ---- rail -------------------------------------------------------------
    sub1(r'(<p class="rail-h">Contents</p>\s*<nav>).*?(</nav>)',
         lambda m: m.group(1) + "\n" + build_rail(badges) + "\n    " + m.group(2),
         "rail nav", re.S)
    sub1(r'<p class="foot">Section numbers follow.*?</p>',
         '<p class="foot">Section numbers follow <b>Briggs 3e</b>, the MA&nbsp;26100 text.'
         '<br>Badges are the Fall&nbsp;2026 quiz that tests the section.</p>', "rail foot", re.S)

    # ---- unit headers -----------------------------------------------------
    for old, new in [
        ("Ch. 13–14 · Exam 1", "Ch. 12–14 · Quizzes 1–4"),
        ("Ch. 15 · Exam 1 ends at 16.5", "Ch. 15 · Quizzes 4–6 · Midterm 1 ends at 15.7"),
        ("Ch. 16 · Exam 2", "Ch. 16 · Quizzes 6–8"),
        ("Ch. 17 · Exam 2 → Final", "Ch. 17 · Quizzes 8–10 → Midterm 2 → Final"),
    ]:
        if f'<span class="x">{old}</span>' not in h:
            sys.exit(f"patch_guide: unit header {old!r} not found")
        h = h.replace(f'<span class="x">{old}</span>', f'<span class="x">{new}</span>')

    # ---- insert 12.1 ------------------------------------------------------
    if 'id="s121"' not in h:
        anchor = '<article class="sec" id="s135">'
        if anchor not in h:
            sys.exit("patch_guide: s135 anchor not found")
        h = h.replace(anchor, guide_121.html(M) + "\n\n  " + anchor, 1)

    # ---- section badges ---------------------------------------------------
    def badge(m):
        sid, num, title = m.group(1), m.group(2), m.group(3)
        labels = badges.get(sid, [])
        if sid == "s167":
            tag = '<span class="qz n">bonus &middot; not on the plan</span>'
        elif labels:
            first = labels[0]
            cls = "qz m" if not first.startswith("Quiz") else "qz"
            txt = " &middot; ".join(labels)
            tag = f'<a class="{cls}" href="/quiz.html#{STOP_ID[first]}">{txt}</a>'
        else:
            return m.group(0)
        return (f'<article class="sec" id="{sid}">\n'
                f'    <div class="sec-h"><span class="sec-n">{num}</span>'
                f'<h3>{title}</h3>{tag}</div>')

    # s167's header already carries a trailing <span class="x">, so the h3 body
    # and any trailing markup are matched without letting .*? run into the next
    # article.
    h, n = re.subn(
        r'<article class="sec" id="(s[0-9a-z]+)">\s*'
        r'<div class="sec-h"><span class="sec-n">([^<]*)</span>'
        r'<h3>((?:(?!</h3>).)*)</h3>(?:(?!</div>).)*</div>',
        badge, h, flags=re.S)
    if n < 40:
        sys.exit(f"patch_guide: only badged {n} sections, expected 40+")

    # ---- R.1 exam map -> Fall 2026 calendar --------------------------------
    start = h.find('<article class="sec" id="rexam">')
    end = h.find('<article class="sec" id="rchoose">')
    if start < 0 or end < 0:
        sys.exit("patch_guide: rexam block not found")
    head = re.search(r'<div class="sec-h">.*?</div>', h[start:end], re.S).group(0)
    head = head.replace("<h3>Exam map</h3>", "<h3>Fall 2026 map</h3>")
    h = (h[:start]
         + f'<article class="sec" id="rexam">\n    {head}\n'
         + calendar_table() + "\n  </article>\n\n  "
         + h[end:])

    # ---- footer -----------------------------------------------------------
    if 'class="gfoot"' not in h:
        foot = (
            '<footer class="gfoot">\n'
            f'  Lesson numbering and quiz badges follow the official '
            f'<a href="{course.SCHED_PDF}" target="_blank" rel="noopener">'
            f'MA&nbsp;261 Fall&nbsp;2026 calendar</a> and '
            f'<a href="{course.RULES_PDF}" target="_blank" rel="noopener">ground rules</a>, '
            f'read {course.VERIFIED}. Confirm your own section in Brightspace.<br>\n'
            '  Section numbers are <b>Briggs 3e</b>. '
            '<a href="/">Semester map</a> &middot; '
            '<a href="/quiz.html">Study by quiz</a><br>\n'
            '  Not affiliated with or endorsed by Purdue University.\n'
            '</footer>\n')
        sub1(r"</body>", foot + "</body>", "footer")

    p.write_text(h, encoding="utf-8")
    print(f"guide.html     {orig:,} -> {len(h):,} bytes, {n} sections badged")
