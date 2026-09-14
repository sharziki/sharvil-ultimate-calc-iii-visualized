"""exam1.html — the official Exam 1 study guide, worked.

Purdue publishes a study guide for Exam 1: thirteen lesson sections, the
formulas that matter, and 68 practice problems with a bare final answer under
each. It is the source of truth for what the exam covers, and it is also the
least useful possible format for actually practising, because the answer is one
click away and there is no work in between.

This page keeps the instructor's structure and text exactly, and adds the three
things it is missing:

  1. **The work.** Every problem gets a worked solution and a trap note.
  2. **A commitment step.** The answer stays shut until you say you have tried,
     which is the entire mechanism that makes practice testing work.
  3. **Verification.** 57 of the 68 answers are recomputed with sympy at build
     time. Two of the instructor's published answers are wrong, and the page
     says so, next to the official text rather than instead of it.

The instructor's prose is rendered inside `.official` blocks and is never
edited. Ours is always in a block labelled as ours.
"""

import re
import sys
from pathlib import Path

import course
import exam1_audit
import exam1_src
import exam1_sol

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# Our own guide has a section for every lesson on this exam; each block deep
# links into it, so "I don't actually know this" has somewhere to go.
GUIDE_LABEL = {
    "s131": "13.1", "s132": "13.2", "s133": "13.3", "s133b": "13.3",
    "s134": "13.4", "s135": "13.5", "s136": "13.6", "s141": "14.1",
    "s142": "14.2", "s143": "14.3", "s144": "14.4", "s151": "15.1",
    "s152": "15.2", "s153": "15.3", "s154": "15.4", "s155": "15.5",
    "s156": "15.6", "s157": "15.7",
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@'
         '0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap">')

