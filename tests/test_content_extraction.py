"""Offline structural contract against actual upstream Git blobs; no game SDK needed."""
import collections
import json
from functools import cache
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = "9a2fd4e2b2e24046de08c7a86aff335294558939"
LEGACY = Path("assets/questline/questline")
SOURCE = Path("questline") / LEGACY
REMOVED = {"betterruins", "charcoalkiln", "seafarer"}
GROUPS = {
    "vanilla": (25, 322), "bricklayers": (3, 24),
    "efchefstricks": (3, 4), "efmealsmodule": (1, 1),
    "expandedfoods": (8, 37), "fromgoldencombs": (1, 14), "hexsmech": (2, 38),
    "tailorsdelight": (5, 21), "wool": (3, 8),
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def blob(path):
    return git("show", f"{UPSTREAM}:{path}")


class ContentExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstream = {}
        for name in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines():
            if name.startswith(f"{SOURCE}/chapters/") and name.endswith(".json"):
                cls.upstream[Path(name).name] = blob(name)

    @classmethod
    def retained(cls):
        return {name: payload for name, payload in cls.upstream.items()
                if not REMOVED.intersection(json.loads(payload).get("requiresMod", []))}

    @classmethod
    @cache
    def removed_lang_keys(cls):
        # Conventional chapter/quest names, explicit art/page/task keys and provider structure labels.
        english = json.loads(blob("questline/assets/questline/lang/en.json"))
        def keys(payloads):
            found = set()
            def visit(value):
                if isinstance(value, str):
                    found.add(value.removeprefix("questline:"))
                elif isinstance(value, list):
                    for item in value: visit(item)
                elif isinstance(value, dict):
                    for item in value.values(): visit(item)
            for payload in payloads:
                chapter = json.loads(payload)
                found.add(chapter["id"] + "-title")
                for quest in chapter["quests"]:
                    found.update((quest["id"] + "-title", quest["id"] + "-desc"))
                visit(chapter)
            return found
        removed = keys(p for name, p in cls.upstream.items() if name not in cls.retained())
        removed.update(k for k in english if k.startswith("betterruins:structure-"))
        return (removed - keys(cls.retained().values())) & english.keys()

    def manifest(self):
        return json.loads((ROOT / "docs/content-packages.json").read_text())

    def test_every_chapter_is_moved_once_byte_for_byte(self):
        actual = list((ROOT / "content").glob("*/assets/questline/questline/chapters/*.json"))
        self.assertEqual(56, len(self.upstream))
        self.assertEqual(set(self.retained()), {p.name for p in actual})
        self.assertEqual(51, len(actual))
        for path in actual:
            with self.subTest(path=path):
                self.assertEqual(self.upstream[path.name], path.read_bytes())
                data = json.loads(path.read_bytes())
                group = next(iter(data.get("requiresMod", [])), "vanilla")
                self.assertEqual(group, path.relative_to(ROOT / "content").parts[0])
        self.assertFalse((ROOT / SOURCE / "chapters").exists())

    def test_core_is_content_free_and_default_is_owned_only_by_vanilla(self):
        self.assertFalse((ROOT / SOURCE / "questline.json").exists())
        self.assertEqual(blob(SOURCE / "questline.json"),
                         (ROOT / "content/vanilla" / LEGACY / "questline.json").read_bytes())
        self.assertEqual([ROOT / "content/vanilla" / LEGACY / "questline.json"],
                         list((ROOT / "content").glob("*/assets/*/questline/questline.json")))

    def test_package_metadata_and_explicit_dependency_closure(self):
        manifest = self.manifest()
        self.assertEqual(UPSTREAM, manifest["upstream"])
        packages = manifest["packages"]
        self.assertEqual(set(GROUPS), {p["key"] for p in packages})
        self.assertEqual(9, len(packages))
        ids = set()
        for package in packages:
            group = package["key"]
            self.assertEqual(f"content/{group}", package["path"])
            info = json.loads((ROOT / package["path"] / "modinfo.json").read_text())
            expected_id = f"questline{group}"
            self.assertEqual(expected_id, info["modid"])
            self.assertEqual(expected_id, package["modid"])
            ids.add(info["modid"])
            self.assertEqual("content", info["type"])
            self.assertEqual("0.14.0", info["version"])
            expected = {"game": "1.22.0", "questline": "0.15.0"}
            if group != "vanilla":
                expected.update({"questlinevanilla": "0.14.0", group: "0.0.0"})
            if group in ("efchefstricks", "efmealsmodule"):
                expected.update({"expandedfoods": "0.0.0", "questlineexpandedfoods": "0.14.0"})
            self.assertEqual(expected, info["dependencies"])
            self.assertEqual(expected, package["dependencies"])
            paths = sorted((ROOT / package["path"] / LEGACY / "chapters").glob("*.json"))
            self.assertEqual([p.name for p in paths], package["chapters"])
            self.assertEqual(GROUPS[group][0], len(paths))
            self.assertEqual(GROUPS[group][1], sum(len(json.loads(p.read_bytes())["quests"]) for p in paths))
        self.assertEqual(9, len(ids))

    def test_totals_and_replacements_are_identical_to_upstream(self):
        def signature(payloads):
            docs = [json.loads(p) for p in payloads]
            ids = collections.Counter(q["id"] for d in docs for q in d["quests"])
            tasks = sum(len(q.get("tasks", [])) for d in docs for q in d["quests"])
            replacements = {k: v for k, v in ids.items() if v > 1}
            extensions = sorted((d["id"], d["extends"]) for d in docs if "extends" in d)
            return (len(docs), sum(ids.values()), tasks, len(ids)), replacements, extensions
        expected = signature(self.retained().values())
        actual = signature(p.read_bytes() for p in (ROOT / "content").glob("*/assets/questline/questline/chapters/*.json"))
        self.assertEqual((51, 469, 520, 453), expected[0])
        self.assertEqual(expected, actual)
        self.assertEqual(16, len(actual[1]))

    def test_removed_packages_and_provider_references_are_absent(self):
        for provider in REMOVED:
            self.assertFalse((ROOT / "content" / provider).exists(), provider)
        for path in (ROOT / "content").rglob("*.json"):
            text = path.read_text()
            for provider in REMOVED:
                self.assertNotIn(provider, text, str(path))

    def test_shared_translations_remain_in_core_unchanged(self):
        prefix = "questline/assets/questline/lang/"
        names = [p for p in git("ls-tree", "-r", "--name-only", UPSTREAM).decode().splitlines() if p.startswith(prefix)]
        self.assertTrue(names)
        for name in names:
            original = json.loads(blob(name))
            current = json.loads((ROOT / name).read_bytes())
            for key in self.removed_lang_keys():
                self.assertNotIn(key, current, f"{name}:{key}")
            for key, value in original.items():
                if key in self.removed_lang_keys():
                    continue
                self.assertIn(key, current, name)
                self.assertEqual(value, current[key], f"{name}:{key}")
        self.assertFalse(list((ROOT / "content").glob("*/assets/*/lang/*")))


if __name__ == "__main__":
    unittest.main()
