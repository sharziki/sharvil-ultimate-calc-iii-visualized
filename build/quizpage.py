"""quiz.html — "study by quiz".

Each tab singles out only the sections that quiz covers, in full (figures,
algorithms, traps, check-yourself questions — the real guide content, not a
summary), then the questions on exactly those sections.

The guide's stylesheet, SVG marker defs and both scripts are carried over
verbatim so the 3-D scenes and the dot-product dial keep working. The scene
booter is patched to run per-pane, because a canvas inside a hidden tab has
zero size and would render blank.
"""
import re
import sys
from pathlib import Path

import course
import guide_121

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


# ------------------------------------------------------ guide extraction ----

def guide_parts(M):
    """Pull the reusable pieces out of the untouched guide source."""
    h = (HERE / "guide.src.html").read_text(encoding="utf-8")

    # Every <style> block, in document order — the guide has three, and the
    # last one holds all the 3-D viewer rules. Missing it lets the canvases
    # size themselves from their own width/height attributes, which feeds back
    # into layout and blows them up to the 33-million-pixel canvas limit.
    css = "\n".join(re.findall(r"<style>(.*?)</style>", h, re.S))
    if ".viz canvas" not in css:
        sys.exit("quizpage: viewer CSS missing — guide stylesheets changed")

    m = re.search(r'<svg width="0" height="0"[^>]*>.*?</svg>', h, re.S)
    if not m:
        sys.exit("quizpage: marker defs not found")
    defs = m.group(0)

    scripts = re.findall(r"<script>(.*?)</script>", h, re.S)
    if len(scripts) != 2:
        sys.exit(f"quizpage: expected 2 guide scripts, found {len(scripts)}")

    sections = {}
    for m in re.finditer(r'<article class="sec" id="(s[0-9a-z]+)">(.*?)</article>',
                         h, re.S):
        sections[m.group(1)] = m.group(0)
    if len(sections) < 39:
        sys.exit(f"quizpage: only {len(sections)} sections extracted")

    # 12.1 exists only in the generated section, never in the source.
    sections["s121"] = guide_121.html(M).strip()
    return dict(css=css, defs=defs, s1=scripts[0], s2=scripts[1], sections=sections)


BOOT_OLD = """function boot(){
  document.querySelectorAll('.viz[data-scene]').forEach(function(el){
    var d = SCENES[el.getAttribute('data-scene')];
    if (d) { try { Scene(el, d); } catch(e){} }
  });"""

BOOT_NEW = """function boot(root){
  /* At load there is no root: just publish the booter and stop. Every canvas
     is inside a hidden tab and would measure 0x0, so nothing can be built yet.
     show() calls this again with the pane it just revealed. */
  window.__bootViz = boot;
  if (!root) return;
  root.querySelectorAll('.viz[data-scene]').forEach(function(el){
    if (el.dataset.booted) return;
    var d = SCENES[el.getAttribute('data-scene')];
    if (d) { try { Scene(el, d); el.dataset.booted='1'; } catch(e){} }
  });
  return;
  /* the guide's reveal observer is unreachable below: elements in a hidden
     pane never intersect, so they would stay at opacity 0 forever. */"""


def patch_viz(script):
    """Boot scenes on demand, per pane, and drop the reveal animation.

    A tab's canvases have no size until the tab is shown, so Scene() must run
    then, not at load. The reveal observer is dropped outright: elements in a
    hidden pane never intersect, so they would stay at opacity 0 forever.
    """
    if BOOT_OLD not in script:
        sys.exit("quizpage: viz boot() not found — the guide script changed")
    return script.replace(BOOT_OLD, BOOT_NEW, 1)


# ------------------------------------------------------------------ page ----

