# Art of Growing integration and progression graph

> **Evidence boundary:** the exact supplied public upload `srMi9` returns HTTP 404. The inspected local cache cannot be asserted to equal the current pack. All mechanics below are conditional on the inspected **Art of Growing 1.2.2 + Core of Arts 1.2.2** archives, not a freshly downloaded current server pack. Their SHA-256 hashes, source inventory and decompiled-code evidence are recorded in [crop research](artofgrowing-crop-research.md) and the [full impact audit](artofgrowing-impact-audit.md).

## Installation and namespace contract

Install core `questline`, `questlinevanilla`, the optional `questlineartofgrowing` content addon, and the inspected provider pair. The provider mod ID is **`artofgrowingpatch`**, not `artofgrowing`; the latter is only its asset domain. Core of Arts is `coreofartspatch`. Optional EF, Chef's Tricks and Bricklayers content remains optional; install each provider with its matching Questline content package when wanted. Never put AoG-specific filters or prose into core or shared vanilla records.

The addon lives under `content/artofgrowing`. Its JSON patches and extension chapters live under its own `questlineartofgrowing` asset domain. Indexed replacement patches retain each original quest ID and chapter placement, replace only the 65 audited D/C records, and gate optional targets on their owning content package. AoG stages use new namespaced IDs so they cannot silently steal a vanilla alias. Original source files remain byte-identical to their extraction baseline. Addon prose belongs in its own English language asset, not the shared core translation corpus.

The mod manifest controls installation requirements; chapter/patch provider gates independently protect composition if the provider disappears. Headless tests intentionally exercise that otherwise unsupported missing-dependency state. Without the addon there is no curriculum change, even if the provider is present. Without the provider, addon patches and chapters remain inactive. This tests content gating rather than claiming a native mod manager permits invalid dependencies.

## Complete audit coverage

The machine-readable [impact ledger](artofgrowing-impact-ledger.json) enumerates **532 authored records**, keyed by source path plus ID (not deduplicated aliases): **25 direct (D), 40 contextual (C), 467 locally unaffected (U)**. Every row includes the original canonical quest SHA-256, recommendation and direct upstream impacts. The [full matrix](artofgrowing-impact-audit.md) gives every record's classification, local justification and transitive progression exposure. U means the local contract remains valid, not that the record has no affected ancestors.

`verification/artofgrowing/check.py` rejects changed source records, missing ledger rows, stale indexed overrides, changed saved IDs, duplicate replacement targets, mismatched provider gates and any replacement outside the exact D+C set. This makes the matrix an executable coverage contract, not a manually maintained list of examples. The original 56 source chapters and 16 optional-pack replacement contracts remain separately verified; addon extension chapters and patch files are not counted as original extracted source chapters.

## Process graph and preservation rules

Read arrows as material/process prerequisites, not as claims that a craft event fires for a timed world transition:

```text
harvest grass -> fresh grass -> dry grass (hay) -> hay/feed/storage branches
                                        \-> aging -> aged grass
harvest cereal -> wet bundle -> drying -> dry bundle
    -> ground-storage threshing -> grain + straw
                                      |      \-> roofs / beds / fuel alternatives
                                      \-> flour / dough / food consumers (unchanged local recipes)
legume bundle -> held interaction processing (not cereal ground threshing)
flax cereal bundle -> dry bundle -> ground threshing -> dry stalks
    -> water retting -> washing clear -> softening -> ridge combing
    -> flax fiber -> twine / linen / cordage and downstream consumers
```

The inspected build does **not** establish hay turning into straw: drygrass and straw can each perish into agedgrass. Do not teach a fictitious hay-to-straw drying transition. Likewise do not invent `flaxbundle-raw` or an unsupported clear-to-dry flax transition. Verify cattail material contracts against assets: the inspected storage patch has a suspicious `catttailtops` target; no inferred reed-drying route is accepted as evidence.

Quest prerequisites must express the actual grass, cereal, flax and processing sequence without cycles or cross-module dangling references. Existing IDs survive, including the original early-game and optional replacement IDs. Early survival must remain achievable before cereal processing: do not gate the only initial shelter, fire, torch or tool behind unavailable straw/fiber stages. New recipes are often additive, not wholesale removals of vanilla routes. Firepit, bed and roof task filters need the actual provider namespace while retaining applicable vanilla alternatives. Shared cook/smelt inventory handlers do not become invalid merely because a block namespace changes.

