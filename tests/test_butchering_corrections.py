"""Regression contracts for automatic, output-based Butchering objectives."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'content/butchering/assets/questline'


def records():
    return [q for p in (PACK / 'questline/chapters').glob('*.json')
            for q in json.loads(p.read_text())['quests']]


class Corrections(unittest.TestCase):
    def test_all_definitions_have_semantic_icons_and_automatic_tasks(self):
        quests = records()
        self.assertEqual(35, len(quests))
        self.assertEqual(35, len({q['id'] for q in quests}))
        self.assertGreaterEqual(len({q['icon'] for q in quests}), 13)
        for q in quests:
            self.assertTrue(q['icon'])
            for task in q['tasks']:
                self.assertIn(task['type'], ('obtain', 'kill', 'craft'))
                self.assertTrue(task.get('item') or task.get('block') or task.get('entity'))
                self.assertFalse(task.get('consume', False))
        by_id = {q['id']: q for q in quests}
        self.assertEqual('butchering-retrieve', by_id['butchering-bleed']['requires'])
        self.assertEqual('butchering-table', by_id['butchering-blood']['requires'])
        self.assertEqual('butchering:dead*-dead', by_id['butchering-retrieve']['tasks'][0]['item'])
        self.assertEqual('butchering:dead*-bledout', by_id['butchering-bleed']['tasks'][0]['item'])
        self.assertEqual('craft', by_id['butchering-table']['tasks'][0]['type'])
        for id in ('hook', 'table'):
            self.assertIn('block', by_id['butchering-' + id]['tasks'][0])
        en = json.loads((PACK / 'lang/en.json').read_text())
        self.assertNotIn('Tick ', ' '.join(en.values()))
        for q in quests:
            if q['id'] != 'first-hunt':
                self.assertTrue(en[q['id'] + '-desc'].strip())

    def test_native_links_have_known_destinations_and_optional_guards(self):
        en = json.loads((PACK / 'lang/en.json').read_text())
        all_ids = {q['id'] for p in (ROOT / 'content').glob('*/assets/questline/questline/chapters/*.json')
                   for q in json.loads(p.read_text()).get('quests', [])}
        optional_links = 0
        for q in records():
            for block in q['page']:
                text = en.get(block.get('lang'), '')
                for target in re.findall(r'handbook://quest:questline:([^"<>]+)', text):
                    self.assertIn(target, all_ids)
                    if block.get('requiresMod'):
                        optional_links += 1
                        self.assertIn('questline:' + target, block['requiresQuest'])
        self.assertGreaterEqual(optional_links, 4)
        self.assertIn('handbook://butcheringguide', ' '.join(en.values()))
        self.assertIn('handbook://butcheringinfo', ' '.join(en.values()))

    def test_all_icons_and_objective_examples_match_pinned_asset_receipt(self):
        audit = json.loads((ROOT / 'docs/evidence/butchering-assets.json').read_text())
        quests = records()
        self.assertEqual({q['icon'] for q in quests}, set(audit['icons']))
        self.assertEqual({'butcheringguide', 'butcheringinfo'}, set(audit['guides'].values()))
        for q in quests:
            if q['id'] == 'first-hunt':
                continue
            example = audit['taskExamples'][q['id']]
            task = q['tasks'][0]
            kind = 'block' if 'block' in task else 'item'
            self.assertEqual(kind, example['kind'])
            domain, pattern = task[kind].split(':', 1)
            code_domain, code = example['code'].split(':', 1)
            self.assertEqual(domain, code_domain)
            regex = pattern[1:] if pattern.startswith('@') else re.escape(pattern).replace(r'\*', '.*')
            self.assertRegex(code, '^' + regex + '$')
        en = json.loads((PACK / 'lang/en.json').read_text())
        self.assertIn('whole litre', en['butchering-blood-desc'])
        self.assertIn('corpse', en['butchering-retrieve-desc'].lower())
        self.assertIn('80%', en['butchering-table-desc'])

    def test_audited_icon_and_target_ledger_is_complete(self):
        ledger = json.loads((ROOT / 'docs/evidence/butchering-objectives.json').read_text())
        quests = {q['id']: q for q in records()}
        self.assertEqual(set(quests), set(ledger['quests']))
        for id, q in quests.items():
            self.assertEqual(q['icon'], ledger['quests'][id]['icon'])
            self.assertEqual(q['tasks'], ledger['quests'][id]['tasks'])
            self.assertTrue(ledger['quests'][id]['source'])
            self.assertTrue(ledger['quests'][id]['proves'])


if __name__ == '__main__':
    unittest.main()
