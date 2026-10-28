// ===== Button-triggered typewriter for all .code-block elements =====
// Non-destructive: shows each code block dimmed with a "▶ コードを打つ" button.
// On click, it re-types the code line-by-line, character-by-character, with a
// blinking caret, preserving syntax-highlight colors and the ORIGINAL line breaks.
//
// Robust line handling: each direct child <span class="cl"> is treated as exactly
// ONE line (its inner highlighted markup is the line content). Code blocks that
// don't use .cl wrappers fall back to splitting the plain text on "\n".

(function(){
  // ---- inject CSS once ----
  const css = `
  .tw-shell{position:relative;}
  .tw-btn{display:inline-flex;align-items:center;gap:.4rem;background:var(--primary,#2563eb);color:#fff;border:none;
    border-radius:8px;padding:.4rem 1rem;font-weight:700;font-size:.82rem;cursor:pointer;font-family:inherit;
    margin:0 0 .5rem;transition:all .2s;}
  .tw-btn:hover{filter:brightness(1.08);transform:translateY(-1px);}
  .tw-btn:disabled{opacity:.6;cursor:default;transform:none;}
  .code-block.tw-dim{opacity:.4;transition:opacity .25s;}
  .tw-caret{display:inline-block;width:7px;height:1em;background:#86efac;margin-left:1px;
    animation:twblink 1s step-end infinite;vertical-align:text-bottom;}
  .tw-caret.tw-done{animation:none;opacity:.35;}
  @keyframes twblink{0%,100%{opacity:1;}50%{opacity:0;}}
  `;
  const style=document.createElement('style'); style.textContent=css; document.head.appendChild(style);

  // Build a list of "lines". Each line is a list of atoms {ch, cls}.
  // cls = nearest highlight class (cm/kw/st/nm) or null. The .cl wrapper class is ignored (it's just a line box).
  function buildLines(block){
    const HILITE = new Set(['cm','kw','st','nm']);
    const lines = [];

    function atomsFromNode(node){
      // returns array of {ch, cls} for a single line's content node
      const out=[];
      function walk(n, cls){
        n.childNodes.forEach(c=>{
          if(c.nodeType===3){
            for(const ch of c.textContent) out.push({ch, cls});
          } else if(c.nodeType===1){
            const classes=(c.getAttribute('class')||'').split(/\s+/);
            let next=cls;
            for(const k of classes){ if(HILITE.has(k)){ next=k; break; } }
            walk(c, next);
          }
        });
      }
      walk(node, null);
      return out;
    }

    const clChildren = Array.from(block.children).filter(el=>
      el.tagName==='SPAN' && (el.getAttribute('class')||'').split(/\s+/).includes('cl'));

    if(clChildren.length>0){
      // Each .cl = one line (may be empty = blank line)
      clChildren.forEach(cl=>{ lines.push(atomsFromNode(cl)); });
    } else {
      // Fallback: no .cl wrappers — split the raw text on newlines, keep simple coloring by walking.
      const all=atomsFromNode(block);
      let cur=[];
      all.forEach(a=>{
        if(a.ch==='\n'){ lines.push(cur); cur=[]; }
        else cur.push(a);
      });
      lines.push(cur);
    }
    // trim trailing fully-empty lines
    while(lines.length>1 && lines[lines.length-1].length===0) lines.pop();
    return lines;
  }

  function typeLines(block, lines, btn){
    block.innerHTML='';
    block.classList.remove('tw-dim');
    const caret=document.createElement('span'); caret.className='tw-caret';
    block.appendChild(caret);

    const baseSpeed=20;
    let li=0;            // line index
    let ai=0;            // atom index within line
    let lineEl=null;     // current line container (div)
    let curSpan=null, curCls=null;

    function startLine(){
      // Use the original line class ".cl" so the line-number ::before counter
      // and "display:block; white-space:pre" styling apply exactly as before.
      lineEl=document.createElement('span');
      lineEl.className='cl';
      block.appendChild(lineEl);   // append at end (caret will be moved inside)
      curSpan=null; curCls=null;
      lineEl.appendChild(caret);   // caret lives inside the current line
    }

    function step(){
      if(li>=lines.length){
        caret.classList.add('tw-done');
        if(btn){ btn.disabled=false; btn.innerHTML='↻ もう一度'; }
        return;
      }
      if(lineEl===null) startLine();

      const line=lines[li];
      if(ai>=line.length){
        // end of line -> next line
        li++; ai=0; lineEl=null;
        if(li<lines.length){ return setTimeout(()=>{ startLine(); step(); }, baseSpeed*4); }
        return setTimeout(step, baseSpeed);
      }
      const a=line[ai];
      if(curCls!==a.cls){
        curCls=a.cls;
        if(a.cls){ curSpan=document.createElement('span'); curSpan.className=a.cls; lineEl.insertBefore(curSpan, caret); }
        else curSpan=null;
      }
      const tn=document.createTextNode(a.ch);
      if(curSpan) curSpan.appendChild(tn);
      else lineEl.insertBefore(tn, caret);
      ai++;
      let d=baseSpeed + Math.random()*baseSpeed*0.6;
      if('(){},=+'.includes(a.ch)) d*=1.5;
      setTimeout(step, d);
    }
    step();
  }

  document.querySelectorAll('.code-block').forEach(block=>{
    if(block.closest('.tw-shell')) return;
    const lines=buildLines(block);
    if(lines.length===0) return;

    const shell=document.createElement('div'); shell.className='tw-shell';
    block.parentNode.insertBefore(shell, block);
    const btn=document.createElement('button'); btn.className='tw-btn'; btn.innerHTML='▶ コードを打つ';
    shell.appendChild(btn);
    shell.appendChild(block);
    block.classList.add('tw-dim');

    btn.addEventListener('click', ()=>{
      btn.disabled=true; btn.innerHTML='⌨️ 入力中…';
      typeLines(block, lines, btn);
    });
  });
})();
