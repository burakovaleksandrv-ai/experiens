
(function(){
  var q=document.getElementById('q'),chips=document.getElementById('chips'),
      none=document.getElementById('none'),grps=document.querySelectorAll('.grp'),cur=0;
  function apply(){
    var t=(q.value||'').trim().toLowerCase(), any=false;
    grps.forEach(function(g){
      var s=+g.dataset.s, show=(cur===0||cur===s), left=0;
      g.querySelectorAll('.sub').forEach(function(sub){
        var vis=0;
        sub.querySelectorAll('.card').forEach(function(c){
          var ok=show && (!t || c.dataset.n.indexOf(t)>=0);
          c.hidden=!ok; if(ok)vis++;
        });
        sub.hidden=!vis; left+=vis;
      });
      g.hidden=!left; if(left)any=true;
    });
    none.hidden=any;
  }
  q.addEventListener('input',apply);
  chips.addEventListener('click',function(ev){
    var b=ev.target.closest('.chip'); if(!b)return;
    cur=+b.dataset.s;
    chips.querySelectorAll('.chip').forEach(function(x){
      var on=x===b; x.setAttribute('aria-pressed',on);
      x.style.background=on&&x.dataset.s!=='0'?x.style.getPropertyValue('--c'):'';
      x.style.color=on&&x.dataset.s!=='0'?'#fff':'';
      if(on&&x.dataset.s==='0'){x.style.background='var(--accent)';x.style.color='var(--accent-ink)';}
    });
    apply();
  });
  var first=chips.querySelector('.chip');
  first.style.background='var(--accent)';first.style.color='var(--accent-ink)';
  apply();
})();