CSS = """
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
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}
  *{animation:none!important;transition:none!important}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
  font-size:17.5px;line-height:1.62;-webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:repeating-linear-gradient(to right,var(--rule) 0 1px,transparent 1px 40px),
             repeating-linear-gradient(to bottom,var(--rule) 0 1px,transparent 1px 40px);
  opacity:.16}
h1,h2,h3,h4{font-family:var(--disp);text-wrap:balance;margin:0}
p{margin:0}a{color:inherit}
:focus-visible{outline:2px solid var(--revise);outline-offset:3px;border-radius:2px}
.eyebrow{font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
.wrap{position:relative;z-index:1;max-width:1080px;margin:0 auto;padding:0 28px 120px}
.sitenav{display:inline-block;margin:16px 0 0 28px;font:500 12px/1 var(--mono);
  color:var(--ink-3);text-decoration:none;position:relative;z-index:2}
.sitenav:hover{color:var(--contour)}

header.top{padding:58px 0 26px;border-bottom:2px solid var(--ink)}
header.top h1{font-size:clamp(38px,7vw,68px);font-weight:800;line-height:.92;
  letter-spacing:-.038em;margin-top:14px}
header.top h1 em{font-family:var(--body);font-style:italic;font-weight:300;color:var(--contour)}
header.top .sub{margin-top:18px;font-size:19px;line-height:1.5;color:var(--ink-2);max-width:60ch}
.facts{margin-top:24px;display:grid;gap:10px;
  grid-template-columns:repeat(auto-fit,minmax(178px,1fr))}
.fact{background:var(--card);border:1px solid var(--rule);border-radius:3px;padding:12px 14px}
.fact b{display:block;font:700 9.5px/1 var(--mono);letter-spacing:.14em;
  text-transform:uppercase;color:var(--ink-3)}
.fact span{display:block;margin-top:7px;font-family:var(--disp);font-weight:700;
  font-size:16px;letter-spacing:-.015em;line-height:1.25}
.srcline{margin-top:20px;font:400 13px/1.7 var(--mono);color:var(--ink-3)}
.srcline a{color:var(--contour)}
.gapbox{margin-top:22px;border:1px solid var(--revise);border-left:3px solid var(--revise);
  border-radius:3px;background:color-mix(in srgb,var(--revise) 7%,transparent);
  padding:16px 19px;max-width:78ch}
.gapbox>b{display:block;font-family:var(--disp);font-size:17px;letter-spacing:-.015em;
  color:var(--ink)}
.gapbox p{margin-top:9px;font-size:16.5px;line-height:1.55;color:var(--ink-2)}
.gapbox ul{margin:9px 0 0;padding-left:20px;font-size:16.5px;color:var(--ink-2)}
.gapbox li{margin-top:5px}
.gapbox li b{color:var(--ink)}
.gapbox a{color:var(--contour)}

/* ---- the contents rail ------------------------------------------------ */
.toc{position:sticky;top:0;z-index:20;background:var(--paper);
  border-bottom:1px solid var(--rule);margin-top:22px;padding:10px 0}
.toc-in{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none;padding:2px 0}
.toc-in::-webkit-scrollbar{display:none}
.toc a{flex:0 0 auto;text-decoration:none;border-radius:3px;padding:7px 11px;
  font:600 12px/1 var(--disp);color:var(--ink-2);white-space:nowrap;
  border:1px solid transparent}
.toc a:hover{color:var(--contour);border-color:var(--rule)}
.toc a.on{background:var(--ink);color:var(--paper)}
.toc a i{font-style:normal;font-family:var(--mono);font-size:10px;
  color:inherit;opacity:.6;margin-right:6px}

/* ---- progress --------------------------------------------------------- */
.prog{position:sticky;top:0;z-index:21;height:3px;background:transparent}
.prog i{display:block;height:100%;width:0;background:var(--contour)}

/* ---- a lesson --------------------------------------------------------- */
.lesson{padding-top:14px;scroll-margin-top:74px}
.lh{margin-top:46px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;
  border-top:2px solid var(--ink);padding-top:18px}
.lh .n{font:700 12px/1 var(--mono);letter-spacing:.14em;color:var(--contour);flex:none}
.lh h2{font-size:clamp(25px,3.4vw,34px);font-weight:800;letter-spacing:-.026em;
  line-height:1.03;flex:1 1 320px}
.lh .x{font:500 10.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3);border:1px solid var(--rule);border-radius:2px;padding:5px 8px;
  white-space:nowrap}
.lgo{display:inline-flex;align-items:center;gap:7px;margin-top:12px;
  font:500 11.5px/1 var(--mono);text-decoration:none;color:var(--ink-3);
  border:1px solid var(--rule);border-radius:2px;padding:7px 10px}
.lgo:hover{color:var(--contour);border-color:var(--contour)}

/* the instructor's own text, untouched */
.official{margin-top:18px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--water);border-radius:2px;padding:6px 20px 18px;
  max-width:78ch}
.official .tag{display:inline-block;margin-top:14px;font:700 9.5px/1 var(--mono);
  letter-spacing:.14em;text-transform:uppercase;color:var(--water)}
.official h3{margin-top:18px;font-size:16.5px;font-weight:700;letter-spacing:-.01em}
.official p{margin-top:9px;font-size:16.5px;line-height:1.6;color:var(--ink-2)}
.official ul{margin:9px 0 0;padding-left:20px;color:var(--ink-2);font-size:16.5px}
.official li{margin-top:5px}
.official li strong,.official p strong{color:var(--ink);font-weight:600}
.official .katex{color:var(--ink)}
.official table{width:100%;border-collapse:collapse;margin-top:12px;font-size:15px}
.official th,.official td{border:1px solid var(--rule);padding:8px 10px;
  text-align:left;vertical-align:top;color:var(--ink-2)}
.official th{font-family:var(--disp);font-size:12px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--ink);background:var(--paper-2)}
.official caption{caption-side:top;text-align:left;font-family:var(--disp);
  font-weight:700;padding-bottom:6px}
.formula-box{margin-top:10px;padding:2px 0;overflow-x:auto}

/* ---- problems --------------------------------------------------------- */
.ph2{margin-top:30px;display:flex;align-items:baseline;gap:12px}
.ph2 h3{font-size:19px;font-weight:800;letter-spacing:-.02em}
.ph2 span{font:500 10.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink-3)}
.ph2 .done{margin-left:auto;font:500 11px/1 var(--mono);color:var(--ink-3)}
.ph2 .done b{color:var(--veg)}
.probs{list-style:none;margin:8px 0 0;padding:0;max-width:86ch}
.prob{border-top:1px solid var(--rule-2);padding:20px 0 18px}
.prob.seen{border-left:3px solid var(--veg);padding-left:15px}
.pn{display:flex;align-items:baseline;gap:11px;flex-wrap:wrap}
.pn .num{font:700 11.5px/24px var(--mono);color:var(--paper);background:var(--ink);
  border-radius:50%;width:24px;height:24px;text-align:center;flex:none}
.prob.seen .num{background:var(--veg)}
.pn .tagx{font:700 9.5px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--paper);background:var(--contour);padding:4px 6px;border-radius:2px}
.stem{margin-top:10px;font-size:18px;line-height:1.55}
.tryrow{margin-top:13px;display:flex;gap:9px;align-items:center;flex-wrap:wrap}
.tryrow button{cursor:pointer;border-radius:2px;border:1px solid var(--rule);
  background:var(--card);color:var(--ink-2);padding:9px 13px;
  font:600 12px/1 var(--disp)}
.tryrow button.go{background:var(--contour);border-color:var(--contour);color:var(--paper)}
.tryrow .hintx{font:400 13px/1.5 var(--mono);color:var(--ink-3)}
.work{margin-top:12px;background:var(--paper-2);border:1px solid var(--rule);
  border-left:3px solid var(--contour);border-radius:2px;padding:15px 18px}
.work[hidden]{display:none}
.ansline{display:flex;gap:11px;align-items:baseline;flex-wrap:wrap;
  padding-bottom:11px;border-bottom:1px solid var(--rule)}
.ansline .lab{font:700 10px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--veg);flex:none}
.ansline .val{font-size:18px;color:var(--ink)}
.ansline .ver{margin-left:auto;font:500 10px/1 var(--mono);letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink-3);border:1px solid var(--rule);
  border-radius:2px;padding:4px 6px;white-space:nowrap}
.ansline .ver.no{color:var(--ink-3)}
.ansline.right{border-bottom:0;padding-top:11px}
.ansline.right .lab{color:var(--veg)}
.ansline .ver.bad{color:var(--revise);border-color:var(--revise)}
/* the official answer stays visible and stays readable — you will meet it
   again on the real study guide — but it is marked as superseded. */
.ansline .val.struck{text-decoration:line-through;text-decoration-thickness:1px;
  text-decoration-color:var(--revise);color:var(--ink-3)}
.ansline .val.struck .katex{color:var(--ink-3)}
.steps{list-style:none;margin:13px 0 0;padding:0;counter-reset:st}
.steps li{position:relative;padding-left:27px;margin-top:9px;font-size:16.5px;
  line-height:1.6;color:var(--ink-2)}
.steps li::before{counter-increment:st;content:counter(st);position:absolute;left:0;top:2px;
  font:700 10px/16px var(--mono);width:16px;height:16px;text-align:center;
  border:1px solid var(--rule);border-radius:50%;color:var(--ink-3)}
.steps .katex{color:var(--ink)}
.trapl{margin-top:13px;font-size:15.5px;color:var(--ink-2)}
.trapl>span:first-child{font:700 10px/1 var(--mono);letter-spacing:.13em;
  text-transform:uppercase;color:var(--revise);margin-right:9px}
.trapl .katex{color:var(--ink)}
.fixl{margin-top:13px;padding:12px 14px;border:1px solid var(--revise);
  border-radius:2px;background:color-mix(in srgb,var(--revise) 8%,transparent);
  font-size:15.5px;color:var(--ink-2)}
.fixl>span:first-child{display:block;font:700 10px/1 var(--mono);letter-spacing:.13em;
  text-transform:uppercase;color:var(--revise);margin-bottom:7px}
.fixl .katex{color:var(--ink)}
.notel{margin-top:10px;font:400 13px/1.6 var(--mono);color:var(--ink-3)}

.katex-display{max-width:100%;overflow-x:auto;overflow-y:hidden;padding:2px 0 6px}
.katex-display::-webkit-scrollbar{height:5px}
.katex-display::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px}

footer.efoot{margin-top:56px;padding:24px 0 80px;border-top:1px solid var(--rule);
  font:400 13px/1.75 var(--mono);color:var(--ink-3)}
footer.efoot a{color:var(--contour)}

@media (max-width:760px){
  .wrap{padding:0 16px 90px}
  .sitenav{margin-left:16px}
  header.top{padding:38px 0 20px}
  .lh{margin-top:34px}
  .official{padding:4px 14px 14px}
  .prob{padding:17px 0 15px}
  .stem{font-size:17px}
  .steps li{font-size:16px}
}
"""

