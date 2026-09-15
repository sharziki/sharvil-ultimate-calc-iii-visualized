#!/usr/bin/env python3
"""Build the MA 261 Quiz 3 cram sheet — one PDF, everything, in order.

The web page is the better tool for practice; this is the better tool for a
cold start with a clock running. Everything on one continuous read, nothing to
click, nothing to navigate, printable.

Structure is deliberately the order you should actually study in:

  1. THE ONE PAGE      — every formula, boxed, for the walk to class
  2. BUILD IT UP       — each rule derived, not asserted
  3. ALGORITHMS        — the eight recipes, as numbered steps
  4. WORKED PROBLEMS   — all 11 official, fully worked
  5. MORE PRACTICE     — 13 multiple-choice, answers and traps at the end

Every problem and answer comes out of the same verified bank the site uses, so
the PDF cannot drift from the pages: 139 of 154 answers recomputed with sympy,
and the six known errors in the official guide are shown struck through with
the correction, exactly as on the site.

    python3 build/cram.py            # writes ../MA261-Quiz3-cram.pdf
"""

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import exam1_src            # noqa: E402
import exam1_sol            # noqa: E402
import newbank              # noqa: E402

LESSONS = {5, 6, 7}
OUT_TEX = Path("/tmp/ma261-quiz3.tex")
OUT_PDF = ROOT / "MA261-Quiz3-cram.pdf"


# --------------------------------------------------------------- markup ----

def tex(s):
    """Our light HTML/markdown dialect -> LaTeX.

    The banks are authored for the web: $...$ maths with a little HTML around
    it. Maths passes through untouched; everything else becomes LaTeX.
    """
    if s is None:
        return ""
    # protect maths first — nothing below may touch the inside of $...$
    slots = []

    def stash(m):
        slots.append(m.group(0))
        return f"@@M{len(slots)-1}@@"

    s = re.sub(r"\$\$.+?\$\$|\$.+?\$", stash, s, flags=re.S)

    s = s.replace("<br>", "\\\\ ")
    s = re.sub(r"</?(p|div|span)[^>]*>", "", s)
    s = re.sub(r"<b>(.*?)</b>", r"\\textbf{\1}", s, flags=re.S)
    s = re.sub(r"<i>(.*?)</i>", r"\\textit{\1}", s, flags=re.S)
    s = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)

    # entities and unicode the fonts will choke on
    for a, b in (("&mdash;", "---"), ("&ndash;", "--"), ("&nbsp;", "~"),
                 ("&middot;", "\\textperiodcentered{}"), ("&rarr;", "$\\to$"),
                 ("&sect;", "\\S"), ("&ldquo;", "``"), ("&rdquo;", "''"),
                 ("&times;", "$\\times$"), ("&le;", "$\\le$"),
                 ("&amp;", "\\&"), ("\u2014", "---"), ("\u2013", "--"),
                 ("\u2019", "'"), ("\u2018", "`"), ("\u201c", "``"),
                 ("\u201d", "''"), ("\u00b7", "\\textperiodcentered{}"),
                 ("\u2192", "$\\to$"), ("\u00d7", "$\\times$"),
                 ("\u2264", "$\\le$"), ("\u2265", "$\\ge$"),
                 ("\u00b1", "$\\pm$"), ("\u221a", "$\\sqrt{\\ }$"),
                 ("\u03c0", "$\\pi$"), ("\u2260", "$\\ne$"),
                 ("\u2032", "$'$"), ("\u00a0", "~"), ("\u2026", "\\ldots")):
        s = s.replace(a, b)

    # LaTeX specials, outside maths only
    s = s.replace("\\", "\\textbackslash{}") if "\\text" not in s else s
    for ch in ("&", "%", "#", "_"):
        s = s.replace(ch, "\\" + ch)
    s = s.replace("\\\\textbf", "\\textbf").replace("\\\\textit", "\\textit")

    # Any named entity still standing is one the table above does not know.
    # Decode it rather than shipping "&check;" as literal text into a PDF, and
    # say so on stderr so the table can grow.
    def _ent(m):
        import html as _h
        dec = _h.unescape(m.group(0))
        if dec == m.group(0):
            print(f"cram: unknown entity {m.group(0)}", file=sys.stderr)
            return ""
        return {"\u2713": "\\checkmark{}", "\u2714": "\\checkmark{}"}.get(
            dec, dec)

    s = re.sub(r"&[a-zA-Z][a-zA-Z0-9]{1,9};", _ent, s)

    for i, m in enumerate(slots):
        s = s.replace(f"@@M{i}@@", m)
    return s.strip()


