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
Install optional integrations only for gameplay mods you use:

| Directory | Mod ID | Chapters | Quest records |
| --- | --- | ---: | ---: |
| vanilla | questlinevanilla | 25 | 322 |
| betterruins | questlinebetterruins | 1 | 22 |
| bricklayers | questlinebricklayers | 3 | 24 |
| charcoalkiln | questlinecharcoalkiln | 1 | 6 |
| efchefstricks | questlineefchefstricks | 3 | 4 |
| efmealsmodule | questlineefmealsmodule | 1 | 1 |
| expandedfoods | questlineexpandedfoods | 8 | 37 |
| fromgoldencombs | questlinefromgoldencombs | 1 | 14 |
| hexsmech | questlinehexsmech | 2 | 38 |
| seafarer | questlineseafarer | 3 | 35 |
| tailorsdelight | questlinetailorsdelight | 5 | 21 |
| wool | questlinewool | 3 | 8 |
| livestockwelfare | questlinelivestockwelfare | 1 | 16 |

The Livestock Welfare addon is new authored content, not part of the frozen
upstream extraction totals. See [installation, care map and coexistence](livestockwelfare.md)
and its pinned [source research](research/livestockwelfare-0.15.0.md). It requires
Livestock Welfare >= 0.15.0; its sixteen tasks are explicit manual care checks.
Non-English locale entries currently use English fallback text.

Declare `game >= 1.22.0` and `questline >= 0.15.0` in every package. Optional
packages also depend on `questlinevanilla >= 0.14.0` and their same-named
gameplay mod. Gameplay-mod minimum versions are `0.0.0`: the mod must be present,
but this does not assert a specific tested release.

Chef's Tricks and Meals Module also require `expandedfoods` and
`questlineexpandedfoods >= 0.14.0`. Their original quests reference Expanded
Foods content and quest prerequisites, including `make-breadcrumbs`,
`crack-egg`, `make-brine`, `make-mixing-bowl`, and `cut-nuggets`. Keep these
explicit content dependencies so installing gameplay mods alone cannot leave
dangling references. Original chapter-level `requiresMod` gates are unchanged.

## Preservation and asset identity

All 56 original chapter JSON blobs were moved byte-for-byte from upstream
`9a2fd4e2b2e24046de08c7a86aff335294558939`. Keep each package's internal path:
`assets/questline/questline/chapters/<original-name>.json`. **The unique package
Mod ID is not the asset domain.** Changing `questline` in these paths changes
how the loader qualifies chapter IDs, quest IDs, page keys, extension targets
and prerequisites, breaking saved progression identity.

Keep the unchanged original `assets/questline/questline/questline.json` in
vanilla only. Do not duplicate that manifest in optional packages. The extraction
preserved 532 quest records, 589 task records and 516 distinct quest IDs.
The 16 duplicate IDs are intentional extension replacement records; do not
remove them as accidental copies. The loader joins extensions into their
original chapters and replaces matching IDs. Extraction rewrote none of these
records, fields, dependencies, rewards, page links, or strings.

## Shared translation ownership limitation

Keep the original translations unchanged in core at
`questline/assets/questline/lang/`, including integration-specific text and
links. Content packages do not own self-contained localization: framework-only
installs still load text for uninstalled packages, and content-text updates may
need a coordinated core update. This deliberate initial limit avoids concurrent
edits and preserves every original translation.

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
snapshot. They check one-to-one relocation, exact bytes, original paths,
package counts and IDs, explicit dependency closure, manifest ownership,
translation preservation, totals, and extension/replacement identity.

Historical extraction evidence: the TDD baseline ran 5 tests, with 3 failures
and 1 error. Missing content/manifest and chapters still in core caused the
expected failures; translation preservation already passed. After extraction,
all 5 passed. These recorded structural results are not a new test run or proof
of a native game installation or integration smoke test.
