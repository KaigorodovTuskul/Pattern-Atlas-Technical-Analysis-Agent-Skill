import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from install import TARGETS, install

class InstallerTests(unittest.TestCase):
 def test_copy_and_protect(self):
  with tempfile.TemporaryDirectory() as d:
   expected=Path(d)/'.opencode/skills/pattern-atlas'
   dry=install(d,'opencode',dry_run=True)
   self.assertEqual(expected,dry)
   self.assertFalse(expected.exists())
   result=install(d,'opencode')
   self.assertTrue((result/'SKILL.md').is_file())
   self.assertTrue((result/'data/catalog.json').is_file())
   with self.assertRaises(FileExistsError):install(d,'opencode')
   again=install(d,'opencode',force=True)
   self.assertEqual(again,result)

 def test_bad_project_and_agent(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):install(d,'not-real')
   with self.assertRaises(ValueError):install(Path(d)/'absent','codex')

if __name__=='__main__':unittest.main()
