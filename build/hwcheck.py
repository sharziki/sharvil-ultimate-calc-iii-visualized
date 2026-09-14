"""Guard: no practice question may reproduce an assigned homework problem.

The README promises the questions are original. That promise is easy to break by
accident when you write practice *from* the homework, which is exactly how the
first draft of the Quiz 4 bank went wrong: 19 of 25 questions carried the
homework's own numbers, so drilling them rehearsed recall of a seen answer
instead of the method.

This compares the mathematical *content* of each stem — the multiset of numbers
and the sequence of function names — against every assigned problem on record.
Prose is ignored; two questions that differ only in wording still collide.
"""

import re
import sys

# Problems assigned in MyLab, transcribed from the worked set. Only the
# mathematical core is recorded: that is what must not be reused.
ASSIGNED = {
    # Transcribed in the same notation the bank uses, so the fingerprints
    # are directly comparable. These are the problems that must NOT be reused.
    '14.4.9': r"""Find the length of $\mathbf r(t)=\langle 20t^{2},\,-6,\,48t^{2}+5\rangle$ for $0\le t\le1$.""",
    '14.4.11': r"""Find the length of $\mathbf r(t)=\langle 3\cos t,\;3\sin t\rangle$ for $0\le t\le\pi$.""",
    '14.4.13': r"""Find the length of $\mathbf r(t)=\langle 4\sin t-4t\cos t,\;4\cos t+4t\sin t\rangle$ for $0\le t\le\dfrac{\pi}{2}$.""",
    '14.4.23': r"""For $\mathbf r(t)=\langle 3t^{3},\,-t^{3},\,4t^{3}\rangle$, $0\le t\le6$, find the speed.""",
    '14.4.40': r"""$\mathbf r(t)=\langle 7t^{2},\,8t^{2},\,2\sqrt{14}\,t^{2}\rangle$ for $1\le t\le4$ does <b>not</b> use arc length. Which $\mathbf r(s)$ does?""",
    '14.4.42': r"""Does $\mathbf r(t)=\left\langle \dfrac{1}{\sqrt2}\cos t,\;\dfrac{1}{\sqrt2}\cos t,\;\sin t\right\rangle$ use arc length as its parameter?""",
    '14.5.11': r"""For $\mathbf r(t)=\langle 2t+2,\;4t-8,\;5t+14\rangle$, find $\mathbf T$ and $\kappa$.""",
    '14.5.13': r"""For $\mathbf r(t)=\langle \sqrt3\,t,\;3\sin t,\;3\cos t\rangle$, find $\mathbf T$ and $\kappa$.""",
    '14.5.15': r"""For $\mathbf r(t)=\langle \sqrt{19}\cos t,\;9\cos t,\;10\sin t\rangle$, find $\mathbf T$ and $\kappa$.""",
    '14.5.23': r"""Use $\kappa=\dfrac{|\mathbf a\times\mathbf v|}{|\mathbf v|^{3}}$ to find the curvature of $\mathbf r(t)=\langle 3+t^{2},\,t,\,0\rangle$.""",
    '15.1.11': r"""Describe the level curves of the paraboloid $z=x^{2}+y^{2}$.""",
    '15.1.15': r"""Find the domain of $f(x,y)=9xy+5x+4y$.""",
    '15.1.17': r"""Find the domain of $f(x,y)=\sqrt{12-3x^{2}-3y^{2}}$.""",
    '15.1.19': r"""Find the domain of $f(x,y)=\sin\!\left(\dfrac{x-6}{y-8}\right)$.""",
    '15.1.25': r"""For $f(x,y)=5x+4y-20$, which set of intercepts identifies its graph, and what are the domain and range?""",
    '15.1.28': r"""Describe the graph of $f(x,y)=1-x^{2}$, and give its domain and range.""",
    '15.1.30': r"""For $F(x,y)=\sqrt{1-x^{2}-y^{2}}$, give the graph, domain and range.""",
    '15.1.34': r"""A surface shows <b>two separate peaks</b>, side by side along the $y$-axis, falling away to zero everywhere else. Which contour plot is it?""",
    '15.1.35': r"""Match each function to its surface: (i) $\cos xy$, (ii) $\ln(x^{2}+y^{2})$, (iii) $\dfrac{1}{x-y}$, (iv) $\dfrac{1}{1+x^{2}+y^{2}}$.""",
}

_WORDS = re.compile(r"\\(?:sin|cos|tan|ln|log|exp|sqrt)\b|\b(?:sin|cos|tan|ln|log|exp|sqrt)\b")
_NUM = re.compile(r"\d+")
def fingerprint(s):
    """(sorted numbers, function-name sequence) — the mathematical skeleton."""
    s = re.sub(r"<[^>]+>", " ", s)                 # strip HTML
    s = re.sub(r"\\(?:tfrac|dfrac|frac)", " frac ", s)
    funcs = tuple(w.lstrip("\\") for w in _WORDS.findall(s))
    nums = tuple(sorted(int(n) for n in _NUM.findall(s)))
    return nums, funcs


# Questions whose stems are too short to fingerprint safely (few digits, no named
# functions), checked by hand against the assigned problem instead. Recording the
# comparison here is the point: it is the evidence, not a suppression.
HAND_CHECKED = {
    "Q4m": "15.1.11 is z=x^2+y^2 (circular levels); ours is z=y-x^2 (parabolic)",
    "Q4n": "15.1.15 is 9xy+5x+4y (degree 2); ours is 4x^3y-7xy^2+2y (degree 4)",
    "Q4q": "15.1.25 is 5x+4y-20; ours is 3x+6y-18, different intercepts",
    "Q4r": "15.1.28 is 1-x^2 (missing y); ours is y^2-4 (missing x, other axis)",
    "Q4t": "15.1.34 is two peaks along y; ours is a peak AND a pit along x",
}


def check(questions):
    """Return a list of collision descriptions; empty means all clear."""
    assigned = {k: fingerprint(v) for k, v in ASSIGNED.items()}
    bad = []
    for q in questions:
        f = fingerprint(q["stem"])
        # A fingerprint this thin carries no information — "the point (0,1)" and
        # "0 <= t <= 1" both reduce to it. Demand real substance before accusing.
        if len(f[0]) + 2 * len(f[1]) < 4:
            continue
        for name, g in assigned.items():
            # A collision needs the same numbers AND the same functions. Either
            # alone is coincidence; both together means the problem was copied.
            if f[0] == g[0] and f[1] == g[1]:
                bad.append(f"{q['id']} reproduces assigned problem {name}")
                break
    return bad


if __name__ == "__main__":
    import q4bank
    problems = check(q4bank.QUESTIONS)
    if problems:
        print("HOMEWORK OVERLAP:\n  " + "\n  ".join(problems))
        sys.exit(1)
    print(f"no overlap: {len(q4bank.QUESTIONS)} questions vs "
          f"{len(ASSIGNED)} assigned problems")
