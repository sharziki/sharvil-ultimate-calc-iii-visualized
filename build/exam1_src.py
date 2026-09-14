"""Read the official MA 261 Exam 1 study guide and hand back its structure.

The vendored copy in `sources/StudyGuide-Exam1.html` is Purdue's own page
(msunkula, Spring 2026), saved verbatim. It is the *source of truth* for what
Exam 1 covers: the lesson split, the section numbers, the exam date, and the
practice problems with the instructor's own answers.

Nothing here rewrites the instructor's text. The stems and answers come out of
the file exactly as written; this module only finds them. Anything the page
does not say — the worked steps between a problem and its answer — lives in
`exam1_sol.py` and is clearly labelled as ours.

The parse is strict on purpose. If the page is re-published with a different
shape, every function below exits rather than silently shipping half a guide.
"""

import html as _html
import re
import sys
from pathlib import Path

import course

HERE = Path(__file__).resolve().parent
SRC = HERE / "sources" / "StudyGuide-Exam1.html"

# section id on the official page -> (our lesson key, guide section ids)
# The guide ids are the ones patch_guide.py already emits, so every lesson can
# deep-link into the material we wrote for it.
LESSON_MAP = [
    ("lesson1",     "L1",    [1],      ["s131", "s132", "s133", "s133b", "s134"]),
    ("lesson2",     "L2",    [2],      ["s135"]),
    ("lesson3-4",   "L3-4",  [3, 4],   ["s136"]),
    ("lesson5",     "L5",    [5],      ["s141"]),
    ("lesson6-7",   "L6",  [6, 7],   ["s142", "s143"]),
    ("lesson8",     "L8",    [8],      ["s144"]),
    ("lesson9",     "L9",    [9],      ["s151"]),
    ("lesson10",    "L10",   [10],     ["s152"]),
    ("lesson11",    "L11",   [11],     ["s153"]),
    ("lesson12",    "L12",   [12],     ["s154"]),
    ("lesson13",    "L13",   [13],     ["s155"]),
    ("lesson14",    "L14",   [14],     ["s156"]),
    ("lesson15-16", "L15", [15, 16], ["s157"]),
]

SOURCE_URL = ("https://www.math.purdue.edu/~msunkula/MA261/Sp26/"
              "StudyGuide-Exam1.html")
VERIFIED = "2026-09-14"


def _text(frag):
    """Strip tags, keep the instructor's \\( ... \\) maths as $...$."""
    t = re.sub(r"<[^>]+>", "", frag)
    t = _html.unescape(t)
    t = t.replace("\\(", "$").replace("\\)", "$")
    t = t.replace("\\[", "$$").replace("\\]", "$$")
    return re.sub(r"\s+", " ", t).strip()


def _dollars(frag):
    """Same, but for body copy that must keep its inline markup."""
    t = _html.unescape(frag)
    t = t.replace("\\(", "$").replace("\\)", "$")
    t = t.replace("\\[", "$$").replace("\\]", "$$")
    return t


