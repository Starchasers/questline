# Art of Growing: crop, grain and flax research

## Scope and exact authority

- Audited supplied `pszczoly-roadmap/integration-data/Mods/ArtOfGrowing_1.2.2.zip`; ZIP SHA-256 `39f08f333b98c0d561f1e3207a7a7d56a154acc8ce0719378af324a68acddf76`. `modinfo.json`: **artofgrowingpatch 1.2.2**, dependency **coreofartspatch**; asset domain **artofgrowing** (do not confuse domain with mod ID).
- Unpacked to `<research-scratch>/pszczoly-roadmap/integration-data/aog-research-unpacked/` (below **A**). Static ILSpy source at `<research-scratch>/aog-decompiled/` (below **D**). DLL SHA-256 `69186038c4600f1b9f528e381cf7dde08e060cb2c97b5012d3fea16e1b7fc8e9`. No bundled DLL was executed.
- Snapshot enabled authority: `integration-data/serverconfig.json` → parsed `LastLaunchMods` contains `artofgrowingpatch=1.2.2`, `coreofartspatch=1.2.2`; neither `aogbreedingaddon` nor another breeding addon was found in the inspected bundled Mod ZIP metadata. `Logs/server-main.log:81–82,289,332,388` records these modules and `It grows...`; `server-debug.log:214–215,371` records AoG loading/instantiation. These are pre-existing integration logs, not a new live-game test.
- **No AoG gameplay config/module switches found** in supplied ModConfig or decompiled AoG. The only file in `ModConfig/Arts/` is `CoreOfArts.json`: `EnableLiquidMixing=true`; this is not a crop/flax toggle. `D/ArtOfGrowing/ArtOfGrowingModSystem.cs:20–66` registers the crop/storage/items and installs Harmony patches unconditionally. Crop drop changes generally have `dependsOn: [{modid:"aogbreedingaddon",invert:true}]`; that branch applies to this inspected snapshot, not necessarily an unknown newer pack. Do not invent breeding sizes/modules from dormant code branches.
- Focused scratch discovery found `<research-scratch>/srMi9/download-response`: **100-byte JSON HTTP 404**, not a ZIP. Its `identity-verdict.json` independently records no archive saved and exact export unresolved. No `srMi9` archive found by name. **This report does not establish the configuration or installed mods of the later exact srMi9 export.** Obtain that export before claiming current-pack authority; do not substitute another retained pack.

## Grain: actual processing chain

1. Plant `game:seeds-{type}` on farmland; retain part of the seed harvest for replanting.
2. Harvest the ripe `game:crop-{type}-{stage}`. AoG replaces direct grain/seed/fiber drops with **wet bundles**:

| Type | Ripe stage | Output | JSON quantity (`avg`, `var`) |
|---|---:|---|---|
| rye | 9 | `artofgrowing:grainbundle-rye-wet` | 12, 1 |
| spelt | 9 | `artofgrowing:grainbundle-spelt-wet` | 13, 2 |
| rice | 10 | `artofgrowing:grainbundle-rice-wet` | 14, 2 |
| amaranth | 9 | `artofgrowing:grainbundle-amaranth-wet` | 7, 1 |
| flax | 9 | `artofgrowing:grainbundle-flax-wet` | 9, 1 |

These are asset drop parameters, not guaranteed live yields after farmland damage/player multipliers. Non-ripe fallback is `game:thatch`, avg 0.7, not recoverable planting seeds. Sources: `A/assets/artofgrowing/patches/crop/{type}.json` → `/dropsByType`.

3. **Shift + RMB** place bundles on the ground as AoG storage (`artofgrowing:haystorage`); let them become `artofgrowing:grainbundle-{type}-dry`. Keep the pile out of water and sheltered from rain. There is no separate mandatory drying rack. `grainbundle.json` defines Dry transition 120±24 hours, ratio 1; custom ground-storage speed is 16× for Dry outside water, 0× in water, and rain/water can reset Dry progress. Thus base nominal ground-pile drying is **7.5±1.5 in-game hours**, not five game days; this is a static nominal estimate, not a measured live clock. Wet bundles also have Perish freshHours 84 + transitionHours 6 → `game:thatch`; do not leave them in inventory indefinitely.
4. **Hold RMB on the dry ground pile with `game:stick`** to thresh; `artofgrowing:flail` or `artofgrowing:flail-sturdy` is an optional faster tool. Stop handler requires >0.9 seconds. Per consumed bundle: **one `game:seeds-{type}` plus one `game:thatch`**, except flax produces **one `artofgrowing:flaxbundle-dry`** instead of thatch. Stick action processes up to 4, flail up to 16; flail loses 1 durability per successful action. No 3.5-seed yield applies to these cereal piles: that belongs to the separate handheld head/pod handler. Size-based straw multipliers exist in code, but the base bundle has no size variant.
5. Shapeless grid craft **1 `game:seeds-{type}` + `game:knife-*` (tool) → 1 `game:grain-{type}`**. Types: flax, rye, rice, spelt, sunflower, amaranth, pumpkin. The knife is required for this defined recipe; grain and planting seeds are distinct outputs. Continue to ordinary grain/flour/food processing; do not teach that harvesting immediately supplies `game:grain-*`.

