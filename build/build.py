#!/usr/bin/env python3
"""Rebuild the site around the Fall 2026 MA 26100 quiz calendar.

Inputs :  build/bank.html (the 55 original questions)
          guide.html (patched in place)
Outputs:  index.html, practice.html, guide.html

Run from this directory:  python3 build.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import course
import bank_q1
import guide_121
import patch_guide

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- katex ----

_cache = {}


def _render_batch(items):
    """items: list of (tex, display). Returns list of html."""
    todo = [it for it in items if it not in _cache]
    if todo:
        payload = json.dumps([{"tex": t, "display": d} for t, d in todo])
        out = subprocess.run(
            ["node", str(HERE / "katex_render.js")],
            input=payload, capture_output=True, text=True, check=True,
        ).stdout
        for it, html in zip(todo, json.loads(out)):
            _cache[it] = html
    return [_cache[it] for it in items]


_MATH = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.S)


def M(text):
    """Render $inline$ and $$display$$ TeX inside an HTML string."""
    hits = []
    for m in _MATH.finditer(text):
        hits.append((m.group(1) or m.group(2), m.group(1) is not None))
    if not hits:
        return text
    rendered = _render_batch(hits)
    it = iter(rendered)
    return _MATH.sub(lambda m: next(it), text)


def MM(*texts):
    """Prime the cache for a whole page in one node call, then render."""
    hits = []
    for t in texts:
        for m in _MATH.finditer(t):
            hits.append((m.group(1) or m.group(2), m.group(1) is not None))
    _render_batch(hits)
    return [M(t) for t in texts]


# ------------------------------------------------------- question bank ----

def read_bank():
    """Read the 55 original question blocks out of build/bank.html."""
    src = (HERE / "bank.html").read_text(encoding="utf-8")
    out = {}
    for b in re.split(r'(?=<li class="q" id=)', src):
        m = re.match(r'<li class="q" id="q-([A-Z0-9]+)" data-key="([A-Z])" '
                     r'data-sec="([^"]+)"', b)
        if not m:
            continue
        qid, key, sec = m.groups()
        b = b.rstrip()
        out[qid] = dict(id=qid, key=key, sec=sec,
                        html=b[:b.rfind("</li>") + 5])
    if len(out) != 55:
        sys.exit(f"bank.html: expected 55 questions, found {len(out)}")
    return out


# 13.5 and 16.5 span two assessments; the question itself decides which side.
SPLIT = {
    "A12": "13.5P",   # plane through three points -> Quiz 2
    "A16": "16.5C",   # cylindrical volume         -> Quiz 7
    "B9":  "16.5S",   # spherical triple integral  -> Quiz 8
}

SEC_LABEL = {
    "12.1": "12.1 Parametric equations", "13.1": "13.1 Vectors",
    "13.2": "13.2 Space, distance, spheres", "13.3": "13.3 Dot product",
    "13.4": "13.4 Cross product", "13.5L": "13.5 Lines", "13.5P": "13.5 Planes",
    "13.6": "13.6 Quadric surfaces", "14.1": "14.1 Vector functions",
    "14.2": "14.2 Derivatives & integrals", "14.3": "14.3 Motion",
    "14.4": "14.4 Arc length", "14.5": "14.5 Curvature & TNB",
    "15.1": "15.1 Surfaces & level curves", "15.2": "15.2 Limits",
    "15.3": "15.3 Partial derivatives", "15.4": "15.4 Chain rule",
    "15.5": "15.5 Gradient", "15.6": "15.6 Tangent planes",
    "15.7": "15.7 Max & min", "15.8": "15.8 Lagrange",
    "16.1": "16.1 Double integrals", "16.2": "16.2 General regions",
    "16.3": "16.3 Polar", "16.4": "16.4 Triple integrals",
    "16.5C": "16.5 Cylindrical", "16.5S": "16.5 Spherical",
    "16.6": "16.6 Mass & moments", "17.1": "17.1 Vector fields",
    "17.2": "17.2 Line integrals", "17.3": "17.3 Conservative fields",
    "17.4": "17.4 Green's theorem", "17.5": "17.5 Curl & divergence",
    "17.6": "17.6 Surface integrals", "17.7": "17.7 Stokes",
    "17.8": "17.8 Divergence theorem",
}

GUIDE_ANCHOR = {
    "12.1": "s121", "13.1": "s131", "13.2": "s132", "13.3": "s133",
    "13.4": "s134", "13.5L": "s135", "13.5P": "s135", "13.6": "s136",
    "14.1": "s141", "14.2": "s142", "14.3": "s143", "14.4": "s144",
    "14.5": "s144", "15.1": "s151", "15.2": "s152", "15.3": "s153",
    "15.4": "s154", "15.5": "s155", "15.6": "s156", "15.7": "s157",
    "15.8": "s158", "16.1": "s161", "16.2": "s162", "16.3": "s163",
    "16.4": "s164", "16.5C": "s165c", "16.5S": "s165s", "16.6": "s166",
    "17.1": "s171", "17.2": "s172", "17.3": "s173", "17.4": "s174",
    "17.5": "s175", "17.6": "s176f", "17.7": "s177", "17.8": "s178",
}


# guide section id -> printed section number, taken from the rail so the chip
# and the sidebar can never disagree.
SID_LABEL = {sid: num for sid, num, title, _ in patch_guide.RAIL if title}


def bucket(bank):
    """Assign every question to a stop id."""
    buckets = {s["id"]: [] for s in course.STOPS}
    for qid, q in bank.items():
        tag = SPLIT.get(qid, q["sec"])
        stop = course.SEC_TO_STOP.get(tag)
        if stop is None:                      # 13.5 / 16.5 with no explicit split
            sys.exit(f"{qid}: section {tag} maps to no assessment")
        q["tag"] = tag
        buckets[stop].append(q)
    return buckets


# ----------------------------------------------------- new Q1 questions ----

def render_new_questions():
    """Turn bank_q1.QUESTIONS into the same <li class="q"> markup."""
    bank_q1.verify()
    texts = []
    for q in bank_q1.QUESTIONS:
        texts.append(q["stem"])
        for v in q["opts"].values():
            if isinstance(v, dict):
                texts.append(v.get("text", "") + (f"${v['tex']}$" if "tex" in v else ""))
            else:
                texts.append(f"${v}$")
        texts.extend(q["sol"])
        texts.append(q["trap"])
    MM(*texts)

    out = []
    for q in bank_q1.QUESTIONS:
        opts = []
        for letter in sorted(q["opts"]):
            v = q["opts"][letter]
            body = (v.get("text", "") + (M(f"${v['tex']}$") if "tex" in v else "")) \
                if isinstance(v, dict) else M(f"${v}$")
            opts.append(
                f'<li><label><input type="radio" name="{q["id"]}" value="{letter}">'
                f'<span class="let">{letter}</span><span class="ot">{body}</span></label></li>'
            )
        sol = "\n".join(f"<p>{M(p)}</p>" for p in q["sol"])
        anchor = GUIDE_ANCHOR.get(q["sec"], "s131")
        label = SEC_LABEL.get(q["sec"], q["sec"])
        out.append(dict(
            id=q["id"], key=q["key"], sec=q["sec"], tag=q["sec"], new=True,
            html=(
                f'<li class="q" id="q-{q["id"]}" data-key="{q["key"]}" data-sec="{q["sec"]}">\n'
                f'<div class="qh"><span class="qn">@@N@@</span>'
                f'<span class="qsec">{q["title"]}</span>'
                f'<span class="qnew">new</span></div>\n'
                f'<div class="stem">{M(q["stem"])}</div>\n'
                f'<ol class="opts">\n' + "\n".join(opts) + "\n</ol>\n"
                f'<div class="sol" hidden>\n'
                f'<p class="solh">Answer <b>{q["key"]}</b></p>\n'
                f'<div class="solb">{sol}</div>\n'
                f'<p class="trapl"><span>Trap</span>{M(q["trap"])}</p>\n'
                f'<p class="review">Review <a href="/guide.html#{anchor}">'
                f'&sect;{label} in the study guide</a></p>\n'
                f'</div></li>'
            ),
        ))
    return out


# ------------------------------------------------------------ practice ----

SHARED_HEAD_CSS = """
:root{
  --paper:#EAEEE6; --paper-2:#E0E5DA; --card:#F5F7F1;
  --ink:#1B241F; --ink-2:#55655A; --ink-3:#7E8C82;
  --rule:#C6CFBF; --rule-2:#D5DCCE;
  --contour:#A65523; --water:#1D6E8C; --veg:#42743A; --revise:#AE2668;
  --disp:"Archivo","Helvetica Neue",Arial,sans-serif;
  --body:"Newsreader",Georgia,"Times New Roman",serif;
  --mono:"JetBrains Mono",ui-monospace,"SF Mono",Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#121A14; --paper-2:#0C120E; --card:#1A241C;
  --ink:#E6EBE1; --ink-2:#9DAC9C; --ink-3:#7B8B7C;
  --rule:#2C3A2E; --rule-2:#233026;
  --contour:#E5904F; --water:#5FBBDC; --veg:#84C46E; --revise:#F26EA6;
}}
:root[data-theme="dark"]{
  --paper:#121A14; --paper-2:#0C120E; --card:#1A241C;
  --ink:#E6EBE1; --ink-2:#9DAC9C; --ink-3:#7B8B7C;
  --rule:#2C3A2E; --rule-2:#233026;
  --contour:#E5904F; --water:#5FBBDC; --veg:#84C46E; --revise:#F26EA6;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:17.5px;line-height:1.62;-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(to right,var(--rule) 0 1px,transparent 1px 40px),
             repeating-linear-gradient(to bottom,var(--rule) 0 1px,transparent 1px 40px);opacity:.16}