def display(s):
    """A step that is a lone $$...$$ reads better unwrapped."""
    t = tex(s)
    m = re.fullmatch(r"\$\$(.+?)\$\$", t, flags=re.S)
    return f"\\[{m.group(1)}\\]" if m else t


# ----------------------------------------------------------- the content ----

PREAMBLE = r"""\documentclass[10pt]{article}
\usepackage[a4paper,margin=15mm,bottom=17mm]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[dvipsnames]{xcolor}
\usepackage{mdframed}
\usepackage{enumitem}
\usepackage{multicol}
\usepackage{titlesec}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\usepackage{bm}
\usepackage{amssymb}

\definecolor{ink}{HTML}{1B241F}
\definecolor{rule}{HTML}{C6CFBF}
\definecolor{paper2}{HTML}{EFF2EA}
\definecolor{contour}{HTML}{A65523}
\definecolor{water}{HTML}{1D6E8C}
\definecolor{veg}{HTML}{42743A}
\definecolor{revise}{HTML}{AE2668}
\color{ink}

\setlist{nosep,leftmargin=1.5em}
\setlength{\parindent}{0pt}
\setlength{\parskip}{3.2pt}
\linespread{1.04}

\titleformat{\section}{\normalfont\Large\bfseries\color{ink}}{\thesection.}{0.5em}{}
\titlespacing{\section}{0pt}{12pt}{5pt}
\titleformat{\subsection}{\normalfont\large\bfseries\color{contour}}{}{0em}{}
\titlespacing{\subsection}{0pt}{10pt}{3pt}

\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0.3pt}
\fancyhead[L]{\footnotesize\color{contour}MA 26100 \textperiodcentered\ Quiz 3 \textperiodcentered\ Lessons 5--7 \textperiodcentered\ \S14.1--14.3}
\fancyhead[R]{\footnotesize\color{contour}Tue Sep 15 \textperiodcentered\ no calculator}
\fancyfoot[C]{\footnotesize\thepage}

% boxes
\newmdenv[linecolor=contour,linewidth=1.1pt,topline=false,bottomline=false,
  rightline=false,backgroundcolor=paper2,innerleftmargin=8pt,innerrightmargin=8pt,
  innertopmargin=5pt,innerbottommargin=5pt,skipabove=5pt,skipbelow=5pt]{key}
\newmdenv[linecolor=revise,linewidth=1.1pt,topline=false,bottomline=false,
  rightline=false,innerleftmargin=8pt,innerrightmargin=8pt,
  innertopmargin=4pt,innerbottommargin=4pt,skipabove=4pt,skipbelow=4pt]{trap}
\newmdenv[linecolor=rule,linewidth=0.6pt,roundcorner=2pt,
  innerleftmargin=8pt,innerrightmargin=8pt,innertopmargin=6pt,
  innerbottommargin=6pt,skipabove=6pt,skipbelow=6pt]{card}

\newcommand{\trapl}[1]{\begin{trap}\textbf{\footnotesize\color{revise}TRAP}\ \ #1\end{trap}}
\newcommand{\qnum}[1]{\textbf{\color{contour}#1.}}
\newcommand{\vr}{\vec r}
\newcommand{\vv}{\vec v}
\newcommand{\va}{\vec a}
\newcommand{\vT}{\vec T}

\begin{document}
"""

