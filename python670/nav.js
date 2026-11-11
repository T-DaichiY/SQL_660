// ===== Foldable header navigation =====
// Collapses the module lesson list into a single toggle button.
// The open/closed state is remembered across pages via localStorage.
(function(){
  var btn=document.getElementById('navToggle');
  var grp=document.getElementById('navGroups');
  if(!btn||!grp) return;
  var KEY='sqlNavOpen';
  function set(v){
    grp.classList.toggle('open',v);
    btn.classList.toggle('open',v);
    btn.setAttribute('aria-expanded',v?'true':'false');
    try{ localStorage.setItem(KEY,v?'1':'0'); }catch(e){}
  }
  var open=false;
  try{ open=localStorage.getItem(KEY)==='1'; }catch(e){}
  set(open);
  btn.addEventListener('click',function(){ set(!grp.classList.contains('open')); });
})();
