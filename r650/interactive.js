// ===== M6 Interactive helpers =====

// Accordion self-check
document.addEventListener('click', function(e){
  const q = e.target.closest('.cp-q');
  if (q) q.classList.toggle('open');
  const fc = e.target.closest('.flip-card');
  if (fc) fc.classList.toggle('flipped');
});

// Scroll reveal
(function(){
  const obs = new IntersectionObserver(es=>{
    es.forEach(x=>{ if(x.isIntersecting) x.target.classList.add('visible'); });
  }, {threshold:0, rootMargin:'0px 0px -20px 0px'});
  document.querySelectorAll('.unit').forEach(u=>obs.observe(u));
  setTimeout(()=>document.querySelectorAll('.unit:not(.visible)').forEach(u=>u.classList.add('visible')), 600);
})();

// ---- Ch1: Binary outcome simulator ----
function initBinaryDemo(){
  const slider = document.getElementById('bin-prob');
  if(!slider) return;
  function upd(){
    const p = +slider.value;
    document.getElementById('bin-prob-v').textContent = p.toFixed(2);
    const outcome = p >= 0.5 ? 1 : 0;
    const pct = Math.round(p*100);
    document.getElementById('bin-outcome').textContent = outcome;
    const v = document.getElementById('bin-verdict');
    if(outcome===1){
      v.textContent = '✅ 1（グループA: 成功/あり）';
      v.className = 'verdict good';
    } else {
      v.textContent = '❌ 0（グループB: 失敗/なし）';
      v.className = 'verdict bad';
    }
    document.getElementById('bin-pct').textContent = pct + '%';
    // update sigmoid dot
    const svg_x = 40 + p * 320;
    const sig_y = 1/(1+Math.exp(-(p*10-5)));
    const svg_y = 160 - sig_y * 120;
    const dot = document.getElementById('sig-dot');
    const line = document.getElementById('sig-line');
    if(dot){ dot.setAttribute('cx', svg_x); dot.setAttribute('cy', svg_y); }
    if(line){ line.setAttribute('x1', svg_x); line.setAttribute('x2', svg_x); line.setAttribute('y2', svg_y); }
  }
  slider.addEventListener('input', upd); upd();
}

// ---- Ch2: Probability → Odds → LogOdds live calculator ----
function initTransformCalc(){
  const slider = document.getElementById('tr-prob');
  if(!slider) return;
  function upd(){
    const p = Math.max(0.001, Math.min(0.999, +slider.value));
    const odds = p / (1 - p);
    const logodds = Math.log(odds);
    document.getElementById('tr-prob-v').textContent = p.toFixed(3);
    document.getElementById('tr-odds-v').textContent = odds.toFixed(3);
    document.getElementById('tr-logodds-v').textContent = logodds.toFixed(3);
    // color indicators
    const lo_el = document.getElementById('tr-logodds-v');
    if(logodds > 0){ lo_el.style.color='var(--green)'; }
    else if(logodds < 0){ lo_el.style.color='var(--red)'; }
    else { lo_el.style.color='var(--text)'; }
    // bar fill
    const bar = document.getElementById('tr-bar');
    if(bar) bar.style.width = (p*100) + '%';
  }
  slider.addEventListener('input', upd); upd();
}

// ---- Ch3: Sigmoid curve with draggable dot ----
function initSigmoidViz(){
  const slider = document.getElementById('sg-x');
  if(!slider) return;
  function sigmoid(x){ return 1/(1+Math.exp(-x)); }
  function upd(){
    const x = +slider.value;
    const p = sigmoid(x);
    document.getElementById('sg-x-v').textContent = x.toFixed(1);
    document.getElementById('sg-p-v').textContent = p.toFixed(3);
    // SVG: x maps -6..6 → 30..370, p maps 0..1 → 160..20
    const svgX = 30 + (x+6)/12 * 340;
    const svgY = 160 - p * 140;
    const dot = document.getElementById('sg-dot');
    const vx = document.getElementById('sg-vline-x');
    const vy = document.getElementById('sg-vline-y');
    if(dot){ dot.setAttribute('cx', svgX); dot.setAttribute('cy', svgY); }
    if(vx){ vx.setAttribute('x1',svgX); vx.setAttribute('x2',svgX); vx.setAttribute('y2',svgY); }
    if(vy){ vy.setAttribute('y1',svgY); vy.setAttribute('y2',svgY); }
    const v = document.getElementById('sg-verdict');
    if(v){
      if(p>0.7){ v.textContent='高確率 → グループ1（あり）に判定'; v.className='verdict good'; }
      else if(p<0.3){ v.textContent='低確率 → グループ0（なし）に判定'; v.className='verdict bad'; }
      else { v.textContent='中間（0.3〜0.7）→ 判定が難しい領域'; v.className='verdict warn'; }
    }
  }
  slider.addEventListener('input', upd); upd();
}

// ---- Ch4: Abalone step-by-step revealer ----
function initAbaloneSteps(){
  let step = 0;
  const steps = document.querySelectorAll('.ab-step');
  const btn = document.getElementById('ab-next');
  if(!btn) return;
  steps.forEach((s,i)=>{ s.style.opacity = i===0?'1':'0.2'; s.style.transform = i===0?'none':'translateX(20px)'; });
  btn.addEventListener('click', function(){
    step++;
    if(step < steps.length){
      steps[step].style.opacity='1';
      steps[step].style.transition='all .4s ease';
      steps[step].style.transform='none';
    }
    if(step >= steps.length-1) btn.textContent='完了！✅';
  });
}

