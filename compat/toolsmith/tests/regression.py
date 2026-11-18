"""Source boundary checks; run before/after the Toolsmith extraction."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

class Extraction(unittest.TestCase):
    def test_core_has_no_provider_hooks(self):
        core = (ROOT / 'questline/Server/StationPatches.cs').read_text()
        self.assertNotIn('Toolsmith', core)
        self.assertIn('engine?.Report(serverPlayer, type, made.Collectible.Code', core)
        self.assertIn('static bool OnServer', core)

    def test_adapter_is_separate_server_mod(self):
        import json
        info = json.loads((ROOT / 'compat/toolsmith/modinfo.json').read_text())
        self.assertEqual('Server', info['side'])
        self.assertEqual('0.15.0', info['dependencies']['questline'])
        self.assertIn('toolsmith', info['dependencies'])
        self.assertTrue((ROOT / 'compat/toolsmith/QuestlineToolsmith.csproj').exists())

    def test_report_remains_custom_only(self):
        api = (ROOT / 'questline/QuestlineApi.cs').read_text()
        self.assertIn('engine.Report(player, "custom", new AssetLocation(key), amount)', api)
        self.assertIn('public bool ReportCraft(', api)
        self.assertIn('engine.Report(player, "craft", code, amount)', api)

if __name__ == '__main__':
    unittest.main()
