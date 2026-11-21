# Separately installable quest content

Keep the framework in `questline/` and quest content in separate packages. The
framework no longer owns chapter files or the `default` questline manifest.
Use [`content-packages.json`](content-packages.json) as the machine-readable
inventory of content roots. Package each root separately, with its `modinfo.json`
and `assets/` tree at the archive root—not inside `content/<name>/`.
Build-script integration has separate ownership.

## Installation and dependencies

Install the Questline framework (`questline`, minimum `0.15.0`). Add
`content/vanilla` (`questlinevanilla`, minimum `0.14.0`) for the original vanilla
progression. Framework-only installations have no default questline by design.
The current inventory contains ten content packages: vanilla and nine optional integrations. Install optional integrations only for gameplay mods you use:

| Directory | Mod ID | Chapters | Quest records |
| --- | --- | ---: | ---: |
| vanilla | questlinevanilla | 25 | 322 |
| bricklayers | questlinebricklayers | 3 | 24 |
| butchering | questlinebutchering | 4 | 35 |
| efchefstricks | questlineefchefstricks | 3 | 4 |
| efmealsmodule | questlineefmealsmodule | 1 | 1 |
| expandedfoods | questlineexpandedfoods | 8 | 37 |
| fromgoldencombs | questlinefromgoldencombs | 1 | 14 |
| hexsmech | questlinehexsmech | 2 | 38 |
| tailorsdelight | questlinetailorsdelight | 5 | 21 |
| wool | questlinewool | 3 | 8 |

Declare `game >= 1.22.0` and `questline >= 0.15.0` in every package. Optional
packages also depend on `questlinevanilla >= 0.14.0` and their same-named
gameplay mod. Inherited gameplay-mod minimum versions are `0.0.0`: the mod must
be present, but this does not assert a specific tested release. The authored
Butchering addon requires `butchering >= 1.14.3`; see its evidence below.

Chef's Tricks and Meals Module also require `expandedfoods` and
`questlineexpandedfoods >= 0.14.0`. Their original quests reference Expanded
Foods content and quest prerequisites, including `make-breadcrumbs`,
`crack-egg`, `make-brine`, `make-mixing-bowl`, and `cut-nuggets`. Keep these
explicit content dependencies so installing gameplay mods alone cannot leave
dangling references. Original chapter-level `requiresMod` gates are unchanged.

## Preservation and asset identity

The 51 retained original chapter JSON blobs were moved byte-for-byte from upstream
`9a2fd4e2b2e24046de08c7a86aff335294558939`. Keep each package's internal path:
`assets/questline/questline/chapters/<original-name>.json`. **The unique package
Mod ID is not the asset domain.** Changing `questline` in these paths changes
how the loader qualifies chapter IDs, quest IDs, page keys, extension targets
and prerequisites, breaking saved progression identity.

Keep the unchanged original `assets/questline/questline/questline.json` in
vanilla only. Do not duplicate that manifest in optional packages. The retained content contains 469 quest records, 520 task records and 453 distinct quest IDs.
The 16 duplicate IDs are intentional extension replacement records; do not
remove them as accidental copies. The loader joins extensions into their
original chapters and replaces matching IDs. Extraction rewrote none of these
records, fields, dependencies, rewards, page links, or strings.

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
every other inherited key/value is preserved. Content packages do not own
self-contained localization: framework-only installs still load text for other
uninstalled packages, and content-text updates may need a coordinated core update.
This initial limitation avoids concurrent edits.

For a later localization split, assign each key exactly one owner. Retain its
`questline:` domain and cross-package links. Do not copy whole language files
into every pack.

## Offline verification

Run from the repository root:

```sh
python -m unittest discover -s tests -p test_content_extraction.py -v
```

Keep the upstream commit available locally; fetch it in shallow checkouts.
The tests read actual `git show <upstream>:<path>` blobs, not a regenerated
snapshot. They explicitly account for the three removed packages, and check retained relocation, exact bytes, original paths,
package counts and IDs, explicit dependency closure, manifest ownership,
translation preservation, totals, and extension/replacement identity.

Historical extraction evidence: the TDD baseline ran 5 tests, with 3 failures
and 1 error. Missing content/manifest and chapters still in core caused the
expected failures; translation preservation already passed. After extraction,
all 5 passed. These recorded structural results are not a new test run or proof
of a native game installation or integration smoke test.

## Authored Butchering addon

Install `questlinebutchering_0.15.0.zip` alongside framework, vanilla and Butchering >= 1.14.3. Its four files add thirty-four quests and replace only `first-hunt` in place, retaining its kill task and saved ID. Other vanilla assets remain byte-identical. It owns only new English localization keys; other languages use the game's English fallback (not native-reviewed translations). This is separate from the historical extraction totals above. See [journey and evidence](butchering.md).
