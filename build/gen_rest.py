# -*- coding: utf-8 -*-
import re, os, html
DATA=os.path.join(os.path.dirname(os.path.abspath(__file__)),'data')+os.sep
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site')
RANKS=[("Новичок","1","Белый","#FFFFFF"),("Ученик","2–3","Серебристо-серый","#A8B0BC"),
("Искусник","4–5","Изумрудно-зелёный","#0E9F6E"),("Эксперт","6–7","Сапфирово-синий","#1D4ED8"),
("Мастер","8–9","Фиолетовый","#7C3AED"),("Грандмастер","10–11","Оранжевый","#F97316"),
("Великий","12–13","Красный","#C81E1E"),("Высший","14–15","Магента","#DB2777"),
("Верховный","16–17","Золотой","#F5B301"),("Совершенный","18–19","Морская волна","#06B6D4"),
("Абсолютный","20","Чёрный","#0A0A0A")]
FONTS=('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
 'family=Commissioner:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Spectral:wght@600&display=swap">')
NAV=[("","Главная"),("spravochnik/","Справочник"),("treker/","Трекер"),("mehanika/","Как это работает")]
def chrome(title,desc,body,cur,up=1,extra_head="",raw=False):
    p="../"*up
    nav="".join('<a href="%s%s"%s>%s</a>'%(p,h,' aria-current="page"' if h==cur else '',t) for h,t in NAV)
    inner=body if raw else '<main><div class="wrap">%s</div></main>'%body
    return ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
     '<meta name="viewport" content="width=device-width,initial-scale=1">'
     '<title>%s</title><meta name="description" content="%s">%s'
     '<link rel="stylesheet" href="%sassets/style.css">%s</head><body>'
     '<header class="site"><div class="wrap"><a class="logo" href="%s">ExperienS</a><nav>%s</nav></div></header>'
     '%s'
     '<footer><div class="wrap"><span>ExperienS · семь сфер · 126 навыков</span>'
     '<span>Материал для развития навыков. Не заменяет медицинскую, психологическую, правовую или финансовую помощь.</span>'
     '</div></footer></body></html>')%(html.escape(title),html.escape(desc),FONTS,p,extra_head,p,nav,inner)

# ---------- механика ----------
rows="".join('<tr><td><span class="rk" style="background:%s"></span>%s</td><td class="mono">%s</td><td>%s</td></tr>'
             %(hx,n,lv,cl) for n,lv,cl,hx in RANKS)
