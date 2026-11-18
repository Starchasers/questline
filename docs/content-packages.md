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
Install only the integrations whose gameplay mods you use:

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

Every package explicitly depends on `game >= 1.22.0` and `questline >= 0.15.0`.
Every optional package also depends on `questlinevanilla >= 0.14.0`. The eleven
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

Chef's Tricks and Meals Module additionally require both `expandedfoods` and
`questlineexpandedfoods >= 0.14.0`: their original quests reference Expanded
Foods content and quest prerequisites (for example `make-breadcrumbs`,
`crack-egg`, `make-brine`, `make-mixing-bowl`, and `cut-nuggets`). Explicit
content dependencies prevent these references dangling when only the gameplay
mods are installed. Original chapter-level `requiresMod` gates remain untouched.

## Preservation and asset identity

All 56 original chapter JSON blobs are moved byte-for-byte from upstream
`9a2fd4e2b2e24046de08c7a86aff335294558939`. Each package retains the internal
`assets/questline/questline/chapters/<original-name>.json` path. **The unique
package Mod ID is not the asset domain**: changing `questline` in these asset
paths changes the loader's qualification of chapter IDs, quest IDs, page keys,
extension targets and prerequisites, and breaks saved progression identity.

The original `assets/questline/questline/questline.json` is likewise unchanged
and belongs only to vanilla. Optional packages must not duplicate that manifest.
The original corpus has 532 quest records, 589 task records and 516 distinct quest IDs. The
16 duplicate IDs are intentional extension replacement records, not accidental
copies to remove. The loader joins extensions into their original chapters and
replaces matching IDs; none of those records, fields, dependencies, rewards,
page links, or strings were rewritten during extraction.

## Shared translation ownership limitation

All original translations remain in core at `questline/assets/questline/lang/`
unchanged, including integration-specific text and links. The original twelve content packages are
therefore not self-contained localization owners: installing only the framework
still loads quest text for uninstalled packages, and updating content text may
require a coordinated core update. This deliberate initial limitation avoids
concurrent edits and preserves every original translation. A later localization
split must assign each key exactly one owner while retaining its `questline:`
domain and cross-package links; do not copy whole language files into every pack.

## Offline verification

Run from the repository root:

```sh
python3 tests/test_content_extraction.py -v
python3 verification/artofgrowing/check.py
```

The canonical extraction suite isolates the twelve original catalog entries and shared translation namespace while explicitly allowing new addon-owned assets; the AoG checker validates the thirteenth package separately. The tests use actual `git show <upstream>:<path>` blobs, not a regenerated
snapshot. The upstream commit must remain available locally (fetch it in shallow
checkouts). They verify one-to-one relocation, exact bytes, original paths,
package counts and IDs, explicit dependency closure, manifest ownership,
translation preservation, totals, and extension/replacement identity.

TDD baseline before extraction: 5 tests ran, with 3 failures and 1 error
(expected missing content/manifest and chapters still in core); translation
preservation already passed. After extraction all 5 pass. These are structural
tests, not a claim of a native game installation or integration smoke test.