The coverage matrix separates direct task/filter changes from contextual descriptions (feed, grass/straw storage, tinder, flax and fiber progression). Linen, clay and grain consumers with valid local mechanics are preserved rather than automatically rewritten because an ancestor changes. Optional EF grain routes and Chef's Tricks replacements must compose after the same source-index patches; Bricklayers alternatives must preserve their own identifiers. The real-loader suite checks **all prerequisites in every loaded quest**, not just those introduced by AoG.

### Shipped additive nodes (15 records in four extension chapters)

All identifiers below are fully qualified. These are additive stages, not 15 more upstream overrides.

| Extension target | New quest ID | Authored prerequisites |
|---|---|---|
| `questline:farming` | `questlineartofgrowing:harvest-cereal-bundles` | `{"all":["questline:make-hoe","questline:gather-seeds"]}` |
| `questline:farming` | `questlineartofgrowing:dry-cereal-bundles` | `"questlineartofgrowing:harvest-cereal-bundles"` |
| `questline:farming` | `questlineartofgrowing:thresh-cereal-bundles` | `"questlineartofgrowing:dry-cereal-bundles"` |
| `questline:farming` | `questlineartofgrowing:hull-cereal-seeds` | `"questlineartofgrowing:thresh-cereal-bundles"` |
| `questline:stone-age` | `questlineartofgrowing:gather-fresh-grass` | `"questline:make-knife"` |
| `questline:stone-age` | `questlineartofgrowing:dry-grass` | `"questlineartofgrowing:gather-fresh-grass"` |
| `questline:stone-age` | `questlineartofgrowing:convert-hay-straw-blocks` | `"questline:cut-grass"` |
| `questline:textiles` | `questlineartofgrowing:harvest-flax-bundles` | `"questline:harvest-grain"` |
| `questline:textiles` | `questlineartofgrowing:dry-flax-bundles` | `"questlineartofgrowing:harvest-flax-bundles"` |
| `questline:textiles` | `questlineartofgrowing:thresh-flax-stalks` | `"questlineartofgrowing:dry-flax-bundles"` |
| `questline:textiles` | `questlineartofgrowing:ret-flax-stalks` | `"questlineartofgrowing:thresh-flax-stalks"` |
| `questline:textiles` | `questlineartofgrowing:wash-flax-stalks` | `"questlineartofgrowing:ret-flax-stalks"` |
| `questline:textiles` | `questlineartofgrowing:soften-flax-stalks` | `"questlineartofgrowing:wash-flax-stalks"` |
| `questline:textiles` | `questlineartofgrowing:make-flax-ridge` | `{"all":["questlineartofgrowing:thresh-flax-stalks","questline:make-rope"]}` |
| `questline:winter` | `questlineartofgrowing:prepare-winter-feed` | `"questline:stock-grain"` |

The fully audited ancestor exposure for **every original record** is retained in the impact ledger and matrix. Real-loader prerequisite closure rejects dangling, disabled or cyclic outcomes after applying these authored edges.

## Reproducible verification

```sh
python3 tests/test_content_extraction.py -v
python3 verification/artofgrowing/check.py
python3 -m unittest discover -s verification/artofgrowing -p test_check.py -v
VINTAGE_STORY=/path/to/game dotnet run --project verification/artofgrowing/ArtOfGrowingTests.csproj -c Release
VINTAGE_STORY=/path/to/game dotnet run --project verification/composition/CompositionTests.csproj -c Release
python3 tools/lang/check.py
```

The AoG suite reads the shipped patch assets, applies their indexed whole-record replacement payloads to actual source chapter JSON, then passes the patched chapters and shipped extension JSON to the production `QuestLoader`. The Python patch executor deliberately supports only the addon's audited `replace /quests/N` operations; unsupported operations fail, rather than pretending to implement the entire native game's patch engine. All eight EF/Chef's Tricks/Bricklayers selection combinations are exercised with addon/provider absent or present, plus the complete integration set. Each case is loaded in multiple shuffled orders under en-US and tr-TR. Assertions include retained IDs, unaffected content, final replacement payloads, complete prerequisite closure, no ambiguity/duplicate diagnostics and deterministic composition.

The headless `IGameFacts` uses permissive collectible/language existence responses so this suite isolates graph composition. Addon language references are checked separately against the shipped English files. These loader tests do **not** establish native item-pattern existence or behavior against an installed provider DLL.

**Native gameplay has not been run.** These checks are offline loader/asset contracts, not evidence of survival timing, harvesting, drying, ground-storage threshing, retting, ridge use, item collection events, UI layout, or reward delivery in a world. Native acceptance must cover an early survival start, a complete cereal and flax loop, the optional-provider combinations, and persistence/reload before marking those gates passed. Revalidate mechanics against the exact live pack if the unavailable public source becomes accessible.