PAGE_CSS = """
/* quiz.html additions — the guide stylesheet above does the section work.
   These rules come after it on purpose, so they win. */
body{overflow-x:hidden}
/* the guide pins its back-link to the top-left corner, where it would sit on
   top of this page's sticky tab bar; put it back in the flow instead */
.sitenav{position:static;display:inline-block;margin:14px 0 0 32px}
/* clear the sticky tab bar when jumping to a section */
.sec{scroll-margin-top:96px}
.wrap{position:relative;z-index:1;max-width:1180px;margin:0 auto;padding:0 32px}
header.top{padding:56px 0 26px;border-bottom:2px solid var(--ink)}
header.top h1{font-size:clamp(36px,6.4vw,60px);font-weight:800;line-height:.94;
  letter-spacing:-.035em;margin-top:14px}
header.top h1 em{font-family:var(--body);font-style:italic;font-weight:300;color:var(--contour)}
header.top .sub{margin-top:16px;font-size:18.5px;color:var(--ink-2);max-width:62ch}
/* --- the picker ------------------------------------------------------- */
.picker{position:sticky;top:0;z-index:30;margin-top:22px;padding:12px 0 13px;
  background:var(--paper);border-bottom:1px solid var(--rule)}
.picker-h{display:flex;align-items:baseline;gap:12px;padding-bottom:10px}
.picker-h span{font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3)}
.picker-h em{font:500 10px/1 var(--mono);font-style:normal;letter-spacing:.1em;
  text-transform:uppercase;color:var(--contour);margin-left:auto}
.tabs{display:flex;gap:6px;flex-wrap:wrap;align-items:stretch}
.tabs button{flex:0 0 auto;display:flex;flex-direction:column;justify-content:center;
  align-items:flex-start;gap:5px;text-align:left;cursor:pointer;
  background:var(--card);color:var(--ink-2);border:1px solid var(--rule);
  border-radius:3px;padding:9px 12px 8px;transition:border-color .15s,background .15s}
.tabs button b{font:700 13px/1 var(--disp);letter-spacing:-.01em;color:var(--ink)}
.tabs button i{font:500 9.5px/1 var(--mono);font-style:normal;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-3);white-space:nowrap}
.tabs button:hover{border-color:var(--ink-3)}
/* "exam", not "ex" — the guide's stylesheet is loaded above and styles .ex
   as its worked-example block, whose padding silently resized these tabs.
   Accent is drawn inside the box so exam tabs stay exactly the same size. */
.tabs button.exam{box-shadow:inset 0 -2px 0 var(--water)}
.tabs button.exam b{color:var(--water)}
.tabs button.on,.tabs button.on b,.tabs button.on i{color:var(--paper)}
.tabs button.on{background:var(--contour);border-color:var(--contour);box-shadow:none}
.tabs button.on i{opacity:.8}
.tabs button.exam.on{background:var(--water);border-color:var(--water)}
.tabs button.next::after{content:"";width:6px;height:6px;border-radius:50%;
  background:var(--contour);position:absolute;top:-3px;right:-3px}
.tabs button.next{position:relative}
.tabs button.on.next::after{display:none}
.pksel{display:none;flex-direction:column;gap:7px}
.pksel span{font:700 10px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;
  color:var(--ink-3)}
.pksel select{width:100%;font:600 15px/1.2 var(--disp);color:var(--ink);
  background:var(--card);border:1px solid var(--rule);border-radius:3px;
  padding:13px 12px;-webkit-appearance:none;appearance:none;
  background-image:linear-gradient(45deg,transparent 50%,var(--ink-3) 50%),
                   linear-gradient(135deg,var(--ink-3) 50%,transparent 50%);
  background-position:calc(100% - 19px) 50%,calc(100% - 13px) 50%;
  background-size:6px 6px,6px 6px;background-repeat:no-repeat}
.pane{padding-bottom:140px}
.phd{padding:34px 0 0;max-width:74ch}
.pwhen{font:500 11px/1.6 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--contour)}
.ph{font-size:clamp(32px,5vw,46px);font-weight:800;letter-spacing:-.03em;margin-top:10px;line-height:1}
.pn{margin-top:14px;font-size:19px;line-height:1.5;color:var(--ink-2)}
.pnote{margin-top:18px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--revise);border-radius:2px;padding:14px 17px;
  font-size:16px;line-height:1.55;color:var(--ink-2)}
.pnote b{color:var(--ink)}
.step-h{margin-top:52px;display:flex;align-items:baseline;gap:14px;
  border-top:2px solid var(--ink);padding-top:18px}
.step-h .n{font:700 12px/1 var(--mono);letter-spacing:.14em;color:var(--contour);flex:none}
.step-h h2{font-size:clamp(26px,3.6vw,36px);font-weight:800;letter-spacing:-.026em;line-height:1;flex:1 1 auto}
.step-h .x{font:500 10.5px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);border:1px solid var(--rule);border-radius:2px;padding:5px 8px;white-space:nowrap}
.step-note{margin-top:14px;font-size:17px;color:var(--ink-2);max-width:64ch}
.step-note b{color:var(--ink);font-weight:500}
.topics{max-width:820px}
.topics .sec:first-child{border-top:0}
.seclink{font:500 11px/1 var(--mono);text-decoration:none;color:var(--ink-3);
  border:1px solid var(--rule);border-radius:2px;padding:5px 7px;margin-left:auto;
  align-self:center;white-space:nowrap}
.seclink:hover{color:var(--contour);border-color:var(--contour)}
.half{margin-top:10px;font:500 12.5px/1.5 var(--mono);color:var(--revise)}
/* questions */
.bar{position:sticky;top:62px;z-index:6;display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  background:var(--paper-2);border:1px solid var(--rule);border-radius:3px;padding:11px 14px;margin-top:22px}
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
.qs{list-style:none;margin:0;padding:0;max-width:900px}
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
  border-left:3px solid var(--water);border-radius:2px;padding:14px 17px;max-width:820px}
.solh{font:700 11px/1 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--water)}
.solh b{color:var(--ink);font-size:14px}
.solb{margin-top:10px;font-size:16.5px;line-height:1.65;color:var(--ink-2)}
.solb p+p{margin-top:7px}
.solb .katex{color:var(--ink)}
.trapl{margin-top:11px;font-size:15.5px;color:var(--ink-2)}
/* first-child only — trap text may contain KaTeX, whose root is also a direct
   <span> child and must not inherit the label's mono/uppercase rules. */
.trapl>span:first-child{font:700 10px/1 var(--mono);letter-spacing:.13em;
  text-transform:uppercase;color:var(--revise);margin-right:9px}
.trapl .katex{color:var(--ink)}
.review{margin-top:8px;font:500 13px/1 var(--mono)}
.review a{color:var(--contour)}
footer.qfoot{margin-top:20px;padding:22px 0 90px;border-top:1px solid var(--rule);
  font:400 13px/1.7 var(--mono);color:var(--ink-3)}
footer.qfoot a{color:var(--contour)}

/* Wide typeset maths (aligned blocks, determinants, long chains) must scroll
   inside its own box — otherwise it drags the whole page sideways on a phone. */
.katex-display{max-width:100%;overflow-x:auto;overflow-y:hidden;padding:2px 0 6px}
.mathd,.solb,.stem,.ans,.qt,.opts .ot,.step p,.trapl{max-width:100%}
.mathd{overflow-x:auto}
.katex-display::-webkit-scrollbar{height:5px}
.katex-display::-webkit-scrollbar-thumb{background:var(--rule);border-radius:3px}

/* --- responsive ------------------------------------------------------- */
@media (max-width:1000px){
  .wrap{padding:0 20px}
  .topics{max-width:none}
}
@media (max-width:760px){
  /* 13 tabs is a lot of thumb; hand the phone a native picker instead */
  .tabs{display:none}
  .pksel{display:flex}
  .picker-h{display:none}
  .picker{padding:10px 0}
  .wrap{padding:0 16px}
  .phd{padding-top:26px}
  .step-h{margin-top:38px;flex-wrap:wrap;gap:6px 12px}
  .step-h .x{margin-left:auto}
  .step-note,.pn{font-size:16px}
  .bar{position:static}
  .opts{grid-template-columns:1fr}
  .sec-h{gap:8px}
  .seclink{margin-left:0;order:3;flex-basis:100%}
  .sol{padding:13px 14px}
  .qs,.sol{max-width:none}
}
@media (max-width:430px){
  .wrap{padding:0 13px}
  .pksel span{display:none}
  .pksel select{padding:11px 10px;font-size:14px}
  .ph{font-size:30px}
  header.top{padding:40px 0 20px}
  .stem{font-size:17px}
  .opts label{padding:10px 8px}
}
"""