TITLE = r"""
\begin{center}
{\LARGE\bfseries Calculus III --- Quiz 3, everything}\\[2pt]
{\footnotesize\color{contour}LESSONS 5--7 \textperiodcentered\ \S14.1 VECTOR FUNCTIONS \textperiodcentered\ \S14.2 DERIVATIVES \& INTEGRALS \textperiodcentered\ \S14.3 MOTION}\\[1pt]
{\footnotesize Read \S1 and \S2. Do the problems. Everything here is verified; answers were recomputed, not asserted.}
\end{center}
\vspace{-2pt}
\hrule height 1pt
\vspace{6pt}
"""

ONE_PAGE = r"""
\section{The whole quiz on one page}

If you read nothing else, read this. Every formula below is derived in \S2 --- so
if you forget one, you can rebuild it rather than guess.

\begin{key}
\textbf{The single idea.} A vector function is three ordinary functions wearing one
coat. \emph{Everything} --- limits, derivatives, integrals, continuity --- is done
\textbf{slot by slot} and then reassembled. There is no new calculus in this quiz.
\end{key}

\begin{multicols}{2}

\textbf{Position, velocity, acceleration}
\[\vr(t)=\langle x(t),y(t),z(t)\rangle\]
\[\vv=\vr\,'=\langle x',y',z'\rangle \qquad \va=\vr\,''\]

\textbf{Speed is a number, velocity is a vector}
\[\text{speed}=|\vv(t)|=\sqrt{x'^2+y'^2+z'^2}\]

\textbf{Unit tangent} --- direction only, length 1
\[\vT(t)=\frac{\vr\,'(t)}{|\vr\,'(t)|}\]

\textbf{Arc length} --- rate $\times$ time, summed
\[L=\int_a^b|\vr\,'(t)|\,dt\]

\columnbreak

\textbf{Integrals} --- slot by slot, vector constant
\[\int\vr\,dt=\Big\langle \int x,\int y,\int z\Big\rangle+\vec C\]
$\vec C$ has \textbf{three} components; $\vr(0)$ finds it.

\textbf{Limits and continuity} --- slot by slot
\[\lim_{t\to a}\vr(t)=\big\langle \lim x,\lim y,\lim z\big\rangle\]
Domain $=$ where \emph{every} slot is defined at once.

\textbf{Projectile} --- $\va=\langle 0,0,-9.8\rangle$
\[\vr(t)=\langle 0,0,-4.9t^2\rangle+t\,\vv(0)+\vr(0)\]

\textbf{Product rules} --- order matters for $\times$
\[(\vec u\cdot\vec v)'=\vec u\,'\!\cdot\vec v+\vec u\cdot\vec v\,'\]
\[(\vec u\times\vec v)'=\vec u\,'\!\times\vec v+\vec u\times\vec v\,'\]

\end{multicols}

\begin{trap}
\textbf{\footnotesize\color{revise}THE MARK YOU WILL LOSE}\ \ ``Find the \textbf{speed}'' means
take the square root at the end. If your answer to a speed question still has
$\langle\ \rangle$ around it, you stopped one step early.
\end{trap}

\begin{key}
\textbf{Domains, in one line each.}\quad
$\sqrt{\ }$ needs $\ge 0$ \quad\textperiodcentered\quad
$\ln$ needs $>0$ (strict) \quad\textperiodcentered\quad
denominators need $\ne 0$ \quad\textperiodcentered\quad
$e^t,\sin,\cos$ are fine everywhere.\\
Then \textbf{intersect} the conditions --- every slot must work at the same time.
\end{key}
"""

