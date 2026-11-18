# Questbook content

The questbook ships inside the single `questline` mod. There are no separate
content packages: one ZIP holds the framework, the shared translations and every
chapter.

## Layout

| Path | Holds |
|---|---|
| `questline/assets/questline/questline/questline.json` | The default questline (`questline:default`). |
| `questline/assets/questline/questline/chapters/*.json` | The 29 chapter files, one per chapter. |
| `questline/assets/questline/lang/*.json` | Titles, descriptions and page text for every quest. |

Chapters are grouped for the target modpack (see [the chapter plan](questbook/chapter-plan.md)):
six age chapters from `first-days` to `steel-age`, then workshop, land, kitchen, craft and
world chapters. No chapter is gated on a mod and none `extends` another: the former
integration files are merged in, with their sixteen replacement quests applied in place.

Every quest record is upstream's: ID, tasks, prerequisites, rewards and page text are
unchanged. Only its position on the canvas and the chapter it sits in differ. Positions are
generated: prerequisites inside a chapter sit to the left, columns 2 apart, rows 1.5 apart.

## Removed integrations

Chapters for Better Ruins, Charcoal Kiln, Hex's Machinery and Seafarer are not
shipped: those mods are outside the target modpack. Their language keys remain in
the shared translation files and are unused.

## Upgrading from 0.15.0

Version 0.15.0 shipped the same chapters as twelve separate content mods
(`questlinevanilla`, `questline<provider>`). Remove those ZIPs when installing
0.16.0: loading them beside the single mod supplies every chapter twice.

All quests keep the `questline` asset domain and their IDs, so saved progress carries
over; progress is stored per quest, not per chapter. Progress on quests from the four removed integrations is no
longer shown.

## Checks

`tests/test_content_extraction.py` verifies offline that:

- no `content/` directory exists and the default questline is upstream's;
- all 415 upstream quests of the kept integrations ship exactly once, each identical to its
  upstream record (replacements applied) apart from `pos`;
- the 29 chapters are plain (`id`, `order`, `icon`, `age`, `quests`), have a title, distinct
  orders, no two quests in one cell, and prerequisites to the left;
- every prerequisite resolves to a shipped quest;
- upstream translation keys are unchanged.

The composition and reward harnesses read the same chapter folder.
