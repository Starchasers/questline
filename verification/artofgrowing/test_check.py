#!/usr/bin/env python3
"""Fail-closed regression tests mutate loaded data only, never shipped content."""
import copy
import unittest
from unittest.mock import patch
import check as audit


class AssetContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = audit.validate_ledger()
        cls.keys = {p["key"] for p in audit.read(audit.ROOT / "docs/content-packages.json")["packages"]} - {"artofgrowing"}
        cls.patches = sorted((audit.ADDON / "assets" / audit.DOMAIN / "patches").rglob("*.json"))
        if not cls.patches:
            raise AssertionError("shipped AoG patches must exist before negative contract tests run")

    def mutation(self, transform, expected):
        original = audit.read
        target = self.patches[0]
        data = copy.deepcopy(original(target))
        transform(data)
        with patch.object(audit, "read", side_effect=lambda p: copy.deepcopy(data) if p == target else original(p)):
            with self.assertRaisesRegex(AssertionError, expected):
                audit.corpus(self.keys)

    def test_stale_ledger_fingerprint_fails(self):
        original = audit.read
        path = audit.ROOT / "docs/artofgrowing-impact-ledger.json"
        data = copy.deepcopy(original(path))
        data["records"][0]["sha256"] = "0" * 64
        with patch.object(audit, "read", side_effect=lambda p: data if p == path else original(p)):
            with self.assertRaisesRegex(AssertionError, "stale source audit"):
                audit.validate_ledger()

    def test_missing_provider_gate_fails(self):
        def mutate(data):
            data[0]["dependsOn"] = [g for g in data[0].get("dependsOn", []) if g["modid"] != "artofgrowingpatch"]
        self.mutation(mutate, "missing actual AoG modid gate")

    def test_provider_asset_domain_is_not_modid(self):
        def mutate(data):
            data[0]["dependsOn"].append({"modid": "artofgrowing"})
        self.mutation(mutate, "asset domain used as mod gate")

    def test_changed_saved_id_fails(self):
        self.mutation(lambda d: d[0]["value"].update(id="invented-stale-id"), "stale index or changed saved ID")

    def test_duplicate_override_fails(self):
        self.mutation(lambda d: d.insert(1, copy.deepcopy(d[0])), "competing/stale override")

    def test_nonindexed_or_partial_override_fails(self):
        self.mutation(lambda d: d[0].update(path="/quests/0/tasks"), "indexed whole-record replacement")

    def test_unimplemented_patch_operation_fails(self):
        self.mutation(lambda d: d[0].update(op="add"), "unsupported patch operation")

    def test_provider_absent_applies_no_patches(self):
        self.assertEqual([], audit.corpus(self.keys, addon=True, provider=False)["edits"])


if __name__ == "__main__":
    unittest.main()
