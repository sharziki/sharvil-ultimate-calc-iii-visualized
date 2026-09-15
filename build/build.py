#!/usr/bin/env python3
"""Rebuild the site around the Fall 2026 MA 26100 quiz calendar.

Inputs :  build/bank.html (the 55 original questions)
          guide.html (patched in place)
Outputs:  index.html, quiz.html, guide.html, exam1.html

Run from this directory:  python3 build.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import course
import exam1page
import primer
import newbank
import guide_121
import patch_guide
import quizpage

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- katex ----

_cache = {}


def _render_batch(items):
    """items: list of (tex, display). Returns list of html."""
    todo = [it for it in items if it not in _cache]
    if todo:
        payload = json.dumps([{"tex": t, "display": d} for t, d in todo])
        r = subprocess.run(["node", str(HERE / "katex_render.js")],
                           input=payload, capture_output=True, text=True)
        if r.returncode:
            # KaTeX fails the whole batch on one bad expression, so re-run the
            # batch one at a time to name it. Worth the extra seconds: the
            # alternative is a stack trace that points at subprocess.run.
            for tex, disp in todo:
                one = subprocess.run(["node", str(HERE / "katex_render.js")],
                                     input=json.dumps([{"tex": tex, "display": disp}]),
                                     capture_output=True, text=True)
                if one.returncode:
                    msg = next((l for l in one.stderr.splitlines()
                                if "ParseError" in l or "KaTeX" in l), one.stderr[:200])
                    sys.exit(f"KaTeX rejected: {tex!r}\n  {msg.strip()}")
            sys.exit(f"katex_render.js failed:\n{r.stderr[:500]}")
        for it, html in zip(todo, json.loads(r.stdout)):
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
    "A12": "13.5P",   # plane through three points  -> Quiz 2
    "A16": "16.5C",   # cylindrical volume          -> Quiz 7
    "B9":  "16.5S",   # spherical triple integral   -> Quiz 8
    # Tagged 14.3 in the old bank, but the tangential component of acceleration
    # is 14.5 — Lesson 8, not Lessons 6-7. Purdue's Lesson 6 and 7 pages cover
    # velocity, acceleration, circular motion and projectiles only.
    "C5":  "14.5",    # tangential component a_T    -> Quiz 4
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
        if tag != q["sec"]:
            # keep the markup's data-sec in step with the split, so the
            # "sections to reread" list after grading names one section, not two
            q["html"] = q["html"].replace(f'data-sec="{q["sec"]}"',
                                          f'data-sec="{tag}"', 1)
            q["sec"] = tag
        buckets[stop].append(q)
    return buckets


def coverage_chips(stop):
    """Guide sections to show under an assessment.

    A quiz gets every section its lessons touch. An exam gets only the sections
    that no quiz covers — the rest are reachable through the quiz tabs, and
    repeating all 38 under the final would be noise, not navigation.
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


# ------------------------------------------------------ new questions ----

