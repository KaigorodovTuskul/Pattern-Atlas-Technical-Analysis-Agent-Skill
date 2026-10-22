import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/pattern-atlas/scripts'))
from scan_ohlcv import load_csv,scan_bars,scan_confirmed_double,pivots,scan


def row(i,lo,hi,close=None):
 c=(hi+lo)/2 if close is None else close
 return {'date':f'2024-01-{i+1:02d}','open':c,'high':hi,'low':lo,'close':c}

class ScannerTests(unittest.TestCase):
 def test_precise_bar_rules(self):
  bars=[row(0,90,110),row(1,94,106),row(2,88,112),row(3,115,125),row(4,120,123)]
  result=scan_bars(bars)
  event={(x['pattern'],x['bar_index']) for x in result}
  self.assertIn(('inside_day',1),event)
  self.assertIn(('outside_day',2),event)
  self.assertIn(('full_gap_up',3),event)
  self.assertIn(('inside_day',4),event)
  self.assertIn(('nr4',4),event)
  self.assertNotIn(('full_gap_up',2),event)

 def test_strict_width_ties(self):
  bars=[row(i,90,100) for i in range(7)]
  self.assertFalse(any(x['pattern'].startswith('nr') for x in scan_bars(bars)))

 def test_pivots_become_known_after_right_bars(self):
  closing=[120,118,116,113,110,100,110,115,120,122,118,112,107,101,109,114,120,124,125]
  bars=[row(i,c-1,c+1,c) for i,c in enumerate(closing)]
  highs,lows=pivots(bars)
  self.assertIn((5,7),lows)
  self.assertIn((13,15),lows)
  event=[x for x in scan_confirmed_double(bars) if x['pattern']=='double_bottom']
  self.assertTrue(event)
  self.assertGreaterEqual(event[0]['bar_index'],15)
  self.assertTrue(event[0]['heuristic'])

 def test_bad_data_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a.csv'
   p.write_text('date,open,high,low,close\n2024-01-02,101,102,100,101\n2024-01-01,101,102,100,101\n',encoding='utf8')
   with self.assertRaisesRegex(ValueError,'strictly increasing'):load_csv(p)
   p.write_text('date,open,high,low,close\n2024-01-01,103,102,100,101\n',encoding='utf8')
   with self.assertRaisesRegex(ValueError,'Inconsistent'):load_csv(p)

 def test_example_data_runs(self):
  rows=load_csv(ROOT/'examples/demo_ohlcv.csv')
  self.assertGreater(len(rows),20)
  self.assertIsInstance(scan(rows),list)

if __name__=='__main__':unittest.main()