JS = r"""
(function(){
  "use strict";
  var KEY="ma261-exam1";
  var seen={};
  try{ seen=JSON.parse(localStorage.getItem(KEY)||"{}"); }catch(e){ seen={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(seen)); }catch(e){} }

  /* --- reveal ----------------------------------------------------------
     The answer is shut until you commit. That is the whole point: an answer
     you can see while thinking is an answer you will nod along with. */
  function open_(p, remember){
    p.querySelector(".work").hidden=false;
    p.classList.add("seen");
    var b=p.querySelector("[data-try]");
    if(b) b.textContent="Answer shown";
    if(remember!==false){ seen[p.id]=1; save(); tally(); }
  }
  document.querySelectorAll(".prob").forEach(function(p){
    var b=p.querySelector("[data-try]");
    if(b) b.addEventListener("click",function(){ open_(p); });
    if(seen[p.id]) open_(p,false);
  });

  function tally(){
    document.querySelectorAll(".lesson").forEach(function(L){
      var all=L.querySelectorAll(".prob"), n=0;
      all.forEach(function(p){ if(seen[p.id]) n++; });
      var el=L.querySelector("[data-done]");
      if(el) el.innerHTML="<b>"+n+"</b> / "+all.length+" worked";
    });
    var total=document.querySelectorAll(".prob").length, got=0;
    document.querySelectorAll(".prob").forEach(function(p){ if(seen[p.id]) got++; });
    var bar=document.getElementById("pbar");
    if(bar) bar.style.width=(100*got/total)+"%";
  }
  tally();

  document.querySelectorAll("[data-all]").forEach(function(b){
    b.addEventListener("click",function(){
      var L=b.closest(".lesson");
      L.querySelectorAll(".prob").forEach(function(p){ open_(p); });
    });
  });

  var reset=document.getElementById("resetall");
  if(reset) reset.addEventListener("click",function(){
    seen={}; save();
    document.querySelectorAll(".prob").forEach(function(p){
      p.querySelector(".work").hidden=true;
      p.classList.remove("seen");
      var b=p.querySelector("[data-try]");
      if(b) b.textContent="I tried it \u2014 show the work";
    });
    tally();
    window.scrollTo({top:0,behavior:"smooth"});
  });

  /* --- which lesson am I in -------------------------------------------- */
  var links=[].slice.call(document.querySelectorAll(".toc a"));
  var secs=links.map(function(a){ return document.querySelector(a.getAttribute("href")); });
  function mark(){
    var y=window.scrollY+120, idx=0;
    secs.forEach(function(s,i){ if(s && s.offsetTop<=y) idx=i; });
    links.forEach(function(a,i){ a.classList.toggle("on", i===idx); });
    var on=links[idx];
    if(on){
      var rail=document.querySelector(".toc-in");
      var want=on.offsetLeft-(rail.clientWidth-on.offsetWidth)/2;
      rail.scrollLeft=Math.max(0,Math.min(want,rail.scrollWidth-rail.clientWidth));
    }
  }
  window.addEventListener("scroll",mark,{passive:true});
  window.addEventListener("resize",mark);
  mark();

  /* --- days until the exam --------------------------------------------- */
  var el=document.getElementById("countdown");
  if(el){
    var d=new Date(el.dataset.date+"T18:30:00");
    var days=Math.ceil((d-new Date())/864e5);
    el.textContent = days>1 ? days+" days away"
                   : days===1 ? "tomorrow"
                   : days===0 ? "today" : "past";
  }
})();
"""


