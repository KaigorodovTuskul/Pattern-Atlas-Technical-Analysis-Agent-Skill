#!/usr/bin/env python3
"""Generate local, original, deterministic conceptual SVGs. No external imagery."""
import json, math, html, random, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/pattern-atlas/assets/charts'
CAT=ROOT/'skills/pattern-atlas/data/catalog.json'
# Points are synthetic diagrams; they do not purport to be market observations.
PROFILES={
 'triangles':[(0,.65),(.1,.16),(.19,.62),(.28,.17),(.37,.54),(.47,.16),(.55,.45),(.64,.17),(.72,.35),(.79,.17),(.86,.29),(.95,.13)],
 'wedges':[(0,.81),(.08,.35),(.18,.73),(.26,.29),(.37,.64),(.45,.26),(.56,.55),(.64,.24),(.75,.45),(.82,.23),(.95,.66)],
 'broadening':[(0,.50),(.1,.40),(.20,.62),(.31,.28),(.43,.78),(.56,.15),(.69,.87),(.81,.06),(.92,.90),(1,.67)],
 'double':[(0,.13),(.1,.38),(.22,.84),(.32,.41),(.42,.31),(.53,.68),(.62,.84),(.73,.38),(.85,.23),(.95,.12)],
 'triple':[(0,.16),(.12,.45),(.22,.83),(.33,.38),(.45,.22),(.55,.82),(.65,.39),(.76,.23),(.85,.81),(.95,.18)],
 'head_shoulders':[(0,.80),(.11,.48),(.22,.29),(.31,.56),(.40,.37),(.5,.06),(.61,.52),(.7,.29),(.79,.35),(.86,.59),(.98,.87)],
 'cup':[(0,.12),(.12,.31),(.24,.60),(.37,.81),(.5,.84),(.63,.77),(.74,.50),(.82,.17),(.88,.35),(.93,.27),(.98,.10)],
 'rounding':[(0,.13),(.11,.30),(.22,.53),(.34,.70),(.44,.78),(.53,.81),(.62,.77),(.72,.63),(.84,.37),(.95,.11)],
 'diamond':[(0,.50),(.10,.39),(.20,.56),(.30,.24),(.40,.78),(.51,.09),(.62,.82),(.72,.26),(.82,.67),(.91,.43),(1,.48)],
 'flags':[(0,.91),(.19,.74),(.29,.36),(.35,.09),(.45,.20),(.55,.15),(.65,.30),(.75,.25),(.83,.33),(.9,.11),(1,.04)],
 'pennants':[(0,.93),(.18,.58),(.29,.11),(.39,.28),(.48,.48),(.56,.29),(.63,.43),(.7,.32),(.77,.38),(.82,.26),(.96,.06)],
 'rectangles':[(0,.53),(.1,.15),(.21,.81),(.34,.16),(.45,.80),(.56,.18),(.67,.82),(.78,.18),(.87,.77),(.95,.09)],
 'gaps':[(0,.83),(.13,.68),(.23,.79),(.32,.60),(.42,.68),(.52,.22),(.61,.38),(.7,.13),(.84,.28),(.96,.10)],
 'islands':[(0,.70),(.14,.66),(.25,.72),(.38,.32),(.49,.17),(.58,.26),(.7,.68),(.85,.74),(.96,.85)],
 'vturn':[(0,.09),(.18,.20),(.35,.52),(.49,.91),(.61,.68),(.77,.28),(.94,.07)],
 'scallops':[(0,.22),(.07,.45),(.14,.56),(.22,.44),(.29,.25),(.37,.40),(.44,.58),(.51,.41),(.6,.22),(.67,.39),(.74,.53),(.82,.31),(.91,.15),(1,.08)],
 'pipes_horns':[(0,.28),(.18,.38),(.36,.56),(.46,.21),(.56,.77),(.69,.48),(.81,.32),(.96,.16)],
 'harmonics':[(0,.77),(.16,.16),(.33,.61),(.48,.37),(.65,.82),(.79,.31),(.96,.49)],
 'waves':[(0,.85),(.14,.50),(.24,.68),(.38,.29),(.48,.45),(.68,.09),(.78,.26),(.88,.17),(.98,.52)],
 'measured':[(0,.87),(.18,.34),(.33,.17),(.47,.46),(.61,.60),(.74,.22),(.92,.07)],
 'deadcat':[(0,.15),(.10,.19),(.19,.09),(.33,.87),(.46,.73),(.57,.56),(.66,.70),(.82,.82),(.96,.93)],
 'bars':[(0,.75),(.12,.55),(.24,.61),(.36,.31),(.48,.45),(.60,.32),(.72,.56),(.84,.23),(.96,.29)],
 'volume':[(0,.67),(.12,.58),(.24,.75),(.36,.37),(.48,.44),(.60,.23),(.72,.52),(.84,.28),(.96,.39)],
 'trend':[(0,.78),(.11,.67),(.21,.73),(.31,.45),(.41,.56),(.54,.34),(.62,.44),(.75,.15),(.86,.28),(.98,.06)],
 'cats_ears':[(0,.21),(.12,.71),(.22,.65),(.36,.30),(.46,.57),(.56,.41),(.68,.34),(.83,.65),(.96,.87)],
 'pothole':[(0,.32),(.11,.30),(.22,.36),(.31,.29),(.38,.35),(.48,.77),(.58,.82),(.69,.46),(.81,.31),(.92,.24),(.99,.10)],
 'multipeak':[(0,.86),(.11,.28),(.20,.65),(.3,.29),(.4,.64),(.50,.30),(.60,.65),(.70,.08),(.80,.50),(.91,.75),(.98,.93)],
 'bump_run':[(0,.82),(.14,.75),(.27,.61),(.40,.48),(.53,.17),(.62,.05),(.69,.29),(.77,.51),(.89,.67),(.98,.82)],
 'roof':[(0,.80),(.14,.73),(.27,.43),(.4,.17),(.5,.08),(.63,.25),(.78,.50),(.9,.75),(.98,.78)],
 'cloud_bank':[(0,.20),(.12,.32),(.24,.16),(.36,.24),(.48,.64),(.62,.87),(.75,.67),(.86,.44),(.98,.33)],
 'lindsay':[(0,.74),(.07,.19),(.15,.47),(.22,.16),(.30,.48),(.37,.18),(.45,.83),(.56,.68),(.68,.31),(.80,.09),(.91,.37),(.99,.74)],
 'two_b':[(0,.68),(.18,.45),(.33,.14),(.48,.61),(.6,.09),(.72,.48),(.86,.73),(.98,.85)],
 'steps':[(0,.23),(.14,.47),(.26,.32),(.4,.57),(.54,.43),(.67,.70),(.82,.55),(.98,.86)],
 'event':[(0,.49),(.13,.50),(.28,.48),(.39,.52),(.51,.26),(.59,.13),(.72,.33),(.84,.26),(.97,.35)],
}
def path_from_points(pts):
 def px(x):return 67+x*516
 def py(y):return 82+y*202
 return ' '.join(('M' if i==0 else 'L')+f'{px(x):.1f} {py(y):.1f}' for i,(x,y) in enumerate(pts))