Sources: `A/assets/artofgrowing/itemtypes/grain/grainbundle.json` → variants, AOGHayStorable drops, transitions; `recipes/grid/grains.json`; `A/assets/game/itemtypes/resource/grainseeds.json` → plantable seed definitions; `A/assets/artofgrowing/patches/grain.json`; `D/ArtOfGrowing.BlockEntites/AOGBlockEntityGroundStorage.cs:377–421,464–505,925–1057`; `D/ArtOfGrowing.Blocks/AOGBlockCrop.cs` → knife/scythe harvesting. Knife or scythe on a mature AoG crop creates the pile from the first drop; ordinary other-tool/bare-hand path delegates to base crop breaking. Existing handbook controls corroborate Shift+RMB placement and stick+RMB threshing (`A/assets/artofgrowing/lang/en.json`, grainbundle help keys). API enum meanings Dry=1, Melt=6 and Knife=0, Scythe=13 verified by static inspection of retained `questline-ci-game/VintagestoryAPI.dll`.

## Flax: actual fiber chain (not immediate crop fibers)

`game:crop-flax-9` → `artofgrowing:grainbundle-flax-wet` → dry → `artofgrowing:grainbundle-flax-dry` → thresh → `game:seeds-flax` + **`artofgrowing:flaxbundle-dry`** → ret/soak → **`flaxbundle-wet`** → wash → **`flaxbundle-clear`** → crumple → **`flaxbundle-soft`** → comb → **`game:flaxfibers`**.

All four `flaxbundle-*` IDs use domain `artofgrowing`; their exact localized names are Linen straw / Soaked linen straw / Pure linen straw / Crumpled linen straw.

- **Retting/soaking:** put dry linen straw in AoG ground storage occupying a water block. JSON uses **Melt** transition, not Dry: `freshHours=0`, `transitionHours avg=672,var=24`, ratio 1 to `flaxbundle-wet`; custom storage runs Melt at 16× in water and 0× outside it. Nominal **42±1.5 in-game hours** in this ground-water path. Dry straw also has Perish freshHours 336 + transitionHours 6 → `game:thatch`. Rain resets drying, but the Melt speed test specifically checks water at the storage block; do not present rain alone as retting. These transition estimates are not barrel sealing times.
- **Wash:** barrel recipe `flaxbundle-wet` + 1 litre `game:waterportion` → one `flaxbundle-clear`, **consumeLitres=0**, with no sealHours specified. Grid alternatives use wet straw + `game:woodbucket`, `game:bowl-*-fired` or `game:jug-*-fired`, requiring water content and 1 litre via `liquidContainerProps`. These are defined alternatives; no invented washing station or timed barrel fermentation. Native liquid recipe semantics beyond the source fields were not live-tested.
- **Crumple:** hold clear straw in main/right hand, RMB without Shift for about 2 seconds (stop threshold 1.9s) → soft straw **1:1**. A creaser is **optional**, not a metal-age gate: `artofgrowing:creaser-{wood}` in offhand increases batch 1→4; floor sitting doubles batch (2, or 8 with creaser). Tool is damaged by processed count.
- **Comb:** soft straw in main/right hand, **ridge in offhand**, RMB without Shift for about 2 seconds → **1 `game:flaxfibers` per soft bundle**. `artofgrowing:ridge-rough` processes 1 per action; `artofgrowing:ridge-wooden-{wood}` processes 4; floor sitting doubles either. Ridge is required by the normal interaction-start/step path and loses durability by count.
- **Bootstrap tools:** rough ridge = **3 `game:stick` + 1 `game:rope` OR 1 `game:flaxtwine`**. Wooden ridge = plank + stick + knife tool. Creaser = 2 planks + rope OR flaxtwine. Thus use an available rope route to avoid circular “make twine before first fibers”; availability of the rope's own upstream production is outside this crop audit. Flail additionally costs leather, 2 nails/strips, 2 sticks, firewood and knife+hammer tools; it must not be required to begin threshing.

Sources: `A/assets/artofgrowing/itemtypes/grain/flaxbundle.json` → types/classes, canWater and transitions; `recipes/barrel/flaxbundle-clear.json`; `recipes/grid/flaxbundle-clear.json`; `recipes/grid/flaxtools.json`; `recipes/grid/flail{,-sturdy}.json`; `itemtypes/tool/{ridge-rough,ridge,creaser}.json`; `D/ArtOfGrowing.Items/AOGItemInteract.cs:95–119,138–199`; `D/ArtOfGrowing.Items/AOGItemFlaxSoft.cs` → OnHeldInteractStart/Step and lines 122–166. Do not infer a guaranteed extra thatch byproduct from crumpling/combing: the code creates only the next straw state/fibers.

