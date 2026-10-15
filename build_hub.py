#!/usr/bin/env python3
"""Build the integrated study hub (index.html) from the three sites' index pages.
Run in the repo root. SQL index must be sql_index.html; stats/index.html, python520/index.html."""
import re, os, json, html
COURSES = [
    dict(id='sql', name='SQL（660）', icon='🗄️', index='sql_index.html', prefix=''),
    dict(id='stats', name='統計・回帰（550／650）', icon='📊', index='stats/index.html', prefix='stats/'),
    dict(id='py', name='Python（520）', icon='🐍', index='python520/index.html', prefix='python520/'),
]
def clean(s):
    s = re.sub(r'<a [^>]*>.*?</a>', '', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()
items = []
for c in COURSES:
    t = open(c['index'], encoding='utf-8').read()
    base = os.path.dirname(c['index'])
    parts = re.split(r'(<h2>.*?</h2>)', t, flags=re.S)
    mod = ''
    for p in parts:
        if p.startswith('<h2>'):
            mod = clean(p); continue
        for m in re.finditer(r'<div class="chapter-card[^"]*"[^>]*>(.*?)<div class="card-arrow">', p, flags=re.S):
            b = m.group(1)
            h = re.search(r'<a href="([^"]+\.html)"', b)
            if not h: continue
            href = h.group(1)
            if not os.path.exists(os.path.join(base, href)): continue
            icon = clean(re.search(r'class="card-icon">(.*?)</div>', b, re.S).group(1))
            tag = clean(re.search(r'class="card-num">(.*?)</div>', b, re.S).group(1)).replace('· 公開中', '').strip(' ·')
            title = clean(re.search(r'class="card-title">(.*?)</div>', b, re.S).group(1))
            d = re.search(r'class="card-desc">(.*?)</div>', b, re.S)
            desc = clean(d.group(1)) if d else ''
            easy = href[:-5] + '_easy.html'
            if not os.path.exists(os.path.join(base, easy)): easy = None
            practice = 'practice' in href or '演習' in mod or '演習' in tag
            items.append(dict(id=c['prefix'] + href, course=c['id'], mod=mod, icon=icon, title=title, tag=tag,
                              desc=desc[:140], easy=(c['prefix'] + easy) if easy else None, practice=practice))
import glob
def page_item(path, course, prefix, mod, icon):
    s = open(path, encoding='utf-8').read()
    h = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    ti = clean(h.group(1)) if h else clean(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    tag = re.search(r'class="ch-tag">(.*?)<', s)
    return dict(id=prefix + os.path.basename(path), course=course, mod=mod, icon=icon, title=ti[:60], tag=clean(tag.group(1)) if tag else '', desc='', easy=None, practice=True)
for p in sorted(glob.glob('m[678]_practice_*.html')):
    items.append(page_item(p, 'sql', '', '🏋️ SQL 演習（スキル別）', '🏋️'))
for p in sorted(glob.glob('stats/ex_*.html')):
    items.append(page_item(p, 'stats', 'stats/', '🏋️ 統計・回帰 演習（各15問）', '🏋️'))
seen = set(); out = []
for i in items:
    if i['id'] in seen: continue
    seen.add(i['id']); out.append(i)
data = json.dumps(dict(courses=[dict(id=c['id'], name=c['name'], icon=c['icon'], home=c['index']) for c in COURSES], items=out), ensure_ascii=False)
tpl = open('hub_template.html', encoding='utf-8').read()
open('index.html', 'w', encoding='utf-8').write(tpl.replace('/*DATA*/null', data))
print(len(out), 'items', {c['id']: sum(1 for i in out if i['course'] == c['id']) for c in COURSES})