BUILD = r"""
\section{Build it up --- so you can rebuild it}

\subsection{Why everything goes slot by slot}

Between time $t$ and a moment $h$ later the bug moves from $\vr(t)$ to $\vr(t+h)$.
The change is the subtraction, and subtracting triples means subtracting each slot:
\[\vr(t+h)-\vr(t)=\big\langle x(t+h)-x(t),\ y(t+h)-y(t),\ z(t+h)-z(t)\big\rangle\]
Dividing by $h$ divides each slot, so each becomes its own rise-over-run. Letting
$h\to0$, a point is close to another exactly when it is close in \emph{all three}
coordinates --- so the limit of a triple is the triple of the limits.

\begin{key}
\[\vr\,'(t)=\langle x'(t),\,y'(t),\,z'(t)\rangle\]
\textbf{Slot by slot is forced, not a convention.} The slots never had an
opportunity to interact. The same argument covers limits, integrals and continuity,
because all of them are built from subtracting, dividing and taking limits.
\end{key}

\subsection{Why $\vr\,'$ points along the curve}

$\vr(t+h)-\vr(t)$ is the arrow from where you are to where you will be --- a chord
cutting across the curve. Dividing by a positive $h$ stretches it but
\textbf{cannot rotate it}, so the direction survives. As $h$ shrinks the far end
slides back and the chord pivots until it grazes the curve. Hence $\vr\,'$ points
exactly the way you are heading, and its length says how fast.

\subsection{Why speed is $|\vr\,'|$, and arc length for free}

$|\vr(t+h)-\vr(t)|$ is the distance travelled in $h$ seconds; divide by $h$ and you
have distance over time. In the limit that is the speed. And if you move at speed
$|\vr\,'|$ for a tiny time $dt$ you cover $|\vr\,'|\,dt$ of ground --- add up every
piece and you have arc length. \textbf{It is distance $=$ rate $\times$ time,
summed.} Rebuild it from that sentence if you blank.

\subsection{Why acceleration leans into the bend}

Suppose speed never changes. Then $|\vv|^2=\vv\cdot\vv$ is constant, so
differentiating gives
\[0=\frac{d}{dt}(\vv\cdot\vv)=\vv\,'\!\cdot\vv+\vv\cdot\vv\,'=2\,\va\cdot\vv
\quad\Longrightarrow\quad \va\perp\vv.\]
Physically: acceleration along your direction of travel would speed you up or slow
you down. If speed is constant, all of it is spent \textbf{turning}. For
$\vr=\langle a\cos t,a\sin t\rangle$ you get $\va=-\vr$ --- pointing straight back
at the centre.

\subsection{Projectiles are Newton plus those integrals}

Gravity is a constant acceleration and nothing pushes sideways, so
$\va=\langle0,0,-9.8\rangle$. Integrate once for $\vv$, again for $\vr$, using
$\vv(0)$ and $\vr(0)$ to fix each vector constant. Then \textbf{every question is
the $z$ slot}, because only $z$ has gravity in it.
"""

ALGORITHMS = r"""
\section{The algorithms --- eight recipes}

\begin{multicols}{2}

\begin{card}
\textbf{1. Domain of a vector function}
\begin{enumerate}[label=\arabic*.]
\item Write the condition each slot needs: $\sqrt{\ }\ge0$, $\ln>0$, denominator $\ne0$.
\item Solve each one separately as an interval.
\item \textbf{Intersect} them. All slots must work at once.
\item Watch bracket types: $\sqrt{\ }$ allows equality, $\ln$ never does.
\end{enumerate}
\end{card}

\begin{card}
\textbf{2. Limit of a vector function}
\begin{enumerate}[label=\arabic*.]
\item Do each slot as a separate one-variable limit.
\item Recognise the standard ones: $\frac{\sin kt}{t}\to k$,
      $\frac{e^t-1}{t}\to1$, $\frac{1-\cos t}{t^2}\to\frac12$.
\item Bounded $\times$ something going to zero $\to$ zero (squeeze).
\item Reassemble into $\langle\ ,\ ,\ \rangle$.
\end{enumerate}
\end{card}

\begin{card}
\textbf{3. Velocity, speed, acceleration}
\begin{enumerate}[label=\arabic*.]
\item Differentiate each slot $\to\vv$.
\item Differentiate again $\to\va$.
\item Substitute the time \emph{after} differentiating, never before.
\item If it asked for \textbf{speed}, take $|\vv|=\sqrt{\text{sum of squares}}$.
\end{enumerate}
\end{card}

\begin{card}
\textbf{4. Unit tangent $\vT$}
\begin{enumerate}[label=\arabic*.]
\item $\vr\,'(t)$, then substitute the time.
\item Compute $|\vr\,'|$ at that time.
\item Divide the vector by that number.
\item Sanity check: the components squared must sum to 1.
\end{enumerate}
\end{card}

\begin{card}
\textbf{5. Position from velocity or acceleration}
\begin{enumerate}[label=\arabic*.]
\item Integrate slot by slot, adding $\vec C=\langle C_1,C_2,C_3\rangle$.
\item Substitute $t=0$ --- every $t$ term dies, so what is left \emph{is} $\vec C$.
\item Match against the given initial position/velocity to read off all three.
\item Integrate again if you started from acceleration.
\end{enumerate}
\end{card}

\begin{card}
\textbf{6. Tangent line to a curve at $t_0$}
\begin{enumerate}[label=\arabic*.]
\item Point: $\vr(t_0)$. Direction: $\vr\,'(t_0)$.
\item Line: $\vec L(u)=\vr(t_0)+u\,\vr\,'(t_0)$ --- \textbf{a new parameter $u$}.
\item To hit a plane, set that coordinate to 0 and solve for $u$.
\item Substitute $u$ back to get the point.
\end{enumerate}
\end{card}

\begin{card}
\textbf{7. Projectile}
\begin{enumerate}[label=\arabic*.]
\item $\va=\langle0,0,-9.8\rangle$. Integrate $\to\vv$, add $\vv(0)$.
\item Integrate $\to\vr$, add $\vr(0)$.
\item \textbf{Max height}: solve $z'=0$, put that $t$ into $z$.
\item \textbf{Time of flight}: solve $z=0$. \textbf{Range}: that $t$ into $x,y$.
\end{enumerate}
\end{card}

\begin{card}
\textbf{8. What curve is this?}
\begin{enumerate}[label=\arabic*.]
\item Look for $\cos^2+\sin^2$: that is a circle of radius $a$ in some plane.
\item A slot that is constant $\Rightarrow$ the curve is flat in that direction.
\item A slot linear in $t$ while the others go round $\Rightarrow$ helix.
\item Eliminate $t$ between two slots to get the surface it lies on.
\end{enumerate}
\end{card}
\end{multicols}
"""


