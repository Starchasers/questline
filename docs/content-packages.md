# Separately installable quest content

The framework directory is `questline/`. It no longer owns any chapter files or the
`default` questline manifest. Content package roots are listed in
[`content-packages.json`](content-packages.json), the machine-readable packaging
inventory. Each root contains a `modinfo.json` and `assets/` tree and must be
packaged separately with those entries at the archive root, not a wrapping
`content/<name>/` directory. Build-script integration is owned separately.

## Installation and dependencies

Install the Questline framework (`questline`, minimum `0.15.0`). For the original
vanilla progression also install `content/vanilla` (`questlinevanilla`, minimum
`0.14.0`). Framework-only installations intentionally have no default questline.
Install only the integrations whose gameplay mods you use. The current inventory
contains nine content packages: vanilla and eight optional integrations.

| Directory | Mod ID | Chapters | Quest records |
| --- | --- | ---: | ---: |
| vanilla | questlinevanilla | 25 | 322 |
| bricklayers | questlinebricklayers | 3 | 24 |
| efchefstricks | questlineefchefstricks | 3 | 4 |
| efmealsmodule | questlineefmealsmodule | 1 | 1 |
| expandedfoods | questlineexpandedfoods | 8 | 37 |
| fromgoldencombs | questlinefromgoldencombs | 1 | 14 |
| hexsmech | questlinehexsmech | 2 | 38 |
| tailorsdelight | questlinetailorsdelight | 5 | 21 |
| wool | questlinewool | 3 | 8 |

Every package explicitly depends on `game >= 1.22.0` and `questline >= 0.15.0`.
Every optional package also depends on `questlinevanilla >= 0.14.0` and its
same-named gameplay mod. Gameplay mod minimum versions use `0.0.0`: presence is
required, but no specific tested gameplay-mod release is asserted here.

Chef's Tricks and Meals Module additionally require both `expandedfoods` and
`questlineexpandedfoods >= 0.14.0`: their original quests reference Expanded
Foods content and quest prerequisites (for example `make-breadcrumbs`,
`crack-egg`, `make-brine`, `make-mixing-bowl`, and `cut-nuggets`). Explicit
content dependencies prevent these references dangling when only the gameplay
mods are installed. Original chapter-level `requiresMod` gates remain untouched.

## Preservation and asset identity

The 51 retained original chapter JSON blobs are preserved byte-for-byte from upstream
`9a2fd4e2b2e24046de08c7a86aff335294558939`. Each package retains the internal
`assets/questline/questline/chapters/<original-name>.json` path. **The unique
package Mod ID is not the asset domain**: changing `questline` in these asset
paths changes the loader's qualification of chapter IDs, quest IDs, page keys,
extension targets and prerequisites, and breaks saved progression identity.

The original `assets/questline/questline/questline.json` is likewise unchanged
and belongs only to vanilla. Optional packages must not duplicate that manifest.
There are 469 quest records, 520 task records and 453 distinct quest IDs. The
16 duplicate IDs are intentional extension replacement records, not accidental
copies to remove. The loader joins extensions into their original chapters and
replaces matching IDs; none of those records, fields, dependencies, rewards,
page links, or strings were rewritten during extraction.

Better Ruins, Charcoal Kiln and Seafarer packages were removed after the original
extraction. This removes their five chapter files from the shipped inventory,
not generic structure discovery, visit tasks, or third-party addon support.
Remaining chapter assets and the vanilla manifest keep their original bytes.
Removal does not clean existing `ModConfig/questline/working/` editor copies or
saved progress, uninstall old mod ZIPs, or delete old build output. Review stale
copies separately and use a clean output directory to check the current package set.

## Shared translation ownership limitation

Retained translations remain in core at `questline/assets/questline/lang/`.
The 150 keys exclusively owned by the removed integrations (chapter/quest text,
provider labels and Better Ruins structure names) are removed from all 34 locales;
every other inherited key/value is preserved. Content packages are therefore not
self-contained localization owners: installing only the framework still loads
quest text for other uninstalled packages, and updating content text may require
a coordinated core update. This initial limitation avoids concurrent edits.
A later localization
split must assign each key exactly one owner while retaining its `questline:`
domain and cross-package links; do not copy whole language files into every pack.

## Offline verification

Run from the repository root:

```sh
python -m unittest discover -s tests -p test_content_extraction.py -v
```

The tests use actual `git show <upstream>:<path>` blobs, not a regenerated
snapshot. The upstream commit must remain available locally (fetch it in shallow
checkouts). Checks must account explicitly for the three removed packages rather
than requiring their restoration. They verify retained relocation, exact bytes, original paths,
package counts and IDs, explicit dependency closure, manifest ownership,
translation preservation, totals, and extension/replacement identity.

Historical TDD baseline before extraction: 5 tests ran, with 3 failures and 1 error
(expected missing content/manifest and chapters still in core); translation
preservation already passed. After the original 56-chapter extraction all 5 passed
(532 quest records, 589 tasks, 516 distinct IDs). This is historical evidence,
not a post-removal test result. These are structural
tests, not a claim of a native game installation or integration smoke test.
