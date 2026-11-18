"""Offline contract for the single-mod questbook against upstream Git blobs; no game SDK needed."""
import collections
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "9a2fd4e2b2e24046de08c7a86aff335294558939"
BOOK = Path("questline/assets/questline/questline")
# Integrations for mods outside the target modpack; their chapters are not shipped.
REMOVED = {"betterruins": (1, 22), "charcoalkiln": (1, 6), "hexsmech": (2, 38), "seafarer": (3, 35)}
KEPT = {
    "vanilla": (25, 322), "bricklayers": (3, 24), "efchefstricks": (3, 4), "efmealsmodule": (1, 1),
    "expandedfoods": (8, 37), "fromgoldencombs": (1, 14), "tailorsdelight": (5, 21), "wool": (3, 8),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def blob(path):
    return git("show", f"{UPSTREAM}:{path}")


def group(payload):
    return next(iter(json.loads(payload).get("requiresMod", [])), "vanilla")


class QuestbookContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstream = {}
        for name in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines():
            if name.startswith(f"{BOOK}/chapters/") and name.endswith(".json"):
                cls.upstream[Path(name).name] = blob(name)
        cls.shipped = sorted((ROOT / BOOK / "chapters").glob("*.json"))

    def test_questbook_ships_inside_the_one_mod(self):
        self.assertFalse((ROOT / "content").exists())
        self.assertFalse((ROOT / "docs/content-packages.json").exists())
        self.assertEqual(blob(BOOK / "questline.json"), (ROOT / BOOK / "questline.json").read_bytes())
        manifests = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/modinfo.json"))
        manifests += sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("*/*/modinfo.json")
                            if "tests" not in p.parts and "bin" not in p.parts and "obj" not in p.parts)
        self.assertEqual(["questline/modinfo.json", "compat/toolsmith/modinfo.json"], manifests)
        info = json.loads((ROOT / "questline/modinfo.json").read_text())
        self.assertEqual(("questline", "code", {"game": "1.22.0"}),
                         (info["modid"], info["type"], info["dependencies"]))

    def test_shipped_chapters_are_upstream_bytes_and_only_unused_integrations_are_gone(self):
        self.assertEqual(56, len(self.upstream))
        groups = collections.defaultdict(list)
        for name, payload in self.upstream.items():
            groups[group(payload)].append(name)
        self.assertEqual(set(KEPT) | set(REMOVED), set(groups))
        expected = {name for key in KEPT for name in groups[key]}
        self.assertEqual(expected, {p.name for p in self.shipped})
        self.assertEqual(49, len(self.shipped))
        for path in self.shipped:
            with self.subTest(path=path.name):
                self.assertEqual(self.upstream[path.name], path.read_bytes())
        for key, (files, quests) in {**KEPT, **REMOVED}.items():
            with self.subTest(group=key):
                self.assertEqual(files, len(groups[key]))
                self.assertEqual(quests, sum(len(json.loads(self.upstream[n])["quests"]) for n in groups[key]))

    def test_no_shipped_quest_depends_on_a_removed_integration(self):
        removed = {name for name, payload in self.upstream.items() if group(payload) in REMOVED}
        removed_ids = {q["id"] for name in removed for q in json.loads(self.upstream[name])["quests"]}
        shipped_ids = {q["id"] for p in self.shipped for q in json.loads(p.read_bytes())["quests"]}
        only_removed = removed_ids - shipped_ids

        def refs(node):
            if isinstance(node, str):
                yield node
            elif isinstance(node, list):
                for item in node:
                    yield from refs(item)
            elif isinstance(node, dict):
                for key, value in node.items():
                    if key in ("quest", "all", "any", "of", "atLeast"):
                        yield from refs(value)

        for path in self.shipped:
            data = json.loads(path.read_bytes())
            self.assertNotIn(group(path.read_bytes()), REMOVED)
            for quest in data["quests"]:
                with self.subTest(quest=quest["id"]):
                    self.assertFalse(set(refs(quest.get("requires", []))) & only_removed)

    def test_totals_and_replacements(self):
        docs = [json.loads(p.read_bytes()) for p in self.shipped]
        ids = collections.Counter(q["id"] for d in docs for q in d["quests"])
        tasks = sum(len(q.get("tasks", [])) for d in docs for q in d["quests"])
        self.assertEqual((49, 431, 464, 415), (len(docs), sum(ids.values()), tasks, len(ids)))
        self.assertEqual(16, len([k for k, v in ids.items() if v > 1]))
        bases = {d["id"] if "id" in d else None for d in docs if "extends" not in d}
        for doc in docs:
            if "extends" in doc:
                self.assertIn(doc["extends"], bases)

    def test_shared_translations_remain_in_core_unchanged(self):
        prefix = "questline/assets/questline/lang/"
        names = [p for p in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines() if p.startswith(prefix)]
        self.assertTrue(names)
        for name in names:
            original = json.loads(blob(name))
            current = json.loads((ROOT / name).read_bytes())
            for key, value in original.items():
                self.assertIn(key, current, name)
                self.assertEqual(value, current[key], f"{name}:{key}")


if __name__ == "__main__":
    unittest.main()