body=('<h1 style="font-size:clamp(30px,5vw,44px)">Как это работает</h1>'
 '<p class="lead" style="margin-top:10px">Система переводит реальные действия в видимый прогресс. '
 'Ничего не начисляется само: опыт появляется только тогда, когда закрыта неделя.</p>'
 '<h2 class="sec">Недельный цикл</h2>'
 '<div class="rules">'
 '<div><b>Выберите навыки на неделю</b><p>До двадцати одного за раз. Открытые навыки видны в справочнике; '
 'остальные откроются с уровнем.</p></div>'
 '<div><b>Задайте себе критерий</b><p>Не «больше двигаться», а «три прогулки по тридцать минут». '
 'Критерий должен быть таким, чтобы в конце недели вы могли однозначно сказать: закрыт или нет.</p></div>'
 '<div><b>Отметьте результат</b><p>Два варианта: выполнено или не вышло. Промежуточного нет — '
 'половина критерия опыта не даёт, и это сделано намеренно: иначе критерий перестаёт быть критерием.</p></div>'
 '<div><b>Закройте неделю</b><p>Опыт начисляется один раз, в момент закрытия. Пока неделя не закрыта, '
 'отметки можно менять сколько угодно.</p></div>'
 '</div>'
 '<h2 class="sec">Откуда берётся опыт</h2>'
 '<p>Каждый выполненный навык даёт опыт: десять единиц на первом уровне, больше — на следующих. '
 'Логика простая: задание для навыка пятнадцатого уровня требовательнее, чем для первого, и стоит дороже.</p>'
 '<div class="rules">'
 '<div><b>Ритм — множитель 1,25</b><p>Если за неделю выполнено девяносто процентов взятого и больше, '
 'весь опыт недели умножается на 1,25. Это награда за собранную неделю, а не за отдельный подвиг.</p></div>'
 '<div><b>Закрытая сфера — множитель 1,15</b><p>Если в сфере выполнены все взятые навыки, они получают '
 'дополнительный множитель. Так система поощряет доводить сферу до конца, а не растягиваться тонким слоем.</p></div>'
 '<div><b>Штрафов нет</b><p>Опыт никогда не уменьшается. Пропущенная неделя ничего не отнимает. '
 'Невыполненное задание влияет только на бой со Стражем.</p></div>'
 '</div>'
 '<h2 class="sec">Уровни и ранги</h2>'
 '<p>Опыт навыка поднимает сам навык, подсферу и сферу. Сумма опыта всех навыков — это общий уровень, '
 'а общий уровень определяет ранг и открывает новые навыки: по семь на каждом уровне со второго по шестнадцатый. '
 'К шестнадцатому открыты все сто двадцать шесть.</p>'
 '<div class="tw"><table><thead><tr><th>Ранг</th><th>Уровни</th><th>Цвет</th></tr></thead><tbody>%s</tbody></table></div>'
 '<p class="note">Уровень отдельного навыка не может обгонять общий уровень более чем на три. '
 'Опыт сверх этого не теряется — он ждёт повышения общего уровня и превращается в уровни сразу.</p>'
 '<h2 class="sec">Профиль важнее уровня</h2>'
 '<p>Два человека с одинаковым общим уровнем могут быть совершенно разными: у одного развито тело и деятельность, '
 'у другого — мышление и социум. Поэтому в системе всегда видны обе величины: насколько вы развиты в целом '
 'и в чём именно. Одна цифра ничего не говорит о человеке.</p>'
 '<h2 class="sec">Стражи</h2>'
 '<p>У каждой сферы свой Страж и семь кругов. Выполненные навыки наносят ему урон, невыполненные дают ему удары. '
 'Пройденный круг приносит артефакт. Страж — не препятствие: он не блокирует уровень и существует как отдельная '
 'цель для тех, кому она интересна.</p>')%rows
open(os.path.join(ROOT,'mehanika','index.html'),'w',encoding='utf-8').write(
    chrome("Как это работает — ExperienS",
           "Недельный цикл, опыт, уровни, ранги и Стражи ExperienS простым языком.",body,"mehanika/"))

# ---------- трекер ----------
app=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'treker_app.html'),encoding='utf-8').read()
app=app.split('<title>',1)[1].split('</title>',1)[1]           # убрать title
app=re.sub(r'<link rel="preconnect".*?display=swap">','',app,flags=re.S)  # шрифты даёт chrome
style=re.findall(r'<style>.*?</style>',app,flags=re.S)
rest=app
for s in style: rest=rest.replace(s,'')
rest=rest.replace('<div class="eyebrow">Колесо развития · семь сфер · 126 навыков</div>\n      <h1>ExperienS</h1>',
                  '<div class="eyebrow">Личный прогресс</div>\n      <h1>Трекер недели</h1>')
rest=rest.replace('<p>Справочник, недельный чек-лист и игровая механика в одном месте.</p>',
                  '<p>Прогресс сохраняется в этом браузере. Полные описания навыков — в <a href="../spravochnik/">справочнике</a>.</p>')
extra="".join(style)+'<style>body>main{padding:0}.wrap{max-width:1180px}</style>'
open(os.path.join(ROOT,'treker','index.html'),'w',encoding='utf-8').write(
    chrome("Трекер недели — ExperienS","Недельный чек-лист с опытом, уровнями и Стражем.",
           rest,"treker/",extra_head=extra,raw=True))
print("ok")
