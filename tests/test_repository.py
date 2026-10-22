import json
import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate import validate

class RepositoryTests(unittest.TestCase):
 def test_no_structure_problems(self):
  self.assertEqual([],validate())

 def test_gallery_embeds_offline_index(self):
  s=(ROOT/'gallery.html').read_text(encoding='utf8')
  matches=re.search(r'<script type="application/json" id="dataset">(.*?)</script>',s,re.S)
  self.assertIsNotNone(matches)
  arr=json.loads(matches.group(1))
  self.assertEqual(383,len(arr))
  self.assertIn('search',s)
  self.assertNotIn('<script src=',s)

 def test_behaviour_cases(self):
  a=json.loads((ROOT/'tests/evals.json').read_text(encoding='utf8'))['scenarios']
  self.assertGreaterEqual(len(a),6)
  self.assertEqual(len(set(x['id'] for x in a)),len(a))
  self.assertTrue(all(x['must'] and x['prompt'] for x in a))

if __name__=='__main__':unittest.main()
