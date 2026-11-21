# Butchering verification receipt

## Player journey 0.15.0 (supersedes earlier inventories)

Removed `butchering-javelin` and its Armory extension, rewrote every description for players, replaced imperative/disclaimer titles with plain nouns, and made the knapped flint component a prerequisite of the primitive skinning hook. The primitive table is now the first Butchering node. Upgrade rows run rightward in order and never feed back into the processing trunk: tables, hook components and floor skinning stations; ceiling variants are terminal alternatives. Copper requires first smithing, bronze any supported alloy, and iron iron smithing. Bronze variants are alternatives, not three mandatory redundant stations. Independent outputs no longer form an offal → sinew → prime chain. Hide pages link directly into native Leatherworking.

Current content: **four chapter assets, 35 definitions / 34 added IDs, 35 exact icons and 34 automatic output targets** (28 obtain tasks, six grid-craft tasks, one retained first-hunt kill). Addon version is **0.15.0**; framework remains 0.15.0, Vanilla dependency 0.14.0, Butchering minimum 1.14.3. Twelve ZIP packages remain independently installable.

Fresh local execution: **21 Python content tests, 33 packaging tests, three Toolsmith source regressions; 15 production composition tests, 21 reward tests exercising 493 rewarded definitions, and 23 synthetic runtime adapter checks all passed**. Both Release builds had zero warnings/errors. Localization: zero errors, pre-existing Chef's Tricks English warnings only. Used official Vintage Story 1.22.7 SDK assets and .NET SDK 10.0.404. New player-journey regressions failed before content changes. Asset receipt was regenerated, then independently compared with no changes; every original source-ledger hash was checked. Native wildcard checks accept all three bronze alternatives and reject neighboring tiers.

Rate evidence reproduced from `attributes.butcheringEfficiencyByType` in the provider's `butchertable.json`, `butcherhook.json` and `butcherhookceiling.json`: primitive 0.8, copper/bronze 1.0, iron 1.2. Retained `ButcheringConfigV3.json` has table and rack multipliers 1.0. The checked-in asset receipt now records both station and configured multipliers; regression tests compare all station descriptions to those values. Hook item states are flint, copper, tinbronze, bismuthbronze, blackbronze and iron; no steel or flint ceiling variants exist. Four-hook ingot smithing is enabled; one-hook nugget smithing is disabled. Components do not have independent drop rates, ceiling mounting does not improve rates, and skinning/table rates apply to distinct reward sets rather than multiplying together.

No full-pack/native rendered GUI or station gameplay run was performed. Authored coordinates, ordered dependency rows and optional destinations are checked structurally and by the production loader, not accepted as a rendered-layout or gameplay proof. Historical receipts below retain their original counts and limitations. Hosted CI must independently verify the pushed revision.

## Integration-removal conflict reconciliation

Merged main's removal of Better Ruins, Charcoal Kiln and Seafarer while retaining all five Butchering chapters, its owned English text, provider gates and production-loader checks. Current inventory is 12 ZIPs: framework, ten content packs and Toolsmith adapter; release assets also include `SHA256SUMS` (13 assets). Earlier 15-package receipts below describe historical inventories, not this merge.

Fresh local checks: 15 Python content tests, 33 packaging tests and three Toolsmith source regressions passed. Localization reports zero errors with existing Chef's Tricks English warnings only. No local .NET SDK or Vintage Story SDK was available for this reconciliation; hosted CI must establish the exact pushed revision's builds and C# checks. Native/full-pack acceptance remains pending.

Conflict decisions: combine main's retained-provider inventory with Butchering's additions in CI, README and package documentation/manifest; retain main's extraction/removal assertions scoped to inherited packs; update composition file count to 51 retained plus five Butchering chapters. Release assertions/notes and both package-count regressions follow the combined inventory, rather than either stale branch total.

## Website C252–C268 implementation receipt (historical inventory; current content)