PAGE_JS = r"""
(function(){
  "use strict";
  var KEY="calc3-quiz-f26";
  var state={};
  try{ state=JSON.parse(localStorage.getItem(KEY)||"{}"); }catch(e){ state={}; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(state)); }catch(e){} }

  var tabs=[].slice.call(document.querySelectorAll(".tabs button"));
  var sel=document.getElementById("pksel");

  /* whichever stop is next by date — marked on the tab and named above it */
  var today=new Date(); today.setHours(0,0,0,0);
  var nextId=null;
  for(var i=0;i<tabs.length;i++){
    if(new Date(tabs[i].dataset.date+"T00:00:00")>=today){ nextId=tabs[i].dataset.tab; break; }
  }
  if(nextId){
    tabs.forEach(function(b){ b.classList.toggle("next", b.dataset.tab===nextId); });
    var lab=[].slice.call(tabs).filter(function(b){return b.dataset.tab===nextId;})[0];
    var note=document.getElementById("nextnote");
    if(note && lab) note.textContent="next up · "+lab.querySelector("b").textContent;
  }

  function show(id){
    tabs.forEach(function(b){ b.classList.toggle("on", b.dataset.tab===id); });
    if(sel) sel.value=id;
    var pane=null;
    document.querySelectorAll(".pane").forEach(function(p){
      p.hidden = p.id!=="pane-"+id;
      if(!p.hidden) pane=p;
    });
    /* canvases have no size until the pane is visible, so boot scenes now */
    if(pane && window.__bootViz) window.__bootViz(pane);
    try{ history.replaceState(null,"","#"+id); }catch(e){}
  }
  tabs.forEach(function(b){ b.addEventListener("click",function(){ show(b.dataset.tab); window.scrollTo({top:0}); }); });
  if(sel) sel.addEventListener("change",function(){ show(sel.value); window.scrollTo({top:0}); });
  var want=(location.hash||"").replace("#","");
  show(tabs.some(function(b){return b.dataset.tab===want;}) ? want : (nextId||"@@FIRST@@"));

  /* The viz script registers its booter on DOMContentLoaded, which fires after
     this file runs — so the first pane's scenes need a second pass. */
  function bootVisible(){
    var p=document.querySelector(".pane:not([hidden])");
    if(p && window.__bootViz) window.__bootViz(p);
  }
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",bootVisible);
  else bootVisible();

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
      pane.querySelector(".bar").scrollIntoView({behavior:"smooth",block:"start"});
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
        ? "Read the worked solution under everything you missed, then scroll back up to that section and redo its check-yourself questions."
        : "Clean sweep. Read a couple of the solutions anyway — the trap notes are where the marks actually go.")+"</p>"+
      (list? "<p class=\"miss\">Sections to reread: <b>"+list+"</b></p>":"");
    box.scrollIntoView({behavior:"smooth",block:"center"});
  }
})();
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Archivo:wght@500;600;700;800&family=Newsreader:ital,opsz,wght@'
         '0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,400&'
         'family=JetBrains+Mono:wght@400;500;700&display=swap">')

# Sections whose guide article covers more than this quiz does.
PARTIAL = {
    ("q1", "s135"): "Quiz 1 covers the <b>lines</b> half of 13.5 only. "
                    "Planes are Lesson 3, on Quiz 2.",
    ("q2", "s135"): "Quiz 2 covers the <b>planes</b> half of 13.5. "
                    "Lines were Lesson 2, on Quiz 1.",
    ("q4", "s144"): "Lesson 8 runs 14.4 and 14.5 <b>as far as Theorem 14.5</b>. "
                    "The later part of 14.5 is not on this quiz.",
    ("q3", "s143"): "Quiz 3 covers <b>14.3 only</b> — velocity, acceleration, "
                    "circular and projectile motion. The T, N, B frame and the "
                    "components of acceleration are 14.5, on Quiz 4 and later.",
}


def section_html(parts, sid, stop_id):
    """One guide section, re-headed for use inside a quiz tab."""
    raw = parts["sections"].get(sid)
    if raw is None:
        sys.exit(f"quizpage: no guide section {sid}")

    # unique ids per page: 13.5 appears under both Quiz 1 and Quiz 2
    html = raw.replace(f'id="{sid}"', f'id="{stop_id}-{sid}"', 1)

    # swap the guide's trailing "not on the lesson plan" chip for a deep link
    link = (f'<a class="seclink" href="/guide.html#{sid}">'
            f'open in the full guide &rarr;</a>')
    html = re.sub(r'(<div class="sec-h">.*?</h3>)(.*?)(</div>)',
                  lambda m: m.group(1) + link + m.group(3), html, count=1, flags=re.S)

    note = PARTIAL.get((stop_id, sid))
    if note:
        html = html.replace('</div>', f'</div>\n    <p class="half">{note}</p>', 1)
    return html


def build(buckets, M, sid_label, coverage_chips):
    parts = guide_parts(M)
    tabs, panes, options = [], [], []

    for s in course.STOPS:
        qs = list(buckets[s["id"]])
        qs.sort(key=lambda q: (q["tag"], q["id"]))
        sids = coverage_chips(s)

        cls = "exam" if s["kind"] == "exam" else ""
        short = s["when"].split(" \u00b7 ")[0]
        tabs.append(
            f'<button data-tab="{s["id"]}" class="{cls}" data-date="{s["date"]}">'
            f'<b>{s["label"]}</b><i>{short}</i></button>')
        options.append(
            f'<option value="{s["id"]}" data-date="{s["date"]}">'
            f'{s["label"]} &middot; {short} &middot; {s["secs_label"]}</option>')

        lessons = (", ".join(str(l) for l in s["lessons"]) if len(s["lessons"]) <= 6
                   else f'{s["lessons"][0]}&ndash;{s["lessons"][-1]}')
        head = (
            f'<div class="phd">'
            f'<p class="pwhen">{s["when"]} &middot; Lessons {lessons} '
            f'&middot; {s["secs_label"]}</p>'
            f'<h2 class="ph">{s["label"]}</h2>'
            f'<p class="pn">{s["blurb"]}</p>'
        )
        if s.get("extra"):
            head += f'<div class="pnote"><b>Worth knowing.</b> {s["extra"]}</div>'
        if s["kind"] == "exam":
            head += ('<div class="pnote">Only the sections <b>no quiz ever covers</b> '
                     'are shown here. Everything from the earlier quizzes is on this '
                     'exam too &mdash; work those tabs as well.</div>')
        head += "</div>"

        n_sec = len(sids)
        what = "section" if n_sec == 1 else "sections"
        topics = "\n".join(section_html(parts, sid, s["id"]) for sid in sids)
        chips = " &middot; ".join(f"&sect;{sid_label.get(sid, sid)}" for sid in sids)

        items = []
        for n, q in enumerate(qs, 1):
            html = q["html"]
            html = (html.replace('<span class="qn">@@N@@</span>',
                                 f'<span class="qn">{n}</span>')
                    if "@@N@@" in html else
                    re.sub(r'<span class="qn">\d+</span>',
                           f'<span class="qn">{n}</span>', html, count=1))
            items.append(html)

        panes.append(
            f'<section class="pane" id="pane-{s["id"]}" hidden>\n{head}\n'
            f'<div class="step-h"><span class="n">STEP 01</span>'
            f'<h2>The material</h2><span class="x">{n_sec} {what}</span></div>\n'
            f'<p class="step-note">{chips} &mdash; and nothing else. '
            f'Read them, then do the check-yourself questions inside each one '
            f'with the answer folded away.</p>\n'
            f'<div class="topics">{topics}</div>\n'
            f'<div class="step-h"><span class="n">STEP 02</span>'
            f'<h2>The questions</h2><span class="x">{len(qs)} questions</span></div>\n'
            f'<p class="step-note">On those sections only. Untimed, '
            f'<b>no calculator</b> &mdash; the quiz doesn\'t allow one either.</p>\n'
            f'<div class="bar">'
            f'<button class="submit" data-submit>Check answers</button>'
            f'<button data-reset>Reset</button>'
            f'<span class="bstat"><span data-answered>0</span>/{len(qs)} answered</span>'
            f'</div>\n'
            f'<div class="result" data-result hidden></div>\n'
            f'<ol class="qs">\n' + "\n".join(items) + "\n</ol>\n</section>"
        )

    total = sum(len(buckets[s["id"]]) for s in course.STOPS)
    js = PAGE_JS.replace("@@FIRST@@", course.STOPS[0]["id"])

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Study by quiz &middot; MA 26100 Fall 2026</title>
<meta name="description" content="Pick a quiz and get only the sections it covers, in full, followed by {total} verified questions on exactly those sections.">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="Study by quiz &middot; MA 26100 Fall 2026">
<meta property="og:description" content="Only the sections your next quiz covers, in full, followed by questions on exactly those sections.">
<meta property="og:type" content="website">
{FONTS}
</head>
<body>
<a class="sitenav" href="/">&larr; Semester map</a>
<link rel="stylesheet" href="/katex.css">
<style>{parts["css"]}{PAGE_CSS}</style>
{parts["defs"]}

<div class="wrap">
<header class="top">
  <p class="eyebrow">Purdue MA 26100 &middot; Fall 2026</p>
  <h1>Study <em>by quiz.</em></h1>
  <p class="sub">Pick the one you are sitting. You get the sections it covers and
  nothing else &mdash; the full guide material, figures and all &mdash; then questions
  on exactly those sections. Coverage follows the department's own Fall&nbsp;2026
  lesson calendar.</p>
</header>

<div class="picker">
  <div class="picker-h"><span>Pick a quiz</span><em id="nextnote"></em></div>
  <div class="tabs" role="tablist">{"".join(tabs)}</div>
  <label class="pksel"><span>Studying for</span>
    <select id="pksel">{"".join(options)}</select></label>
</div>
{"".join(panes)}

<footer class="qfoot">
  Coverage from the official
  <a href="{course.SCHED_PDF}" target="_blank" rel="noopener">MA&nbsp;261 F26 calendar</a>
  and <a href="{course.RULES_PDF}" target="_blank" rel="noopener">ground rules</a>,
  read {course.VERIFIED}. Confirm your own section in Brightspace.<br>
  Questions are <b>original</b> and every answer was recomputed with sympy, not
  asserted &mdash; they are not past Purdue questions.
  <a href="/guide.html">Study all the material instead &rarr;</a><br>
  Not affiliated with or endorsed by Purdue University.
</footer>
</div>

<script>{parts["s1"]}</script>
<script>{patch_viz(parts["s2"])}</script>
<script>{js}</script>
</body>
</html>
"""
    (ROOT / "quiz.html").write_text(html, encoding="utf-8")
    return total