_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)


def B(text):
    """**bold** -> <b>bold</b>.

    The solution text is written in a light markdown, and a stray literal
    `**exists and equals 0**` shipped once. Run before M(): KaTeX would
    otherwise swallow the asterisks inside a $...$ span, and it never emits
    them itself, so there is nothing to collide with.
    """
    return _BOLD.sub(r"<b>\1</b>", text)


def _prob_html(M, p, sol, extra=False):
    """One problem: stem, a commit button, then the work."""
    steps = "\n".join(f"<li>{M(B(s))}</li>" for s in sol["steps"])
    # The badge describes the *official* answer printed beside it. Saying
    # "recomputed" next to an answer we go on to call wrong would be a lie in
    # the one place it matters most.
    if sol.get("fix"):
        verified = ('<span class="ver bad">checked \u00b7 official answer wrong</span>')
    elif sol.get("check"):
        verified = '<span class="ver">answer recomputed \u00b7 sympy</span>'
    else:
        verified = '<span class="ver no">prose answer \u00b7 not machine-checkable</span>'
    right = (f'<div class="ansline right"><span class="lab">Correct answer</span>'
             f'<span class="val">{M(sol["right"])}</span>'
             f'<span class="ver">recomputed \u00b7 sympy</span></div>'
             if sol.get("right") else "")
    fix = (f'<p class="fixl"><span>The official answer is wrong</span>'
           f'{M(B(sol["fix"]))}</p>' if sol.get("fix") else "")
    note = (f'<p class="notel">{sol["note"]}</p>' if sol.get("note") else "")
    tag = '<span class="tagx">restored</span>' if extra else ""
    return (
        f'<li class="prob" id="p-{p["pid"]}">\n'
        f'<div class="pn"><span class="num">{p["n"]}</span>{tag}</div>\n'
        f'<div class="stem">{M(p["stem"])}</div>\n'
        f'<div class="tryrow">'
        f'<button class="go" data-try>I tried it &mdash; show the work</button>'
        f'<span class="hintx">no calculator, same as the exam</span></div>\n'
        f'<div class="work" hidden>\n'
        f'<div class="ansline"><span class="lab">{"Official answer" if sol.get("fix") else "Answer"}</span>'
        f'<span class="val{" struck" if sol.get("fix") else ""}">{M(p["answer"])}</span>{verified}</div>\n{right}\n'
        f'<ol class="steps">{steps}</ol>\n'
        f'<p class="trapl"><span>Trap</span>{M(B(sol["trap"]))}</p>\n'
        f'{fix}{note}</div></li>'
    )


