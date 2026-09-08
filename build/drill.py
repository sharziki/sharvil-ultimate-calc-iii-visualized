"""Drill mode — one question at a time, graded on the spot, then cycled.

The shipped quiz is a batch grader: answer all 17, press Check, read the damage.
That is a fine way to *audit* what you know and a bad way to *learn* it, because
nothing stops you skimming ahead, and the feedback arrives long after the guess.

Drill mode is the other shape. One question on screen, the next one unreachable
until this one is answered, the answer and the worked solution the instant you
commit, and the whole set cycled — with everything you got wrong asked again
first. Both modes run off the same markup; this is a progressive enhancement
layered on the DOM the bank already emits, not a second question bank.

Three details are load-bearing:

**Options are shuffled, letters are not.** The bank keys every answer to a
letter and the original set is badly skewed — on Quiz 2, fifteen of seventeen
answers are A, which means you can score 15/17 by reflex and learn nothing. So
the <li> order is shuffled and the visible A–F labels are rewritten to stay
sequential, while each input keeps its ORIGINAL value. Grading compares
input.value to data-key and is unaffected by display order.

**The solution header has to follow the shuffle.** It reads "Answer A", meaning
the original letter. After shuffling, that letter is somewhere else on screen,
so it is rewritten to whatever the correct option is now labelled. Missing this
would have every explanation confidently name the wrong choice.

**Progress is per pane and per cycle**, not global — each quiz tab drills on its
own, and the tab you are sitting is the one you want.
"""

CSS = r"""
/* ---- drill mode ------------------------------------------------------- */
.modes{display:flex;gap:2px;padding:3px;border:1px solid var(--rule);
  border-radius:999px;background:var(--paper-2)}
.modes button{border:0;background:none;cursor:pointer;border-radius:999px;
  padding:7px 14px;color:var(--ink-3);
  font:600 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  transition:background .18s ease,color .18s ease}
.modes button[aria-pressed="true"]{background:var(--ink);color:var(--paper)}

.dprog{display:flex;align-items:center;gap:12px;margin-left:auto;
  font:500 11px/1 var(--mono);letter-spacing:.06em;color:var(--ink-3)}
.dprog b{color:var(--ink);font-weight:700}
.dprog .ok{color:var(--veg)}
.dprog .no{color:var(--revise)}
.dbar{flex:0 0 92px;height:3px;border-radius:2px;background:var(--rule-2);
  overflow:hidden}
.dbar i{display:block;height:100%;width:0;background:var(--contour);
  transition:width .35s cubic-bezier(.22,1,.36,1)}

/* In drill, the list shows exactly one card. Everything else stays in the DOM
   so the batch grader can take it back over untouched. */
.qs.drill{list-style:none;padding:0;counter-reset:none}
.qs.drill>.q{display:none}
.qs.drill>.q.dnow{display:block;animation:dcard .32s cubic-bezier(.22,1,.36,1) both}
@keyframes dcard{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}

.qs.drill>.q .opts label{cursor:pointer}
.qs.drill>.q.dlocked .opts label{cursor:default}

/* Answered state: the chosen wrong option and the right one both stay visible,
   because the useful comparison is between them. */
.q.dlocked .opts label.correct{border-color:var(--veg);
  background:color-mix(in srgb,var(--veg) 9%,transparent)}
.q.dlocked .opts label.chosen-wrong{border-color:var(--revise);
  background:color-mix(in srgb,var(--revise) 9%,transparent)}

.dverdict{display:flex;align-items:center;gap:9px;margin-top:15px;
  font:700 12px/1 var(--mono);letter-spacing:.09em;text-transform:uppercase}
.dverdict.ok{color:var(--veg)}
.dverdict.no{color:var(--revise)}
.dverdict span{width:17px;height:17px;border-radius:50%;display:grid;
  place-items:center;font-size:11px;color:var(--paper)}
.dverdict.ok span{background:var(--veg)}
.dverdict.no span{background:var(--revise)}

.dnext{display:flex;align-items:center;gap:14px;margin-top:17px;
  padding-top:15px;border-top:1px solid var(--rule)}
.dnext button{cursor:pointer;border:1px solid var(--ink);background:var(--ink);
  color:var(--paper);border-radius:2px;padding:11px 20px;
  font:600 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;
  transition:opacity .18s ease}
.dnext button:hover{opacity:.82}
.dnext button.retry{background:none;color:var(--ink);border-color:var(--ink)}
.dnext em{font:400 11px/1.5 var(--mono);font-style:normal;color:var(--ink-3);
  letter-spacing:.04em}

.dhint{margin:0 0 14px;font:400 11px/1.5 var(--mono);letter-spacing:.04em;
  color:var(--ink-3)}
.dhint b{color:var(--ink-2);font-weight:500}

/* End-of-cycle card */
.dend{border:1px solid var(--rule);border-left:3px solid var(--contour);
  border-radius:2px;background:var(--card);padding:22px 24px;box-shadow:var(--shadow)}
.dend h4{margin:0 0 8px;font:700 15px/1.2 var(--disp);color:var(--ink)}
.dend p{margin:0 0 16px;font:400 14px/1.6 var(--body);color:var(--ink-2);max-width:62ch}
.dend .score{font:700 34px/1 var(--disp);color:var(--ink);letter-spacing:-.02em}
.dend .score small{font:500 12px/1 var(--mono);color:var(--ink-3);letter-spacing:.08em}
.dend .again{display:flex;gap:9px;flex-wrap:wrap;margin-top:16px}
.dend button{cursor:pointer;border:1px solid var(--ink);background:var(--ink);
  color:var(--paper);border-radius:2px;padding:11px 18px;
  font:600 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase}
.dend button.ghost{background:none;color:var(--ink)}
@media (max-width:640px){
  .dprog{width:100%;margin:8px 0 0}
  .modes{width:100%;justify-content:center}
}
"""