def official_section():
    d = exam1_src.read()
    bank = exam1_sol.all_solutions()
    out = ["\\section{Every official problem, worked}",
           "These are the department's own Exam~1 study-guide problems for "
           "Lessons 5--7 --- the closest thing to the real quiz that exists. "
           "Cover the solution, try it, then check.\n"]
    n = 0
    for sec in d["sections"]:
        if not set(sec["lessons"]) & LESSONS:
            continue
        out.append(f"\\subsection{{{tex(sec['title'])} \\ \\normalfont"
                   f"\\small\\color{{contour}}{tex(sec['secs_label'])}}}")
        for p in sec["problems"]:
            sol = bank.get(p["pid"])
            if not sol:
                continue
            n += 1
            out.append("\\begin{card}")
            out.append(f"\\qnum{{{n}}} {tex(p['stem'])}\n")
            if sol.get("fix"):
                out.append(f"\\textbf{{Official answer:}} \\sout{{{tex(p['answer'])}}}"
                           .replace("\\sout", "\\textcolor{revise}{\\bfseries WRONG}~"))
                out.append(f"\\quad\\textbf{{\\color{{veg}}Correct:}} {tex(sol['right'])}\n")
            else:
                out.append(f"\\textbf{{\\color{{veg}}Answer:}} {tex(p['answer'])}\n")
            out.append("\\vspace{2pt}\\hrule height 0.3pt\\vspace{3pt}")
            out.append("\\begin{enumerate}[label=\\textit{\\arabic*.},leftmargin=1.6em]")
            for st in sol["steps"]:
                out.append(f"\\item {display(st)}")
            out.append("\\end{enumerate}")
            out.append(f"\\trapl{{{tex(sol['trap'])}}}")
            if sol.get("fix"):
                out.append(f"\\begin{{trap}}\\textbf{{\\footnotesize\\color{{revise}}"
                           f"THE OFFICIAL ANSWER IS WRONG}}\\ \\ {tex(sol['fix'])}"
                           f"\\end{{trap}}")
            out.append("\\end{card}\n")
    return "\n".join(out), n