def coverage_gap(data):
    """Sections on Sharvil's Fall Midterm 1 that this Spring guide never covers.

    The guide is msunkula's Spring 2026 section. It is authoritative for the
    *material*, and it is not his calendar: his exam is Mon Oct 5, Mummert's
    Fall section. The lesson->section split also differs slightly, and the one
    difference that costs marks is Lesson 2 — Fall reaches back to 12.1
    (parametric curves in the plane) before 13.5, and the Spring guide has no
    12.1 section at all.

    Computed rather than asserted, so if either calendar changes the warning
    follows instead of going quietly stale.
    """
    covered = set()
    for sec in data["sections"]:
        label = sec["secs_label"]
        # "13.1-13.4" is a range and means 13.1, 13.2, 13.3, 13.4
        for ch, lo, hi in re.findall(r"(\d+)\.(\d+)\s*[-\u2013]\s*\d+\.(\d+)", label):
            for n in range(int(lo), int(hi) + 1):
                covered.add(f"{ch}.{n}")
        # and any bare section number, range endpoints included
        covered.update(re.findall(r"\d+\.\d+", label))

    m1 = next(s for s in course.STOPS if s["id"] == "m1")
    missing = []
    for ln in m1["lessons"]:
        if ln not in course.LESSONS:
            continue
        for tok in re.findall(r"\d+\.\d+", course.LESSONS[ln][0]):
            if tok not in covered and tok not in [m[0] for m in missing]:
                missing.append((tok, ln))
    return missing


