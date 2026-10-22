"""Metadata-level tests; these do not claim source-page content verification."""
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/pattern-atlas'
sys.path.insert(0,str(SKILL/'scripts'))
from search_catalog import find

class CatalogTests(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((SKILL/'data/catalog.json').read_text(encoding='utf8'))
  self.records=self.data['records']

 def test_counts(self):
  self.assertEqual(383,len(self.records))
  self.assertEqual(334,sum(bool(x['example']) for x in self.records))
  self.assertEqual(35,sum(bool(x['verified_detail_url']) for x in self.records))
  self.assertEqual(38,len(json.loads((SKILL/'data/families.json').read_text(encoding='utf8'))))

 def test_unique_ids(self):
  self.assertEqual(len(self.records),len(set(x['id'] for x in self.records)))

 def test_lookup_and_exact(self):
  r=find('ascending triangles')
  self.assertTrue(r)
  self.assertEqual('Ascending triangles',r[0]['name'])
  self.assertEqual('triangles',r[0]['family'])
  self.assertTrue(find('double',kind='pattern'))
  self.assertFalse(find('zzqqnotrealpattern987'))

 def test_unique_definition_not_faked(self):
  r=next(x for x in self.records if x['name']=='3L-R')
  self.assertEqual('family_level',r['confidence'])
  self.assertIsNone(r['verified_detail_url'])
  self.assertFalse(r['automatic_detection_implemented'])

 def test_assets(self):
  for r in self.records:
   self.assertTrue((SKILL/'patterns'/(r['id']+'.md')).is_file())
   if r['example']:
    self.assertTrue((SKILL/r['example']).is_file())
   if r['category']=='pattern':self.assertIsNotNone(r['example'])

if __name__=='__main__':unittest.main()
