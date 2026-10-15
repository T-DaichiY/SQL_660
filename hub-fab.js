/* Floating hub button + review marks on every lesson page. Idempotent, no dependencies. */
(function(){
  try{
    var me=document.currentScript||[].slice.call(document.scripts).filter(function(s){return /hub-fab\.js/.test(s.src)}).pop();
    if(!me)return;
    var base=new URL('.',me.src).href, here=location.href.split('#')[0].split('?')[0];
    if(here.indexOf(base)!==0)return;
    var id=here.slice(base.length); if(!id)return;var homeOnly=/(^|\/)index\.html$|^sql_index\.html$/.test(id);if(id==='index.html')return;
    var KEY='dsHub:status',VK='dsHub:last';
    function ld(k,d){try{return JSON.parse(localStorage.getItem(k))||d}catch(e){return d}}
    function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
    var key=id.replace(/_easy\.html$/,'.html');
    var title=(document.querySelector('h1')||document.title).textContent.replace(/\s+/g,' ').trim().slice(0,60);
    if(!homeOnly)sv(VK,{id:key,title:title});
    var st=ld(KEY,{});
    var box=document.createElement('div');
    box.style.cssText='position:fixed;right:14px;bottom:14px;z-index:9999;display:flex;gap:6px;font:600 13px -apple-system,"Hiragino Sans",sans-serif';
    function mk(txt,fn,href){var e=document.createElement(href?'a':'button');e.textContent=txt;if(href)e.href=href;e.style.cssText='border:0;border-radius:99px;padding:8px 13px;background:#1e293b;color:#fff;cursor:pointer;text-decoration:none;box-shadow:0 3px 10px rgba(0,0,0,.3)';if(fn)e.onclick=fn;return e}
    var hub=mk('🎓 ハブ',null,base+'index.html');
    var d=mk('',null),s=mk('',null);
    function paint(){d.textContent=st[key]==='done'?'✓ 復習済み':'✓ 復習した';d.style.background=st[key]==='done'?'#16a34a':'#1e293b';s.textContent=st[key]==='star'?'★ 要復習':'☆ 要復習';s.style.background=st[key]==='star'?'#f59e0b':'#1e293b'}
    function tog(a){return function(){st[key]=st[key]===a?undefined:a;if(!st[key])delete st[key];sv(KEY,st);paint()}}
    d.onclick=tog('done');s.onclick=tog('star');paint();
    box.appendChild(hub);if(!homeOnly){box.appendChild(s);box.appendChild(d);}
    (document.body||document.documentElement).appendChild(box);
  }catch(e){}
})();
