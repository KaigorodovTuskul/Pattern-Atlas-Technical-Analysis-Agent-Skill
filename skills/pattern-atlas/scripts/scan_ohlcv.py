#!/usr/bin/env python3
"""Deliberately limited, deterministic, offline OHLCV screen; not an encyclopedia-wide detector."""
import argparse, csv, json, math, sys
from pathlib import Path

def load_csv(path):
 with open(path,encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f)
  required={'date','open','high','low','close'}
  if reader.fieldnames is None or not required.issubset(reader.fieldnames):
   raise ValueError('Required CSV columns: date,open,high,low,close (volume optional)')
  bars=[]
  for line,r in enumerate(reader,2):
   try:
    item={'date':r['date'],'open':float(r['open']),'high':float(r['high']),'low':float(r['low']),'close':float(r['close'])}
    if 'volume' in reader.fieldnames and r.get('volume') not in (None,''):item['volume']=float(r['volume'])
   except (ValueError,TypeError) as e:raise ValueError(f'Bad numeric data at CSV line {line}') from e
   if not item['date'] or not all(math.isfinite(x) for x in item.values() if isinstance(x,float)):
    raise ValueError(f'Missing date or nonfinite data at {line}')
   if item['low']>min(item['open'],item['close'],item['high']) or item['high']<max(item['open'],item['close'],item['low']) or item['low']<=0:
    raise ValueError(f'Inconsistent OHLC or nonpositive price at {line}')
   if 'volume' in item and item['volume']<0:raise ValueError(f'Negative volume at {line}')
   if bars and item['date']<=bars[-1]['date']:
    raise ValueError('Date must be strictly increasing in sortable ISO 8601 format; duplicate bar dates rejected')
   bars.append(item)
 if not bars:raise ValueError('No rows')
 return bars

def evt(pattern, direction, bar, date, detail,**kwargs):
 return {'pattern':pattern,'direction':direction,'bar_index':bar,'detected_at':date,'detail':detail,**kwargs}

def scan_bars(bars):
 events=[]
 for i,b in enumerate(bars):
  if i==0:continue
  prev=bars[i-1]
  if b['high']<prev['high'] and b['low']>prev['low']:
   events.append(evt('inside_day','neutral',i,b['date'],'Strict inside range; next-bar breakout not assumed.'))
  if b['high']>prev['high'] and b['low']<prev['low']:
   events.append(evt('outside_day','neutral',i,b['date'],'Strict outside range; bullish/bearish depends on context.'))
  if b['low']>prev['high']:
   events.append(evt('full_gap_up','up',i,b['date'],'Today low exceeds previous high; session gaps depend on corporate-action adjustments.'))
  elif b['high']<prev['low']:
   events.append(evt('full_gap_down','down',i,b['date'],'Today high below previous low; do not label exhaustion/breakaway automatically.'))
  width=b['high']-b['low']
  for period in (4,7):
   if i+1>=period and all(width<bars[j]['high']-bars[j]['low'] for j in range(i-period+1,i)):
    events.append(evt(f'nr{period}','neutral',i,b['date'],f'Strict narrowest range across {period} consecutive bars (ties excluded).'))
 return events

def pivots(bars,left=2,right=2):
 """Pivot becomes *known* only after right bars have closed. Return (pivot index, confirmation index)."""
 highs=[];lows=[]
 for i in range(left,len(bars)-right):
  if all(bars[i]['high']>bars[j]['high'] for j in range(i-left,i)) and all(bars[i]['high']>=bars[j]['high'] for j in range(i+1,i+right+1)):
   highs.append((i,i+right))
  if all(bars[i]['low']<bars[j]['low'] for j in range(i-left,i)) and all(bars[i]['low']<=bars[j]['low'] for j in range(i+1,i+right+1)):
   lows.append((i,i+right))
 return highs,lows

def scan_confirmed_double(bars,tolerance=0.035,min_sep=4,max_sep=70):
 """Heuristic confirmed double reversals. Avoid retrospective using unavailable pivot points."""
 hi,lo=pivots(bars);out=[]
 for kind,sets,pricekey,direction in [('double_bottom',lo,'low','up'),('double_top',hi,'high','down')]:
  for idx,(p1,c1) in enumerate(sets):
   for p2,c2 in sets[idx+1:]:
    distance=p2-p1
    if distance<min_sep:continue
    if distance>max_sep:break
    a,b=bars[p1][pricekey],bars[p2][pricekey]
    if abs(a-b)/max(abs(a),abs(b))>tolerance:continue
    middle=bars[p1+1:p2]
    if not middle:continue
    neckline=max(x['high'] for x in middle) if direction=='up' else min(x['low'] for x in middle)
    height=(neckline-min(a,b)) if direction=='up' else (max(a,b)-neckline)
    if height<=0.03*(max(a,b)):continue
    # Require neckline away from pivot level, confirmation after pivot becomes observable.
    confirm_from=max(p2+1,c2)
    for k in range(confirm_from,len(bars)):
     close=bars[k]['close']
     crossed=close>neckline if direction=='up' else close<neckline
     if crossed:
      out.append(evt(kind,direction,k,bars[k]['date'],f'Candidate two-extrema confirmation; extrema at {bars[p1]["date"]}/{bars[p2]["date"]}.',pivot_dates=[bars[p1]['date'],bars[p2]['date']],neckline=round(neckline,6),height=round(height,6),pivot_known_after=bars[c2]['date'],heuristic=True))
      break
  # deduplicate confirmations of repeated overlapping candidate pairs by kind and date
 seen=set();filtered=[]
 for e in sorted(out,key=lambda e:(e['bar_index'],e['pattern'])):
  key=(e['pattern'],e['detected_at'])
  if key not in seen:filtered.append(e);seen.add(key)
 return filtered

def scan(bars,include_double=True):
 result=scan_bars(bars)
 if include_double:result+=scan_confirmed_double(bars)
 return sorted(result,key=lambda e:(e['bar_index'],e['pattern']))

def run(argv=None):
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('csv_path',type=Path)
 ap.add_argument('--no-double',action='store_true')
 ap.add_argument('--output',type=Path)
 args=ap.parse_args(argv)
 try:bars=load_csv(args.csv_path);events=scan(bars,not args.no_double)
 except (ValueError,OSError) as err:ap.error(str(err))
 data={'tool':'pattern-atlas-ohlcv-screen','bars':len(bars),'events':events,'limitations':['Only inside/outside days, strict NR4/NR7, full-range gaps and heuristic confirmed double extrema are implemented.','Confirmation uses a completed pivot window to avoid look-ahead; this is not an optimized trading strategy.','No accuracy/profit claims, no corporate action calendar handling, no market-data access.','Event classification such as earnings/exhaustion and most catalog patterns requires separate research.']}
 payload=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
 if args.output:args.output.write_text(payload,encoding='utf-8');print(f'Wrote {args.output}')
 else:print(payload,end='')
 return 0
if __name__=='__main__':sys.exit(run())
