"""Content contract; static source evidence is not a native gameplay receipt."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'content/butchering'
CHAPTERS = PACK / 'assets/questline/questline/chapters'

class ButcheringTests(unittest.TestCase):
    def test_journey_and_action_semantics(self):
        chapter = json.loads((CHAPTERS / 'butchering.json').read_text())
        quests = {q['id']: q for q in chapter['quests']}
        spine = ['butchering-prepare', 'butchering-hook', 'butchering-table', 'butchering-retrieve', 'butchering-bleed', 'butchering-process']
        for a, b in zip(spine, spine[1:]):
            self.assertEqual(a, quests[b]['requires'])
        for q in quests.values():
            self.assertEqual([{'type': 'item', 'item': 'questline:questcookie', 'count': 1}], q['rewards'])
            self.assertTrue(all(t['type'] in ('obtain', 'craft') for t in q['tasks']))
        self.assertNotIn('butchering-blood', str(quests['butchering-process']['requires']))
        self.assertEqual(['butchering'], chapter['requiresMod'])
        en = json.loads((PACK / 'assets/questline/lang/en.json').read_text())
        self.assertIn(chapter['id'] + '-title', en)
        self.assertEqual('butchering:butcherhook-flint-north', chapter['icon'])
        self.assertGreaterEqual(len({q['icon'] for q in quests.values()}), 12)
        self.assertEqual(len(quests), len({tuple(q['pos']) for q in quests.values()}))

    def test_ci_and_release_count_every_owned_package(self):
        manifests = [ROOT / 'questline/modinfo.json']
        manifests += sorted((ROOT / 'content').glob('*/modinfo.json'))
        manifests += sorted((ROOT / 'compat').glob('*/modinfo.json'))
        package_count = len(manifests)
        self.assertEqual(12, package_count)
        ci = (ROOT / '.github/workflows/ci.yml').read_text()
        release = (ROOT / '.github/workflows/release.yml').read_text()
        self.assertIn(f'len(manifests) == len(expected) == {package_count}', ci)
        self.assertIn(f"-type f | wc -l)\" -eq {package_count}", release)
        self.assertIn(f'wc -l < Releases/SHA256SUMS)\" -eq {package_count}', release)
        self.assertIn(f"len(release['assets']) == {package_count + 1}", release)

    def test_only_hunt_is_replaced_and_localization_is_owned(self):
        docs = [json.loads(p.read_text()) for p in CHAPTERS.glob('*.json')]
        vanilla = {q['id']: q for p in (ROOT / 'content/vanilla/assets/questline/questline/chapters').glob('*.json') for q in json.loads(p.read_text())['quests']}
        replacements = [q for d in docs if 'extends' in d for q in d['quests'] if q['id'] in vanilla]
        self.assertEqual(['first-hunt'], [q['id'] for q in replacements])
        self.assertEqual(vanilla['first-hunt']['tasks'], replacements[0]['tasks'])
        en = json.loads((PACK / 'assets/questline/lang/en.json').read_text())
        core = json.loads((ROOT / 'questline/assets/questline/lang/en.json').read_text())
        self.assertFalse(set(core) & set(en))
        for d in docs:
            for q in d['quests']:
                if q['id'] != 'first-hunt':
                    self.assertIn(q['id'] + '-title', en)
                for block in q['page']:
                    self.assertIn(block['lang'], en)
        info = json.loads((PACK / 'modinfo.json').read_text())
        self.assertEqual('1.14.3', info['dependencies']['butchering'])

if __name__ == '__main__':
    unittest.main()
