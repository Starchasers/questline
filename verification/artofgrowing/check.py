#!/usr/bin/env python3
"""Validate AoG shipped assets and emit patched real-loader inputs; no mock chapter data.

This deliberately supports only the addon's audited indexed `replace` operations.
It is NOT an implementation of the game's complete JSON-patch engine.
"""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
ADDON = ROOT / "content/artofgrowing"
DOMAIN = "questlineartofgrowing"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def original_files():
    return sorted((ROOT / "content").glob("*/assets/questline/questline/chapters/*.json"))


def validate_ledger():
    ledger = read(ROOT / "docs/artofgrowing-impact-ledger.json")
    actual = {(p.relative_to(ROOT).as_posix(), q["id"]): q for p in original_files() for q in read(p)["quests"]}
    records = ledger["records"]
    keys = [(r["path"], r["id"]) for r in records]
    assert len(keys) == len(set(keys)) == len(actual) == 532, "532 distinct authored source records required"
    assert set(keys) == set(actual), "ledger missing or stale source record identities"
    counts = {s: sum(r["status"] == s for r in records) for s in "DCU"}
    assert counts == {"D": 25, "C": 40, "U": 467}, counts
    for r in records:
        assert r["reason"].strip(), r
        assert r["sha256"] == fingerprint(actual[(r["path"], r["id"])]), f"stale source audit: {r['path']}::{r['id']}"
    return records


def installed_modules(keys, addon, provider):
    catalog = read(ROOT / "docs/content-packages.json")["packages"]
    mods = {"game", "questline", "questlinevanilla"}
    for p in catalog:
        if p["key"] in keys:
            mods.add(p["modid"])
            mods.update(p["dependencies"])
    if addon:
        mods.add(DOMAIN)
    if provider:
        mods.update({"artofgrowingpatch", "coreofartspatch"})
    else:
        mods.discard("artofgrowingpatch")
        mods.discard("coreofartspatch")
    return mods


def applicable(patch, mods):
    for gate in patch.get("dependsOn", []):
        present = gate["modid"] in mods
        if present == bool(gate.get("invert", False)):
            return False
    condition = patch.get("condition")
    assert condition is None, "unsupported conditional patch must be explicitly audited"
    return True