def read(path=None, expect=None):
    """Parse one official study guide.

    `path` defaults to the Exam 1 guide. `expect` is the live problem count the
    caller believes the page has; a mismatch is fatal, because a silently
    half-parsed guide is worse than no guide.

    Sections are discovered from the page rather than hardcoded, so the Exam 2
    and Final guides parse with the same code. Only the mapping from a lesson to
    *our* guide's section ids is a lookup, and lessons we have no section for
    simply deep-link to nothing rather than failing.
    """
    src = Path(path) if path else SRC
    if not src.exists():
        sys.exit(f"exam1_src: {src} missing — vendor the official guide first")
    h = src.read_text(encoding="utf-8")
    # The published page carries one commented-out problem (a distance from a
    # point to a plane, in Lesson 2). It is not live on the instructor's page,
    # so it is not live here either — but the *skill* is still examinable, and
    # exam1_sol.py restores it as an explicitly-labelled extra.
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)

    # The Final guide publishes no date — the registrar sets it — so a missing
    # date is information, not a parse failure.
    m = re.search(r"<strong>Exam Date:</strong>\s*([^<]+)<", h)
    exam_date = m.group(1).strip() if m else ""
    m = re.search(r"<strong>Time:</strong>\s*([^<]+)<", h)
    exam_time = m.group(1).strip() if m else ""
    m = re.search(r"<strong>Coverage:</strong>\s*([^<]+)<", h)
    coverage = _html.unescape(m.group(1)).strip() if m else ""

    known = {sid: (key, lessons, gids) for sid, key, lessons, gids in LESSON_MAP}

    out = []
    for sm in re.finditer(r'<section id="(lesson[^"]*)".*?</section>', h, re.S):
        sid = sm.group(1)
        block = sm.group(0)
        if '<div class="practice-problems"' not in block:
            continue
        key, lessons, guide_ids = known.get(sid, (None, None, None))
        if key is None:
            # Not in the Exam 1 map: derive both from the id, e.g.
            # "lesson31-33" -> key "L31", lessons [31, 32, 33].
            nums = [int(n) for n in re.findall(r"\d+", sid)]
            if not nums:
                sys.exit(f"exam1_src: cannot read a lesson number out of {sid!r}")
            lessons = list(range(nums[0], nums[-1] + 1))
            key = f"L{nums[0]}"
            guide_ids = [g for ln in lessons if ln in course.LESSONS
                         for g in course.LESSONS[ln][1]]

        hm = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        title_full = _text(hm.group(1))
        # "Review of Vectors [Lesson 1] (§13.1-13.4)"
        tm = re.match(r"(.*?)\s*\[(.*?)\]\s*\((.*?)\)\s*$", title_full)
        if not tm:
            sys.exit(f"exam1_src: unparsable heading {title_full!r}")
        title, lesson_label, secs_label = tm.groups()

        # the instructor's own notes: everything before the practice block
        body = block.split('<div class="practice-problems"', 1)[0]
        body = re.sub(r"<h2[^>]*>.*?</h2>", "", body, flags=re.S)
        body = re.sub(r'<div class="lecture-links">.*?</div>', "", body, flags=re.S)
        body = re.sub(r"</?section[^>]*>", "", body)

        probs = []
        for pm in re.finditer(
                r'<div class="practice-question".*?>\s*'
                r'<div class="question-prompt"><p>(.*?)</p>'
                r'<span class="toggle-hint">.*?</span></div>\s*'
                r'<div class="answer-box"><span class="answer-label">Answer'
                # Exam 1 writes "Answer</span><p>value</p>"; the Exam 2 and
                # Final guides write "Answer: value</span>" with no <p>. Accept
                # either, and capture whichever side carries the value.
                r'(?::\s*(?P<inline>[^<]*))?</span>'
                r'(?P<block>.*?)</div>\s*</div>', block, re.S):
            stem_raw, ans_raw = pm.group(1), pm.group(2)
            ans_raw = (pm.group("inline") or "") + (pm.group("block") or "")
            nm = re.match(r"\s*<strong>Problem\s+(\d+)\.</strong>\s*(.*)$",
                          stem_raw, re.S)
            if not nm:
                sys.exit(f"exam1_src: unnumbered problem in {sid}")
            n, stem = nm.group(1), nm.group(2)
            ans = re.sub(r"</?p>", "", ans_raw)
            probs.append(dict(
                pid=f"{key}P{n}", n=int(n), lesson=key,
                stem=_dollars(stem).strip(),
                answer=_dollars(ans).strip(),
            ))
        if not probs:
            sys.exit(f"exam1_src: no practice problems in {sid}")

        out.append(dict(
            id=sid, key=key, title=title.strip(), lesson_label=lesson_label,
            secs_label=secs_label, lessons=lessons, guide_ids=guide_ids,
            notes_html=_dollars(body).strip(), problems=probs,
        ))

    if not out:
        sys.exit(f"exam1_src: no lesson sections found in {src.name}")
    total = sum(len(s["problems"]) for s in out)
    if expect is not None and total != expect:
        sys.exit(f"exam1_src: {src.name}: expected {expect} live practice "
                 f"problems, found {total}")
    return dict(exam_date=exam_date, exam_time=exam_time, coverage=coverage,
                sections=out, total=total)


if __name__ == "__main__":
    d = read(expect=68)
    print(d["exam_date"], "|", d["exam_time"], "|", d["coverage"])
    for s in d["sections"]:
        print(f'{s["key"]:<7} {s["title"][:44]:<46} {s["secs_label"]:<16} '
              f'{len(s["problems"])} problems')
    print("total", d["total"])