## Vegetable crops: harvest food before seed stage

AoG extends these stages; **last stage is seed/rot, not maximum food**. Table gives main edible harvest parameter at its peak, then last stage. Sources: `A/assets/artofgrowing/patches/crop/{name}.json` → variantgroups, dropsByType, cropProps.

| Crop | Peak food stage → output avg,var | Final seed stage |
|---|---|---:|
| carrot | 7 → `game:vegetable-carrot` 11,2 | 11 |
| onion | 7 → `game:vegetable-onion` 12,2; also scallions avg 5,var 1 | 11 |
| parsnip | 8 → `game:vegetable-parsnip` 12,2 | 12 |
| turnip | 5 → `game:vegetable-turnip` 7,1 | 8 |
| cabbage | 12 → `game:vegetable-cabbage` 2,0 | 16 |

- Final stage of each has `game:seeds-{type}` avg **3.2**, rot avg 1 and drygrass avg 0.7; food yields decline between peak and seed stage. Reserve seed plants instead of cutting everything at peak.
- Onion stages 2–7 supply `artofgrowing:vegetable-scallions`; edible onion bulbs start stage 6.
- Carrot/onion/turnip/parsnip food items receive **AOGItemSeedling** (`patches/vegetable.json`). Replant one vegetable on farmland to create `game:crop-seed-{type}-1`; the separate seed crop's final stage yields seeds avg **2.1**, not 3.2. Exact separate seed crop assets: `A/assets/game/blocktypes/plant/crop/seed{carrot,onion,parsnip,turnip}.json`; placement implementation `D/ArtOfGrowing.Items/AOGItemSeedling.cs`. Cabbage is not in this vegetable-replant class mapping.

## Other grain-like harvests: avoid applying drying to every crop

- Soybean: stage 11 yields `artofgrowing:grainbundle-soybean` avg3,var1; stage10 avg2,var0.5. Peanut: stage9 `grainbundle-peanut` avg4,var2; stage8 avg3,var0.5. Sunflower: stage12 `grainbundle-sunflower` avg5,var1 plus thatch avg3,var2.
- These use **AOGItemInteract**, not the wet/dry cereal storage path. Hold RMB about 2 seconds without Shift to process; standing with empty offhand batches 2, floor sitting doubles it. Handler yields `RoundRandom(3.5) * consumedCount` of `game:legume-soybean`, `game:legume-peanut`, or `game:seeds-sunflower`, respectively; no promised straw output from this handler.
- Source: crop patches `{soybean,peanut,sunflower}.json`; `itemtypes/grain/{legume-head,sunflower-head}.json`; `D/ArtOfGrowing.Items/AOGItemInteract.cs:201–234`. These distinct definitions explain why a wildcard “grainbundle” can be misleading.

## Quest inventory implications (repository read only)

Repository `<repository>`, files `content/vanilla/assets/questline/questline/chapters/{farming,textiles,baking}.json`:

- `farming/harvest-grain`: obtains 16 `game:grain-*`, after make-hoe + gather-seeds. Missing teaching: mature bundle harvest, sheltered ground drying, stick threshing, retaining planting seeds, knife conversion. Obtain-grain detection alone proves none of those interactions.
- `textiles/grow-flax`: obtains 16 `game:flaxfibers`, after harvest-grain. Missing the entire thresh→ret→wash→crumple→comb sequence. Split/group around meaningful first usable grain and first usable fiber outcomes; creaser, flail and wooden ridge remain upgrades rather than mandatory first-fiber equipment.
- `farming/grow-vegetables`: obtains 12 `game:vegetable-*`, after harvest-grain. Teach food-stage harvesting versus reserved seed plants; final-stage-only wording would be actively harmful.
- `farming/full-harvest`: 32 grain +24 vegetables and prerequisite grow-flax; `textiles/spin-twine` and `make-linen` are downstream of grow-flax. `baking/grind-flour` follows make-quern. Existing endpoints can remain, but their instruction text needs actual pack processing. No repository files changed.

## Verification limits

Static asset and exact-DLL inspection, config lookup, historical module-load evidence, source hash checks and quest-definition reads completed. No live crop run, recipe execution, world setting measurement or newer srMi9 pack verification. Mod ZIP JSON patch scan found no other bundled patch matching the inspected crop/bundle targets, but that is not proof against every possible compiled cross-mod modification. All yield/time claims above are defined parameters or explicitly marked nominal calculations, not fabricated runtime observations.
