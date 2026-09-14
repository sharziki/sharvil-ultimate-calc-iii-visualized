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
import drill
import guide_121
import guide_136

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

    # 13.6 in the source teaches only the quadrics; Lesson 3 is "13.6 (to Ex 2)",
    # which in Briggs is the cylinder half. Add it, plus completing the square.
    sections["s136"] = guide_136.augment(sections["s136"], M)
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
/* --- the picker -------------------------------------------------------
   A single-row rail with one sliding indicator, which condenses to a slim bar
   once it sticks. Mechanics ported from 21st.dev "Animated Tabs" (sliding
   indicator + roving tabindex + arrow-key nav) and "Sticky Header" (condense
   on scroll); both are React, so this is a hand-written vanilla equivalent. */
.picker{position:sticky;top:0;z-index:30;margin-top:22px;
  background:var(--paper);border-bottom:1px solid var(--rule);
  transition:box-shadow .3s ease,padding .28s cubic-bezier(.22,1,.36,1);
  padding:12px 0 10px}
.picker.stuck{box-shadow:0 10px 24px -22px rgba(0,0,0,.95);padding:6px 0 4px}
/* grid-template-rows 1fr -> 0fr is the one way to animate a row to nothing */
.picker-h{display:grid;grid-template-rows:1fr;
  transition:grid-template-rows .3s cubic-bezier(.22,1,.36,1),opacity .2s ease}
.picker.stuck .picker-h{grid-template-rows:0fr;opacity:0}
/* min-height:0 zeroes the content box but not the padding, so the row
   would stay 9px tall; collapse the padding on the same curve. */
.picker.stuck .picker-h>div{padding-bottom:0}
.picker-h>div{overflow:hidden;min-height:0;display:flex;align-items:baseline;
  gap:12px;padding-bottom:9px;transition:padding-bottom .3s cubic-bezier(.22,1,.36,1)}
.picker-h span{font:700 10px/1 var(--mono);letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-3)}
.picker-h em{font:500 10px/1 var(--mono);font-style:normal;letter-spacing:.1em;
  text-transform:uppercase;color:var(--contour);margin-left:auto;white-space:nowrap}

.qrail{position:relative}
/* "qrail", not "rail" — the guide's stylesheet owns .rail for its sidebar,
   whose padding:40px 0 would add 80px of dead space here.
   Edge fades, so a half-scrolled tab reads as "there is more". */
.qrail::before,.qrail::after{content:"";position:absolute;top:0;bottom:0;width:34px;
  pointer-events:none;z-index:3;opacity:0;transition:opacity .2s ease}
.qrail::before{left:0;background:linear-gradient(to right,var(--paper),transparent)}
.qrail::after{right:0;background:linear-gradient(to left,var(--paper),transparent)}
.qrail.at-start::after,.qrail.mid::before,.qrail.mid::after,.qrail.at-end::before{opacity:1}

.tabs{display:flex;gap:2px;position:relative;overflow-x:auto;overflow-y:hidden;
  scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth;
  padding:4px 0;margin:-4px 0}
.tabs::-webkit-scrollbar{display:none}
.tabs button{flex:0 0 auto;position:relative;z-index:1;cursor:pointer;
  display:flex;flex-direction:column;align-items:flex-start;justify-content:center;
  gap:5px;text-align:left;background:none;border:0;border-radius:4px;
  padding:9px 14px;color:var(--ink-2);
  transition:color .18s ease,padding .28s cubic-bezier(.22,1,.36,1)}
.tabs button b{font:700 13px/1 var(--disp);letter-spacing:-.01em;color:var(--ink);
  white-space:nowrap;transition:color .18s ease}
.tabs button i{font:500 9.5px/1 var(--mono);font-style:normal;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-3);white-space:nowrap;
  max-height:12px;opacity:1;overflow:hidden;
  transition:max-height .28s cubic-bezier(.22,1,.36,1),opacity .16s ease,color .18s ease}
.picker.stuck .tabs button{padding:7px 13px}
.picker.stuck .tabs button i{max-height:0;opacity:0}
.tabs button:hover b{color:var(--contour)}
.tabs button.exam:hover b{color:var(--water)}
/* an exam reads blue until it is selected, when the pill carries the colour.
   This pair must sit ABOVE the selected rules: equal specificity, source wins. */
