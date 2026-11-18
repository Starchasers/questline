#!/usr/bin/env python3
"""Lay out questbook chapters on the canvas from their prerequisites.

    python3 tools/questbook/layout.py                  # every chapter
    python3 tools/questbook/layout.py first-days baking

A quest sits one column right of its deepest prerequisite in the same chapter. Columns
are 2 apart and rows 1.5 apart; a quest is placed on the row nearest the average of its
in-chapter prerequisites. Only `pos` is rewritten, and quests are stored column by column.
"""
import collections, json, pathlib, sys

CHAPTERS = pathlib.Path(__file__).resolve().parents[2] / "questline/assets/questline/questline/chapters"


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


def layout(chapter):
    quests = chapter["quests"]
    inside = {q["id"] for q in quests}
    parents = {q["id"]: [r for r in dict.fromkeys(refs(q.get("requires", []))) if r in inside and r != q["id"]]
               for q in quests}
    depth = {}

    def measure(quest, trail=()):
        if quest in trail:
            raise ValueError(f"prerequisite cycle through {quest}")
        if quest not in depth:
            depth[quest] = 1 + max((measure(p, trail + (quest,)) for p in parents[quest]), default=-1)
        return depth[quest]

    columns = collections.defaultdict(list)
    for quest in quests:
        columns[measure(quest["id"])].append(quest)
    row = {}
    for column in sorted(columns):
        def wanted(quest):
            near = parents[quest["id"]]
            return sum(row[p] for p in near) / len(near) if near else None
        members = columns[column] if column == 0 else sorted(columns[column], key=wanted)
        taken = set()
        for index, quest in enumerate(members):
            slot = index if column == 0 else round(wanted(quest))
            while slot in taken:
                slot += 1
            taken.add(slot)
            row[quest["id"]] = slot
    ordered = []
    for column in sorted(columns):
        for quest in sorted(columns[column], key=lambda q: row[q["id"]]):
            quest["pos"] = [column * 2, row[quest["id"]] * 1.5]
            ordered.append(quest)
    chapter["quests"] = ordered


def main():
    names = sys.argv[1:] or sorted(p.stem for p in CHAPTERS.glob("*.json"))
    for name in names:
        path = CHAPTERS / f"{name}.json"
        chapter = json.loads(path.read_text(encoding="utf-8"))
        layout(chapter)
        path.write_text(json.dumps(chapter, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{name}: {len(chapter['quests'])} quests")


if __name__ == "__main__":
    main()
