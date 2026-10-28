#!/usr/bin/env python3
"""Fill/refresh the shared nav in every page (single source: site.json). Idempotent."""
import json,glob,os,re
os.chdir(os.path.dirname(os.path.abspath(__file__)))
cfg=json.load(open('site.json',encoding='utf-8'))
files={f for f in glob.glob('*.html') if not f.startswith('_')}
def row(m,active):
    out='<div class="nav-row %s%s"><span class="nav-mod">%s</span>'%(m['cls'],' sep' if m.get('sep') else '',m['title'])
    for p in m['pages']:
        k=p['key']
        if p.get('href'):
            out+='<span class="navg"><a class="n-main" href="%s">%s</a></span>'%(p['href'],p['label']); continue
        if k+'.html' not in files and k+'_easy.html' not in files: continue
        a=' active' if active==k+'.html' else ''
        e=' active' if active==k+'_easy.html' else ''
        out+='<span class="navg"><a class="n-main%s" href="%s.html">%s</a>'%(a,k,p['label'])
        if not m.get('noeasy') and k+'_easy.html' in files: out+='<a class="n-easy%s" href="%s_easy.html" title="やさしい版">🍎</a>'%(e,k)
        out+='</span>'
    return out+'</div>'
labels={}
for m in cfg['modules']:
    for p in m['pages']:
        labels[p['key']+'.html']=(m['short'],p['label']); labels[p['key']+'_easy.html']=(m['short'],p['label']+' 🍎')
n=0
for f in sorted(files):
    s=open(f,encoding='utf-8').read()
    nav='\n'.join('      '+row(m,f) for m in cfg['modules'])
    block='<!--NAV:start-->\n'+nav+'\n<!--NAV:end-->'
    if '<!--NAV:start-->' in s: s2=re.sub(r'<!--NAV:start-->.*?<!--NAV:end-->',lambda m:block,s,flags=re.S)
    elif '<!--NAV-->' in s: s2=s.replace('<!--NAV-->',block,1)
    else: continue
    if f in labels:
        mod,lab=labels[f]
        s2=re.sub(r'(id="navToggle"[^>]*>).*?(<span class="nav-caret">)',lambda m:m.group(1)+'📚 '+mod+' '+lab+' '+m.group(2),s2,count=1,flags=re.S)
    if s2!=s: open(f,'w',encoding='utf-8').write(s2); n+=1
print('updated',n,'pages')
