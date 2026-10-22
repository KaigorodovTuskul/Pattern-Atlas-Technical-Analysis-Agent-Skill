#!/usr/bin/env python3
"""Offline discovery and citation-aware retrieval for Pattern Atlas."""
import argparse, json, re, sys, unicodedata
from pathlib import Path
CATALOG=Path(__file__).resolve().parents[1]/'data/catalog.json'
FAMILIES=Path(__file__).resolve().parents[1]/'data/families.json'

def normalize(s):
 s=unicodedata.normalize('NFKC',str(s)).casefold()
 return ' '.join(re.findall(r'[\w]+',s,flags=re.UNICODE))

def find(query='',family=None,kind=None,limit=20):
 records=json.loads(CATALOG.read_text(encoding='utf-8'))['records']
 needle=normalize(query)
 candidates=[]
 for r in records:
  if family and r['family']!=family:continue
  if kind and r['category']!=kind:continue
  name=normalize(r['name']); summary=normalize(r['description_ru']+' '+r['variant_note_ru'])
  if needle and needle not in name and needle not in summary and needle not in normalize(r['id']):continue
  score=0 if name==needle else 1 if name.startswith(needle) else 2 if needle in name else 3
  candidates.append((score,r['name'].casefold(),r))
 candidates.sort(key=lambda x:(x[0],x[1]))
 return [x[2] for x in candidates[:limit]]

def run(argv=None):
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('query',nargs='?',default='',help='English pattern name or Russian text')
 ap.add_argument('--family',help='Exact family ID')
 ap.add_argument('--kind',choices=('pattern','method','event','study'))
 ap.add_argument('--id',dest='id_',help='Exact slug')
 ap.add_argument('--limit',type=int,default=20)
 ap.add_argument('--json',action='store_true')
 ap.add_argument('--stats',action='store_true')
 ap.add_argument('--families',action='store_true')
 args=ap.parse_args(argv)
 if not 1<=args.limit<=1000:ap.error('--limit should be 1..1000')
 catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
 if args.stats:print(json.dumps(catalog['counts'],ensure_ascii=False,indent=2));return 0
 if args.families:
  print(json.dumps({k:v['title_ru'] for k,v in json.loads(FAMILIES.read_text(encoding='utf-8')).items()},ensure_ascii=False,indent=2));return 0
 if args.id_:
  results=[r for r in catalog['records'] if r['id']==args.id_]
 else:results=find(args.query,args.family,args.kind,args.limit)
 if args.json:print(json.dumps(results,ensure_ascii=False,indent=2));return 0 if results else 1
 if not results:print('No matches. Try --families or use the exact English name.');return 1
 for r in results:
  print(f'## {r["name"]}  [{r["id"]}]')
  print(f'Category: {r["category"]} | Family: {r["family"]} | Evidence: {r["confidence"]}')
  print('Описание:',r['description_ru'])
  print('Распознавание:',r['identification_ru'])
  print('Подтверждение:',r['confirmation_ru'])
  print('Ошибки/отмена:',r['failure_ru'])
  print('Особенности:',r['variant_note_ru'])
  print('Source:',r['verified_detail_url'] or r['source_index_url'])
  if r['example']:print('Original schematic:',str(CATALOG.parent.parent/r['example']))
  print()
 return 0
if __name__=='__main__':sys.exit(run())
