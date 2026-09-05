# -*- coding: utf-8 -*-
import json, os, html, collections, shutil
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')+os.sep
V=json.load(open(DATA+'v21.json'))
RECS=json.load(open(DATA+'recs.json'))
DEFS=json.load(open(DATA+'defs.json'))
COL=json.load(open(DATA+'spherecolors.json'))
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
SPH=[(1,"Здоровье","Тело"),(2,"Мышление","Разум"),(3,"Личность","Дух"),
     (4,"Деятельность","Земля"),(5,"Ресурсы","Вода"),(6,"Социум","Огонь"),(7,"Наполненность","Воздух")]
SPHN={n:(a,b) for n,a,b in SPH}
RANKS=[("Новичок",1,1,"#FFFFFF"),("Ученик",2,3,"#A8B0BC"),("Искусник",4,5,"#0E9F6E"),
("Эксперт",6,7,"#1D4ED8"),("Мастер",8,9,"#7C3AED"),("Грандмастер",10,11,"#F97316"),
("Великий",12,13,"#C81E1E"),("Высший",14,15,"#DB2777"),("Верховный",16,17,"#F5B301"),
("Совершенный",18,19,"#06B6D4"),("Абсолютный",20,20,"#0A0A0A")]
BY=collections.defaultdict(list)
for r in RECS: BY[r['skill_id']].append(r)
for k in BY: BY[k].sort(key=lambda z:z['no'])
SK={r['id']:r for r in V}
SUBS=collections.OrderedDict()
for r in sorted(V,key=lambda r:(r['sphere_id'],int(r['subfield_id'].split('.')[1]),r['no'])):
    SUBS.setdefault(r['subfield_id'],{"name":r['subfield'],"sph":r['sphere_id'],
                                      "def":DEFS['sub'][r['subfield_id']],"skills":[]})
    SUBS[r['subfield_id']]["skills"].append(r)
e=html.escape
FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Commissioner:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Spectral:wght@600&display=swap">')
NAV=[("","Главная"),("spravochnik/","Справочник"),("treker/","Трекер"),("mehanika/","Как это работает")]

def page(path, title, desc, body, cur="", up=0):
    p="../"*up
    nav="".join('<a href="%s%s"%s>%s</a>'%(p,h,' aria-current="page"' if h==cur else '',t) for h,t in NAV)
    doc=('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
     '<meta name="viewport" content="width=device-width,initial-scale=1">'
     '<title>%s</title><meta name="description" content="%s">%s'
     '<link rel="stylesheet" href="%sassets/style.css"></head><body>'
     '<header class="site"><div class="wrap"><a class="logo" href="%s">ExperienS</a><nav>%s</nav></div></header>'
     '<main><div class="wrap">%s</div></main>'
     '<footer><div class="wrap"><span>ExperienS · семь сфер · 126 навыков</span>'
     '<span>Материал для развития навыков. Не заменяет медицинскую, психологическую, правовую или финансовую помощь.</span>'
     '</div></footer></body></html>')%(e(title),e(desc),FONTS,p,p,nav,body)
    full=os.path.join(ROOT,path)
    os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w',encoding='utf-8').write(doc)

# ---------- главная ----------
cards="".join(
 '<a class="sphere" href="sfery/%d.html"><span class="stripe" style="background:%s"></span>'
 '<em style="color:%s">%s</em><b>%s</b><span>6 подсфер · 18 навыков</span></a>'
 %(n,COL[b],COL[b],e(b),e(a)) for n,a,b in SPH)
nums="".join('<div><b>%s</b><span>%s</span></div>'%(x,y) for x,y in
 [("7","сфер"),("42","подсферы"),("126","навыков"),("630","практик"),("20","уровней"),("11","рангов")])
body=('<div class="hero"><div class="eyebrow">Колесо развития</div>'
 '<h1>Жизнь как система развития, а не список дел</h1>'
 '<p>Семь сфер, 126 навыков и понятные недельные действия. Справочник, по которому можно работать самому, '
 'и игровая механика, которая показывает, что именно у вас растёт.</p></div>'
 '<div class="nums">%s</div>'
 '<div class="doors">'
 '<a class="door" href="spravochnik/"><b>Справочник</b><span>126 навыков с определениями и пятью практическими '
 'рекомендациями к каждому. Поиск и фильтр по сферам.</span><em>Открыть →</em></a>'
 '<a class="door" href="treker/"><b>Трекер недели</b><span>Взять навыки на неделю, отметить выполнение, '
 'получить опыт и увидеть, как растёт профиль.</span><em>Начать →</em></a>'
 '<a class="door" href="mehanika/"><b>Как это работает</b><span>Опыт, уровни, ранги и недельный цикл — '
 'человеческим языком, без формул.</span><em>Разобраться →</em></a>'
 '</div><h2 style="font-size:24px;margin-bottom:14px">Семь сфер</h2><div class="spheres">%s</div>')%(nums,cards)
page("index.html","ExperienS — колесо развития",
     "Справочник 126 навыков, недельный трекер и игровая механика развития по семи сферам жизни.",body,"")