Implementation base: `f464bfaab2c73f46b7f2ca5f5709950a649bb5ff`. Added thirteen quests and two provider-gated extensions, for **28 definitions / 27 added IDs**, with 21 obtain tasks, six supported grid crafts and the unchanged first-hunt kill. All existing saved quest/task IDs and all unrelated chapter bytes are preserved. No manual checkbox or duplicate fat/cleaver milestone was added. Every website candidate is reconciled in [the coverage ledger](butchering-website-coverage.json); this section supersedes the older counts below.

**RED → GREEN:** before content edits, `python3 -m unittest discover -s tests -p test_butchering_website.py -v` failed for thirteen missing quests and missing coverage ledger. The production C# test also failed the new 27-ID addition count before implementation. During verification the provider matrix caught that quest-level `requiresMod` is not supported; the final implementation uses gated chapter extensions and passes all eight Butchering/Armory/Rustic Cookery combinations in both file orders. Native wildcard positive/negative cases cover every output and distinguish table tiers, metal from flint hook, and raw from smoked slab. All loaded prerequisites and conditional links are checked, including cycle detection. The canonical historical extraction corpus stays unchanged.

Exact commands executed in this worktree (set `SDK=/home/brunette/.hermes/cache/scratch/questline-ci-game` and `DN=/home/brunette/.hermes/cache/scratch/questline-ci-dotnet/dotnet`):

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tools/packaging -v
python3 tools/lang/check.py
python3 compat/toolsmith/tests/regression.py
VINTAGE_STORY="$SDK" "$DN" run --project verification/composition --configuration Release -- .
VINTAGE_STORY="$SDK" "$DN" run --project verification/rewards --configuration Release -- .
python3 tools/verify_butchering_assets.py --export /home/brunette/.hermes/game-context/vintage-story/1571480359365771304/prizC/modpack.zip --sdk "$SDK"
VINTAGE_STORY="$SDK" DOTNET="$DN" sh ./build.sh --configuration Release --output /home/brunette/.hermes/cache/scratch/questline-pr4-website-build
git diff --check
```

Results: **14 Python content tests; 32 packaging tests; 3 Toolsmith regressions; 15 production composition tests; 21 production reward tests (549 rewarded definitions); zero localization errors** (existing Chef’s Tricks warnings only). Source verification resolves **28 exact icons and 27 automatic output examples**, with original archive/member SHA-256s plus pinned Armory/Rustic Cookery assets, recipes, DLLs and configuration. Release framework/adapter builds return zero warnings/errors and produce all **15 packages**. A separate read-only reviewer inspected the diff, original recipes, provider gates and liquid tracking; no actionable finding. A final evidence check corrected the sinew grinding source citation to the actual `grindingPropsByType` item property, not a nonexistent quern recipe file.

Source mechanics boundary: Rustic Cookery DLL inspection establishes `ButcheringCompat.Prefix` / `SlabSplitter.Split` create slabs from eligible workstation yields; `SlabSlicing.CreatePiece` reverses slabs into meat pieces; `BlockEntitySmokeRack.OnInteract`, `OnSmokeTick` and `FinishSmoking` require whole raw slabs and adequate smoke. Original pinned `rusticcookery.json` sets slab size 6 and full-smoke duration 2880 accumulated tick-seconds. These facts are static evidence, not a running machine acceptance test. The historical srMi9 upload remains unavailable; inspected Pszczoly 1.2.0 is not claimed to be that exact upload or the current live server pack.

**Still not run:** native GUI render/link clicking, actual full-pack station and craft attribution playthrough, old-save/multiplayer interaction checks. English fallback keys are complete; human translations remain pending. Parent must publish the revised graph showing optional Armory/Rustic branches, separate smoking machines, table upgrades, glue/sausage and rare-prime side branches. No push, PR edit, merge or website publication was performed here.

## Automatic-objective correction receipt (historical; superseded above)

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
