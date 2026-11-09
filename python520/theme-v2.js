/* Wrap the first body mention of each glossary term in a JP|EN chip. */
(function(){
  var items=document.querySelectorAll('.glossary .term-item');
  var colors=['blue','green','amber','red','purple'];
  var terms=[];
  items.forEach(function(it,i){
    var en=(it.querySelector('.term-name')||{}).textContent||'';
    var jp=(it.querySelector('.term-en')||{}).textContent||'';
    en=en.trim();jp=jp.trim();
    if(!en||!jp||/[\/／~]/.test(en+jp)||/[（(]/.test(jp))return;
    terms.push({en:en,jp:jp,c:colors[i%colors.length],done:false});
  });
  function esc(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
  var scope=document.querySelectorAll('.unit > p,.unit > ul > li');
  scope.forEach(function(root){
    var w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{acceptNode:function(n){
      if(n.parentNode.closest('code,pre,button,a,.term,script,style'))return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;}});
    var nodes=[];while(w.nextNode())nodes.push(w.currentNode);
    nodes.forEach(function(n){
      terms.forEach(function(t){
        if(t.done||!n.parentNode)return;
        var txt=n.nodeValue,idx=-1,len=0;
        var j=txt.indexOf(t.jp);
        if(j>=0){idx=j;len=t.jp.length;}
        if(idx<0)return;
        var span=document.createElement('span');span.className='term term-'+t.c;
        span.innerHTML='<span class="term-jp"></span><span class="term-en"></span>';
        span.children[0].textContent=t.jp;span.children[1].textContent=t.en;
        var after=n.splitText(idx);after.nodeValue=after.nodeValue.slice(len);
        var dup=new RegExp('^[（(]\\s*'+esc(t.en)+'\\s*[）)]','i');
        if(dup.test(after.nodeValue))after.nodeValue=after.nodeValue.replace(dup,'');
        else if(after.nodeValue===''&&after.nextSibling&&after.nextSibling.nodeType===1&&/^[（(]/.test(after.nextSibling.textContent)&&after.nextSibling.textContent.toLowerCase().indexOf(t.en.toLowerCase())>-1){after.nextSibling.textContent=after.nextSibling.textContent.replace(/^[（(]\s*[^）)]*[）)]/,'');}
        n.parentNode.insertBefore(span,after);
        var st=span.parentNode.closest&&span.parentNode.closest('strong');if(st)st.classList.add('has-chip');
        t.done=true;
      });
    });
  });
})();

/* block-level <strong> would paint a tall yellow band: only mark inline ones */
document.querySelectorAll('.unit strong,.note-box strong,.warn-box strong,.teal-box strong,.tip-box strong').forEach(function(s){
  if(getComputedStyle(s).display!=='inline')s.classList.add('no-hl');
});