.tabs button.exam b{color:var(--water)}
.tabs button[aria-selected="true"] b,
.tabs button[aria-selected="true"] i,
.tabs button.exam[aria-selected="true"] b{color:var(--paper)}
.tabs button[aria-selected="true"] i{opacity:.75}
.tabs button:focus-visible{outline:2px solid var(--revise);outline-offset:1px}
.tabs button.exam::after{content:"";position:absolute;left:14px;right:14px;bottom:3px;
  height:2px;background:var(--water);border-radius:2px;opacity:.55}
.tabs button.exam[aria-selected="true"]::after{opacity:0}
.tabs button.next .tdot{position:absolute;top:5px;right:7px;width:5px;height:5px;
  border-radius:50%;background:var(--contour);box-shadow:0 0 0 3px var(--paper)}
.tabs button[aria-selected="true"] .tdot{display:none}

/* the one indicator that slides between tabs */
.tabind{position:absolute;z-index:0;left:0;top:4px;height:calc(100% - 8px);
  width:var(--w,0px);transform:translateX(var(--x,0px));
  background:var(--contour);border-radius:4px;opacity:0;
  transition:transform .34s cubic-bezier(.22,1,.36,1),
             width .34s cubic-bezier(.22,1,.36,1),
             background-color .22s ease,opacity .18s ease}
.tabind.ready{opacity:1}
.tabind.is-exam{background:var(--water)}
@media (prefers-reduced-motion:reduce){
  .tabind,.picker,.picker-h,.tabs button,.tabs button i{transition:none}
  .tabs{scroll-behavior:auto}
}

.pane{padding-bottom:140px}
.phd{padding:34px 0 0;max-width:74ch}
.pwhen{font:500 11px/1.6 var(--mono);letter-spacing:.13em;text-transform:uppercase;color:var(--contour)}
.ph{font-size:clamp(32px,5vw,46px);font-weight:800;letter-spacing:-.03em;margin-top:10px;line-height:1}
.pn{margin-top:14px;font-size:19px;line-height:1.5;color:var(--ink-2)}
.pnote{margin-top:18px;background:var(--card);border:1px solid var(--rule);
  border-left:3px solid var(--revise);border-radius:2px;padding:14px 17px;
  font-size:16px;line-height:1.55;color:var(--ink-2)}