def transform(pts,name,family):
 n=name.lower()
 flip=False
 if family in ['double','triple','rounding','pipes_horns','vturn','cup','head_shoulders','scallops','diamond','deadcat']:
  flip=any(x in n for x in ['tops','top','bearish','inverted','big m','roof']) and not ('bottom' in n or 'bullish' in n)
 if family=='triangles':
  if 'descending' in n: return [(x,1-y) for x,y in pts]
  if 'symmetrical' in n: return [(x, 0.5+(y-0.5)*(1-.7*x)) for x,y in pts]
 if family=='wedges' and 'falling' in n:return [(x,1-y) for x,y in pts]
 if family=='vturn' and 'vertical run' in n:return [(x,1-y) for x,y in pts] if 'up' in n else pts
 if family=='flags' and ('earnings' in n or 'expanded' in n):return [(x, .5 + (y-.5)*(1+.25*x)) for x,y in pts]
 return [(x,1-y) for x,y in pts] if flip else pts

def svg(rec):
 family=rec['family'];title=rec['name'];pts=transform(PROFILES[family],title,family)
 name=html.escape(title)
 long=len(name)>48
 title_sz=19 if long else 25
 watermark='ORIGINAL SCHEMATIC  ·  NOT REAL PRICE DATA'
 color='#68e2cc' if not any(w in title.lower() for w in ['bearish','tops','top,','downside']) else '#ffb47f'
 overlays=[]
 def line(x1,y1,x2,y2,stroke='#7890ae',dash='6 6',width=2):
  return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" stroke-dasharray="{dash}" />'
 if family=='triangles':
  n=title.lower()
  if 'descending' in n:overlays=[line(120,254,500,254),line(120,103,500,227)]
  elif 'symmetrical' in n:overlays=[line(120,101,500,196),line(120,260,500,196)]
  else:overlays=[line(120,113,500,113),line(120,249,500,173)]
 elif family=='wedges':overlays=[line(120,153,505,123),line(120,257,505,158)] if 'rising' in title.lower() else [line(120,111,505,218),line(120,206,505,239)]
 elif family=='broadening':overlays=[line(105,170,530,86),line(105,211,530,280)]
 elif family=='rectangles':overlays=[line(95,117,515,117),line(95,251,515,251)]
 elif family=='head_shoulders':overlays=[line(165,204,526,204)]
 elif family=='double':overlays=[line(105,147 if 'top' in title.lower() else 211,525,147 if 'top' in title.lower() else 211)]
 elif family=='triple':overlays=[line(105,158 if 'top' in title.lower() else 222,528,158 if 'top' in title.lower() else 222)]
 elif family=='cup':overlays=[line(94,128 if 'inverted' not in title.lower() else 239,530,128 if 'inverted' not in title.lower() else 239)]
 elif family=='diamond':overlays=[line(82,184,326,101),line(82,184,326,283),line(326,101,551,184),line(326,283,551,184)]
 elif family=='flags':overlays=[line(280,119,499,179),line(280,180,499,226)]
 elif family=='pennants':overlays=[line(280,126,499,176),line(280,218,499,176)]
 elif family=='harmonics':
  for (x,y),t in zip(pts[:5],['X','A','B','C','D']):overlays.append(f'<text x="{67+x*516:.1f}" y="{73+y*202:.1f}" font-size="14" fill="#e9bf7d" text-anchor="middle">{t}</text>')
 elif family=='waves':
  for i,(x,y) in enumerate(pts[1:6],1):overlays.append(f'<text x="{67+x*516:.1f}" y="{75+y*202:.1f}" font-size="14" fill="#e9bf7d">{i}</text>')
 elif family=='roof':overlays=[line(80,241,560,241),line(145,237,320,101),line(320,101,520,238)]
 elif family=='cloud_bank':overlays=['<rect x="80" y="109" width="470" height="63" fill="#dfbd6e" opacity="0.12"/>',line(80,170,550,170)]
 elif family=='two_b':overlays=[line(95,112,510,112)]
 elif family=='event':overlays=[line(325,76,325,290,'#e9bf7d','3 6',2),'<text x="334" y="90" font-size="13" fill="#e9bf7d">EVENT</text>']
 elif family=='gaps':overlays=[line(325,152,325,241,'#e9bf7d','2 5',2)]
 if 'busted' in title.lower():overlays.append('<text x="330" y="302" font-size="12" fill="#ffb47f" text-anchor="middle">FALSE BREAKOUT → REVERSAL: CONCEPTUAL</text>')
 if family=='gaps':
  # Do not connect a real price gap with a fake solid segment.
  price=f'<path d="{path_from_points(pts[:5])}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/><path d="{path_from_points(pts[5:])}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'
 elif family=='islands':
  price=''.join(f'<path d="{path_from_points(segment)}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>' for segment in (pts[:3],pts[3:6],pts[6:]))
 elif family=='volume':
  volumes=[.25,.32,.44,.58,.79,.67,.52,.37,.21,.45,.65,.52,.33,.21,.15,.29,.44,.50,.38,.22,.12,.25]
  if 'u-shaped' in title.lower():volumes=[.88,.71,.62,.51,.41,.34,.25,.22,.20,.15,.14,.17,.19,.23,.29,.37,.44,.55,.65,.74,.83,.92]
  if 'dome' in title.lower():volumes=[.12,.22,.32,.42,.53,.61,.73,.83,.92,.96,.99,.93,.88,.81,.73,.65,.54,.42,.35,.25,.16,.12]
  price=''.join(f'<rect x="{81+i*22}" y="{276-180*v:.0f}" width="13" height="{180*v:.0f}" rx="3" fill="{color}" opacity="{.55+i%3*.12:.2f}"/>' for i,v in enumerate(volumes))
 elif family in ('bars','pipes_horns'):
  price=''
  for i,(x,y) in enumerate(pts):
   X=67+x*516;Y=82+y*202; wick=65 if family=='pipes_horns' and i in (3,4) else 35;C='#ffb47f' if i%3==0 else color
   price+=f'<line x1="{X:.1f}" y1="{Y-wick/2:.1f}" x2="{X:.1f}" y2="{Y+wick/2:.1f}" stroke="{C}" stroke-width="2"/><rect x="{X-7:.1f}" y="{Y-13:.1f}" width="14" height="26" rx="2" fill="{C}"/>'
 else:price=f'<path d="{path_from_points(pts)}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
 return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 380" role="img" aria-labelledby="title desc">