def corpus(keys, addon=True, provider=True):
    mods = installed_modules(keys, addon, provider)
    files = {}
    source = {}
    for p in original_files():
        if p.relative_to(ROOT / "content").parts[0] not in keys:
            continue
        asset = "questline:questline/chapters/" + p.name
        assert asset not in files, asset
        files[asset] = read(p)
        source[asset] = p.relative_to(ROOT).as_posix()
    edits = []
    if addon:
        patches = sorted((ADDON / "assets" / DOMAIN / "patches").rglob("*.json"))
        assert patches, "missing shipped own-domain JSON patches"
        for p in patches:
            patches_in_file = read(p)
            assert isinstance(patches_in_file, list), str(p)
            for patch in patches_in_file:
                assert patch.get("op") == "replace", f"unsupported patch operation: {p} {patch}"
                assert any(g["modid"] == "artofgrowingpatch" and not g.get("invert", False) for g in patch.get("dependsOn", [])), f"missing actual AoG modid gate: {p}"
                assert not any(g["modid"] == "artofgrowing" for g in patch.get("dependsOn", [])), f"asset domain used as mod gate: {p}"
                if not applicable(patch, mods):
                    continue
                target = patch["file"]
                if target not in files:
                    # Optional targets must explicitly gate on their quest content owner.
                    assert patch.get("side") != "client", "chapter patches cannot be client-only"
                    target_paths = [x for x in original_files() if "questline:questline/chapters/" + x.name == target]
                    assert len(target_paths) == 1, f"unknown patch target {target}"
                    owner = "questline" + target_paths[0].relative_to(ROOT / "content").parts[0]
                    assert any(g["modid"] == owner and not g.get("invert", False) for g in patch.get("dependsOn", [])), f"optional target {target} missing {owner} gate"
                    continue
                match = re.fullmatch(r"/quests/(0|[1-9][0-9]*)", patch["path"])
                assert match, f"expected indexed whole-record replacement, got {patch['path']}"
                index = int(match[1])
                old = files[target]["quests"][index]
                value = copy.deepcopy(patch["value"])
                assert old["id"] == value["id"], f"stale index or changed saved ID: {target} {index}"
                key = (source[target], old["id"])
                assert key not in edits, f"competing/stale override {key}"
                assert value != old, f"no-op override falsely claims audit coverage: {target} {index}"
                edits.append(key)
                files[target]["quests"][index] = value
        for p in sorted((ADDON / "assets" / DOMAIN / "questline/chapters").glob("*.json")):
            asset = DOMAIN + ":questline/chapters/" + p.name
            chapter = read(p)
            assert "artofgrowingpatch" in chapter.get("requiresMod", []), f"extension missing provider gate: {p}"
            files[asset] = chapter
    return {"mods": sorted(mods), "edits": [list(k) for k in edits], "chapters": [{"domain": a.split(":", 1)[0], "name": a.rsplit("/", 1)[-1][:-5], "json": json.dumps(d)} for a, d in sorted(files.items())]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", type=Path)
    args = parser.parse_args()
    records = validate_ledger()
    affected = {(r["path"], r["id"]) for r in records if r["status"] in "DC"}
    keys = {p["key"] for p in read(ROOT / "docs/content-packages.json")["packages"]} - {"artofgrowing"}
    baseline = corpus(keys, False, False)
    disabled = corpus(keys, True, False)
    assert disabled["edits"] == [], "patches apply with provider absent"
    enabled = corpus(keys)
    changed = {tuple(x) for x in enabled["edits"]}
    assert changed == affected, f"65 D+C overrides required: missing {sorted(affected-changed)}, stale {sorted(changed-affected)}"
    metadata = read(ADDON / "modinfo.json")
    catalog = next(p for p in read(ROOT / "docs/content-packages.json")["packages"] if p["key"] == "artofgrowing")
    assert metadata["modid"] == catalog["modid"] == DOMAIN
    assert metadata["dependencies"] == catalog["dependencies"]
    assert metadata["dependencies"]["artofgrowingpatch"] == "1.2.2"
    assert "artofgrowing" not in metadata["dependencies"]
    actual_chapters = sorted(p.name for p in (ADDON / "assets" / DOMAIN / "questline/chapters").glob("*.json"))
    assert actual_chapters == catalog["chapters"], (actual_chapters, catalog["chapters"])
    en = read(ADDON / "assets" / DOMAIN / "lang/en.json")
    assert en and all(isinstance(v, str) and v.strip() for v in en.values())
    for locale in sorted((ADDON / "assets" / DOMAIN / "lang").glob("*.json")):
        translated = read(locale)
        assert set(translated) == set(en), f"addon locale keys differ: {locale}"
        for key, value in translated.items():
            assert isinstance(value, str) and value.strip(), f"empty addon translation: {locale}:{key}"
            for pattern in [r"\{p?\d+[:}]", r'<a\s+href="([^"]*)"\s*>', r"</?([a-zA-Z]+)"]:
                assert Counter(re.findall(pattern, value)) == Counter(re.findall(pattern, en[key])), f"addon args/links/markup differ: {locale}:{key}"
    def check_owned_references(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if k in {"lang", "caption", "name"} and isinstance(v, str) and v.startswith(DOMAIN + ":"):
                    assert v.split(":", 1)[1] in en, f"missing addon language reference: {v}"
                check_owned_references(v)
        elif isinstance(value, list):
            for v in value:
                check_owned_references(v)
    for chapter in enabled["chapters"]:
        check_owned_references(json.loads(chapter["json"]))
    lang_keys = set(en)
    for chapter in enabled["chapters"]:
        if chapter["domain"] != DOMAIN:
            continue
        for q in json.loads(chapter["json"])["quests"]:
            qid = q["id"].removeprefix(DOMAIN + ":")
            if ":" not in qid:
                assert qid + "-title" in lang_keys, f"missing addon title: {qid}"
    if args.emit:
        optional = ["expandedfoods", "efchefstricks", "bricklayers"]
        scenarios = []
        for bits in range(8):
            selected = {"vanilla"} | {m for i,m in enumerate(optional) if bits & (1 << i)}
            if "efchefstricks" in selected:
                selected.add("expandedfoods")
            for addon, provider in [(False,False),(False,True),(True,False),(True,True)]:
                scenarios.append({"name": f"optional-{bits}-addon-{addon}-provider-{provider}", "baseline": corpus(selected,False,provider), "active": corpus(selected,addon,provider)})
        scenarios.append({"name":"all-integrations-enabled", "baseline":baseline, "active":enabled})
        args.emit.write_text(json.dumps(scenarios), encoding="utf-8")
    print(f"AoG assets: 532 original records; 25 D + 40 C = {len(changed)} overrides; 467 U preserved; provider-absent patches inactive; addon English keys {len(en)}")


if __name__ == "__main__":
    main()
