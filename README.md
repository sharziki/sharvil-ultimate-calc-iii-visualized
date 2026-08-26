# Sharvil · Ultimate Calc III Visualized

Purdue **MA 26100 (Multivariate Calculus)** rebuilt as pictures you can spin, procedures you can
follow, and practice questions whose answers were computed rather than asserted.

**Live:** https://ultimate-calc3.vercel.app

| Page | What it is |
|---|---|
| [`guide.html`](guide.html) | The study guide — 4 units, 39 sections, 41 figures (12 interactive 3-D), 41 algorithms, 86 self-checks |
| [`drill.html`](drill.html) | The test-out drill — 2 timed 20-question simulations, a gap set, a chapter drill (55 questions) |

## Why it's built this way

**Section numbering is Briggs 3e (Ch. 13–17), not Stewart.** Purdue uses Briggs, Cochran, Gillett &
Schulz, *Calculus: Early Transcendentals*, 3rd ed. Verified against the live
[Spring 2026 lesson plan](https://www.math.purdue.edu/~msunkula/MA261/Sp26/Schedule). Exam
boundaries fall mid-chapter — Exam 1 ends at 15.7, Exam 2 starts at 15.8 (Lagrange), and Stokes /
divergence appear only on the final.

**Everything is self-contained.** No CDN, no build step, no framework:

- **Maths** — KaTeX pre-rendered to static HTML at build time, fonts subset and inlined. Zero
  runtime JS for maths, no flash of raw TeX.
- **3-D** — a ~700-line engine in plain canvas 2D (projection, painter's-algorithm depth sort,
  Lambert shading, drag-to-rotate, auto-framing). No WebGL, no three.js.
- **Diagrams** — hand-authored inline SVG, themed through `currentColor`.

**Practice answers are verified, not asserted.** The question banks are Python with `sympy` check
functions that recompute every answer; the build refuses to emit on a mismatch. That caught two real
errors during authoring (a Green's theorem answer keyed to 243π/2 when it's 243π/4, and a work
integral keyed to 14 when it's 18).

## Design

A topographic survey sheet, because that's what multivariable calculus is — level curves, steepest
ascent, flux across a boundary. USGS map colours where each hue does real work: brown = level sets,
blue = flow and flux, green = the answer, magenta = the punchline. Surfaces render as hypsometric
relief, so the colour *is* the level-set information. Light and dark themes.

## Local

Static files. Serve the directory:

```bash
python3 -m http.server 8000
```

## Note

Practice questions are **original**, written to match the released Spring 2025 final's skill mix and
difficulty. They are not past Purdue questions, and no exam predicts another. Not affiliated with or
endorsed by Purdue University.
