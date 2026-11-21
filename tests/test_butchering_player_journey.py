"""Player-facing Butchering 0.15.0 progression regressions."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'content/butchering'


class PlayerJourney(unittest.TestCase):
    def setUp(self):
        self.docs = [json.loads(p.read_text()) for p in (PACK / 'assets/questline/questline/chapters').glob('*.json')]
        self.quests = {q['id']: q for d in self.docs for q in d['quests']}
        self.en = json.loads((PACK / 'assets/questline/lang/en.json').read_text())

    def test_javelin_removed_and_knapping_required(self):
        self.assertNotIn('butchering-javelin', self.quests)
        self.assertNotIn('butchering-javelin', json.dumps(self.en))
        self.assertIn('butchering-knapped-hook', str(self.quests['butchering-hook']['requires']))

    def test_player_prose_has_no_research_or_tracking_disclaimers(self):
        text = ' '.join(self.en.values()).lower()
        for phrase in ('pinned', 'automatic credit', 'proves possession', 'proof of',
                       'not tracked', 'tracker', 'not scanned', 'inspected', 'verified here',
                       'existing saves', 'does not verify', 'source-backed', 'milestone'):
            self.assertNotIn(phrase, text)
        self.assertEqual('0.15.0', json.loads((PACK / 'modinfo.json').read_text())['version'])

    def test_plain_titles_and_independent_product_branches(self):
        for key, value in self.en.items():
            if key.endswith('-title'):
                self.assertFalse(value.lower().startswith(('obtain ', 'craft ', 'an optional ', 'a ', 'an ')), (key, value))
        for id in ('offal', 'sinew', 'prime', 'bones', 'bag'):
            self.assertEqual('butchering-process', self.quests['butchering-' + id]['requires'])
        self.assertEqual('butchering-sinew', self.quests['butchering-sinew-glue']['requires'])
        self.assertEqual('butchering-offal', self.quests['butchering-blood-sausage']['requires'])

    def test_ordered_station_rows_and_age_gates(self):
        q = self.quests
        self.assertEqual('make-knife', q['butchering-table']['requires'])
        self.assertEqual('butchering-table', q['butchering-prepare']['requires'])
        self.assertEqual('butchering-knapped-hook', q['butchering-hook']['requires'])
        rows = [
            ('butchering-table', 'butchering-simple-table', 'butchering-advanced-table'),
            ('butchering-knapped-hook', 'butchering-metal-hook', 'butchering-bronze-component', 'butchering-iron-component'),
            ('butchering-hook', 'butchering-copper-skinning-hook', 'butchering-bronze-skinning-hook', 'butchering-iron-skinning-hook'),
        ]
        for row in rows:
            for prev, current in zip(row, row[1:]):
                self.assertIn(prev, str(q[current]['requires']))
                self.assertGreater(q[current]['pos'][0], q[prev]['pos'][0])
                self.assertEqual(q[current]['pos'][1], q[prev]['pos'][1])
        for tier, gate, rate in [('copper', 'first-smithing', '100%'), ('bronze', 'alloy-bronze', '100%'), ('iron', 'smith-iron', '120%')]:
            for station in ('skinning-hook', 'ceiling-hook'):
                id = 'butchering-' + tier + '-' + station
                self.assertIn(gate, str(q[id]['requires']))
                self.assertIn(rate, self.en[id + '-desc'])
        self.assertIn('80%', self.en['butchering-table-desc'])
        self.assertIn('80%', self.en['butchering-hook-desc'])
        self.assertEqual('butchering-process', q['butchering-smoking-rack']['requires'][0])
        # Ceiling variants are side leaves. Tier-row progression may only lead to its next tier or matching station.
        for tier in ('copper', 'bronze', 'iron'):
            ceiling = 'butchering-' + tier + '-ceiling-hook'
            self.assertFalse(any(ceiling in str(other.get('requires', '')) for other in q.values()))
        main_ids = {'butchering-prepare','butchering-knapped-hook','butchering-hook','butchering-retrieve','butchering-bleed','butchering-process'}
        upgrades = set(q) - main_ids - {'butchering-table'}
        for id in main_ids:
            self.assertFalse(any(upgrade in str(q[id].get('requires','')) for upgrade in upgrades))

    def test_station_rates_match_asset_receipt(self):
        receipt = json.loads((ROOT / 'docs/evidence/butchering-assets.json').read_text())
        self.assertEqual({'butcheringTableLootMultiplier': 1.0, 'SkinningRackLootMultiplier': 1.0}, receipt['configuredStationMultipliers'])
        patterns = {'table': 'butchertable-primitive-*', 'hook': 'butcherhook-flint-*',
                    'simple-table': 'butchertable-simple-*', 'advanced-table': 'butchertable-advanced-*'}
        for tier, materials in [('copper', ['copper']), ('bronze', ['tinbronze','bismuthbronze','blackbronze']), ('iron', ['iron'])]:
            for station, code in [('skinning-hook','butcherhook'),('ceiling-hook','butcherhookceiling')]:
                id = tier + '-' + station
                for metal in materials:
                    rate = round(receipt['stationDropMultipliers'][f'{code}-{metal}-*'] * 100)
                    self.assertIn(f'{rate}%', self.en['butchering-' + id + '-desc'])
        for id, pattern in patterns.items():
            rate = round(receipt['stationDropMultipliers'][pattern] * 100)
            self.assertIn(f'{rate}%', self.en['butchering-' + id + '-desc'])

    def test_hide_page_links_to_leatherworking(self):
        page = self.quests['butchering-skin']['page']
        self.assertTrue(any(b.get('lang') == 'butchering-leather-links' for b in page))
        self.assertIn('handbook://quest:questline:soak-hide', self.en['butchering-leather-links'])
        self.assertIn('handbook://quest:questline:make-leather', self.en['butchering-leather-links'])


if __name__ == '__main__':
    unittest.main()