def mine_section():
    qs = [q for q in newbank.QUESTIONS if q["quiz"] == "q3"]
    out = ["\\section{More practice --- multiple choice}",
           "Same sections, different numbers. Answers and full solutions start on "
           "the next section, so you can work these honestly.\n",
           "\\begin{enumerate}[label=\\textbf{\\color{contour}\\arabic*.},leftmargin=1.9em]"]
    for q in qs:
        out.append(f"\\item \\textit{{\\small\\color{{contour}}{tex(q['title'])}}}\\\\"
                   f"{tex(q['stem'])}")
        out.append("\\begin{enumerate}[label=(\\Alph*),leftmargin=1.6em,itemsep=0pt]")
        for letter in sorted(q["opts"]):
            v = q["opts"][letter]
            body = (tex(v.get("text", "")) + (f" ${v['tex']}$" if "tex" in v else "")
                    if isinstance(v, dict) else f"${v}$")
            out.append(f"\\item {body}")
        out.append("\\end{enumerate}\\vspace{3pt}")
    out.append("\\end{enumerate}")

    out.append("\\clearpage\n\\section{Answers and solutions}")
    out.append("\\begin{enumerate}[label=\\textbf{\\color{contour}\\arabic*.},leftmargin=1.9em]")
    for q in qs:
        out.append(f"\\item \\textbf{{\\color{{veg}}{q['key']}}} "
                   f"\\quad\\textit{{\\small\\color{{contour}}{tex(q['title'])}}}")
        out.append("\\begin{itemize}[leftmargin=1.2em,itemsep=1pt]")
        for st in q["sol"]:
            out.append(f"\\item {tex(st)}")
        out.append("\\end{itemize}")
        out.append(f"\\trapl{{{tex(q['trap'])}}}")
    out.append("\\end{enumerate}")
    return "\n".join(out), len(qs)


CHECKLIST = r"""
\section{Walking-in checklist}

Say each of these out loud. Anything you cannot, go back to that problem.

\begin{multicols}{2}
\begin{itemize}[label=$\square$,leftmargin=1.3em]
\item Why differentiating goes slot by slot
\item Why $\vr\,'$ points along the curve
\item The difference between velocity and speed
\item How to build $\vT$, and why $|\vT|=1$
\item Why $\vec C$ has three components
\item How $t=0$ finds $\vec C$
\item Why $\va\perp\vv$ at constant speed
\item The three projectile questions
\item Which slot answers each of them
\item Domain $=$ intersect every slot
\item $\sqrt{\ }$ closed, $\ln$ open
\item Arc length $=$ rate $\times$ time, summed
\end{itemize}
\end{multicols}

\vspace{4pt}
\begin{key}
\textbf{In the room.} Read the question twice and ask \emph{which object does it
want} --- a vector or a number? Then: differentiate, substitute, and only then take
a length if it asked for speed or arc length. No calculator, so the numbers will be
clean; if they are not, you have made an arithmetic slip.
\end{key}
"""


def main():
    off, n_off = official_section()
    mine, n_mine = mine_section()

    doc = (PREAMBLE + TITLE + ONE_PAGE + BUILD + ALGORITHMS
           + "\\clearpage\n" + off + "\\clearpage\n" + mine
           + CHECKLIST + "\n\\end{document}\n")
    OUT_TEX.write_text(doc, encoding="utf-8")

    for run in (1, 2):                      # twice, for page refs
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
             "-output-directory", str(OUT_TEX.parent), str(OUT_TEX)],
            capture_output=True, text=True)
        if r.returncode:
            log = [l for l in r.stdout.splitlines() if l.startswith("!")
                   or "l." in l[:4]]
            print("\n".join(log[:25]) or r.stdout[-2500:], file=sys.stderr)
            sys.exit("cram: pdflatex failed")

    built = OUT_TEX.with_suffix(".pdf")
    OUT_PDF.write_bytes(built.read_bytes())
    pages = len(re.findall(rb"/Type\s*/Page[^s]", OUT_PDF.read_bytes()))
    print(f"{OUT_PDF}  {OUT_PDF.stat().st_size:,} bytes, ~{pages} pages")
    print(f"   {n_off} official problems worked, {n_mine} multiple choice")


if __name__ == "__main__":
    main()
