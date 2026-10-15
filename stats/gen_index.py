#!/usr/bin/env python3
"""Regenerate index.html card grid and exercises.html from site.json + page <h1>/intro."""
import json,re,html,os
S=json.load(open('site.json'))
cols=['c-blue','c-purple','c-green','c-yellow','c-red','c-teal']
def info(key):
    p=key+'.html'
    if not os.path.exists(p): return None
    t=open(p,encoding='utf-8').read()
    h=re.search(r'<h1>(.*?)</h1>',t,re.S); tag=re.search(r'class="ch-tag">(.*?)<',t)
    para=re.search(r'</h1>\s*<p>(.*?)</p>',t,re.S)
    h=re.sub(r'<.*?>','',h.group(1)).strip() if h else key
    d=re.sub(r'<.*?>','',para.group(1)).strip() if para else ''
    if len(d)>120: d=d[:117].rstrip('、。 ')+'…'
    return h,(tag.group(1) if tag else ''),d
def card(key,i,easy=False):
    r=info(key)
    if not r: return ''
    h,tag,d=r
    ic=h.split(' ')[0] if not h[0].isascii() else '📘'
    title=h[len(ic):].strip() if ic!='📘' else h
    ez=f' · <a href="{key}_easy.html" style="position:relative;z-index:2;">🍎 やさしい版</a>' if easy and os.path.exists(key+'_easy.html') else ''
    return f'''    <div class="chapter-card {cols[i%6]} fade-in stagger-1" style="position:relative;">
      <a href="{key}.html" style="position:absolute;inset:0;z-index:1;" aria-label="{html.escape(title)} を開く"></a>
      <div class="card-num">{html.escape(tag)}</div><div class="card-icon">{ic}</div>
      <div class="card-title">{title}</div>
      <div class="card-desc">{html.escape(d)}{ez}</div>
      <div class="card-arrow">→</div>
    </div>
'''
body=''
n=0
for m in S['modules']:
    if m['id']=='EX': continue
    cards=''
    for i,p in enumerate(m['pages']):
        c=card(p['key'],i,True)
        if c: cards+=c; n+=1
    if cards:
        body+=f'''  <div class="section-header fade-in stagger-1" style="margin-top:2rem">
    <h2>{html.escape(m['title'])}</h2>
  </div>
  <div class="chapters-grid">
{cards}  </div>
'''
ex=''
for i,p in enumerate([q for m in S['modules'] if m['id']=='EX' for q in m['pages'] if q['key']!='exercises']):
    c=card(p['key'],i)
    if c: ex+=c
# exercises hub
t=open('index.html',encoding='utf-8').read()
head=t[:t.index('<section class="hero">')]
head=head.replace('class="active"','',1) if False else head
tail='''<footer>
  <p>📊 統計レッスン：550 Basic Stats, R ／ 650 Data Visualization</p>
</footer>
<script src="typewriter.js"></script>
</body>
</html>
'''
hero=f'''<section class="hero">
  <div class="hero-content">
    <h1>統計<span>レッスン</span><br>推測 × 回帰 × ロジスティック</h1>
    <p>550 Basic Stats, R と 650 Data Visualization（回帰・ロジスティック回帰）の講義動画を、文字起こしと R の再計算で検証して作り直した学習ガイドです。数値はすべて R で確認済み。</p>
    <div class="hero-badges">
      <span class="badge">📺 講義動画の文字起こしを元に作成</span>
      <span class="badge">📚 {n}レッスン（本編＋やさしい版）</span>
      <span class="badge">🧪 数値はRで再計算</span>
      <span class="badge">📝 英語MCQクイズ</span>
      <span class="badge">🏋️ 演習120問</span>
    </div>
    <p style="margin-top:1rem"><a href="exercises.html" style="color:inherit;font-weight:700">🏋️ 演習ハブへ →</a></p>
  </div>
</section>
'''
open('index.html','w',encoding='utf-8').write(head+hero+'\n<div class="container">\n'+body+'</div>\n\n'+tail)
hub=head.replace('<title>统计','<title>')
hub=re.sub(r'<title>.*?</title>','<title>演習ハブ 統計レッスン</title>',head)
hubbody=f'''<div class="ch-banner"><div class="ch-banner-inner">
  <div class="ch-tag">演習ハブ</div><h1>🏋️ 演習ハブ</h1>
  <p>各モジュール15問（基礎5・中級5・上級5）。R で計算した答えを入力すると、ブラウザ上で自動採点されます。</p>
</div></div>
<div class="container">
  <div class="chapters-grid">
{ex}  </div>
</div>
'''
open('exercises.html','w',encoding='utf-8').write(hub+hubbody+'\n'+tail)
print('lessons',n)