<title id="title">{name}: original conceptual diagram</title><desc id="desc">Not a copied site image, not historical market data. Stylized family-level geometry.</desc>
<rect width="650" height="380" fill="#0c1222" rx="19"/>
<text x="40" y="42" fill="#f5f7fc" font-family="Arial,sans-serif" font-size="{title_sz}" font-weight="700">{name}</text>
<text x="41" y="62" fill="#8da2be" font-size="12" font-family="Arial,sans-serif">{family.replace('_',' / ').upper()} · CONCEPT STUDY</text>
<rect x="41" y="76" width="568" height="228" rx="11" fill="#111d32" stroke="#31455f" />
{''.join(line(53,yy,597,yy,'#26364e','4 7',1) for yy in [109,163,217,271])}
{''.join(overlays)}
{price}
<text x="43" y="328" fill="#72879e" font-family="Arial,sans-serif" font-size="11">{watermark}</text>
<text x="43" y="352" fill="#b7c8d9" font-family="Arial,sans-serif" font-size="12">Not a validated identification or trading signal. See catalog rules.</text>
</svg>'''

def render():
 ASSETS.mkdir(parents=True,exist_ok=True)
 catalog=json.loads(CAT.read_text(encoding='utf-8'))
 n=0
 for rec in catalog['records']:
  if rec['example']:
   assert rec['family'] in PROFILES,(rec['id'],rec['family'])
   (ASSETS/(rec['id']+'.svg')).write_text(svg(rec),encoding='utf-8');n+=1
 print(f'Created {n} original SVG illustrations.')
if __name__=='__main__':render()
