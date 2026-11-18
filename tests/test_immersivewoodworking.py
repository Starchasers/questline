"""Offline authored-contract tests. Not a replacement for a native game smoke.
IW_SOURCE_PACK optionally replays every evidence excerpt against the original ZIP.
"""
import hashlib
import io
import json
import os

from pathlib import Path
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = Path('assets/questline/questline/chapters')
ADDON = ROOT / 'content/immersivewoodworking'
EVIDENCE = ROOT / 'docs/evidence/immersivewoodworking-1.3.13.json'
REPLACEMENTS = {'chop-wood', 'make-boards', 'weak-tannin', 'strong-tannin'}


def read(p):
    return json.loads(p.read_text())


def requires(q):
    v = q.get('requires', [])
    def flatten(value):
        if isinstance(value, str):
            return [value]
        if isinstance(value, dict):
            return [id for children in value.values() for id in flatten(children)]
        return [id for children in value for id in flatten(children)]
    return flatten(v)


class WoodworkingTests(unittest.TestCase):
    def setUp(self):
        self.docs = [read(p) for p in sorted((ADDON / CHAPTERS).glob('*.json'))]
        self.quests = {q['id']: q for d in self.docs for q in d['quests']}
        self.evidence = read(EVIDENCE)

    def test_scope_dependencies_and_no_resource_rewards(self):
        self.assertEqual((4, 26), (len(self.docs), len(self.quests)))
        self.assertEqual(REPLACEMENTS, {q['id'] for d in self.docs if 'extends' in d for q in d['quests']})
        self.assertEqual(22, sum(len(d['quests']) for d in self.docs if 'extends' not in d))
        for d in self.docs:
            self.assertEqual(['immersivewoodworking'], d['requiresMod'])
            for q in d['quests']:
                self.assertEqual([{'type': 'item', 'item': 'questline:questcookie', 'count': 1}], q['rewards'])
                self.assertEqual(1, len(q['tasks']))
                self.assertIn(q['tasks'][0]['type'], ('checkbox', 'obtain'))

    def test_merged_graph_has_no_missing_edges_or_cycles(self):
        merged = {q['id']: q for p in (ROOT / 'content/vanilla' / CHAPTERS).glob('*.json') for q in read(p)['quests']}
        merged.update(self.quests)
        done, active = set(), set()
        def visit(id):
            self.assertIn(id, merged, 'missing quest reference')
            self.assertNotIn(id, active, 'dependency cycle')
            if id in done:
                return
            active.add(id)
            for dep in requires(merged[id]):
                visit(dep)
            active.remove(id)
            done.add(id)
        for id in merged:
            visit(id)
        self.assertEqual(['iw-dry-bark', 'make-quern'], requires(self.quests['iw-crush-bark']))
        self.assertEqual(['make-barrel', 'iw-tanning-bark'], requires(self.quests['weak-tannin']))
        for id in ('iw-sawmill', 'iw-chopper'):
            self.assertIn('connect-power', requires(self.quests[id]))

    def test_localization_and_honest_detection(self):
        en = read(ROOT / 'questline/assets/questline/lang/en.json')
        for q in self.quests.values():
            key = q.get('page', [{}])[0].get('lang', q['id'] + '-desc')
            self.assertIn(key, en)
            desc = en[key]
            if q['tasks'][0]['type'] == 'checkbox':
                self.assertTrue('tick' in desc.lower() or q['id'] == 'iw-workshop', q['id'])
            if q['id'].startswith('iw-'):
                self.assertIn(q['id'] + '-title', en)
        for id in ('weak-tannin', 'strong-tannin'):
            self.assertEqual([{'type': 'checkbox'}], self.quests[id]['tasks'])
        self.assertIn('handbook://craftinginfo-woodworking', en['iw-workshop-desc'])
        self.assertNotIn('cannot make planks', en['iw-beams-desc'])

    def test_exact_captured_active_config_and_source_fingerprints(self):
        self.assertEqual('daafd4c1cb217b2553711128adfbd71511f5f0734cfb2927a6c4ffea02e0bb2d', self.evidence['pack']['sha256'])
        general = self.evidence['configs']['config/ModConfig/ImmersiveWoodworking/general.json']
        for key in ('EnableSawmill', 'EnableChopper', 'EnableBarkChain', 'AutoRestock',
                    'DisableVanillaFirewoodCrafting', 'DisableVanillaPlankCrafting',
                    'DisableVanillaLogTannin', 'AllowVanillaSaw'):
            self.assertIs(True, general[key], key)
        self.assertIs(False, general['CraftableSawhorse'])
        self.assertEqual(9, len(self.evidence['configs']))
        for asset in self.evidence['assets'].values():
            self.assertEqual(asset['sha256'], hashlib.sha256(asset['text'].encode()).hexdigest())
        handbook = '\n'.join(self.evidence['handbook'].values())
        self.assertIn('<hk>ctrl</hk>', handbook)
        self.assertIn('chute', handbook.lower())

    def test_item_and_icon_codes_match_captured_source_definitions(self):
        assets = self.evidence['assets']
        source = 'assets/immersivewoodworking/'
        known = set()
        for file, code, suffix in (
            ('blocktypes/choppingblock.json', 'choppingblock', ''),
            ('blocktypes/sawhorse.json', 'sawhorse', ''),
            ('blocktypes/sawmill/frame.json', 'sawmill', '-frame-north'),
            ('blocktypes/chopper/frame.json', 'chopper', '-frame-north'),
            ('itemtypes/barkcrushed.json', 'barkcrushed', ''),
        ):
            text = assets[source + file]['text']
            self.assertRegex(text, r'code\s*:\s*"' + code + '"')
            if suffix:
                self.assertIn('"frame"', text)
                self.assertIn('abstract/horizontalorientation', text)
                self.assertIn('"*-north"', text)
            known.add('immersivewoodworking:' + code + suffix)
        bark = assets[source + 'itemtypes/bark.json']['text']
        self.assertRegex(bark, r'code\s*:\s*"bark"')
        for kind in ('birch', 'tan'):
            for state in ('green', 'dry'):
                self.assertIn('"' + kind + '-' + state + '"', bark)
                known.add('immersivewoodworking:bark-' + kind + '-' + state)
        for q in self.quests.values():
            codes = [q.get('icon', '')] + [t.get('item', '') for t in q['tasks']]
            for code in codes:
                if code.startswith('immersivewoodworking:'):
                    self.assertIn(code, known, q['id'])

    @unittest.skipUnless(os.environ.get('IW_SOURCE_PACK'), 'set IW_SOURCE_PACK to replay private original archive')
    def test_original_archive_replays_all_captured_source_evidence(self):
        raw = Path(os.environ['IW_SOURCE_PACK']).read_bytes()
        self.assertEqual(self.evidence['pack']['sha256'], hashlib.sha256(raw).hexdigest())
        with zipfile.ZipFile(io.BytesIO(raw)) as pack:
            for name, data in self.evidence['configs'].items():
                self.assertEqual(data, json.loads(pack.read(name)))
            mod = pack.read(self.evidence['mod']['path'])
        self.assertEqual(self.evidence['mod']['sha256'], hashlib.sha256(mod).hexdigest())
        with zipfile.ZipFile(io.BytesIO(mod)) as iw:
            for name, asset in self.evidence['assets'].items():
                self.assertEqual(asset['sha256'], hashlib.sha256(iw.read(name)).hexdigest())
                self.assertEqual(asset['text'], iw.read(name).decode('utf-8-sig'))
            lang = json.loads(iw.read('assets/immersivewoodworking/lang/en.json'))
            self.assertEqual(self.evidence['handbook'], {k: v for k, v in lang.items() if 'handbook' in k})


if __name__ == '__main__':
    unittest.main()