JS = r"""
/* ---- drill mode ------------------------------------------------------- */
(function(){
  function shuffle(a){
    for(var i=a.length-1;i>0;i--){
      var j=Math.floor(Math.random()*(i+1)), t=a[i]; a[i]=a[j]; a[j]=t;
    }
    return a;
  }
  var LETTERS="ABCDEFGH".split("");

  /* Reorder the option <li>s and relabel them A.. in the new visual order.
     input.value keeps the ORIGINAL letter, so data-key still grades correctly.
     Then repoint the solution header at wherever the right answer now sits. */
  function shuffleOpts(q){
    var ol=q.querySelector(".opts"); if(!ol) return;
    var items=shuffle([].slice.call(ol.children));
    items.forEach(function(li,i){
      ol.appendChild(li);
      var let_=li.querySelector(".let"); if(let_) let_.textContent=LETTERS[i];
      var inp=li.querySelector("input");
      if(inp) inp.dataset.shown=LETTERS[i];
    });
    var right=ol.querySelector('input[value="'+q.dataset.key+'"]');
    var solh=q.querySelector(".solh b");
    if(right && solh) solh.textContent=right.dataset.shown;
  }

  function setup(pane){
    var list=pane.querySelector(".qs");
    var bar=pane.querySelector(".bar");
    if(!list||!bar) return;
    var all=[].slice.call(list.children).filter(function(n){
      return n.classList.contains("q");
    });
    if(all.length<2) return;

    /* mode switch + progress, injected ahead of the existing controls */
    var modes=document.createElement("div");
    modes.className="modes";
    modes.innerHTML='<button type="button" data-mode="drill" aria-pressed="true">Drill</button>'+
                    '<button type="button" data-mode="all" aria-pressed="false">Review all</button>';
    var prog=document.createElement("div");
    prog.className="dprog"; prog.hidden=true;
    prog.innerHTML='<span class="dbar"><i></i></span>'+
                   '<span><b data-dn>1</b> / <span data-dt>0</span></span>'+
                   '<span class="ok" data-dok>0 right</span>'+
                   '<span class="no" data-dno>0 wrong</span>';
    bar.insertBefore(modes, bar.firstChild);
    bar.appendChild(prog);

    var order=[], idx=0, right=0, wrong=0, missed=[], cycle=1, endCard=null;
    var origButtons=[].slice.call(bar.querySelectorAll("[data-submit],[data-reset],.bstat"));

    function paint(){
      prog.querySelector("[data-dn]").textContent=Math.min(idx+1,order.length);
      prog.querySelector("[data-dt]").textContent=order.length;
      prog.querySelector("[data-dok]").textContent=right+" right";
      prog.querySelector("[data-dno]").textContent=wrong+" wrong";
      prog.querySelector(".dbar i").style.width=
        (order.length? (idx/order.length*100):0)+"%";
    }

    function clear(q){
      q.classList.remove("graded","right","wrong","dlocked","dnow");
      var sol=q.querySelector(".sol"); if(sol) sol.hidden=true;
      q.querySelectorAll("label").forEach(function(l){
        l.classList.remove("correct","chosen-wrong");
      });
      /* answer() disables every input to lock the question. clear() has to put
         that back or a retry renders a question you physically cannot answer. */
      q.querySelectorAll("input").forEach(function(i){
        i.checked=false; i.disabled=false;
      });
      var v=q.querySelector(".dverdict"); if(v) v.remove();
      var n=q.querySelector(".dnext"); if(n) n.remove();
      var h=q.querySelector(".dhint"); if(h) h.remove();
    }

    function show(){
      if(endCard){ endCard.remove(); endCard=null; }
      if(order[idx]) delete order[idx].dataset.scored;
      all.forEach(function(q){ q.classList.remove("dnow"); });
      if(idx>=order.length){ return finish(); }
      var q=order[idx];
      clear(q);
      shuffleOpts(q);
      var hint=document.createElement("p");
      hint.className="dhint";
      hint.innerHTML="Pick one. You will get the answer and the working "+
                     "immediately, and the next question after that. "+
                     "<b>Choices are shuffled every time.</b>";
      q.insertBefore(hint, q.querySelector(".opts"));
      q.classList.add("dnow");
      paint();
      var top=list.getBoundingClientRect().top+window.scrollY-90;
      window.scrollTo({top:top,behavior:"smooth"});
    }

    function answer(q,inp){
      if(q.classList.contains("dlocked")) return;
      q.classList.add("dlocked","graded");
      var key=q.dataset.key, ok=inp.value===key;
      q.classList.add(ok?"right":"wrong");
      if(!q.dataset.scored){
        if(ok) right++; else { wrong++; missed.push(q); }
      }
      q.querySelectorAll("input").forEach(function(i){
        var lab=i.closest("label");
        if(i.value===key) lab.classList.add("correct");
        else if(i===inp) lab.classList.add("chosen-wrong");
        i.disabled=true;
      });
      var sol=q.querySelector(".sol"); if(sol) sol.hidden=false;

      var v=document.createElement("div");
      v.className="dverdict "+(ok?"ok":"no");
      v.innerHTML="<span>"+(ok?"&#10003;":"&#10007;")+"</span>"+
                  (ok?"Correct":"Not this one &mdash; read the working");
      q.insertBefore(v, sol||null);

      var nx=document.createElement("div");
      nx.className="dnext";
      var last=idx>=order.length-1;
      /* Getting it wrong and reading the working is not the same as being able
         to do it. Retry re-asks this question with the options reshuffled, so
         the second attempt is a real attempt and not a memory of where the
         green box was. The pass score keeps the FIRST answer either way — the
         retry is practice, and the question still returns in the missed pile. */
      nx.innerHTML=(ok?"":'<button type="button" class="retry" data-dretry>'+
                        "Try it again</button>")+
        '<button type="button" data-dnext>'+
        (last?"See how you did":"Next question &rarr;")+'</button>'+
        '<em>'+(ok?"or press Enter":"work it through, then re-answer &mdash; "+
                "Enter moves on")+'</em>';
      q.appendChild(nx);
      nx.querySelector(ok?"[data-dnext]":"[data-dretry]").focus({preventScroll:true});
      paint();
    }

    function finish(){
      var total=order.length;
      var pct=total? Math.round(right/total*100):0;
      endCard=document.createElement("div");
      endCard.className="dend";
      var againMissed=missed.length
        ? '<button type="button" data-again="missed">Drill the '+missed.length+
          ' I missed</button>' : "";
      endCard.innerHTML=
        '<div class="score">'+right+"/"+total+' <small>&middot; '+pct+"% &middot; pass "+
        cycle+"</small></div>"+
        "<h4>"+(pct===100?"Clean sweep.":pct>=80?"Close.":"Worth another pass.")+"</h4>"+
        "<p>"+(missed.length
          ? "Drilling only the ones you missed is the faster loop &mdash; the "+
            "questions you already answered cold teach you nothing on a second pass."
          : "Every question in this set, first try. Reshuffle for a cold re-test, "+
            "or move to the next quiz.")+"</p>"+
        '<div class="again">'+againMissed+
        '<button type="button" class="ghost" data-again="all">Reshuffle all '+
        total+"</button></div>";
      list.appendChild(endCard);
      prog.querySelector(".dbar i").style.width="100%";
      endCard.scrollIntoView({behavior:"smooth",block:"center"});
    }

    function start(set){
      order=shuffle(set.slice());
      idx=0; right=0; wrong=0; missed=[];
      all.forEach(clear);
      show();
    }

    list.addEventListener("change",function(e){
      if(!list.classList.contains("drill")) return;
      var inp=e.target.closest('input[type="radio"]'); if(!inp) return;
      var q=inp.closest(".q"); if(q && q.classList.contains("dnow")) answer(q,inp);
    });

    list.addEventListener("click",function(e){
      var n=e.target.closest("[data-dnext]");
      if(n){ idx++; show(); return; }
      var r=e.target.closest("[data-dretry]");
      if(r){
        var q=r.closest(".q");
        clear(q);
        shuffleOpts(q);
        q.dataset.scored="1";          /* first attempt already counted */
        q.classList.add("dnow");
        var h=document.createElement("p");
        h.className="dhint";
        h.innerHTML="Second attempt. <b>The choices have been reshuffled</b>, so "+
                    "this is the question again rather than a memory of the layout.";
        q.insertBefore(h,q.querySelector(".opts"));
        return;
      }
      var a=e.target.closest("[data-again]");
      if(a){
        cycle++;
        start(a.dataset.again==="missed" && missed.length ? missed : all);
      }
    });

    document.addEventListener("keydown",function(e){
      if(!list.classList.contains("drill")) return;
      if(pane.hidden) return;
      var q=list.querySelector(".q.dnow"); if(!q) return;
      if(e.key==="Enter"){
        var n=q.querySelector("[data-dnext]");
        if(n){ e.preventDefault(); idx++; show(); }
        return;
      }
      if(q.classList.contains("dlocked")) return;
      var i=LETTERS.indexOf(e.key.toUpperCase());
      if(i<0){ var d=parseInt(e.key,10); if(d>=1&&d<=8) i=d-1; }
      if(i<0) return;
      var inp=q.querySelectorAll('.opts input[type="radio"]')[i];
      if(inp){ e.preventDefault(); inp.checked=true; answer(q,inp); }
    });

    function mode(drill){
      list.classList.toggle("drill",drill);
      prog.hidden=!drill;
      origButtons.forEach(function(b){ b.hidden=drill; });
      modes.querySelectorAll("button").forEach(function(b){
        b.setAttribute("aria-pressed", String((b.dataset.mode==="drill")===drill));
      });
      var res=pane.querySelector("[data-result]"); if(res) res.hidden=true;
      if(drill){ cycle=1; start(all); }
      else{
        if(endCard){ endCard.remove(); endCard=null; }
        all.forEach(function(q){
          clear(q);
          q.querySelectorAll("input").forEach(function(i){ i.disabled=false; });
        });
      }
    }
    modes.addEventListener("click",function(e){
      var b=e.target.closest("[data-mode]"); if(!b) return;
      mode(b.dataset.mode==="drill");
    });

    /* Drill is the point of this page; Review all is the escape hatch. Starting
       in review meant every question, every option and every answer was on
       screen at once, which is exactly what one-at-a-time is for. */
    mode(true);
  }

  document.querySelectorAll(".pane").forEach(setup);
})();
"""