h1,h2,h3,h4{font-family:var(--disp);text-wrap:balance;margin:0}
p{margin:0}a{color:inherit}
:focus-visible{outline:2px solid var(--revise);outline-offset:3px;border-radius:2px}
.eyebrow{font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

PRACTICE_CSS = """
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 28px}
header.top{padding:56px 0 26px;border-bottom:2px solid var(--ink)}
header.top h1{font-size:clamp(38px,7vw,64px);font-weight:800;line-height:.92;
  letter-spacing:-.035em;margin-top:14px}
header.top h1 em{font-family:var(--body);font-style:italic;font-weight:300;color:var(--contour)}
header.top .sub{margin-top:18px;font-size:19px;color:var(--ink-2);max-width:62ch}
main{padding-bottom:120px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:26px 0 0}
.tabs button{font:600 12.5px/1 var(--disp);background:var(--card);color:var(--ink-2);
  border:1px solid var(--rule);border-radius:2px;padding:9px 12px;cursor:pointer}
.tabs button.on{background:var(--contour);border-color:var(--contour);color:var(--paper)}
.tabs button.ex{border-left:3px solid var(--water)}
.tabs button.ex.on{background:var(--water);border-color:var(--water)}
.pane{margin-top:24px}
.ph{font-size:26px;font-weight:800;letter-spacing:-.02em;margin-top:6px}
.pwhen{font:500 11px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--contour)}
.pn{margin-top:10px;font-size:16.5px;color:var(--ink-2);max-width:66ch}
.pcov{margin-top:14px;display:flex;flex-wrap:wrap;gap:7px}
.pcov a{font:500 11.5px/1 var(--mono);text-decoration:none;border:1px solid var(--rule);
  background:var(--card);padding:7px 10px;border-radius:2px;color:var(--ink-2)}
.pcov a:hover{border-color:var(--contour);color:var(--ink)}
.pnote{margin-top:16px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--revise);border-radius:2px;padding:13px 16px;
  font-size:15.5px;line-height:1.55;color:var(--ink-2)}
.pnote b{color:var(--ink)}
.bar{position:sticky;top:0;z-index:5;display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  background:var(--paper-2);border:1px solid var(--rule);border-radius:3px;padding:11px 14px;margin-top:20px}
.bar button{font:600 12px/1 var(--disp);border-radius:2px;padding:9px 13px;cursor:pointer;
  border:1px solid var(--rule);background:var(--card);color:var(--ink-2)}
.bar button.submit{background:var(--contour);border-color:var(--contour);color:var(--paper)}
.bar .bstat{font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  color:var(--ink-3);margin-left:auto}
.result{margin-top:14px;border:1px solid var(--rule);border-left:3px solid var(--veg);
  background:var(--card);border-radius:2px;padding:16px 18px}
.result.fail{border-left-color:var(--revise)}
.result h4{font-size:26px;font-weight:800;letter-spacing:-.02em}
.result p{margin-top:8px;font-size:16.5px;color:var(--ink-2)}
.result .miss{margin-top:12px;font:500 13.5px/1.7 var(--mono);color:var(--ink-2)}
.result .miss b{color:var(--revise)}
.qs{list-style:none;margin:0;padding:0}
.q{border-top:1px solid var(--rule-2);padding:24px 0 22px}
.q.right{border-left:3px solid var(--veg);padding-left:16px}
.q.wrong{border-left:3px solid var(--revise);padding-left:16px}
.qh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.qn{font:700 12px/1 var(--mono);color:var(--paper);background:var(--ink);
  border-radius:50%;width:24px;height:24px;line-height:24px;text-align:center;flex:none}
.qsec{font:500 10.5px/1 var(--mono);letter-spacing:.11em;text-transform:uppercase;color:var(--ink-3)}
.qnew{font:700 9.5px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--paper);background:var(--veg);padding:4px 6px;border-radius:2px}
.stem{margin-top:11px;font-size:18px;line-height:1.55;max-width:72ch}
.opts{list-style:none;margin:14px 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:6px}
.opts label{display:flex;gap:10px;align-items:baseline;padding:9px 11px;cursor:pointer;
  border:1px solid transparent;border-radius:2px}
.opts label:hover{background:var(--card);border-color:var(--rule)}
.opts input{margin:0;accent-color:var(--contour);flex:none;align-self:center}
.opts .let{font:700 12px/1 var(--mono);color:var(--ink-3);flex:none}
.opts .ot{font-size:16px}
.q.graded label.correct{background:color-mix(in srgb,var(--veg) 14%,transparent);border-color:var(--veg)}
.q.graded label.chosen-wrong{background:color-mix(in srgb,var(--revise) 12%,transparent);border-color:var(--revise)}
.sol{margin-top:16px;background:var(--paper-2);border:1px solid var(--rule);
  border-left:3px solid var(--water);border-radius:2px;padding:14px 17px}
.solh{font:700 11px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--water)}
.solh b{color:var(--ink);font-size:14px}
.solb{margin-top:10px;font-size:16.5px;line-height:1.65;color:var(--ink-2)}
.solb p+p{margin-top:7px}
.solb .katex{color:var(--ink)}
.trapl{margin-top:11px;font-size:15.5px;color:var(--ink-2)}
/* first-child only — the trap text may contain KaTeX, whose root is also a
   direct <span> child and must not inherit the label's mono/uppercase rules. */
.trapl>span:first-child{font:700 10px/1 var(--mono);letter-spacing:.13em;
  text-transform:uppercase;color:var(--revise);margin-right:9px}
.trapl .katex{color:var(--ink)}
.review{margin-top:8px;font:500 13px/1 var(--mono)}
.review a{color:var(--contour)}
footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--rule);
  font:400 13px/1.7 var(--mono);color:var(--ink-3)}
footer a{color:var(--contour)}
@media (max-width:640px){.opts{grid-template-columns:1fr}}
"""

SITENAV = """<style>
.sitenav{position:fixed;left:14px;top:14px;z-index:50;text-decoration:none;
  font:600 12px/1 var(--disp,sans-serif);color:var(--ink-2,#555);
  background:var(--card,#fff);border:1px solid var(--rule,#ccc);border-radius:3px;padding:8px 11px}
.sitenav:hover{color:var(--ink,#000);border-color:var(--ink-3,#888)}
@media(max-width:1180px){.sitenav{position:static;display:inline-block;margin:12px 0 0 20px}}
</style>"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@'
         '0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap">')


def coverage_chips(stop):
    """Guide sections to link from an assessment.

    A quiz gets every section its lessons touch. An exam gets only the sections
    that no quiz covers — the rest are reachable through the quiz tabs, and
    listing all 38 on the final would be noise, not navigation.
    """
    seen, chips = set(), []
    if stop["kind"] == "exam":
        source = [GUIDE_ANCHOR[tag] for tag in stop["secs"] if tag in GUIDE_ANCHOR]
    else:
        source = [sid for ln in stop["lessons"] if ln in course.LESSONS
                  for sid in course.LESSONS[ln][1]]
    for sid in source:
        if sid not in seen:
            seen.add(sid)
            chips.append(sid)
    return chips



def build_practice(buckets, new_qs):
    stops = course.STOPS
    tabs, panes = [], []

    for s in stops:
        qs = list(buckets[s["id"]])
        if s["id"] == "q1":
            qs = qs + new_qs
        qs.sort(key=lambda q: (q["tag"], q["id"]))
        cls = "ex" if s["kind"] == "exam" else ""
        tabs.append(f'<button data-tab="{s["id"]}" class="{cls}">{s["label"]}</button>')

        chips = "".join(
            f'<a href="/guide.html#{sid}">&sect;{SID_LABEL.get(sid, sid)}</a>'
            for sid in coverage_chips(s))

        lessons = ", ".join(str(l) for l in s["lessons"]) if len(s["lessons"]) <= 6 \
            else f'{s["lessons"][0]}&ndash;{s["lessons"][-1]}'
        head = (
            f'<p class="pwhen">{s["when"]} &middot; Lessons {lessons} '
            f'&middot; {s["secs_label"]}</p>\n'
            f'<h3 class="ph">{s["label"]}</h3>\n'
            f'<p class="pn">{s["blurb"]}</p>\n'
            f'<div class="pcov">{chips}</div>\n'
        )
        if s.get("extra"):
            head += f'<div class="pnote"><b>Worth knowing.</b> {s["extra"]}</div>\n'

        if s["kind"] == "exam":
            head += (f'<div class="pnote">These are the questions on material that '
                     f'<b>no quiz covers</b>. Everything from the earlier quizzes is '
                     f'on this exam too &mdash; work those tabs as well.</div>\n')

        items = []
        for n, q in enumerate(qs, 1):
            items.append(q["html"].replace(
                '<span class="qn">@@N@@</span>', f'<span class="qn">{n}</span>'
            ) if "@@N@@" in q["html"] else re.sub(
                r'<span class="qn">\d+</span>', f'<span class="qn">{n}</span>',
                q["html"], count=1))

        panes.append(
            f'<section class="pane" id="pane-{s["id"]}" hidden>\n{head}'
            f'<div class="bar">'
            f'<button class="submit" data-submit>Check answers</button>'
            f'<button data-reset>Reset</button>'
            f'<span class="bstat"><span data-answered>0</span>/{len(qs)} answered</span>'
            f'</div>\n'
            f'<div class="result" data-result hidden></div>\n'
            f'<ol class="qs">\n' + "\n".join(items) + "\n</ol>\n</section>"
        )

    total = sum(len(buckets[s["id"]]) for s in stops) + len(new_qs)
    js = PRACTICE_JS.replace("@@FIRST@@", stops[0]["id"])

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Practice by quiz &middot; MA 26100 Fall 2026</title>
<meta name="description" content="{total} verified MA 26100 practice questions, sorted into the Fall 2026 quiz and exam buckets. Every answer recomputed symbolically.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Practice by quiz &middot; MA 26100 Fall 2026">
<meta property="og:description" content="{total} verified MA 26100 practice questions, sorted into the Fall 2026 quiz and exam buckets.">
<meta property="og:type" content="website">
{FONTS}
</head>
<body>
<a class="sitenav" href="/">&larr; Semester map</a>
{SITENAV}
<link rel="stylesheet" href="/katex.css">
<style>{SHARED_HEAD_CSS}{PRACTICE_CSS}</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Purdue MA 26100 &middot; Fall 2026 &middot; {total} verified questions</p>
  <h1>Practice, <em>by quiz.</em></h1>
  <p class="sub">Pick the quiz you are sitting. Every question is filed under the
  assessment that actually tests it, using the department's own Fall&nbsp;2026 lesson
  calendar. Untimed, no calculator &mdash; the quizzes don't allow one either.
  Answers and worked solutions appear when you check.</p>
</header>

<main>
<div class="tabs">{"".join(tabs)}</div>
{"".join(panes)}
</main>

<footer>
  Buckets follow the official
  <a href="{course.SCHED_PDF}" target="_blank" rel="noopener">MA&nbsp;261 F26 calendar</a>
  and <a href="{course.RULES_PDF}" target="_blank" rel="noopener">ground rules</a>,
  read {course.VERIFIED}.<br>
  Questions are <b>original</b> and every answer was recomputed with sympy, not asserted.
  They are not past Purdue questions. Not affiliated with or endorsed by Purdue University.
</footer>
</div>

<script>{js}</script>
</body>
</html>
"""
    (ROOT / "practice.html").write_text(html, encoding="utf-8")
    return total


PRACTICE_JS = r"""
(function(){
  "use strict";
  var KEY="calc3-practice-f26";
  var state={};
  try{ state=JSON.parse(localStorage.getItem(KEY)||"{}"); }catch(e){ state={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(state)); }catch(e){} }

  var tabs=[].slice.call(document.querySelectorAll(".tabs button"));
  function show(id){
    tabs.forEach(function(b){ b.classList.toggle("on", b.dataset.tab===id); });
    document.querySelectorAll(".pane").forEach(function(p){ p.hidden = p.id!=="pane-"+id; });
    try{ history.replaceState(null,"","#"+id); }catch(e){}
  }
  tabs.forEach(function(b){ b.addEventListener("click",function(){ show(b.dataset.tab); }); });
  var want=(location.hash||"").replace("#","");
  show(tabs.some(function(b){return b.dataset.tab===want;}) ? want : "@@FIRST@@");

  document.querySelectorAll(".q input[type=radio]").forEach(function(inp){
    if(state[inp.name]===inp.value) inp.checked=true;
    inp.addEventListener("change",function(){
      state[inp.name]=inp.value; save(); count(inp.closest(".pane"));
    });
  });
  function count(pane){
    if(!pane) return;
    var n=pane.querySelectorAll(".q input[type=radio]:checked").length;
    var el=pane.querySelector("[data-answered]"); if(el) el.textContent=n;
  }
  document.querySelectorAll(".pane").forEach(count);

  document.querySelectorAll(".pane").forEach(function(pane){
    var sub=pane.querySelector("[data-submit]"); if(!sub) return;
    sub.addEventListener("click",function(){ grade(pane); });
    pane.querySelector("[data-reset]").addEventListener("click",function(){
      pane.querySelectorAll(".q").forEach(function(q){
        q.classList.remove("graded","right","wrong");
        q.querySelector(".sol").hidden=true;
        q.querySelectorAll("label").forEach(function(l){ l.classList.remove("correct","chosen-wrong"); });
        q.querySelectorAll("input").forEach(function(i){ i.checked=false; delete state[i.name]; });
      });
      pane.querySelector("[data-result]").hidden=true; save(); count(pane);
      window.scrollTo({top:pane.offsetTop-20,behavior:"smooth"});
    });
  });

  function grade(pane){
    var qs=[].slice.call(pane.querySelectorAll(".q")), right=0, missed=[];
    qs.forEach(function(q){
      var key=q.dataset.key;
      var picked=q.querySelector("input:checked");
      q.classList.add("graded");
      q.querySelectorAll("label").forEach(function(l){
        var v=l.querySelector("input").value;
        if(v===key) l.classList.add("correct");
        else if(picked && v===picked.value) l.classList.add("chosen-wrong");
      });
      var ok = picked && picked.value===key;
      q.classList.add(ok?"right":"wrong");
      q.querySelector(".sol").hidden=false;
      if(ok) right++; else missed.push(q.dataset.sec);
    });
    var n=qs.length, pct=Math.round(100*right/n);
    var box=pane.querySelector("[data-result]");
    var tally={}; missed.forEach(function(s){ tally[s]=(tally[s]||0)+1; });
    var list=Object.keys(tally).sort().map(function(s){
      return "§"+s+(tally[s]>1?" ×"+tally[s]:"");
    }).join("  ·  ");
    box.className="result"+(missed.length?" fail":"");
    box.hidden=false;
    box.innerHTML="<h4>"+right+" / "+n+"  —  "+pct+"%</h4>"+
      "<p>"+(missed.length
        ? "Read the worked solution under every question you missed, then fix the idea in the guide before you reset."
        : "Clean sweep. Read a couple of the solutions anyway — the trap notes are where the quiz marks actually go.")+"</p>"+
      (list? "<p class=\"miss\">Sections to review: <b>"+list+"</b></p>":"");
    box.scrollIntoView({behavior:"smooth",block:"center"});
  }
})();
"""


# --------------------------------------------------------------- index ----

INDEX_CSS = """
.wrap{position:relative;z-index:1;max-width:1080px;margin:0 auto;padding:0 28px 120px}
header.hero{position:relative;padding:84px 0 32px;border-bottom:2px solid var(--ink);overflow:hidden}
#field{position:absolute;inset:-40px -220px;width:calc(100% + 440px);height:calc(100% + 80px);z-index:-1}
.hero h1{font-size:clamp(40px,8.4vw,88px);font-weight:800;line-height:.89;
  letter-spacing:-.04em;margin-top:16px}
.hero h1 em{font-family:var(--body);font-style:italic;font-weight:300;color:var(--contour)}
.lede{margin-top:22px;font-size:20px;line-height:1.5;color:var(--ink-2);max-width:58ch}
.chips{margin-top:26px;display:flex;flex-wrap:wrap;gap:9px}
.chip{font:500 11.5px/1 var(--mono);letter-spacing:.05em;border:1px solid var(--rule);
  background:var(--card);padding:8px 11px;border-radius:2px;color:var(--ink-2)}
.chip b{color:var(--ink);font-weight:700}
.next{margin-top:30px;background:var(--card);border:1px solid var(--rule);
  border-left:4px solid var(--contour);border-radius:3px;padding:20px 22px}
.next .k{font:700 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--contour)}
.next h2{font-size:30px;font-weight:800;letter-spacing:-.025em;margin-top:10px;line-height:1.05}
.next h2 span{color:var(--ink-3);font-weight:600;font-size:19px;letter-spacing:0}
.next p{margin-top:10px;font-size:17px;line-height:1.5;color:var(--ink-2);max-width:64ch}
.next .go{margin-top:16px;display:flex;flex-wrap:wrap;gap:8px}
.next .go a{font:600 13px/1 var(--disp);text-decoration:none;border-radius:2px;padding:11px 15px;
  border:1px solid var(--contour);background:var(--contour);color:var(--paper)}
.next .go a.alt{background:var(--card);color:var(--ink-2);border-color:var(--rule)}
.next .go a.alt:hover{color:var(--ink);border-color:var(--ink-3)}
h2.sh{margin-top:52px;font-size:24px;font-weight:800;letter-spacing:-.02em}
p.sn{margin-top:9px;font-size:16.5px;color:var(--ink-2);max-width:68ch}
.stops{list-style:none;margin:22px 0 0;padding:0;display:flex;flex-direction:column;gap:0}
.stop{border-top:1px solid var(--rule-2);padding:18px 0;display:grid;
  grid-template-columns:130px minmax(0,1fr) auto;gap:22px;align-items:baseline}
.stop:last-child{border-bottom:1px solid var(--rule-2)}
.stop.exam{border-left:3px solid var(--water);padding-left:14px;margin-left:-17px}
.stop.done{opacity:.5}
.stop .when{font:500 11px/1.5 var(--mono);letter-spacing:.06em;color:var(--ink-3)}
.stop .when b{display:block;color:var(--contour);font-weight:700;letter-spacing:.13em;
  text-transform:uppercase;font-size:10.5px;margin-bottom:5px}
.stop.exam .when b{color:var(--water)}
.stop .what h3{font-size:19px;font-weight:700;letter-spacing:-.012em}
.stop .what .secs{margin-top:5px;font:500 12px/1.6 var(--mono);color:var(--ink-3)}
.stop .what p{margin-top:7px;font-size:15.5px;line-height:1.5;color:var(--ink-2);max-width:56ch}
.stop .acts{display:flex;flex-direction:column;gap:5px;align-items:flex-end}
.stop .acts a{font:600 12px/1 var(--disp);text-decoration:none;white-space:nowrap;
  border:1px solid var(--rule);background:var(--card);border-radius:2px;padding:8px 11px;color:var(--ink-2)}
.stop .acts a:hover{border-color:var(--contour);color:var(--ink)}
.stop .acts a.n{font:500 10.5px/1 var(--mono);border:0;background:none;padding:2px 0;color:var(--ink-3)}
.skip{margin-top:16px;font:500 12.5px/1.9 var(--mono);color:var(--ink-3)}
.skip b{color:var(--ink-2);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:20px}
.f{background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:15px 16px}
.f.hot{border-left:3px solid var(--revise)}
.f h4{font:700 10.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-3);margin-bottom:8px}
.f .big{font-size:21px;font-weight:800;font-family:var(--disp);letter-spacing:-.02em;line-height:1.15}
.f.hot .big{color:var(--revise)}
.f p{margin-top:6px;font-size:14.5px;line-height:1.45;color:var(--ink-2)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:16px;margin-top:22px}
.card{display:block;text-decoration:none;background:var(--card);border:1px solid var(--rule);
  border-radius:4px;padding:24px;transition:border-color .18s,transform .18s}
.card:hover{border-color:var(--contour);transform:translateY(-2px)}
.card .k{font:700 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--contour)}
.card h3{font-size:24px;font-weight:800;letter-spacing:-.022em;margin-top:11px;line-height:1.06}
.card p{margin-top:10px;font-size:16px;line-height:1.5;color:var(--ink-2)}
.card .go{margin-top:15px;display:inline-block;font:600 13px/1 var(--disp);color:var(--contour)}
.card.b{border-left:3px solid var(--water)}
.card.b .k,.card.b .go{color:var(--water)}
.card.b:hover{border-color:var(--water)}
.note{margin-top:22px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--contour);border-radius:2px;padding:16px 18px}
.note h4{font:700 10.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;
  color:var(--contour);margin-bottom:9px}
.note p{font-size:16.5px;line-height:1.55;color:var(--ink-2)}
.note p+p{margin-top:9px}
.note b{color:var(--ink);font-weight:500}
.tblwrap{overflow-x:auto;margin-top:18px}
.tbl{width:100%;border-collapse:collapse;font-size:15.5px}
.tbl th{font:700 10.5px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);text-align:left;padding:0 14px 8px 0;border-bottom:1.5px solid var(--ink);white-space:nowrap}
.tbl td{padding:10px 14px 10px 0;border-bottom:1px solid var(--rule-2);vertical-align:top;color:var(--ink-2)}
.tbl td:first-child{color:var(--ink);font-weight:600;font-family:var(--disp);white-space:nowrap}
footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--rule);
  font:400 13px/1.7 var(--mono);color:var(--ink-3)}
footer a{color:var(--contour)}
@media (max-width:720px){
  .stop{grid-template-columns:1fr;gap:10px}
  .stop .acts{flex-direction:row;align-items:center;flex-wrap:wrap}
}
"""


def build_index(buckets, new_qs, total):
    rows = []
    for s in course.STOPS:
        n = len(buckets[s["id"]]) + (len(new_qs) if s["id"] == "q1" else 0)
        lessons = (", ".join(str(l) for l in s["lessons"]) if len(s["lessons"]) <= 6
                   else f'{s["lessons"][0]}&ndash;{s["lessons"][-1]}')
        secs = s["secs_label"]
        kind = "exam" if s["kind"] == "exam" else "quiz"
        rows.append(
            f'<li class="stop {kind}" data-date="{s["date"]}">'
            f'<div class="when"><b>{s["label"]}</b>{s["when"]}</div>'
            f'<div class="what"><h3>Lessons {lessons}</h3>'
            f'<p class="secs">{secs}</p><p>{s["blurb"]}</p></div>'
            f'<div class="acts">'
            f'<a href="/practice.html#{s["id"]}">{n} questions &rarr;</a>'
            f'<a class="n" href="/guide.html#{coverage_chips(s)[0]}">read the sections</a>'
            f'</div></li>'
        )

    skips = "".join(f'<div><b>{w}</b> &mdash; {t}</div>' for w, t in course.NO_QUIZ_WEEKS)
    grades = "".join(
        f'<tr><td>{a}</td><td><b>{b}</b></td><td>{c}</td></tr>' for a, b, c in course.GRADING)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MA 26100 &middot; Fall 2026 semester map</title>
<meta name="description" content="Purdue Calc III, organised by the Fall 2026 quiz calendar. Every quiz and exam with the lessons it covers, the sections to read, and {total} verified practice questions.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Calculus III &middot; MA 26100 Fall 2026">
<meta property="og:description" content="Every quiz and exam with the lessons it covers, the sections to read, and {total} verified practice questions.">
<meta property="og:type" content="website">
{FONTS}
<style>{SHARED_HEAD_CSS}{INDEX_CSS}</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <canvas id="field"></canvas>
  <p class="eyebrow">Purdue MA 26100 &middot; {course.TERM} &middot; Briggs 3e &middot; 37 lessons</p>
  <h1>Calculus III,<br><em>by quiz.</em></h1>
  <p class="lede">The whole course as one long walk over a hilly landscape &mdash; cut
  into the ten quizzes and three exams that actually decide your grade. Each stop
  below tells you exactly which lessons it covers, which sections to read, and
  gives you questions whose answers were computed, not asserted.</p>
  <div class="chips">
    <span class="chip"><b>10</b> quizzes &middot; <b>3</b> exams</span>
    <span class="chip"><b>{total}</b> verified questions</span>
    <span class="chip"><b>41</b> figures &middot; 12 you can spin</span>
    <span class="chip"><b>86</b> check-yourself questions</span>
  </div>
</header>

<div class="next" id="next" hidden>
  <span class="k">Next up</span>
  <h2 id="next-t"></h2>
  <p id="next-p"></p>
  <div class="go"><a id="next-q" href="/practice.html">Practise it</a>
  <a class="alt" id="next-r" href="/guide.html">Read the sections</a></div>
</div>

<h2 class="sh">The semester, stop by stop</h2>
<p class="sn">Dates and lesson splits are transcribed from the department's own
Fall&nbsp;2026 calendar &mdash; not from a previous semester. Quizzes are in Tuesday
recitation, timed, and no calculator is allowed.</p>
<ul class="stops">{"".join(rows)}</ul>
<div class="skip">{skips}</div>

<h2 class="sh">What the grade is made of</h2>
<div class="tblwrap"><table class="tbl">
<thead><tr><th>Component</th><th>Weight</th><th>Detail</th></tr></thead>
<tbody>{grades}</tbody>
</table></div>
<div class="grid">
  <div class="f"><h4>Quizzes</h4><p class="big">2 lowest dropped</p>
    <p>Every recitation, timed. No make-ups &mdash; the drops are the make-up.</p></div>
  <div class="f"><h4>Homework</h4><p class="big">3 lowest dropped</p>
    <p>MyLab Math, generally Tue and Thu at 11:59&nbsp;pm. Late work is not accepted.</p></div>
  <div class="f hot"><h4>Drop with no record</h4><p class="big">Fri Sep 4</p>
    <p>After that a drop becomes a <b>W</b>, until Nov&nbsp;24.</p></div>
  <div class="f"><h4>Calculators</h4><p class="big">Never</p>
    <p>Not on quizzes, not on midterms, not on the final. Practise by hand.</p></div>
</div>

<h2 class="sh">The two pages</h2>
<div class="cards">
  <a class="card" href="/guide.html">
    <span class="k">Learn it</span>
    <h3>The study guide</h3>
    <p>All 37 lessons in four units. Intuition first, then the picture, then the
    formula, then the algorithm, then the trap. Each section is badged with the
    quiz that tests it.</p>
    <span class="go">Open the guide &rarr;</span>
  </a>
  <a class="card b" href="/practice.html">
    <span class="k">Prove it</span>
    <h3>Practice by quiz</h3>
    <p>{total} multiple-choice questions filed under the quiz or exam that tests
    them, with a worked solution and the specific trap each one plants.</p>
    <span class="go">Pick a quiz &rarr;</span>
  </a>
</div>

<div class="note"><h4>How to actually use this</h4>
  <p><b>Reading is not preparation.</b> Reading builds recognition; a quiz tests cold
  execution in ten minutes with no calculator. Those are different skills.</p>
  <p>So, each week: read the two or three sections the next quiz covers, do the
  <b>check-yourself</b> questions inside them with the answer hidden, then take that
  quiz's practice tab cold. Whatever it exposes, fix in the guide and re-take.</p>
  <p>Watch the gaps. <b>Lessons 14&ndash;16, 29&ndash;30 and 34&ndash;37 appear on no
  quiz at all</b> &mdash; they go straight onto a midterm or the final, so nothing
  forces you to learn them on time. Those three windows are where people lose the grade.</p>
</div>

<footer>
  Calendar, weights and dates read {course.VERIFIED} from the official
  <a href="{course.SCHED_PDF}" target="_blank" rel="noopener">Fall&nbsp;2026 calendar</a> and
  <a href="{course.RULES_PDF}" target="_blank" rel="noopener">ground rules</a>
  on the <a href="{course.COURSE_PAGE}" target="_blank" rel="noopener">department course page</a>.
  Confirm your own section's dates in Brightspace.<br>
  Practice questions are original and sympy-verified; they are not past Purdue
  questions. Not affiliated with or endorsed by Purdue University.
</footer>
</div>

<script>{INDEX_JS}</script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


INDEX_JS = r"""
(function(){
  /* mark past stops, surface the next one */
  var STOPS=@@STOPS@@;
  var today=new Date(); today.setHours(0,0,0,0);
  var next=null;
  document.querySelectorAll(".stop").forEach(function(el){
    var d=new Date(el.dataset.date+"T00:00:00");
    if(d<today) el.classList.add("done");
    else if(!next) next=el.dataset.date;
  });
  var s=STOPS.filter(function(x){return x.date===next;})[0];
  if(s){
    var box=document.getElementById("next");
    document.getElementById("next-t").innerHTML=s.label+" <span>&middot; "+s.when+"</span>";
    document.getElementById("next-p").innerHTML="Lessons "+s.lessons+" &mdash; "+s.blurb;
    document.getElementById("next-q").href="/practice.html#"+s.id;
    document.getElementById("next-r").href="/guide.html#"+s.anchor;
    box.hidden=false;
  }

  /* contour field behind the hero */
  var cv=document.getElementById("field"); if(!cv||!cv.getContext) return;
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var ctx=cv.getContext("2d");
  var peaks=[[.22,.62,1,.03],[.55,.28,.78,.02],[.82,.66,.62,.024],[.4,.88,-.7,.018]];
  function f(x,y){var s=0;for(var i=0;i<peaks.length;i++){var p=peaks[i],dx=x-p[0],dy=(y-p[1])*.62;
    s+=p[2]*Math.exp(-(dx*dx+dy*dy)/(2*p[3]));}return s;}
  function css(n){return getComputedStyle(document.body).getPropertyValue(n).trim()||"#A65523";}
  function draw(){
    var r=cv.getBoundingClientRect(), W=r.width, H=r.height; if(!W||!H) return;
    var dpr=Math.min(window.devicePixelRatio||1,2);
    cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
    var cols=110, rows=Math.max(20,Math.round(110*H/W)), vals=new Float32Array(cols*rows), i, j;
    for(j=0;j<rows;j++) for(i=0;i<cols;i++) vals[j*cols+i]=f(i/(cols-1), j/(rows-1));
    var sx=W/(cols-1), sy=H/(rows-1);
    ctx.strokeStyle=css("--contour"); ctx.lineWidth=1;
    for(var L=-.6;L<=1;L+=.075){
      ctx.globalAlpha=.10+.14*Math.max(0,L); ctx.beginPath();
      for(j=0;j<rows-1;j++) for(i=0;i<cols-1;i++){
        var a=vals[j*cols+i],b=vals[j*cols+i+1],c=vals[(j+1)*cols+i+1],d=vals[(j+1)*cols+i],p=[];
        if((a<L)!==(b<L)) p.push([(i+(L-a)/(b-a))*sx, j*sy]);
        if((b<L)!==(c<L)) p.push([(i+1)*sx, (j+(L-b)/(c-b))*sy]);
        if((c<L)!==(d<L)) p.push([(i+1-(L-c)/(d-c))*sx, (j+1)*sy]);
        if((d<L)!==(a<L)) p.push([i*sx, (j+1-(L-d)/(a-d))*sy]);
        if(p.length===2||p.length===4){ctx.moveTo(p[0][0],p[0][1]);ctx.lineTo(p[1][0],p[1][1]);
          if(p.length===4){ctx.moveTo(p[2][0],p[2][1]);ctx.lineTo(p[3][0],p[3][1]);}}
      }
      ctx.stroke();
    }
    ctx.globalAlpha=1;
  }
  draw(); window.addEventListener("resize",draw);
})();
"""


def main():
    bank = read_bank()
    new_qs = render_new_questions()
    buckets = bucket(bank)
    total = build_practice(buckets, new_qs)

    global INDEX_JS
    stops_json = json.dumps([
        dict(id=s["id"], label=s["label"], when=s["when"], date=s["date"],
             blurb=s["blurb"], anchor=coverage_chips(s)[0],
             lessons=(", ".join(str(l) for l in s["lessons"]) if len(s["lessons"]) <= 6
                      else f'{s["lessons"][0]}–{s["lessons"][-1]}'))
        for s in course.STOPS])
    INDEX_JS = INDEX_JS.replace("@@STOPS@@", stops_json)
    build_index(buckets, new_qs, total)

    patch_guide.run(M, MM, coverage_chips)

    print(f"practice.html  {total} questions "
          f"({len(new_qs)} new, verified) across {len(course.STOPS)} buckets")
    for s in course.STOPS:
        n = len(buckets[s["id"]]) + (len(new_qs) if s["id"] == "q1" else 0)
        print(f"   {s['label']:<12} {n:>3}")
    print("index.html     semester map")
    print("guide.html     patched")


if __name__ == "__main__":
    main()