// ---- Ch5: Deviance comparison bar ----
function initDevianceBar(){
  const slider = document.getElementById('dv-pred');
  if(!slider) return;
  function upd(){
    const n = +slider.value;
    document.getElementById('dv-pred-v').textContent = n;
    const null_dev = 3924;
    const resid = Math.max(null_dev - n*320, 1200);
    const diff = null_dev - resid;
    document.getElementById('dv-null').style.width = '100%';
    document.getElementById('dv-resid').style.width = (resid/null_dev*100) + '%';
    document.getElementById('dv-null-v').textContent = null_dev.toLocaleString();
    document.getElementById('dv-resid-v').textContent = Math.round(resid).toLocaleString();
    document.getElementById('dv-diff-v').textContent = Math.round(diff).toLocaleString();
    const v = document.getElementById('dv-verdict');
    if(diff > 300){ v.textContent='✅ 大きな改善！予測変数が効いている'; v.className='verdict good'; }
    else if(diff > 100){ v.textContent='🙂 まずまずの改善'; v.className='verdict warn'; }
    else { v.textContent='😟 ほとんど改善なし → この変数は弱い'; v.className='verdict bad'; }
  }
  slider.addEventListener('input', upd); upd();
}

// ---- Ch6: AIC penalty visualizer ----
function initAICDemo(){
  const slider = document.getElementById('aic-k');
  if(!slider) return;
  const base_ll = -1797.9;
  function upd(){
    const k = +slider.value;
    document.getElementById('aic-k-v').textContent = k;
    const aic = -2*base_ll + 2*k;
    document.getElementById('aic-val').textContent = Math.round(aic).toLocaleString();
    document.getElementById('aic-penalty').textContent = (2*k).toLocaleString();
    const bar = document.getElementById('aic-pen-bar');
    if(bar) bar.style.width = Math.min(k/10*100,100)+'%';
  }
  slider.addEventListener('input', upd); upd();
}

// ---- Ch7: K comparison table highlight ----
function initKDemo(){
  const btns = document.querySelectorAll('.k-btn');
  btns.forEach(b=>{
    b.addEventListener('click',function(){
      btns.forEach(x=>x.classList.remove('active-k'));
      b.classList.add('active-k');
      const k = +b.dataset.k;
      const base = 2720944;
      const params = 3; // intercept + 2 predictors
      const aic = base - 2*params + 2*k*params; // simplified
      document.getElementById('k-result').textContent = aic.toLocaleString();
      document.getElementById('k-penalty').textContent = (2*k*params).toLocaleString();
      const v = document.getElementById('k-note');
      if(k===2){ v.textContent='← これが古典的AIC。デフォルト。課題では基本これを使う。'; }
      else if(k===3){ v.textContent='← k=3 はペナルティが強い版。BICに近くなる。'; }
      else { v.textContent='← k=log(n) はBIC（ベイズ情報量規準）。'; }
    });
  });
}

// ---- Ch8: Z-value calculator ----
function initZCalc(){
  const coef = document.getElementById('zc-coef');
  const se   = document.getElementById('zc-se');
  if(!coef) return;
  function upd(){
    const b = +coef.value, s = +se.value;
    if(s===0) return;
    const z = b/s;
    document.getElementById('zc-z').textContent = z.toFixed(3);
    const v = document.getElementById('zc-verdict');
    const az = Math.abs(z);
    if(az>3){ v.textContent='|Z|>3 → 非常に有意（p<0.003）✅'; v.className='verdict good'; }
    else if(az>1.96){ v.textContent='|Z|>1.96 → 有意（p<0.05）✅'; v.className='verdict good'; }
    else if(az>1.645){ v.textContent='|Z|>1.645 → ほぼ有意（p<0.10）🙂'; v.className='verdict warn'; }
    else { v.textContent='|Z|≤1.645 → 有意ではない 😟'; v.className='verdict bad'; }
  }
  [coef,se].forEach(el=>el.addEventListener('input',upd)); upd();
}

// ---- Ch9: German credit chain ----
function initGermanCredit(){
  const good = document.getElementById('gc-good');
  const bad  = document.getElementById('gc-bad');
  if(!good) return;
  function upd(){
    const g = +good.value, b = +bad.value, tot = g+b;
    if(tot===0) return;
    const p = g/tot;
    const odds = p/(1-p);
    const lo = Math.log(odds);
    document.getElementById('gc-p').textContent = p.toFixed(3);
    document.getElementById('gc-odds').textContent = odds.toFixed(3);
    document.getElementById('gc-lo').textContent = lo.toFixed(3);
    document.getElementById('gc-good-pct').textContent = Math.round(p*100);
    document.getElementById('gc-bar-good').style.width = (p*100)+'%';
    document.getElementById('gc-bar-bad').style.width = ((1-p)*100)+'%';
  }
  [good,bad].forEach(el=>el.addEventListener('input',upd)); upd();
}
