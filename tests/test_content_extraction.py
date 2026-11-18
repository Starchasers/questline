"""Offline contract for the single-mod questbook against upstream Git blobs; no game SDK needed.

Chapters are regrouped for the modpack, so files no longer match upstream byte for byte.
Every quest record does: ID, tasks, prerequisites, rewards, page and presentation are
upstream's, with the upstream extension replacements applied. Only `pos` and the chapter a
quest sits in are this fork's.
"""
import collections
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "9a2fd4e2b2e24046de08c7a86aff335294558939"
BOOK = Path("questline/assets/questline/questline")
LANG = ROOT / "questline/assets/questline/lang"
# Integrations for mods outside the target modpack; their quests are not shipped.
REMOVED = {"betterruins", "charcoalkiln", "hexsmech", "seafarer"}
AGES = ["first-days", "clay-and-fire", "copper-age", "bronze-age", "iron-age", "steel-age"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def refs(node):
    if isinstance(node, str):
        yield node.split(":")[-1]
    elif isinstance(node, list):
        for item in node:
            yield from refs(item)
    elif isinstance(node, dict):
        for key, value in node.items():
            if key in ("quest", "all", "any", "of", "atLeast"):
                yield from refs(value)


class QuestbookContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        docs = []
        for name in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines():
            if name.startswith(f"{BOOK}/chapters/") and name.endswith(".json"):
                docs.append(json.loads(git("show", f"{UPSTREAM}:{name}")))
        kept = [d for d in docs if not set(d.get("requiresMod", [])) & REMOVED]
        cls.expected = {}
        for doc in sorted(kept, key=lambda d: "extends" in d):  # base records first, replacements win
            for quest in doc["quests"]:
                cls.expected[quest["id"]] = quest
        cls.shipped = [json.loads(p.read_bytes()) for p in sorted((ROOT / BOOK / "chapters").glob("*.json"))]
        cls.files = sorted(p.stem for p in (ROOT / BOOK / "chapters").glob("*.json"))

    def test_questbook_ships_inside_the_one_mod(self):
        self.assertFalse((ROOT / "content").exists())
        self.assertFalse((ROOT / "docs/content-packages.json").exists())
        self.assertEqual(git("show", f"{UPSTREAM}:{BOOK / 'questline.json'}"),
                         (ROOT / BOOK / "questline.json").read_bytes())
        info = json.loads((ROOT / "questline/modinfo.json").read_text())
        self.assertEqual(("questline", "code", {"game": "1.22.0"}),
                         (info["modid"], info["type"], info["dependencies"]))

    def test_every_upstream_quest_is_shipped_once_and_unchanged_except_position(self):
        self.assertEqual(415, len(self.expected))
        seen = collections.Counter(q["id"] for d in self.shipped for q in d["quests"])
        self.assertEqual(set(self.expected), set(seen))
        self.assertEqual(1, max(seen.values()))
        for doc in self.shipped:
            for quest in doc["quests"]:
                with self.subTest(quest=quest["id"]):
                    want = {k: v for k, v in self.expected[quest["id"]].items() if k != "pos"}
                    self.assertEqual(want, {k: v for k, v in quest.items() if k != "pos"})

    def test_chapters_are_plain_ungated_and_laid_out(self):
        self.assertEqual(29, len(self.shipped))
        self.assertEqual(self.files, sorted(d["id"] for d in self.shipped))
        orders = [d["order"] for d in self.shipped]
        self.assertEqual(len(orders), len(set(orders)))
        self.assertEqual(AGES, [d["id"] for d in sorted(self.shipped, key=lambda d: d["order"]) if d.get("age")])
        english = json.loads((LANG / "en.json").read_text(encoding="utf-8"))
        for doc in self.shipped:
            with self.subTest(chapter=doc["id"]):
                self.assertEqual({"id", "order", "icon", "quests"}, set(doc) - {"age"})
                self.assertIn(f"{doc['id']}-title", english)
                self.assertTrue(doc["quests"])
                positions = [tuple(q["pos"]) for q in doc["quests"]]
                self.assertEqual(len(positions), len(set(positions)), "two quests share a cell")
                inside = {q["id"]: q["pos"][0] for q in doc["quests"]}
                for quest in doc["quests"]:
                    for need in refs(quest.get("requires", [])):
                        if need in inside and need != quest["id"]:
                            self.assertLess(inside[need], inside[quest["id"]], "prerequisite must sit to the left")

    def test_every_prerequisite_resolves(self):
        ids = {q["id"] for d in self.shipped for q in d["quests"]}
        for doc in self.shipped:
            for quest in doc["quests"]:
                with self.subTest(quest=quest["id"]):
                    self.assertFalse(set(refs(quest.get("requires", []))) - ids)

    def test_shared_translations_remain_in_core_unchanged(self):
        prefix = "questline/assets/questline/lang/"
        names = [p for p in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines() if p.startswith(prefix)]
        self.assertTrue(names)
        for name in names:
            original = json.loads(git("show", f"{UPSTREAM}:{name}"))
            current = json.loads((ROOT / name).read_bytes())
            for key, value in original.items():
                self.assertIn(key, current, name)
                self.assertEqual(value, current[key], f"{name}:{key}")


if __name__ == "__main__":
    unittest.main()