# ---------- сферы ----------
for n,a,b in SPH:
    subs=[(k,v) for k,v in SUBS.items() if v['sph']==n]
    blocks=[]
    for k,v in subs:
        cards="".join(
          '<a class="card" href="../spravochnik/%s.html"><span class="t"><b>%s</b><u>ур. %d</u></span>'
          '<p>%s</p></a>'%(s['id'],e(s['skill']),s['unlock_level'],e(s['definition'])) for s in v['skills'])
        blocks.append('<div class="sub"><h3>%s. %s</h3><p>%s</p><div class="cards">%s</div></div>'
                      %(k,e(v['name']),e(v['def']),cards))
    body=('<div class="crumbs"><a href="../">Главная</a> · <span>%s «%s»</span></div>'
     '<div class="skillhead"><div><div class="eyebrow" style="color:%s">Сфера %d · %s</div>'
     '<h1>%s</h1></div><span class="badge">6 подсфер · 18 навыков</span></div>'
     '<p class="lead">%s</p>%s')%(e(a),e(b),COL[b],n,e(b),e(a),e(DEFS['sph'][a]),"".join(blocks))
    page("sfery/%d.html"%n,"%s «%s» — ExperienS"%(a,b),DEFS['sph'][a][:150],body,"",up=1)

# ---------- страницы навыков ----------
for r in V:
    sid=r['id']; n=r['sphere_id']; a,b=SPHN[n]
    sub=SUBS[r['subfield_id']]
    recs="".join('<div class="rec"><span class="n">%d</span><div><b>%s</b><p>%s</p><em>%s</em></div></div>'
                 %(x['no'],e(x['title']),e(x['text']),e(x['effect'])) for x in BY[sid])
    nbs="".join('<a class="nb" href="%s.html">%s <u>ур. %d</u></a>'%(s['id'],e(s['skill']),s['unlock_level'])
                for s in sub['skills'] if s['id']!=sid)
    body=('<div class="crumbs"><a href="../">Главная</a> · <a href="../sfery/%d.html">%s «%s»</a> · '
     '<a href="../spravochnik/#%s">%s</a></div>'
     '<div class="skillhead"><div><div class="eyebrow" style="color:%s">%s</div><h1>%s</h1></div>'
     '<span class="badge">открывается на <b>%d</b> уровне</span></div>'
     '<p class="lead">%s</p><div class="thesis">%s</div>'
     '<h2 class="sec">Пять недельных практик</h2>'
     '<p class="note" style="margin-top:0;margin-bottom:14px">Выберите одну, задайте посильный объём и '
     'отмечайте выполнение в течение недели. Не пытайтесь делать все пять сразу.</p>'
     '<div class="recs">%s</div>'
     '<h2 class="sec">Рядом в подсфере «%s»</h2><div class="neighbours">%s</div>')%(
      n,e(a),e(b),r['subfield_id'],e(sub['name']),COL[b],e(sub['name']),e(r['skill']),
      r['unlock_level'],e(r['definition']),e(r['thesis']),recs,e(sub['name']),nbs)
    page("spravochnik/%s.html"%sid,"%s — навык ExperienS"%r['skill'],r['definition'][:160],body,"spravochnik/",up=1)

# ---------- справочник ----------
chips="".join('<button class="chip" data-s="%d" style="--c:%s">%s «%s»</button>'%(n,COL[b],e(a),e(b)) for n,a,b in SPH)
grps=[]
for n,a,b in SPH:
    subs=[(k,v) for k,v in SUBS.items() if v['sph']==n]
    inner=[]
    for k,v in subs:
        cards="".join(
          '<a class="card" data-n="%s" href="%s.html"><span class="t"><b>%s</b><u>ур. %d</u></span><p>%s</p></a>'
          %(e((s['skill']+" "+v['name']+" "+a).lower()),s['id'],e(s['skill']),s['unlock_level'],e(s['definition']))
          for s in v['skills'])
        inner.append('<div class="sub" id="%s"><h3>%s. %s</h3><p>%s</p><div class="cards">%s</div></div>'
                     %(k,k,e(v['name']),e(v['def']),cards))
    grps.append('<section class="grp" data-s="%d"><h2><i style="background:%s"></i>%s «%s»</h2>'
                '<p>%s</p>%s</section>'%(n,COL[b],e(a),e(b),e(DEFS['sph'][a]),"".join(inner)))
body=('<h1 style="font-size:clamp(30px,5vw,44px)">Справочник навыков</h1>'
 '<p class="lead" style="margin-top:10px">Сто двадцать шесть навыков в семи сферах. У каждого — определение, '
 'ключевой принцип и пять практик, из которых собирается недельное задание.</p>'
 '<div class="tools"><input class="search" id="q" type="search" placeholder="Найти навык, подсферу или сферу"'
 ' autocomplete="off" aria-label="Поиск по навыкам"></div>'
 '<div class="chips" id="chips"><button class="chip" data-s="0" aria-pressed="true">Все сферы</button>%s</div>'
 '<div id="list">%s</div><p class="empty" id="none" hidden>Ничего не нашлось. Попробуйте другое слово.</p>'
 '<script src="../assets/spravochnik.js"></script>')%(chips,"".join(grps))
page("spravochnik/index.html","Справочник 126 навыков — ExperienS",
     "Все 126 навыков ExperienS с определениями и практическими рекомендациями.",body,"spravochnik/",up=1)

open(os.path.join(ROOT,'assets','spravochnik.js'),'w',encoding='utf-8').write('''
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
''')
print("страниц навыков:",len(V),"| сфер:",len(SPH))