def build(M, MM):
    data = exam1_src.read()
    checked, prose = exam1_sol.verify()
    # verify() proves our steps reach our own value. gate() proves that value
    # still matches what the instructor printed, so a mis-transcribed answer
    # cannot ship looking verified.
    agreed, disagreed, _ = exam1_audit.gate()
    gaps = coverage_gap(data)

    # every piece of TeX on the page, primed in one node call
    texts = []
    for s in data["sections"]:
        texts.append(s["notes_html"])
        for p in s["problems"]:
            texts += [p["stem"], p["answer"]]
            sol = exam1_sol.SOL.get(p["pid"])
            if sol is None:
                sys.exit(f"exam1page: no worked solution for {p['pid']} "
                         f"({p['stem'][:60]}...)")
            texts += sol["steps"] + [sol["trap"]]
            for extra_key in ("fix", "right"):
                if sol.get(extra_key):
                    texts.append(sol[extra_key])
    for e in exam1_sol.EXTRA:
        texts += [e["stem"], e["answer"], e["trap"]] + e["steps"]
    MM(*texts)

    n_problems = data["total"] + len(exam1_sol.EXTRA)

    toc, blocks = [], []
    for i, s in enumerate(data["sections"], 1):
        extras = [e for e in exam1_sol.EXTRA if e["lesson"] == s["key"]]

        toc.append(f'<a href="#{s["id"]}"><i>{i:02d}</i>{s["title"]}</a>')

        items = []
        for p in s["problems"]:
            items.append(_prob_html(M, p, exam1_sol.SOL[p["pid"]]))
            for e in extras:
                if e.get("after") == p["n"]:
                    items.append(_prob_html(
                        M, dict(pid=e["pid"], n=f'{p["n"]}\u2032',
                                stem=e["stem"], answer=e["answer"]),
                        e, extra=True))

        gid = s["guide_ids"][0]
        chips = " &middot; ".join(f"&sect;{GUIDE_LABEL.get(g, g)}"
                                  for g in dict.fromkeys(s["guide_ids"]))
        n = len(s["problems"]) + len(extras)

        blocks.append(
            f'<section class="lesson" id="{s["id"]}">\n'
            f'<div class="lh"><span class="n">{i:02d}</span>'
            f'<h2>{s["title"]}</h2>'
            f'<span class="x">{s["lesson_label"]} &middot; &sect;{s["secs_label"].lstrip("§")}</span></div>\n'
            f'<a class="lgo" href="/guide.html#{gid}">'
            f'Don\'t know this yet? {chips} in the full guide &rarr;</a>\n'
            f'<div class="official"><span class="tag">'
            f'From the official study guide</span>\n{M(s["notes_html"])}\n</div>\n'
            f'<div class="ph2"><h3>Practice</h3><span>{n} problems</span>'
            f'<span class="done" data-done></span></div>\n'
            f'<div class="tryrow"><button data-all>Show all the work in this lesson</button></div>\n'
            f'<ol class="probs">\n' + "\n".join(items) + "\n</ol>\n</section>"
        )

    m1 = next(s for s in course.STOPS if s["id"] == "m1")

    # The guide is a different section of the same course, so its coverage can
    # drift from the one Sharvil is actually sitting. Say so where it costs
    # marks, with the gap computed from both calendars rather than asserted.
    if gaps:
        items = "".join(
            f'<li><b>&sect;{tok}</b> &mdash; on Fall Lesson {ln}, and this guide '
            f'has no section for it. '
            f'<a href="/guide.html#s121">Read &sect;{tok} in the full guide &rarr;</a></li>'
            for tok, ln in gaps)
        gapbox = (
            '<div class="gapbox"><b>This guide is the Spring section\u2019s, and it '
            'is missing one thing your exam covers.</b>'
            '<p>Everything below is the source of truth for the material. But the '
            'Fall lesson split is not identical to the Spring one, and the '
            'difference is examinable:</p>'
            f'<ul>{items}</ul>'
            '<p>The date printed on the official guide is the Spring exam. '
            f'Yours is <b>{m1["when"]}</b>.</p></div>')
    else:
        gapbox = ""

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Exam 1 study guide, worked &middot; MA 261</title>
<meta name="description" content="Purdue's official MA 261 Exam 1 study guide with every one of its {n_problems} practice problems worked out, {checked} answers recomputed with sympy, and two published answers corrected.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Exam 1 study guide, worked &middot; MA 261">
<meta property="og:description" content="The official study guide, with the work filled in and the answers verified.">
<meta property="og:type" content="website">
{FONTS}
<link rel="stylesheet" href="/katex.css">
<style>{CSS}</style>
</head>
<body>
<a class="sitenav" href="/">&larr; Semester map</a>
<div class="prog"><i id="pbar"></i></div>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Purdue MA 26100 &middot; official Exam 1 study guide</p>
  <h1>Exam 1, <em>worked.</em></h1>
  <p class="sub">The department's own study guide is the source of truth for what
  Exam&nbsp;1 covers, and it gives you a bare answer under each problem with no work
  in between. This is that guide, section for section and problem for problem
  &mdash; with the work filled in, the traps named, and the answer kept shut until
  you commit to an attempt. All {data["total"]} of its live problems, plus one it
  leaves commented out.</p>

  <div class="facts">
    <div class="fact"><b>Coverage</b><span>{data["coverage"]}</span></div>
    <div class="fact"><b>Official exam date</b><span>{data["exam_date"]}</span></div>
    <div class="fact"><b>Your exam</b><span>{m1["when"]}<br>
      <span id="countdown" data-date="{m1["date"]}"></span></span></div>
    <div class="fact"><b>Answers verified</b><span>{checked} of {n_problems} recomputed<br>{agreed} also re-read from the official page</span></div>
  </div>

  <p class="srcline">Source of truth:
  <a href="{exam1_src.SOURCE_URL}" target="_blank" rel="noopener">the official
  Exam&nbsp;1 study guide</a>, read {exam1_src.VERIFIED}. Every section heading,
  formula box and problem statement below is the instructor's, unedited.
  The worked steps, trap notes and corrections are mine.
  <a href="#lesson10">Two of the published answers are wrong</a> &mdash; the page
  shows the official answer and the correction side by side.
  &nbsp;&middot;&nbsp; <a href="#" id="resetall">Reset my progress</a></p>
