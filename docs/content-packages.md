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
| artofgrowing | questlineartofgrowing | 4 own-domain process extensions | 65 indexed D+C overrides + 15 additive stages |

Declare `game >= 1.22.0` and `questline >= 0.15.0`.
Optional packages also depend on `questlinevanilla >= 0.14.0`. The eleven
original optional packages use same-named gameplay providers with minimum `0.0.0` (presence
required, no tested release asserted). The thirteenth content package,
**Art of Growing**, instead uses **`artofgrowingpatch >= 1.2.2`** and
`coreofartspatch >= 1.2.2`; `artofgrowing` is a provider asset domain, not its mod ID.
Its own asset domain is `questlineartofgrowing`, including chapters, patches and
English strings. See the [integration and graph contract](artofgrowing.md).

**The supplied `srMi9` upload returns 404.** The inspected AoG/Core 1.2.2 cache
cannot be asserted to equal the current pack. Full archive hashes, all 532 audit
rows, 65 D+C recommendations and locally unaffected justifications are linked
from that integration document. Native gameplay remains untested.

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
links. The original twelve content packages do not own self-contained localization: framework-only
installs still load text for uninstalled packages, and content-text updates may
need a coordinated core update. This deliberate initial limit avoids concurrent
edits and preserves every original translation.

For a later localization split, assign each key exactly one owner. Retain its
`questline:` domain and cross-package links. Do not copy whole language files
into every pack.

## Offline verification

Run from the repository root:

```sh
python3 tests/test_content_extraction.py -v
python3 verification/artofgrowing/check.py
```

The canonical extraction suite isolates the twelve original catalog entries and
shared translation namespace while allowing new addon-owned assets. The AoG
checker validates the thirteenth package separately.
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
