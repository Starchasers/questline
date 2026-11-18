# Butchering verification receipt

## Automatic-objective correction receipt (supersedes the original manual draft)

Base revision: `0db35ff20a85cb60f4915800aba9d6dae3f53815`. Corrected all 15 addon definitions: 15 distinct source-resolved icons, 13 obtain tasks, one supported table grid-craft task, and the unchanged first-hunt kill task. No manual checkboxes, new rewards/consumption, saved-ID changes or vanilla asset edits. See [current journey and critique](../butchering.md), [objective ledger](butchering-objectives.json) and [source asset receipt](butchering-assets.json).

Regression-first evidence: the new Python correction suite initially failed on generic icons and absent native links, and errored on the missing objective ledger. The production-loader navigation test initially failed because conditional paragraphs were not filtered. Both were executed before implementation and now pass. The source audit also caught its own initial regex handling error for native `@...` allow/skip variant filters; it was corrected before the receipt passed. Final independent read-only code/source review found no actionable runtime defect; the identified stale manual-quest documentation is corrected here.

Fresh execution in the designated isolated clone used Python 3.14.7, cached .NET 10 and official Vintage Story 1.22.7 SDK assemblies/assets:

| Gate | Actual result |
|---|---|
| `python3 -m unittest discover -s tests -v` | 12 passed (7 Butchering contracts + 5 historical extraction contracts) |
| `python3 -m unittest discover -s tools/packaging -v` | 32 passed |
| `python3 tools/lang/check.py` | Zero errors; existing Chef's Tricks English warnings only |
| `python3 compat/toolsmith/tests/regression.py` | 3 passed |
| `dotnet run --project verification/composition/CompositionTests.csproj -c Release -p:VINTAGE_STORY=...` | 15 passed, zero failed |
| `dotnet run --project verification/rewards/RewardTests.csproj -c Release -p:VINTAGE_STORY=...` | 21 passed; 536 rewarded definitions exercised |
| `dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY=...` | 23 synthetic runtime checks passed |
| `sh ./build.sh` with explicit `DOTNET` and `VINTAGE_STORY` | Framework and adapter Release builds, zero warnings/errors; all 15 packages |
| Repeat full build | Identical `SHA256SUMS`; all 15 initial ZIP CRCs/checksums read back |
| `python3 tools/verify_butchering_assets.py --export ... --sdk ...` | Pinned export + every original ledger member hash; 15 icon variants, 14 output-target examples, both guide pageCodes; checked-in receipt matched |
| `git diff --check` | Clean |

New production checks cover provider absent/present, missing questbook/target, validation-disabled targets, qualification, network registry roundtrip, shuffled/reversed composition, seven absent-provider combinations plus all present, and native WildcardUtil matching of every output-target example. `IGameFacts` in the composition harness still synthesizes mod/collectible availability: source variant/hash expansion is a separate static gate, not a live registry acceptance claim.

Tracker caveats found and reflected in content: carried inventory excludes backpack equipment slots; table credit therefore uses a real grid-craft event and corpse instructions choose inventory-sized animals. Contained liquids count integer litres, so blood requires a whole litre, not one hidden item portion. Raw-hide yields are optional, blood unlocks before the bleeding window, smoking requires smoked output, and class-gated/disabled specialist tools never gate the core route. Ordinary ownership can legitimately satisfy output milestones; it does not prove personal processing. Existing saved manual completions are retained, not relabeled as historically detected actions.

**Not run:** live full-pack client/server, native item/guide registration and link clicking, rendered layouts/text scaling, actual grid-craft attribution, station interaction/timers, large-corpse transport, old-save migration and multiplayer playthrough. No native gameplay acceptance or current server-pack identity is claimed. Existing version labels cannot distinguish old builds: pair framework and addon artifacts from this corrected revision. No push, merge or publishing was executed.

## Historical PR #4 conflict-resolution verification

Merged live `origin/main` at `ee7ba3a26ade50e024960321de42fa4daea7784b` into original feature head `15051df7639c91eb6d31aa7c856964fbf5013323` without rewriting history. Reconciled README and package documentation to retain the authored addon, its English-owned locale, and main's revised developer guides. Main's `CLAUDE.md` is unchanged. Original feature content, source ledger, research, directed map, catalogs, locales and runtime/composition tests remain intact.

Fresh local execution used the official cached Vintage Story 1.22.7 SDK, .NET SDK 10.0.302 (also checked 10.0.404), and Python 3.14.7. Packaging: 32 tests passed; content/extraction: 8 passed; Toolsmith source: 3 passed. Localization had zero errors, with only the existing Chef's Tricks English warnings. Both Release builds passed with zero warnings/errors. Production-loader composition: 13 passed, including 17 replacements and the Butchering present/absent contract. Reward claims: 21 passed, exercising 536 rewarded definitions. Synthetic adapter: 23 passed. All 15 ZIPs and checksum entries were read back; a repeat full build under SDK 10.0.302 produced identical `SHA256SUMS`. The cached primary archive and all 30 source ledger members were rehashed successfully.

The new release-count regression failed against the inherited release workflow's 14-ZIP assumption before correction. The release workflow and current CI documentation now agree on 15 ZIPs (core, 13 content packs, adapter) and 16 release assets including `SHA256SUMS`. No release publishing was executed. Hosted CI must be checked on the pushed merge commit; local results do not establish hosted execution. Native/full-pack acceptance and human translations remain pending.

## Historical original-feature receipt

Executed in the independent `questline-butchering` clone, against the official Vintage Story 1.22.7 assemblies and .NET 10 SDK. No files in `questline-framework` were edited or built.

| Gate | Actual result |
|---|---|
| Primary export identity | Pszczoly 1.2.0; archive SHA-256 `239c31aef93c0960bfb87c8d5e8a2dd0add2d4287ce18836ca36abdefbf4ac9d` |
| Primary evidence readback | Export archive hash and all 30 ledger member hashes verified |
| Packaging unittest suite | 32 passed |
| Content/extraction unittest suite | 7 passed; historical assets byte-identical |
| Core localization checker | All languages: zero errors; existing `addon-efchefstricks` English warnings |
| Toolsmith source regression | 3 passed |
| Release framework/adapter builds | Both succeeded, zero warnings/errors |
| Production-loader composition | 13 passed; including 17 shipped replacements and Butchering present/absent, exactly 14 new IDs |
| Reward claim suite | 21 passed; 536 rewarded quest definitions exercised |
| Synthetic Toolsmith runtime adapter | 23 checks passed |
| Complete package set | 15 independently installable ZIPs, all SHA256SUMS entries verified |
| Repeat full build | Identical SHA256SUMS (`cmp` exited zero) |
| Whitespace | `git diff --check` clean |

The new content tests were first executed before implementation and failed for the missing chapter/replacement; the complete suite passes with the addon. An independent source/content reviewer found the missing chapter-title key, incorrect knife icon shorthand and consumed knife preparation omission. All three were corrected; title/icon contracts now have regressions.

This is offline verification, not live native acceptance. No full modpack client/server, native GUI layout, VsTestkit, spoilage timer or real interaction playthrough was run. The gameplay claims are bounded to archived asset/recipe/config and decompiled DLL inspection. Synthetic adapter checks are not an installed Toolsmith receipt. The historical srMi9 URL was not fetched as a currently available source; locally cached export identity is documented in the research. Human translation remains pending; addon English is the fallback.