</header>

{gapbox}

<nav class="toc" aria-label="Lessons"><div class="toc-in">{"".join(toc)}</div></nav>

{"".join(blocks)}

<footer class="efoot">
  Structure, prose and problems from the official
  <a href="{exam1_src.SOURCE_URL}" target="_blank" rel="noopener">MA&nbsp;261 Exam&nbsp;1
  study guide</a> (Spring 2026), read {exam1_src.VERIFIED}. Your own exam date and
  room come from Brightspace &mdash; the date printed on that page is the Spring
  section's.<br>
  Worked solutions are mine; {checked} of the {n_problems} answers are recomputed
  with sympy at build time and the build refuses to publish on a mismatch. A
  second gate re-reads {agreed} answers straight out of the official page and
  compares them to what was computed, so an answer mis-transcribed from the
  guide cannot ship looking verified. The two corrected answers are not among
  those {agreed}: the guide states them in words ("limit does not exist"), which
  no parser should pretend to read, so they were derived and checked by hand
  and are shown struck through with the correction beside them.
  The remaining {prose} are prose (&ldquo;elliptic cone with axis along the <i>z</i>-axis&rdquo;) and are
  checked by hand.<br>
  <a href="/guide.html">Read the full guide &rarr;</a> &nbsp;&middot;&nbsp;
  <a href="/quiz.html#m1">Practise Midterm 1 by section &rarr;</a><br>
  Not affiliated with or endorsed by Purdue University.
</footer>
</div>

<script>{JS}</script>
</body>
</html>
"""
    (ROOT / "exam1.html").write_text(html, encoding="utf-8")
    return dict(problems=n_problems, checked=checked, prose=prose,
                sections=len(data["sections"]), gaps=gaps,
                agreed=agreed, disagreed=disagreed)