def render_new_questions():
    """Turn newbank.QUESTIONS into the same <li class="q"> markup."""
    newbank.verify()
    texts = []
    for q in newbank.QUESTIONS:
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
    for q in newbank.QUESTIONS:
        opts = []
        for letter in sorted(q["opts"]):
            v = q["opts"][letter]
            # v["text"] is prose that may still carry inline $...$ — it has to
            # go through M like every other field, or the dollars ship literally
            # and the option reads "A sphere of radius $1$".
            body = (M(v.get("text", "")) + (M(f"${v['tex']}$") if "tex" in v else "")) \
                if isinstance(v, dict) else M(f"${v}$")
            opts.append(
                f'<li><label><input type="radio" name="{q["id"]}" value="{letter}">'
                f'<span class="let">{letter}</span><span class="ot">{body}</span></label></li>'
            )
        sol = "\n".join(f"<p>{M(p)}</p>" for p in q["sol"])
        anchor = GUIDE_ANCHOR.get(q["sec"], "s131")
        label = SEC_LABEL.get(q["sec"], q["sec"])
        out.append(dict(
            id=q["id"], key=q["key"], sec=q["sec"], tag=q["sec"], quiz=q["quiz"], new=True,
            # carried so the quiz tab can list what it can ask without
            # re-deriving it from the rendered HTML
            kind=q["title"],
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



# --------------------------------------------------------------- index ----

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@'
         '0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap">')

INDEX_CSS = """
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
  font-size:17.5px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(to right,var(--rule) 0 1px,transparent 1px 40px),
             repeating-linear-gradient(to bottom,var(--rule) 0 1px,transparent 1px 40px);opacity:.16}
h1,h2,h3,h4{font-family:var(--disp);text-wrap:balance;margin:0}
p{margin:0}a{color:inherit}
:focus-visible{outline:2px solid var(--revise);outline-offset:3px;border-radius:2px}
.eyebrow{font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
.wrap{position:relative;z-index:1;max-width:940px;margin:0 auto;padding:0 28px 110px}
header.hero{position:relative;padding:96px 0 40px;overflow:hidden}
#field{position:absolute;inset:-40px -240px;width:calc(100% + 480px);height:calc(100% + 80px);z-index:-1}
.hero h1{font-size:clamp(46px,10vw,104px);font-weight:800;line-height:.87;
  letter-spacing:-.042em;margin-top:16px}
.hero h1 em{font-family:var(--body);font-style:italic;font-weight:300;color:var(--contour)}
.lede{margin-top:24px;font-size:20px;line-height:1.5;color:var(--ink-2);max-width:48ch}
.byline{margin-top:22px;display:flex;align-items:center;flex-wrap:wrap;gap:10px 14px;
  font:500 13px/1 var(--mono);letter-spacing:.05em;color:var(--ink-3)}
.byline a.who{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--rule);
  padding-bottom:2px;transition:color .16s ease,border-color .16s ease}
.byline a.who:hover{color:var(--ink);border-color:var(--contour)}
.socials{display:flex;gap:6px}
.socials a{display:grid;place-items:center;width:34px;height:34px;border-radius:3px;
  border:1px solid var(--rule);background:var(--card);color:var(--ink-3);
  transition:color .16s ease,border-color .16s ease,transform .16s ease}
.socials a:hover{color:var(--contour);border-color:var(--contour);transform:translateY(-2px)}
.socials svg{width:15px;height:15px;display:block;fill:currentColor}
.socials svg.stroke{fill:none;stroke:currentColor;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round}
/* the two doors */
/* Three doors. auto-fit with a 300px floor gives 2+1 at desktop widths and
   leaves the third stranded, so the count is stated explicitly and only
   collapses when a card would genuinely be too narrow to read. */
.doors{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:40px}
@media (max-width:900px){.doors{grid-template-columns:1fr}}
.door{display:block;text-decoration:none;background:var(--card);border:1px solid var(--rule);
  border-radius:4px;padding:28px 26px 24px;transition:border-color .18s,transform .18s}
.door:hover{border-color:var(--contour);transform:translateY(-2px)}
.door .k{font:700 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--contour)}
.door h2{font-size:28px;font-weight:800;letter-spacing:-.028em;margin-top:12px;line-height:1.02}
.door p{margin-top:12px;font-size:16.5px;line-height:1.5;color:var(--ink-2)}
.door .go{margin-top:18px;display:inline-block;font:600 13px/1 var(--disp);color:var(--contour)}
/* This card holds three destinations, so it is a <div> with its own links
   rather than one big <a> — an anchor inside an anchor is invalid and browsers
   silently close the outer one, which breaks the whole card. */
.door.c{cursor:default}
.door.c:hover{transform:none;border-color:var(--rule);border-left-color:var(--revise)}
.door .go2{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.door .go2 a{font:600 12.5px/1 var(--disp);color:var(--revise);text-decoration:none;
  border:1px solid var(--rule);border-radius:2px;padding:9px 12px;
  transition:border-color .16s ease,background .16s ease}
.door .go2 a:hover{border-color:var(--revise);background:var(--paper-2)}
.door.b{border-left:3px solid var(--water)}
.door.b .k,.door.b .go{color:var(--water)}
.door.c{border-left:3px solid var(--revise)}
.door.c .k,.door.c .go{color:var(--revise)}
.door.b:hover{border-color:var(--water)}
/* next up */
.next{margin-top:16px;display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;
  border:1px solid var(--rule);border-left:4px solid var(--contour);background:var(--card);
  border-radius:3px;padding:15px 18px}
.next .k{font:700 10.5px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--contour)}
.next b{font-family:var(--disp);font-size:20px;font-weight:800;letter-spacing:-.02em}
.next span{font:500 12.5px/1.5 var(--mono);color:var(--ink-3)}
.next a{margin-left:auto;font:600 12.5px/1 var(--disp);text-decoration:none;
  border:1px solid var(--contour);background:var(--contour);color:var(--paper);
  border-radius:2px;padding:10px 13px;white-space:nowrap}
/* the calendar */
h2.sh{margin-top:56px;font-size:22px;font-weight:800;letter-spacing:-.02em}
p.sn{margin-top:8px;font-size:16px;color:var(--ink-2);max-width:66ch}
.stops{list-style:none;margin:20px 0 0;padding:0}
.stop{border-top:1px solid var(--rule-2);display:grid;
  grid-template-columns:96px 142px minmax(0,1fr) auto;gap:16px;align-items:baseline;padding:13px 0}
.stop:last-child{border-bottom:1px solid var(--rule-2)}
.stop.exam{border-left:3px solid var(--water);padding-left:13px;margin-left:-16px}
.stop.done{opacity:.42}
.stop .lab{font:700 12.5px/1.3 var(--disp);letter-spacing:-.01em}
.stop.exam .lab{color:var(--water)}
.stop .when{font:500 11.5px/1.4 var(--mono);color:var(--ink-3)}
.stop .secs{font:500 12.5px/1.45 var(--mono);color:var(--ink-2);min-width:0}
.stop .n{font:500 11px/1 var(--mono);color:var(--ink-3);text-decoration:none;white-space:nowrap}
.stop .n:hover{color:var(--contour)}
.skip{margin-top:14px;font:500 12px/1.85 var(--mono);color:var(--ink-3)}
.skip b{color:var(--ink-2);font-weight:700}
.gaps{margin-top:22px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--revise);border-radius:2px;padding:15px 18px;
  font-size:16px;line-height:1.55;color:var(--ink-2)}
.gaps b{color:var(--ink);font-weight:500}
footer{margin-top:44px;padding-top:20px;border-top:1px solid var(--rule);
  font:400 12.5px/1.7 var(--mono);color:var(--ink-3)}
footer a{color:var(--contour)}
@media (max-width:720px){
  .stop{grid-template-columns:1fr auto;gap:4px 12px}
  .stop .when{grid-column:1/2}
  .stop .secs{grid-column:1/3}
  .next a{margin-left:0}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""



# Sharvil's own links, taken from his portfolio repo rather than guessed.
SOCIALS = [
    ("https://sharvilsaxena.com", "Personal site", "stroke", "0 0 24 24",
     '<circle cx="12" cy="12" r="9.2"/><path d="M2.8 12h18.4"/>'
     '<path d="M12 2.8c2.6 2.7 4 5.9 4 9.2s-1.4 6.5-4 9.2c-2.6-2.7-4-5.9-4-9.2s1.4-6.5 4-9.2Z"/>'),
    ("https://github.com/sharziki", "GitHub", "fill", "0 0 16 16",
     '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
     '0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
     '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 '
     '0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 '
     '1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 '
     '3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 '
     '8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/>'),
    ("https://x.com/sharziki", "X", "fill", "0 0 24 24",
     '<path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 '
     '2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>'),
    ("https://instagram.com/sharziki", "Instagram", "stroke", "0 0 24 24",
     '<rect x="2.8" y="2.8" width="18.4" height="18.4" rx="5.2"/><circle cx="12" cy="12" r="4.2"/>'
     '<circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/>'),
    ("https://www.linkedin.com/in/sharvilsaxena", "LinkedIn", "fill", "0 0 24 24",
     '<path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.86-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 '
     '1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28ZM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 '
     '4.13Zm1.78 13.02H3.56V9h3.56v11.45ZM22.23 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 '
     '24h20.46c.98 0 1.77-.77 1.77-1.73V1.73C24 .77 23.21 0 22.23 0Z"/>'),
]


def social_links():
    out = []
    for href, name, kind, vb, path in SOCIALS:
        cls = ' class="stroke"' if kind == "stroke" else ""
        out.append(f'<a href="{href}" target="_blank" rel="noopener me" '
                   f'aria-label="{name}" title="{name}">'
                   f'<svg viewBox="{vb}"{cls} aria-hidden="true" focusable="false">'
                   f'{path}</svg></a>')
    return "".join(out)


def build_index(buckets, total, e1):
    rows = []
    for s in course.STOPS:
        n = len(buckets[s["id"]])
        rows.append(
            f'<li class="stop {"exam" if s["kind"] == "exam" else "quiz"}" '
            f'data-date="{s["date"]}">'
            f'<span class="lab">{s["label"]}</span>'
            # "· recitation" is true of every quiz; the date is the information
            f'<span class="when">{s["when"].replace(" &middot; recitation", "").replace(" · recitation", "")}</span>'
            f'<span class="secs">{s["secs_label"]}</span>'
            f'<a class="n" href="/quiz.html#{s["id"]}">{n} questions &rarr;</a>'
            f'</li>')
    skips = "".join(f'<div><b>{w}</b> &mdash; {t}</div>' for w, t in course.NO_QUIZ_WEEKS)

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Calculus III &middot; MA 26100 Fall 2026</title>
<meta name="description" content="Purdue Calc III: study all the material, or study by quiz — only the sections your next quiz covers, plus {total} verified questions on them.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Calculus III &middot; MA 26100 Fall 2026">
<meta property="og:description" content="Study all the material, or study by quiz — only the sections your next quiz covers, plus questions on them.">
<meta property="og:type" content="website">
{FONTS}
<style>{INDEX_CSS}</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <canvas id="field"></canvas>
  <p class="eyebrow">Purdue MA 26100 &middot; Fall 2026 &middot; 37 lessons</p>
  <h1>Calculus III,<br><em>drawn.</em></h1>
  <p class="lede">The whole course as one long walk over a hilly landscape.
  Three ways in.</p>
  <p class="byline">by <a class="who" href="https://sharvilsaxena.com"
    target="_blank" rel="noopener me">Sharvil Saxena</a>
    <span class="socials">{social_links()}</span></p>
</header>

<div class="doors">
  <a class="door" href="/guide.html">
    <span class="k">Everything, in order</span>
    <h2>Study all the material</h2>
    <p>All 40 sections. Intuition first, then the picture, then the formula, then
    the algorithm, then the trap. 41 figures, 12 you can grab and spin.</p>
    <span class="go">Open the guide &rarr;</span>
  </a>
  <a class="door b" href="/quiz.html">
    <span class="k">Only what's next</span>
    <h2>Study by quiz</h2>
    <p>Pick a quiz and get the sections it covers &mdash; and nothing else &mdash;
    in full, then {total} questions on exactly those sections.</p>
    <span class="go">Pick a quiz &rarr;</span>
  </a>
  <div class="door c">
    <span class="k">The official guides</span>
    <h2>The department's own problems, worked</h2>
    <p>All three official study guides, with every one of their
    {e1["problems"]} practice problems worked out and the answer shut until you
    commit. {e1["checked"]} recomputed with sympy; three of the published answers
    are wrong.</p>
    <span class="go2"><a href="/exam1.html">Exam 1</a>
      <a href="/exam2.html">Exam 2</a>
      <a href="/final.html">Final</a></span>
  </div>
</div>

<div class="next" id="next" hidden>
  <span class="k">Next up</span><b id="next-t"></b><span id="next-s"></span>
  <a id="next-q" href="/quiz.html">Study for it &rarr;</a>
</div>

<h2 class="sh">The Fall 2026 calendar</h2>
<p class="sn">Quizzes are in Tuesday recitation, timed, no calculator. Dates and
lesson splits are transcribed from the department's own calendar &mdash; not from a
previous semester.</p>
<ul class="stops">{"".join(rows)}</ul>
<div class="skip">{skips}</div>

<div class="gaps"><b>Three windows have no quiz.</b> Lessons 14&ndash;16 (tangent
planes, max/min) fall between Quiz&nbsp;5 and Midterm&nbsp;1. Lessons 29&ndash;30
(Green's theorem, curl and divergence) fall between Quiz&nbsp;9 and Midterm&nbsp;2.
Lessons 34&ndash;37 (Stokes, divergence theorem) come after the last quiz and are on
the final only. Nothing paces you through those, which is where the grade goes.</div>

<footer>
  Calendar, weights and dates read {course.VERIFIED} from the official
  <a href="{course.SCHED_PDF}" target="_blank" rel="noopener">Fall&nbsp;2026 calendar</a> and
  <a href="{course.RULES_PDF}" target="_blank" rel="noopener">ground rules</a>.
  Confirm your own section in Brightspace.<br>
  Questions are original and sympy-verified; they are not past Purdue questions.
  Not affiliated with or endorsed by Purdue University.
</footer>
</div>

<script>{INDEX_JS}</script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


INDEX_JS = r"""
(function(){
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
    document.getElementById("next-t").textContent=s.label;
    document.getElementById("next-s").innerHTML=s.when+" &middot; "+s.secs;
    document.getElementById("next-q").href="/quiz.html#"+s.id;
    document.getElementById("next").hidden=false;
  }

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

    for q in new_qs:
        buckets[q["quiz"]].append(q)
    # Prime KaTeX for every primer in one node call, instead of one call per
    # expression while the page is being assembled.
    MM(*[t for st in course.STOPS for t in primer.texts(st["id"])])
    total = quizpage.build(buckets, M, SID_LABEL, coverage_chips,
                           official=exam1page.official_index(),
                           official_problems=lambda lessons, prefix="":
                               exam1page.official_problems(M, MM, lessons,
                                                           prefix=prefix),
                           blind_spots=exam1page.official_blind_spots)

    global INDEX_JS
    INDEX_JS = INDEX_JS.replace("@@STOPS@@", json.dumps([
        dict(id=s["id"], label=s["label"], when=s["when"], date=s["date"],
             secs=s["secs_label"])
        for s in course.STOPS]))
    e1 = exam1page.build(M, MM)
    build_index(buckets, total, e1)

    patch_guide.run(M, MM, coverage_chips)

    print(f"quiz.html      {total} questions ({len(new_qs)} new, verified) "
          f"across {len(course.STOPS)} tabs")
    for s in course.STOPS:
        n = len(buckets[s["id"]])
        print(f"   {s['label']:<12} {len(coverage_chips(s)):>2} sections  {n:>3} questions")
    print("index.html     semester map")
    print("guide.html     patched")
    for pg in e1["pages"]:
        print(f"{pg['out']:<14} {pg['problems']:>3} official problems worked "
              f"across {pg['sections']:>2} lessons")
    print(f"               {e1['checked']} of {e1['problems']} answers recomputed "
          f"({e1['prose']} prose), {e1['agreed']} re-read from the official pages "
          f"and matched")
    print(f"               {e1['fixes']} official answers corrected")
    for tok, ln in e1["gaps"]:
        print(f"               ! §{tok} is on Fall Lesson {ln} and absent from "
              f"the Spring guide — flagged on the page")


if __name__ == "__main__":
    main()
