from pathlib import Path
import json,re,unittest,hashlib,zipfile,io,os
ROOT=Path(__file__).resolve().parents[1]
CHAPTER=ROOT/'content/livestockwelfare/assets/questline/questline/chapters/livestockwelfare-care.json'
class WelfareTests(unittest.TestCase):
 def test_addon_contract_and_locales(self):
  c=json.loads(CHAPTER.read_text());self.assertEqual(['livestockwelfare'],c['requiresMod']);self.assertNotIn('extends',c)
  qs=c['quests'];self.assertEqual(16,len(qs));ids={q['id'] for q in qs};self.assertEqual(16,len(ids));self.assertEqual(16,len({tuple(q['pos']) for q in qs}))
  for q in qs:
   self.assertEqual([{'type':'checkbox'}],q['tasks']);self.assertNotIn('rewards',q)
   if 'requires' in q:self.assertIn(q['requires']['quest'].removeprefix('questline:'),ids)
  for f in (ROOT/'questline/assets/questline/lang').glob('*.json'):
   d=json.loads(f.read_text())
   for q in qs:
    self.assertIn(q['id']+'-title',d);self.assertIn(q['id']+'-desc',d)
  cat=json.loads((ROOT/'docs/content-packages.json').read_text());entry=next(p for p in cat['packages'] if p['key']=='livestockwelfare')
  info=json.loads((ROOT/entry['path']/'modinfo.json').read_text());self.assertEqual(entry['dependencies'],info['dependencies']);self.assertEqual('0.15.0',info['dependencies']['livestockwelfare']);self.assertNotIn('betterhusbandry',info['dependencies'])
 def test_source_fingerprints_and_retained_links(self):
  e=json.loads((ROOT/'docs/research/livestockwelfare-0.15.0-evidence.json').read_text());self.assertEqual('daafd4c1cb217b2553711128adfbd71511f5f0734cfb2927a6c4ffea02e0bb2d',e['pack']['sha256'])
  en=json.loads((ROOT/'questline/assets/questline/lang/en.json').read_text());text=' '.join(v for k,v in en.items() if k.startswith('lw-'))
  self.assertNotIn('item-livestockwelfare:chickencoop"',text);self.assertIn('handbook://livestockwelfare-guide',text);self.assertIn('Breeding.Enabled=false',text);self.assertIn('NOT RequireBedding=true',text)
  pack=os.environ.get('LIVESTOCK_WELFARE_PACK')
  if not pack:return # Static CI remains offline; exact retained archive audit is opt-in.
  b=Path(pack).read_bytes();self.assertEqual(e['pack']['sha256'],hashlib.sha256(b).hexdigest());z=zipfile.ZipFile(io.BytesIO(b));w=zipfile.ZipFile(io.BytesIO(z.read('mods/livestockwelfare_0.15.0.zip')))
  expected={'waterer-fired':'blocktypes/waterer.json','strawbedding-clean':'blocktypes/strawbedding.json','groomingbrush':'itemtypes/groomingbrush.json','chickencoop-oak':'itemtypes/chickencoop.json'}
  for code,f in expected.items():self.assertIn('assets/livestockwelfare/'+f,w.namelist());self.assertIn('livestockwelfare:'+code,text)
  self.assertRegex(w.read('assets/livestockwelfare/config/handbook/livestockwelfare.json').decode(),r'pageCode\s*:\s*"livestockwelfare-guide"')
if __name__=='__main__':unittest.main()
