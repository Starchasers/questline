"""Source/content contracts; real QuestLoader presence matrix lives in composition harness."""
import copy
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / 'content/betterhusbandry/assets/questline/questline/chapters'
def load(p):
    return json.loads(p.read_text())

class BetterHusbandryTests(unittest.TestCase):
    def test_provider_dependency_and_catalog(self):
        info = load(ROOT / 'content/betterhusbandry/modinfo.json')
        self.assertEqual(info['dependencies']['betterhusbandry'], '1.4.0')
        package = next(p for p in load(ROOT / 'docs/content-packages.json')['packages'] if p['key'] == 'betterhusbandry')
        self.assertEqual(package['dependencies'], info['dependencies'])
        self.assertEqual(package['chapters'], sorted(p.name for p in CHAPTERS.glob('*.json')))

    def test_existing_saved_records_change_only_page(self):
        vanilla = {q['id']: q for q in load(ROOT / 'content/vanilla/assets/questline/questline/chapters/husbandry.json')['quests']}
        records = load(CHAPTERS / 'betterhusbandry-husbandry.json')['quests']
        replacements = [q for q in records if q['id'] in vanilla]
        self.assertEqual({q['id'] for q in replacements}, {'make-trough','make-large-trough','breed-animals','milk-animal'})
        for q in replacements:
            original, replacement = copy.deepcopy(vanilla[q['id']]), copy.deepcopy(q)
            original.pop('page', None); replacement.pop('page', None)
            self.assertEqual(q['page'][0], {'type':'text','lang':q['id']+'-desc'})
            self.assertEqual(original, replacement)

    def test_new_observations_are_manual_and_gated(self):
        ids = set()
        for p in CHAPTERS.glob('*.json'):
            chapter = load(p)
            self.assertEqual(chapter['extends'], 'husbandry')
            self.assertIn('betterhusbandry', chapter['requiresMod'])
            for q in chapter['quests']:
                self.assertNotIn(q['id'], ids); ids.add(q['id'])
                if q['id'].startswith('bh-'):
                    self.assertEqual(q['tasks'], [{'type':'checkbox'}])
                    self.assertNotIn('rewards', q)
        self.assertEqual(len(ids),11)
        self.assertEqual(load(CHAPTERS/'betterhusbandry-welfare.json')['requiresMod'], ['betterhusbandry','livestockwelfare'])
        self.assertEqual(load(CHAPTERS/'betterhusbandry-wool.json')['requiresMod'], ['betterhusbandry','wool','shearlib','questlinewool'])

    def test_all_text_is_reachable_and_fallbacks_explicit(self):
        english = load(ROOT/'questline/assets/questline/lang/en.json')
        keys = set()
        for p in CHAPTERS.glob('*.json'):
            for q in load(p)['quests']:
                if q['id'].startswith('bh-'):
                    keys.update([q['id']+'-title',q['id']+'-desc'])
                keys.update(b['lang'] for b in q.get('page',[]) if b.get('lang','').startswith('bh-'))
        self.assertEqual(len(keys),18)
        for p in (ROOT/'questline/assets/questline/lang').glob('*.json'):
            data=load(p)
            for key in keys:
                self.assertTrue(english[key].strip()); self.assertEqual(data[key],english[key])

    def test_configuration_caveats_remain_visible(self):
        e=load(ROOT/'questline/assets/questline/lang/en.json')
        self.assertIn('RequireBedding',e['bh-breed-animals-guidance'])
        self.assertIn('not a cap',e['bh-offline-plan-desc'])
        self.assertIn('two game days',e['bh-offline-plan-desc'])
        self.assertIn('prefix',e['bh-shearing-care-desc'])
        self.assertIn('Manual:',e['bh-observe-care-change-desc'])
        self.assertIn('possession',e['bh-milk-animal-guidance'])

if __name__ == '__main__':
    unittest.main()
