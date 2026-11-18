"""Website C252-C268 implementation contracts; possession is not machine-action proof."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'content/butchering/assets/questline'
NEW = {
    'butchering-javelin': ('obtain', 'item', 'armory:javelin-plain-*'),
    'butchering-knapped-hook': ('obtain', 'item', 'butchering:hook-flint'),
    'butchering-raw-slab': ('obtain', 'item', 'rusticcookery:meatslab-*-raw'),
    'butchering-rustic-rack': ('craft', 'block', 'rusticcookery:smokerack-*'),
    'butchering-smoked-slab': ('obtain', 'item', 'rusticcookery:meatslab-*-smoked'),
    'butchering-blood-sausage': ('craft', 'item', 'butchering:sausage-bloodsausage-raw'),
    'butchering-hide-glue': ('obtain', 'item', 'butchering:glueportion-hide-*'),
    'butchering-sinew-glue': ('obtain', 'item', 'butchering:glueportion-sinew-cold'),
    'butchering-metal-hook': ('obtain', 'item', 'butchering:@hook-(copper|tinbronze|bismuthbronze|blackbronze|iron)'),
    'butchering-smoking-rack': ('craft', 'block', 'butchering:smokingrack-*'),
    'butchering-simple-table': ('craft', 'block', 'butchering:butchertable-simple-*'),
    'butchering-advanced-table': ('craft', 'block', 'butchering:butchertable-advanced-*'),
    'butchering-prime': ('obtain', 'item', 'butchering:primemeat-raw'),
}

class Website(unittest.TestCase):
    def test_all_feasible_gaps_and_tier_specific_existing_tasks(self):
        quests = {q['id']: q for p in (PACK / 'questline/chapters').glob('*.json') for q in json.loads(p.read_text())['quests']}
        self.assertTrue(set(NEW) <= set(quests), set(NEW) - set(quests))
        for id, (type, kind, target) in NEW.items():
            self.assertEqual([{'type': type, kind: target, 'count': 1}], quests[id]['tasks'])
        self.assertEqual('butchering:butcherhook-flint-*', quests['butchering-hook']['tasks'][0]['block'])
        self.assertEqual('butchering:butchertable-primitive-*', quests['butchering-table']['tasks'][0]['block'])
        for provider, ids in [('armoryfork', ('javelin',)), ('rusticcookery', ('raw-slab', 'rustic-rack', 'smoked-slab'))]:
            extension = json.loads((PACK / ('questline/chapters/butchering-' + provider + '.json')).read_text())
            self.assertEqual(['butchering', provider], extension['requiresMod'])
            self.assertEqual('questline:butchering', extension['extends'])
            self.assertEqual({'butchering-' + id for id in ids}, {q['id'] for q in extension['quests']})
        self.assertEqual('butchering-process', quests['butchering-prime']['requires'])
        self.assertFalse(any('butchering-prime' in str(q.get('requires', '')) for q in quests.values()))

    def test_all_seventeen_candidates_reconciled_with_explicit_departures(self):
        ledger = json.loads((ROOT / 'docs/evidence/butchering-website-coverage.json').read_text())
        self.assertEqual(['C' + str(i) for i in range(252, 269)], [r['candidate_id'] for r in ledger['candidates']])
        for row in ledger['candidates']:
            self.assertTrue(row['quest_ids'])
            self.assertTrue(row['evidence'])
            self.assertIn(row['status'], ('implemented', 'reused', 'evidenced-departure'))
        for id in ('C258', 'C259', 'C260', 'C261', 'C268'):
            self.assertEqual('evidenced-departure', next(r for r in ledger['candidates'] if r['candidate_id'] == id)['status'])

if __name__ == '__main__':
    unittest.main()
