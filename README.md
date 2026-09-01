# Ultimate Calc III — MA 26100, Fall 2026

Purdue **MA 26100 (Multivariate Calculus)**, two ways: read all of it in order, or
pick the quiz you are sitting and get only the sections it covers plus questions on
exactly those. Pictures you can spin, procedures you can follow, and answers that
were computed rather than asserted.

**Live:** https://ultimate-calc3.vercel.app

| Page | What it is |
|---|---|
| [`index.html`](index.html) | The landing page: two ways in, plus the Fall 2026 calendar with whichever stop is next surfaced. |
| [`guide.html`](guide.html) | **Study all the material** — 40 sections, 41 figures (12 interactive 3-D), 41 algorithms, 86 check-yourself questions. Each section badged with the quiz that tests it. |
| [`quiz.html`](quiz.html) | **Study by quiz** — pick a quiz and get only the sections it covers, in full, then 64 questions on exactly those sections. |

## Where the schedule comes from

Everything — quiz dates, the lesson→section split, exam dates, grade weights — is
transcribed from the department's own Fall 2026 documents, read 2026-09-01:

- [Fall 2026 calendar (PDF)](https://www.math.purdue.edu/academic/courses/semester/202710/ma26100/Schedule261.pages.pdf)
- [Ground rules (PDF)](https://www.math.purdue.edu/academic/courses/semester/202710/ma26100/MA261F26GroundRules.pages2.pdf)

Nothing is carried over from a previous semester. `build/course.py` is the single
source of truth; change a date there and every page follows.

Three facts worth knowing, all of which fall out of that calendar:

- **Section numbering is Briggs 3e**, and Lesson 2 reaches back to **12.1**
  (parametric equations) before 13.5. That section is on Quiz 1.
- **Three windows have no quiz.** Lessons 14–16 land between Quiz 5 and Midterm 1;
  Lessons 29–30 between Quiz 9 and Midterm 2; Lessons 34–37 after the last quiz,
  on the final only. Nothing forces you to learn those on time.
- **16.7 (change of variables / Jacobian) is not on the lesson plan at all** — the
  calendar goes 16.6 → 17.1. It is kept in the guide, badged as a bonus.

## How it's built

`build/` regenerates all three pages. There is no framework and no runtime
dependency; the output is static HTML with the maths already typeset.

```bash
cd build
npm install          # katex, for pre-rendering
python3 build.py
```

- `course.py` — the Fall 2026 calendar, weights and deadlines
- `bank.html` — the 55 original questions, pre-rendered
- `bank_q1.py` — 9 further Quiz 1 questions, each recomputed with `sympy` at build
  time; the build refuses to emit on a mismatch
- `guide_121.py` — the 12.1 section the guide was missing
- `patch_guide.py` — reads `guide.src.html`, writes `../guide.html`
- `quizpage.py` — builds `quiz.html` by re-hosting the guide's own sections,
  stylesheet and 3-D engine inside each quiz tab

**Everything is self-contained.** No CDN, no build step at serve time:

- **Maths** — KaTeX pre-rendered to static HTML, fonts subset and inlined into
  `katex.css`. Zero runtime JS for maths, no flash of raw TeX.
- **3-D** — a ~700-line engine in plain canvas 2D (projection, painter's-algorithm
  depth sort, Lambert shading, drag-to-rotate, auto-framing). No WebGL, no three.js.
- **Diagrams** — hand-authored inline SVG, themed through `currentColor`.

**Practice answers are verified, not asserted.** The Quiz 1 additions carry `sympy`
check functions that recompute every keyed answer. The original 55 were built the
same way, which caught two real errors during authoring (a Green's theorem answer
keyed to 243π/2 when it's 243π/4, and a work integral keyed to 14 when it's 18).

## Design

A topographic survey sheet, because that's what multivariable calculus is — level
curves, steepest ascent, flux across a boundary. USGS map colours where each hue
does real work: brown = level sets, blue = flow and flux, green = the answer,
magenta = the punchline. Surfaces render as hypsometric relief, so the colour *is*
the level-set information. Light and dark themes.

## Local

Static files. Serve the directory:

```bash
python3 -m http.server 8000
```

## Note

Practice questions are **original**, written to match the skill mix and difficulty
of the course. They are not past Purdue questions, and no practice set predicts a
quiz. Confirm your own section's dates in Brightspace. Not affiliated with or
endorsed by Purdue University.
