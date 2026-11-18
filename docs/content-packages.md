# Questbook content

The questbook ships inside the single `questline` mod. There are no separate
content packages: one ZIP holds the framework, the shared translations and every
chapter.

## Layout

| Path | Holds |
|---|---|
| `questline/assets/questline/questline/questline.json` | The default questline (`questline:default`). |
| `questline/assets/questline/questline/chapters/*.json` | All 49 chapter files. |
| `questline/assets/questline/lang/*.json` | Titles, descriptions and page text for every quest. |

Chapter files keep their upstream names and bytes:

- 25 base chapters (`stone-age.json`, `kitchen.json`, …).
- 24 integration files named `<modid>-<chapter>.json` for Bricklayers, Expanded
  Foods, Chef's Tricks, Meals Module, From Golden Combs, Tailor's Delight and Wool.
  They still `extends` a base chapter and keep their `requiresMod` gate, so they
  stay inactive when the gameplay mod is absent. Sixteen of their quests replace a
  base quest in place and keep its saved ID.

## Removed integrations

Chapters for Better Ruins, Charcoal Kiln, Hex's Machinery and Seafarer are not
shipped: those mods are outside the target modpack. Their language keys remain in
the shared translation files and are unused.

## Upgrading from 0.15.0

Version 0.15.0 shipped the same chapters as twelve separate content mods
(`questlinevanilla`, `questline<provider>`). Remove those ZIPs when installing
0.16.0: loading them beside the single mod supplies every chapter twice.

All chapters keep the `questline` asset domain, chapter IDs and quest IDs, so saved
progress carries over. Progress on quests from the four removed integrations is no
longer shown.

## Checks

`tests/test_content_extraction.py` verifies offline that:

- no `content/` directory or content manifest exists, and only `questline` and the
  Toolsmith adapter are packaged;
- every shipped chapter is byte-identical to its upstream blob, and exactly the four
  unused integrations are missing;
- no shipped quest requires a quest that only a removed integration defined;
- totals are 49 files, 431 quest records, 464 tasks, 415 distinct IDs and 16
  in-place replacements;
- upstream translation keys are unchanged.

The composition and reward harnesses read the same chapter folder.
