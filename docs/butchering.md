# Butchering journey

Install framework `questline_0.15.0.zip`, `questlinevanilla_0.14.0.zip`, **Butchering 1.14.3 or newer**, and `questlinebutchering_0.14.0.zip`. Use framework and content built from the **same corrected revision**: native quest links and conditional page blocks require the accompanying framework change. Existing minimum-version numbers alone cannot distinguish pre-correction builds. The verified provider modid is `butchering`, not Butchery; future provider versions are not automatically verified.

## Automatic objectives and progression

All fifteen addon definitions have distinct, source-resolved item/block icons. There are **13 obtain objectives, one real grid-craft objective, and the unchanged first-hunt kill objective**; no manual checkboxes remain. Each added milestone still pays one cookie. Saved quest IDs, task-slot counts and unrelated vanilla asset bytes are preserved.

```text
Vanilla make-knife
  -> Obtain a working knife [butchering-prepare]
  -> Obtain a skinning hook [butchering-hook]
  -> Craft a butchering table [butchering-table]
      -> Obtain collected blood [butchering-blood; optional; prepare bucket BEFORE bleeding]
  -> Obtain an intact corpse [butchering-retrieve]
      -> Obtain a raw hide [butchering-skin; optional mammal product]
          -> Obtain tanned leather [butchering-leather; Leatherwork chapter]
  -> Obtain a bled-out corpse [butchering-bleed]
  -> Obtain raw table meat [butchering-process]
      -> Obtain smoked food [butchering-preserve]
      -> Obtain clean offal [butchering-offal; optional]
      -> Obtain dry sinew [butchering-sinew; optional]
      -> Obtain a strong bone [butchering-bones; optional]
      -> Obtain a butchery bag [butchering-bag; optional]
```

Arrows are actual prerequisites, not a claim that inventory proves the player performed every step. The page still teaches corpse → hook → knife → bleeding → table mechanics. The objective proves only the named output. Raw meat acquired earlier can count, and another player's hide or leather can count. Bled-out corpse ownership proves that item state, not the player's skinning or waiting action. Table crafting is a supported grid-craft event; its credit does not prove placement. First-hunt still proves a chicken kill, not carcass processing.

Obtain tasks use the existing server tracker and history/latching rules, without a new provider hook. Ordinary hotbar and backpack inventories are scanned, **not backpack equipment slots**. Start the corpse route with a chicken, hare or fox that fits ordinary inventory. Large equipped corpses remain a gameplay option, but are not silently promised automatic credit. The table uses **craft**, not obtain, because its backpack-equipment transport mode would otherwise be invisible. Carry a bag unequipped until its objective is credited. Blood requires **at least one whole litre** in a carried supported liquid container: the tracker floors contained litres, not item portions. Ground buckets are not inventory proof.

## Critique and corrections

| Previous problem | Current contract |
|---|---|
| Every action was a manual checkbox with a generic knife icon | Actual output targets, 15 distinct relevant icons, automatic grid-craft/obtain/kill credit |
| Titles promised skinning, bleeding, table processing or tanning that ownership cannot establish | Titles/outcomes name the output; instructions retain mechanics and explicitly limit what is proved |
| A raw-hide gate blocked animals that yield feathers or fur | Raw hide is an optional branch; bleeding depends on corpse retrieval, not raw-hide possession |
| Blood unlocked after skinning, potentially too late to place the bucket | Blood branch unlocks after table preparation; instructions place the bucket before bleeding finishes |
| “Preserve” accepted unrelated cooking/handling | Obtain an actual `butchering:smoked-*` food; ordinary unsalted meat route suffices, no rare prime meat gate |
| “Use bones” or “next trip” implied unsupported tool crafting/transport actions | Obtain a strong bone or bag; disabled bone pickaxe, class-gated recipes and optional cleaver remain contextual advice |
| Prose mod names without navigation | Clickable native handbook/quest destinations, guarded by provider and surviving destination |

No dressing station/state is invented. Species-dependent offal, sinew, strong bones, raw hides and blood never gate the core meat route. Primitive tools/stations give a stone-age start. A knife skins on the hook; a cleaver is only an optional table upgrade. Oiled hides/pelts are not tanned leather. The table consumes a stone knife and axe in its primitive recipe, so the instructions reserve a second working knife.

## Native crossmod navigation

Pages use `handbook://<pageCode>` for the two bundled Butchering guides and `handbook://quest:questline:<saved-id>` for native quest selection. Item/block icons and task output icons use the existing clickable handbook behavior.

- **Leatherwork:** links to hide, soaking, scraping, preparation, weak/strong tannin and finished leather quests. No existing leatherwork quest is replaced.
- **Immersive Woodworking:** provider-gated link to the existing boards quest, contextualized by verified bark by-products/tannin recipes. No nonexistent Woodworking questbook or invented bark quest ID is referenced.
- **Tailor's Delight:** provider- and destination-gated awl/needle links, with optional hide bundles and class-tool warnings; no finished backpack gate.
- **Expanded Foods:** provider- and destination-gated sausage, meat-rack and dry-aging links. These are separate uses, not evidence of Butchering smoking or table work.
- **Chef's Tricks:** optional salt crystallization/drying links, requiring both gameplay providers and both surviving quest destinations. Salt is not required by the unsalted smoked-food objective.
- **Better Husbandry / Livestock Welfare:** provider-gated native breeding/feeding quest links; no claim that killing proves welfare, feeding or breeding.
- **Vanilla farming/tools:** bonemeal and cleaver links remain optional. Player grave recovery is not an animal-processing prerequisite.

`PageBlock.requiresMod` and `requiresQuest` are all-of guards. The server qualifies destination IDs, removes unavailable blocks before validation, and rechecks after validation can disable a target. Gameplay provider present but questbook absent cannot leave a dangling link. The filtered page travels in the normal registry JSON. Missing destinations fail closed rather than opening unrelated search results. Existing content without guards is unaffected.

## Save compatibility

All fifteen IDs and one task slot per definition remain intact. No aliases, new rewards, consumption or migration grants are added. Existing completed/claimed progress remains saved progress; these edits do not retroactively prove that old manual completions were detected actions. Uncompleted quests now use the existing automatic tracker. A native old-save/load and multiplayer playthrough is still a release gate.

## Evidence and verification boundary

Primary source is the cached **Pszczoly 1.2.0** export for game 1.22.7, Butchering 1.14.3 assets/DLL, handbook and exported configuration. See [research](evidence/butchering-research.md), [archive/member hashes](evidence/butchering-sources.json), [objective ledger](evidence/butchering-objectives.json), [asset variant receipt](evidence/butchering-assets.json) and [verification](evidence/butchering-verification.md). This is not a fetched current live server pack.

To reproduce the static asset receipt (requires Python `json5`, plus an independently obtained matching export and SDK):

```sh
python3 tools/verify_butchering_assets.py --export /path/to/modpack.zip --sdk /path/to/vintage-story
```

It verifies the archive and every original source-ledger member hash, expands native variant groups including orientation properties and regex allow/skip filters, resolves all 15 icons and samples all 14 automatic output targets, and compares the checked-in receipt. `--write` explicitly regenerates after inspection. Production-loader tests additionally match the samples with Vintage Story's actual wildcard utility.

Offline tests/builds do **not** establish live asset registration, native link clicking, layout, real station/craft attribution, timer behavior, class availability, multiplayer or persistence acceptance. No full-pack/VsTestkit client/server gameplay or rendered GUI run was performed. Human translations remain pending; addon-owned English is the fallback. No proprietary archive or game binaries are committed.
