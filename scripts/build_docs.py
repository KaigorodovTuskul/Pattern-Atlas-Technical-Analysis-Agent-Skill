#!/usr/bin/env python3
"""Offline build of per-entry Markdown articles and an accessible zero-network gallery."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/pattern-atlas'
CAT=json.loads((SKILL/'data/catalog.json').read_text(encoding='utf-8'))
FAMILIES=json.loads((SKILL/'data/families.json').read_text(encoding='utf-8'))

def generate():
 out=SKILL/'patterns';out.mkdir(parents=True,exist_ok=True)
 for r in CAT['records']:
  source=r['verified_detail_url'] or r['source_index_url']
  note='Проверенная прямая ссылка на конкретную страницу источника.' if r['verified_detail_url'] else 'Прямая страница конкретной записи НЕ проверена; приведён только общий каталог.'
  illustration=f'![Схематический учебный пример {r["name"]}](../{r["example"]})\n\n**Иллюстрация:** самостоятельно сгенерированная схема семейства (НЕ скриншот, НЕ торговая история, НЕ верификация разновидности).\n' if r['example'] else 'Самостоятельная схема не нужна либо по названию отсутствует проверенное определение формы.\n'
  entry=f'''# {r['name']}

**Категория:** {r['category']} · **Семейство:** [{FAMILIES[r['family']]['title_ru']}](../references/{r['family']}.md) · **Уровень проверки:** `{r['confidence']}`

## Схема / пример

{illustration}
## Что означает

{r['description_ru']}

**Особенности именно этой записи:** {r['variant_note_ru']}

## Как проверить фигуру

{r['identification_ru']}

Проверка относится к **семейству**. Если доказана только принадлежность названия к классу, не считайте перечисленное точными уникальными правилами этой страницы источника. Чтобы формализовать детектор, нужны отдельные пороги, масштаб и примеры отрицательных случаев.

## Подтверждение / точка отсчёта

{r['confirmation_ru']}

**Статус:** до выполнения правил подтверждения помечайте объект как `unconfirmed`, после явного выполнения — `confirmed`, при нарушении исходного условия — `invalidated`, при нехватке данных — `indeterminate`.

## Опровержение и распространённые ошибки

{r['failure_ru']}

Конкурирующая гипотеза: обычный участок шума, иной паттерн того же семейства или режим рынка без устойчивого сигнала. Проверяйте по закрытым барам, а не с учётом будущих свечей.

## Амплитуда и риск

{r['measurement_ru']}

Оценивайте данные с поправкой на сплиты, дивиденды, гэпы и ликвидность; корректно разделяйте визуальную модель, торговые правила, доходность и оценку риска.

## Источник и ограничения

- [ThePatternSite — источник]({source}). {note}
- [Общий алфавитный индекс]({r['source_index_url']}).
- Эта страница содержит **самостоятельное методическое изложение**, не копию авторских текстов, таблиц, иллюстраций или исторических примеров.
- Статистические значения и коэффициенты не включены без отдельной верификации исходных условий.
'''
  (out/f'{r["id"]}.md').write_text(entry,encoding='utf-8')
 fam_lines=['# Семейства паттернов','','Выберите **одно** нужное семейство вместо загрузки всех материалов в контекст. Для поиска по фрагменту имени используйте `scripts/search_catalog.py`.','']
 for f,m in FAMILIES.items():
  c=sum(r['family']==f for r in CAT['records'])
  fam_lines.append(f'- [{m["title_ru"]}]({f}.md) — {c} записей · `{f}`')
 (SKILL/'references/REFERENCE_MAP.md').write_text('\n'.join(fam_lines)+'\n',encoding='utf-8')
 # Link individual entries from index
 idx=SKILL/'references/INDEX.md'
 text=idx.read_text(encoding='utf-8')
 for r in CAT['records']:
  text=text.replace(f'**{r["name"]}** —',f'[{r["name"]}](../patterns/{r["id"]}.md) —')
 idx.write_text(text,encoding='utf-8')
 # Offline gallery: load metadata from script tag, no network requests, no framework or CDN.
 js_data=[{'id':r['id'],'name':r['name'],'family':r['family'],'category':r['category'],'description':r['description_ru'],'figure':r['example'],'source':r['verified_detail_url'] or r['source_index_url'],'confidence':r['confidence']} for r in CAT['records']]
 script_json=json.dumps(js_data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 options=''.join(f'<option value="{html.escape(f)}">{html.escape(meta["title_ru"])} · {sum(r["family"]==f for r in CAT["records"])}</option>' for f,meta in FAMILIES.items())
 page='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>Pattern Atlas · Offline Explorer</title>
<style>
:root{--bg:#091020;--surface:#101b30;--line:#293a55;--text:#eaf3fc;--muted:#9db1c8;--accent:#63decb;--orange:#f0bf86}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}body::before{content:"";position:fixed;inset:0;z-index:-1;background:radial-gradient(ellipse at 12% 0%,#173448cc,transparent 48%),radial-gradient(ellipse at 95% 8%,#1c2449aa,transparent 44%)}a{color:var(--accent);text-underline-offset:3px}.wrap{max-width:1400px;padding:28px;margin:auto}.top{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);padding:0 0 18px;gap:14px}.brand{display:flex;align-items:center;gap:12px;font-size:17px;font-weight:700;letter-spacing:.06em}.brand .symbol{color:var(--accent);font-size:24px}.tiny{font-size:12px;color:var(--muted)}.hero{padding:52px 0 36px;max-width:950px}h1{font-size:clamp(35px,5vw,72px);letter-spacing:-.055em;margin:0;line-height:1.08}h1 span{color:var(--accent)}.hero p{color:var(--muted);max-width:710px;font-size:17px;line-height:1.75}.kpis{display:flex;gap:25px;flex-wrap:wrap}.kpis b{font-size:21px;color:#fff}.kpis span{display:block;font-size:12px;color:var(--muted)}.controls{display:flex;gap:12px;flex-wrap:wrap;position:sticky;top:0;background:#091020ef;padding:14px 0;z-index:5;backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}input,select{background:#15243b;border:1px solid #36506c;color:var(--text);padding:14px 16px;border-radius:10px;font:inherit;outline-color:var(--accent)}input{min-width:250px;flex:2}select{flex:1;min-width:180px}#count{margin-left:auto;align-self:center;font-size:13px;color:var(--muted)}.grid{padding:25px 0 48px;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}.card{background:linear-gradient(145deg,#132139,#101a2c);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:transform .15s,border-color .15s}.card:hover{transform:translateY(-3px);border-color:#6589a8}.card img{width:100%;aspect-ratio:650/380;object-fit:contain;background:#10182a}.placeholder{width:100%;aspect-ratio:650/380;display:grid;place-items:center;color:#839ab3;background:repeating-linear-gradient(45deg,#0c1728,#0c1728 12px,#102036 12px,#102036 24px)}.content{padding:17px;display:flex;flex-direction:column;flex:1}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.08em;font-size:10px;font-weight:700}h2{font-size:19px;line-height:1.35;margin:7px 0 10px;letter-spacing:-.02em}.summary{color:var(--muted);font-size:13px;margin:0 0 18px;flex:1}.links{display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:13px;border-top:1px solid var(--line);padding-top:12px}.warn{color:var(--orange);font-size:11px}footer{padding:35px 0 60px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}.btn{font:inherit;cursor:pointer;border:1px solid #3a5875;padding:12px 22px;background:#18334a;color:var(--text);border-radius:10px}.btn:hover{border-color:var(--accent)}.center{text-align:center;padding-bottom:35px}@media(max-width:550px){.wrap{padding:14px}.hero{padding:32px 0}.controls{position:static}#count{width:100%;margin:0}}
</style></head><body><main class="wrap"><header class="top"><div class="brand"><span class="symbol">◈</span> PATTERN ATLAS</div><span class="tiny">ORIGINAL RESEARCH GUIDE · OFFLINE</span></header><section class="hero"><h1>Patterns.<br><span>Evidence first.</span></h1><p>Самостоятельные описания, исходные имена из каталога Bulkowski и оригинальные учебные SVG. Поиск работает без интернета и без сторонних библиотек. Иллюстрации схематичны и не являются историческими сделками.</p><div class="kpis"><div><b>383</b><span>Index entries</span></div><div><b>38</b><span>Families</span></div><div><b>334</b><span>Original diagrams</span></div></div></section><section class="controls" aria-label="Search filters"><input id="q" type="search" autocomplete="off" placeholder="Название, категория, фрагмент описания…" aria-label="Search patterns"><select id="family" aria-label="Family"><option value="">Все семейства</option>'''+options+'''</select><select id="kind" aria-label="Category"><option value="">Все типы</option><option value="pattern">Фигуры и сигналы</option><option value="event">Событийные модели</option><option value="study">Справочные темы</option><option value="method">Методы и риск</option></select><span id="count" role="status"></span></section><section class="grid" id="items"></section><div class="center"><button id="more" class="btn" type="button" hidden>Показать ещё</button></div><footer>Independent illustrations and educational summaries · <a href="https://www.thepatternsite.com/chartpatterns.html">ThePatternSite primary index</a> · No affiliation or performance guarantees · Original site assets are not redistributed.</footer></main><script type="application/json" id="dataset">'''+script_json+'''</script><script>
'use strict';const items=JSON.parse(document.getElementById('dataset').textContent),el=document.getElementById('items'),f=document.getElementById('family'),k=document.getElementById('kind'),q=document.getElementById('q'),counter=document.getElementById('count'),more=document.getElementById('more');let visible=[],shown=0;const page=48;
function normalize(s){return String(s||'').toLocaleLowerCase().normalize('NFKC');}
function tile(r){const card=document.createElement('article');card.className='card';let media;if(r.figure){media=document.createElement('img');media.loading='lazy';media.alt='Original schematic of '+r.name;media.src='skills/pattern-atlas/'+r.figure;}else{media=document.createElement('div');media.className='placeholder';media.textContent='METHOD / REFERENCE';}card.append(media);const c=document.createElement('div');c.className='content';const eyebrow=document.createElement('div');eyebrow.className='eyebrow';eyebrow.textContent=r.family.replaceAll('_',' / ')+' · '+r.category;const h=document.createElement('h2');h.textContent=r.name;const summary=document.createElement('p');summary.className='summary';summary.textContent=r.description;const links=document.createElement('div');links.className='links';const local=document.createElement('a');local.href='skills/pattern-atlas/patterns/'+r.id+'.md';local.textContent='Описание ↗';const remote=document.createElement('a');remote.href=r.source;remote.rel='noopener noreferrer';remote.target='_blank';remote.textContent='Источник ↗';links.append(local,remote);const warn=document.createElement('small');warn.className='warn';warn.textContent=r.confidence==='reference_verified'?'Verified source link':'Family-level reference';c.append(eyebrow,h,summary,warn,links);card.append(c);return card;}
function append(){let next=visible.slice(shown,shown+page);el.append(...next.map(tile));shown+=next.length;more.hidden=shown>=visible.length;}
function refresh(){const t=normalize(q.value);visible=items.filter(x=>(!f.value||x.family===f.value)&&(!k.value||x.category===k.value)&&(!t||normalize(x.name+' '+x.family+' '+x.description).includes(t)));shown=0;el.replaceChildren();counter.textContent=visible.length+' записей';append();}
[q,f,k].forEach(x=>x.addEventListener('input',refresh));more.addEventListener('click',append);refresh();
</script></body></html>'''
 (ROOT/'gallery.html').write_text(page,encoding='utf-8')
 print(f'Built {len(CAT["records"])} entry pages; offline gallery contains {len(js_data)} records.')
if __name__=='__main__':generate()