.pnote b{color:var(--ink)}
.pnote a{color:var(--contour)}
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
  /* the rail is swipeable, so it stays — it just loses its label row sooner */
  .picker{padding:9px 0 7px}
  .picker-h>div{padding-bottom:7px}
  .picker-h em{display:none}
  .tabs button{padding:8px 12px}
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
  var qrail=document.getElementById("qrail");
  var strip=document.getElementById("tabs");
  var ind=document.getElementById("tabind");
  var picker=document.getElementById("picker");

  /* --- condense the picker once it sticks ------------------------------
     A sticky element sits at exactly top:0 the moment it sticks, so its own
     rect is the test, so it can never disagree with the CSS.
     The handler is one rect read and a class toggle, cheap at scroll rate. */
  function syncStuck(){
    var want = picker.getBoundingClientRect().top <= 0.5;
    if(want !== picker.classList.contains("stuck")){
      picker.classList.toggle("stuck", want);
      place();                     /* tab heights change as it condenses */
    }
  }
  window.addEventListener("scroll", syncStuck, {passive:true});
  window.addEventListener("resize", syncStuck);
  syncStuck();

  /* --- the sliding indicator ------------------------------------------- */
  function place(){
    var on=strip.querySelector('[aria-selected="true"]');
    if(!on) return;
    ind.style.setProperty("--x", on.offsetLeft+"px");
    ind.style.setProperty("--w", on.offsetWidth+"px");
    ind.classList.toggle("is-exam", on.classList.contains("exam"));
    ind.classList.add("ready");
  }
  function centre(btn,instant){
    var want=btn.offsetLeft-(strip.clientWidth-btn.offsetWidth)/2;
    var max=strip.scrollWidth-strip.clientWidth;
    want=Math.max(0,Math.min(want,max));
    if(instant){ var b=strip.style.scrollBehavior; strip.style.scrollBehavior="auto";
                 strip.scrollLeft=want; strip.style.scrollBehavior=b; }
    else strip.scrollLeft=want;
  }
  function edges(){
    var max=strip.scrollWidth-strip.clientWidth;
    qrail.classList.remove("at-start","mid","at-end");
    if(max<2) return;
    qrail.classList.add(strip.scrollLeft<2?"at-start":(strip.scrollLeft>max-2?"at-end":"mid"));
  }
  strip.addEventListener("scroll",edges,{passive:true});
  if("ResizeObserver" in window) new ResizeObserver(function(){ place(); edges(); }).observe(strip);
  window.addEventListener("resize",function(){ place(); edges(); });

  /* whichever stop is next by date — dotted on its tab, named above the rail */
  var today=new Date(); today.setHours(0,0,0,0);
  var nextId=null;
  for(var i=0;i<tabs.length;i++){
    if(new Date(tabs[i].dataset.date+"T00:00:00")>=today){ nextId=tabs[i].dataset.tab; break; }
  }
  if(nextId){
    tabs.forEach(function(b){ b.classList.toggle("next", b.dataset.tab===nextId); });
    var lab=tabs.filter(function(b){return b.dataset.tab===nextId;})[0];
    var note=document.getElementById("nextnote");
    if(note && lab) note.textContent="next up · "+lab.querySelector("b").textContent;
  }

  function show(id,opts){
    opts=opts||{};
    var pane=null, btn=null;
    tabs.forEach(function(b){
      var on=b.dataset.tab===id;
      b.setAttribute("aria-selected", on?"true":"false");
      b.tabIndex = on?0:-1;
      if(on) btn=b;
    });
    document.querySelectorAll(".pane").forEach(function(p){
      p.hidden = p.id!=="pane-"+id;
      if(!p.hidden) pane=p;
    });
    place();
    if(btn) centre(btn, !!opts.instant);
    edges();
    /* canvases have no size until the pane is visible, so boot scenes now */
    if(pane && window.__bootViz) window.__bootViz(pane);
    try{ history.replaceState(null,"","#"+id); }catch(e){}
  }

  tabs.forEach(function(b,i){
    b.addEventListener("click",function(){ show(b.dataset.tab); window.scrollTo({top:0}); });
    b.addEventListener("keydown",function(e){
      var n=i;
      if(e.key==="ArrowRight") n=(i+1)%tabs.length;
      else if(e.key==="ArrowLeft") n=(i-1+tabs.length)%tabs.length;
      else if(e.key==="Home") n=0;
      else if(e.key==="End") n=tabs.length-1;
      else return;
      e.preventDefault();
      show(tabs[n].dataset.tab);
      tabs[n].focus();
    });
  });

  var want=(location.hash||"").replace("#","");
  show(tabs.some(function(b){return b.dataset.tab===want;}) ? want : (nextId||"@@FIRST@@"),
       {instant:true});
  edges();
  /* web fonts land after first paint and change tab widths */
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ place(); edges(); });

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
    tabs, panes = [], []

    for s in course.STOPS:
        qs = list(buckets[s["id"]])
        qs.sort(key=lambda q: (q["tag"], q["id"]))
        sids = coverage_chips(s)

        cls = "exam" if s["kind"] == "exam" else ""
        short = s["when"].split(" \u00b7 ")[0]
        tabs.append(
            f'<button role="tab" id="tab-{s["id"]}" aria-controls="pane-{s["id"]}"'
            f' aria-selected="false" tabindex="-1"'
            f' data-tab="{s["id"]}" class="{cls}" data-date="{s["date"]}">'
            f'<b>{s["label"]}</b><i>{short}</i><span class="tdot"></span></button>')

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
        if s["id"] == "m1":
            head += ('<div class="pnote"><b>The department publishes a study guide '
                     'for this exam</b>, and it is the source of truth for coverage. '
                     'Every one of its practice problems is worked out, with the '
                     'answer held back until you commit to an attempt, at '
                     '<a href="/exam1.html">Exam&nbsp;1, worked</a>. Start there; '
                     'use this tab for the sections no quiz ever tested.</div>')
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
            f'<section class="pane" id="pane-{s["id"]}" role="tabpanel" '
            f'aria-labelledby="tab-{s["id"]}" tabindex="0" hidden>\n{head}\n'
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
<style>{parts["css"]}{PAGE_CSS}{drill.CSS}</style>
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

<div class="picker" id="picker">
  <div class="picker-h"><div><span>Pick a quiz</span><em id="nextnote"></em></div></div>
  <div class="qrail" id="qrail">
    <div class="tabs" role="tablist" aria-label="Quizzes and exams" id="tabs">
      <span class="tabind" id="tabind" aria-hidden="true"></span>
      {"".join(tabs)}
    </div>
  </div>
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
<script>{drill.JS}</script>
</body>
</html>
"""
    (ROOT / "quiz.html").write_text(html, encoding="utf-8")
    return total
