// ===== "この章のコマンドまとめ" =====
// Collects every code example shown in the lesson body (not practice answers / quiz),
// groups them by unit, drops exact duplicates and appends them as a cheat-sheet at the
// end of <main>. Must load BEFORE typewriter.js (summary blocks are marked .cs-block).
(function(){
  var main=document.querySelector('main');
  if(!main) return;
  var css='.code-summary{background:var(--white,#fff);border-radius:var(--radius,14px);padding:1.75rem 2rem;box-shadow:var(--shadow,0 2px 12px rgba(0,0,0,.08));border-top:4px solid var(--teal,#0d9488);margin-top:1.5rem;}'+
    '.code-summary>summary{cursor:pointer;font-size:1.25rem;font-weight:800;list-style:none;}'+
    '.code-summary>summary::-webkit-details-marker{display:none;}'+
    '.code-summary>summary::after{content:" ▾";color:var(--text-sec,#64748b);}'+
    '.code-summary[open]>summary::after{content:" ▴";}'+
    '.cs-note{font-size:.82rem;color:var(--text-sec,#64748b);margin:.4rem 0 0;}'+
    '.cs-kws{display:flex;flex-wrap:wrap;gap:.35rem;margin:.9rem 0 0;}'+
    '.cs-kw{background:#1e293b;color:#93c5fd;border-radius:6px;padding:.15rem .55rem;font-size:.78rem;font-family:\'SF Mono\',\'Fira Code\',monospace;}'+
    '.cs-group h3{font-size:1rem;margin:1.4rem 0 .5rem;}'+
    '.cs-item{position:relative;}'+
    '.cs-item .code-block{margin:.5rem 0;}'+
    '.cs-copy{position:absolute;top:.6rem;right:.6rem;background:#334155;color:#e2e8f0;border:none;border-radius:6px;padding:.2rem .6rem;font-size:.72rem;cursor:pointer;font-family:inherit;}'+
    '.cs-copy:hover{background:#475569;}';
  var st=document.createElement('style'); st.textContent=css; document.head.appendChild(st);

  var groups=[], seen={}, cur=null, kws=[], kwSeen={};
  function groupFor(title){
    if(cur&&cur.title===title) return cur;
    cur={title:title,items:[]}; groups.push(cur); return cur;
  }
  var blocks=main.querySelectorAll('.code-block');
  blocks.forEach(function(b){
    if(b.closest('.answer-reveal,.quiz-section,.code-summary')) return;
    var text=b.textContent.replace(/\s+$/,'');
    var key=text.replace(/\s+/g,' ').trim();
    if(!key||seen[key]) return;
    seen[key]=1;
    var unit=b.closest('.unit'), title='';
    if(unit){
      var h=unit.querySelector('.unit-header h2, h2');
      var num=unit.querySelector('.unit-num');
      title=(num?num.textContent.trim()+' ':'')+(h?h.textContent.trim():'');
    }
    b.querySelectorAll('.kw').forEach(function(k){var w=k.textContent.trim().toUpperCase();if(w&&!kwSeen[w]){kwSeen[w]=1;kws.push(w);}});
    groupFor(title).items.push({html:b.innerHTML,text:text});
  });
  if(!groups.length) return;

  var total=0; groups.forEach(function(g){total+=g.items.length;});
  var det=document.createElement('details');
  det.className='code-summary'; det.id='code-summary'; det.open=true;
  var sum=document.createElement('summary'); sum.textContent='📋 この章のコマンドまとめ（'+total+'個）';
  det.appendChild(sum);
  var note=document.createElement('p'); note.className='cs-note';
  note.textContent='このページに出てきたコマンド（SQL文）を単元ごとに並べました。試験前の見直し用に。右上のボタンでコピーできます。';
  det.appendChild(note);
  if(kws.length){var kb=document.createElement('div'); kb.className='cs-kws'; kws.forEach(function(w){var c=document.createElement('span'); c.className='cs-kw'; c.textContent=w; kb.appendChild(c);}); det.appendChild(kb);}
  groups.forEach(function(g){
    var wrap=document.createElement('div'); wrap.className='cs-group';
    if(g.title){var h3=document.createElement('h3'); h3.textContent=g.title; wrap.appendChild(h3);}
    g.items.forEach(function(it){
      var item=document.createElement('div'); item.className='cs-item';
      var pre=document.createElement('pre'); pre.className='code-block cs-block'; pre.innerHTML=it.html;
      var btn=document.createElement('button'); btn.className='cs-copy'; btn.textContent='コピー';
      btn.addEventListener('click',function(){
        var done=function(){btn.textContent='✓ コピー済み'; setTimeout(function(){btn.textContent='コピー';},1500);};
        if(navigator.clipboard) navigator.clipboard.writeText(it.text).then(done,function(){});
      });
      item.appendChild(pre); item.appendChild(btn); wrap.appendChild(item);
    });
    det.appendChild(wrap);
  });
  main.appendChild(det);
})();
