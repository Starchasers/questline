# Art of Growing: full existing-quest impact audit

> Historical pre-implementation source audit. Recommendations below are evidence, not a claim that the implementation or native acceptance has run. See [addon and graph contract](artofgrowing.md) for current integration.

## Scope and evidence boundary

- Repository READ ONLY: `<repository>`, HEAD `ea44f9a4d930c3ab7bd5521c69d4ae89c5fa2116`. No repository edits or builds were performed.
- Audited every production chapter under `content/*/assets/questline/questline/chapters/*.json`, plus shared English quest prose from `questline/assets/questline/lang/en.json`; task filters, required predecessors, rewards, optional overrides and chapter placement included. Test-fixture quests are not production curriculum.
- Coverage: **532 authored quest records, 516 unique textual quest IDs**, 56 chapter files, 12 modules. Repeated IDs across optional overrides are deliberately separate records, never silently deduplicated.
- Classification: **25 D (local correction/additional AoG route recommended), 40 C (context/reward/prerequisite clarification; target can remain), 467 U (locally unaffected, justified below)**. Every record has exactly one status; D/C are the bounded affected list, not a claim every descendant recipe changes.
- Original `https://up.snet.ovh/u/srMi9` was rechecked with `curl -I -L --max-time 30` and returned **HTTP/2 404**. This audit uses the pre-existing LOCAL CACHE, not a fresh download from that URL. No claim is made that the unavailable original currently equals these cached bytes.
- Pack evidence: `<research-scratch>/pszczoly-roadmap/integration-data/Mods` and sibling `ModConfig`. `serverconfig.json` LastLaunchMods records game 1.22.7 and these renamed patch builds; that is historical launch evidence, not a live server test.
- `<research-scratch>/pszczoly-roadmap/integration-data/Mods/ArtOfGrowing_1.2.2.zip` — SHA-256 `39f08f333b98c0d561f1e3207a7a7d56a154acc8ce0719378af324a68acddf76`; `1863415` bytes.
- `<research-scratch>/pszczoly-roadmap/integration-data/Mods/CoreOfArts_1.2.2.zip` — SHA-256 `937800ec4d400bffdf72bf8c5b429505beaf55004b89c72663c03e1d0862a78a`; `252441` bytes.
- AoG `modinfo.json`: modid **artofgrowingpatch**, name **Art Of Growing (Unofficial Update)**, version 1.2.2, dependency **coreofartspatch**. Asset domain remains **artofgrowing**, NOT the mod ID. Core of Arts is likewise **coreofartspatch**, version 1.2.2. Any future conditional quest patch must gate on the actual mod ID while matching the asset domain.
- AoG and Core DLLs were decompiled locally with ilspycmd 11.2.0.10050 into `<research-scratch>/aog-audit-source/{decompiled,core}`. This is inspection of cached binaries, not upstream published source. Missing-reference comments in decompiled C# do not constitute runtime verification.
- Loaded relevant audit/editorial skills. Scope is source/asset audit, not a native gameplay acceptance run. No world was loaded and no final merged recipe registry was exported.

## Highest-priority conclusions

1. **Grass drying belongs before early fire, not only farming.** Ordinary knife-cut grass no longer means immediate usable drygrass. The existing `cut-grass` description hides a real waiting/storage/climate process.
2. **`make-fire` has a namespace matcher mismatch.** The ignite task uses `game:firepit-*`; AoG drygrass placement constructs `artofgrowing:firepit-*`. Support both and exercise both placement/ignition events.
3. **Do not globally substitute straw for drygrass.** In this archive `game:drygrass` is hay/feed; `game:thatch` is straw, `artofgrowing:agedgrass` is aged material, `game:cattailtops` remains reed. Kilns accept multiple fibers, while existing basket/rope/skep/shield recipes can still require fresh reeds.
4. **Flax fibers are a processing product.** The complete bundle drying/threshing, stalk retting/washing/softening/combing chain must precede the existing textile twine/linen endpoints; merely changing the crop task to a bundle would not teach textiles.
5. **Harvest grain, seed and food are not interchangeable.** Dried cereal bundles are ground-threshed into planting seeds; knife-hulling makes culinary game grain. Vegetable food-stage harvest and terminal seed-stage harvest are different decisions. Preserve vanilla game output matchers where source keeps them.
6. **Winter and husbandry need explicit hay/feed planning.** Open-field drying pauses in cold weather and rain can reset it. Existing firewood/grain/pickles goals do not prove livestock have food through winter.
7. **Additive recipes are not removal evidence.** This unofficial DLL contains no AoG config loader or recipe-disabling subsystem; its grid recipes add straw alternatives, while targeted JSON patches can disable individual recipes (haybale is explicitly disabled). Do not erase all vanilla routes based on stale config keys or handbook prose.

## Source findings and citation key

All archive-relative asset paths below are inside `ArtOfGrowing_1.2.2.zip` unless another archive is named. `[G]` etc in ledger rows refer to these source bundles. Exact source paths make every recommendation reproducible without the missing public upload.

### [G] Grass, drying, hay and winter

- `assets/artofgrowing/patches/tallgrass.json` changes regular tallgrass drops to `artofgrowing:grass`; dry tallgrass can yield `game:thatch`. `ArtOfGrowing.Blocks/AOGBlockTallGrass.cs` checks knife/scythe and tallgrass state: normal breaking can leave `artofgrowing:haylayer-*`, Shift/half-height cases return item grass instead. This is not simply an ordinary instant item drop in every interaction.
- `assets/artofgrowing/itemtypes/grass.json`: fresh grass transition `Dry`, freshHours 0, transitionHours 24 (variance 1), output `game:drygrass`, ratio 1. These are asset transition parameters, NOT a universal wall-clock drying promise. `AOGBlockEntityGroundStorage.cs:377-421` accelerates stored grass drying off water and distinguishes drying/curing in water.
- `assets/artofgrowing/blocktypes/plant/haylayer.json`: field grass layer converts to drygrass after 12 in-game hours, stopBelowTemperature 8, resetBelowTemperature -1. `AOGTransient.cs:68-143` applies climate checks and probabilistic exposed precipitation reset. English handbook text mentions 8 hours; code/asset says 12. Prefer qualified process wording, not handbook timing copied uncritically.
- `assets/artofgrowing/patches/drygrass.json`: drygrass gets Perish -> artofgrowing:agedgrass, freshHours 4320, transitionHours 448, plus custom AOGItemDryGrass and hay storage. Straw receives the same Perish timer to agedgrass in patches/thatch.json. Neither is an indefinite reserve; no satiety override or drygrass -> straw transition is present in this cache patch.
- `recipes/grid/agedgrass.json` uses a knife on game:hay-aged-ud to output eight agedgrass; use proper material names. Do not call agedgrass fresh straw or fresh grass.

### [F] Fire, firestarters and torches

- `ArtOfGrowing.Items/AOGItemDryGrass.cs:111` consumes drygrass on empty supported ground and obtains `artofgrowing:firepit-construct1`; `blocktypes/wood/firepit.json` declares code firepit, construction states construct1-construct4/extinct/lit/cold, BlockFirepit + Firepit entity, burn by igniter.
- `recipes/grid/thatch.json` adds a straw firestarter (game:thatch + two sticks) and straw torch (two game:thatch + stick -> game:torch-basic-extinct-up). These are additions; no wholesale disabling of older recipes was found in AoG/Core DLL code; targeted JSON disabling exists, notably game haybale.
- `questline/Server/StationPatches.cs` FirepitOutput intercepts ItemSlotOutput in InventorySmelting, not only game-domain blocks; AoG retains game Firepit entity class. Cook/smelt tasks therefore have no demonstrated domain mismatch merely from using AoG firepit. Ignite selector still needs correction at `make-fire`.
- Cache includes ManualFirestarter, Firestarters, ClickUpTorches and RealSmoke AoG patch. Their existence is not proof of a specific hand gesture or all integration events succeeding. Native regression required for ignition, output and charcoal-pit completion.

### [K] Clay and pit-kiln fuel

- `patches/pitkiln.json` adds `thatch` quantity 2 to `/attributes/buildMats/grass/1` and its texture to game pitkiln. It does NOT replace all stages or add agedgrass. Preserve base drygrass and other layer behavior; obtain resolved game buildMats before publishing total-layer counts. Fresh grass is not added.
- Clayforming templates and most fired outcomes are not replaced by AoG. All downstream clay hive, refractory, crucible, glaze, griddle, casting-bed and crock quests inherit the changed loading instructions without automatically needing new outcome IDs.

### [R] Reed storage

- `patches/cattailtops.json`: game:cattailtops retains its code; patch intends to add AoG hay-storage behavior and handbook entries only. The target file literal is game:itemtypes/resource/catttailtops.json (three t characters), a potential patch-target typo requiring resolved-asset verification. No drying transition is in this patch. No blanket AoG patch was found converting rope, hand-basket, shield, skep or poultice recipes to straw. Preserve those matchers and verify intended storage patch targeting.

### [B] Straw building, bedding and alternate namespaces

- `recipes/grid/thatch.json`: AoG adds straw recipes for firestarter, torch, henbox, improvised armor, mudbrick, strawbedding, cob and daub. Their final base-game outcomes can stay game namespace. The added armor recipe uses knife, firewood and straw, not rope.
- `recipes/grid/bed.json`: three `thatchhay-normal-ud` -> `bed-thatch-head-north` in artofgrowing asset domain; also a wooden game bed recipe with straw blocks. Haybale grid recipe is disabled; blocks are obtained through AoG pile conversion rather than the old grid route. Bed outcome can remain available through new block sourcing.
- `recipes/grid/roofing.json`: output `artofgrowing:slantedroofing-thatch-east-free` and companion ridge/tip/corner forms, while `patches/roofing.json` handles aging/remap; game wildcard `game:slantedroofing-*` does not cross namespaces. Support exact new output family rather than assuming match.

### [H] Grain/legume harvesting and cooking inputs

- `patches/crop/flax.json`, `rye.json`, `spelt.json`, `rice.json`, `amaranth.json`, `sunflower.json`, `soybean.json`, `peanut.json`; `itemtypes/grain/grainbundle.json`, `legume-head.json`. Mature grain crops return bundles; flax crop returns grainbundle-flax-wet. Soybean normal ripe stages return artofgrowing:grainbundle-soybean.
- `AOGItemInteract.cs:201-235`: hold interaction on legume-head grainbundle items -> game:legume-TYPE; this held-processing class is NOT bound to ordinary cereal grainbundles, which use ground threshing; sized bundles use artofgrowing:seeds-SIZE-TYPE. Processing consumes bundles, floor sitting/free offhand changes batching; count is randomized, not fixed exact seed yield.
- `assets/game/itemtypes/resource/grainseeds.json` supplies edible, plantable grain seed bags while preserving game:seeds-* codes. `recipes/grid/grains.json`: knife + one game:seeds-* -> one game:grain-TYPE for flax/rye/rice/spelt/sunflower/amaranth/pumpkin. This supports existing game:grain-* tasks after processing.
- `patches/legume.json` changes game legumes to ItemPlantableSeed. It does NOT prove old game:seeds-soybean is absent: resource seed states still include soybean. Planting reward semantic correction should not be mislabeled a missing-code fix.

### [L] Flax and fiber chain

- `itemtypes/grain/flaxbundle.json`: only dry/wet/clear/soft states exist. Dry stalks have Melt -> wet (freshHours 0, transitionHours 672 +/-24), plus Perish -> straw (freshHours 336, transitionHours 6); wet/clear/soft have Perish -> agedgrass (4320 +448). There is no flaxbundle-raw or clear -> dry transition. These are base asset parameters modulated by storage/environment; do not promise a universal number of days.
- `AOGBlockEntityGroundStorage.cs:377-421`: water gates Melt (retting) and Dry transitions and changes multipliers; place flax in water for retting, not dry ground.
- `recipes/barrel/flaxbundle-clear.json` and `recipes/grid/flaxbundle-clear.json`: wash wet bundles to clear with water. Grid requires a liquid container containing water, not an empty bucket.
- `AOGItemInteract.cs:148-199`, bound by classByType only to flaxbundle-clear, turns cleaned flax held interaction into soft; optional offhand creaser accelerates. `AOGItemFlaxSoft.cs:55-167` requires offhand ridge for soft -> game:flaxfibers, one fiber per consumed soft bundle; wooden ridge accelerates. `recipes/grid/flaxtools.json` supplies rough ridge from sticks+rope OR twine, so using rope avoids demanding advanced twine to make the first fibers.
- Twine, linen and later sewing outputs stay game items. Do not rewrite every textile consumer as if its item code disappeared.

### [V] Vegetables, seeds, pumpkin and optional breeding

- `patches/crop/carrot.json` explicitly extends crop to 11 stages, totalGrowthMonths 2.0. Food at 6-10 (highest average yield 11 at stage 7), seeds/rot at 11; early stages only drygrass. Other vegetable crops have analogous but not necessarily identical timing; do not copy carrot numbers to all crops.
- Normal no-addon drops remain game:vegetable-* in crop patches; AoG `patches/vegetable.json` adds handbook data, not blanket removal of base vegetables. AOGBlockPumpkin/AOGPumpkinCropBehavior and pumpkin patches alter fruit lifecycle/interaction; keep exact harvest procedure as runtime acceptance item rather than assuming vanilla fruit harvesting.
- The archive includes sized/wild vegetables/seeds, relevant recipe extensions and conditional `aogbreedingaddon` checks. That addon is NOT present among cached Mods/LastLaunchMods. Do not justify massive base quest matcher changes using inactive addon-only sized outputs. Other packs with breeding addon need a distinct audit.

### [P] Cooking

- `patches/cooking/{porridge,soup,stew,jam}.json` and `patches/barrel/{pickledvegetable,pickledlegume}.json` add vegetable/legume variants. Porridge patch adds vegetables, not unhulled game seeds as grain. Existing base game ingredients/outcomes are not established removed.
- Expanded Foods recipe scan shows game:grain-* remains in soyculture and roastedgrain recipes, game:legume-soybean in food recipes; hulling and shelling supplies these original culinary items.

### [A] Animal feed

- `patches/trough-large.json`: adds fresh grass (4/fill), straw (8/fill), straw blocks (2/fill), pumpkin grain, legume bundles and named grain seed bags (2/fill). Existing base feeds are not deleted; agedgrass is NOT added by this patch. Never describe all fibers as equivalent food.
- `patches/trough-small.json` adds pumpkin grain and named cereal seed bags with foodFor chicken-*. Match feed to species/loaded trough rules, not just nutrition category. Animal feed acceptance is not proved for a modded feed by its presence in inventory.

### [X] Installed optional integrations and configuration limits

- Cache includes BetterHusbandry, LivestockWelfare, ManualHarvesting, NaturalFertilizer, Expanded Foods/Meals/ChefsTricks, TailorsDelight, Wool, OneRoof, Bricklayers, FromGoldenCombs. It does not include BetterRuins, CharcoalKiln, HexsMech or Seafarer archives. Those optional quest modules were STILL audited as authored content; absent providers are explicitly not native-tested.
- `ModConfig/Arts/ArtOfGrowing.json` contains EnableGrassGrowth, EnableSeaweedGrowth, ChangeVanillaRecipes and DisableVanillaGrainRecipes=true; `ChangeNutsNutrition=false`, `DisableVanillaPlantRecipes=false`. These keys are NOT read by any decompiled AoG class (no AoG config class/load call exists in this cached DLL). CoreOfArts COAConfig only reads EnableLiquidMixing; its cached config also has stale-looking EnableDoughForming/DisableVanillaDoughRecipes fields not represented by that class. Do not turn these unused fields into assertions that all vanilla recipes are disabled.
- Cross-mod recipe scan: NaturalFertilizer manure mix, LivestockWelfare strawbedding and Wool fertilizer still directly use game:drygrass; OneRoof roofing directly uses game:drygrass; Chef Tricks firelogs do too. This is why changing every hay reward/recipe globally to straw would be wrong. Foodshelves has explicit AoG support; RealSmoke patch targets artofgrowing firepit. None of these JSON scans proves the final registry is conflict-free.

### [Q] Repository provenance and optional override constraints

- Authored definitions are under content modules, shared prose under questline/assets/questline/lang. Optional modules repeat IDs such as make-mudbricks, roast-meat, cook-roots, make-sails and other tailoring replacements. Apply future AoG changes to every active override, not only the vanilla source file.
- Keep published quest IDs and progress semantics unless an approved migration explicitly changes them. Adding process milestones can retain existing endpoints; do not complete/grant old quests merely because the wording changed.
- Shared English description keys are keyed by textual quest ID, not provider: different vanilla/Bricklayers workflows sharing make-mudbricks cannot be given contradictory unqualified global prose. A future implementation needs pack-aware text/replacement handling or separate localization keys, plus translations, not a blind global edit.

## Complete affected-record recommendations (D and C)

`D` means change local guidance and/or allow a proven alternate outcome; it does not mean every current item is unresolvable. `C` means retain the target unless a stated native test fails, but fix context/reward intent. Identifiers are quoted exactly as in authored content. In prose, any accidental human spacing in “artofgrowing” refers to asset domain `artofgrowing`.

### D — `bricklayers/bricklayers-clay-and-fire::make-mudbricks`
- Source: `content/bricklayers/assets/questline/questline/chapters/bricklayers-clay-and-fire.json`
- Current prose: Four raw daub make a mudbrick in the crafting grid; daub is soil, dry grass, sand and clay. Mudbricks need no firing.
- Current tasks: `[{"type": "obtain", "item": "bricklayers:mudbrick-*", "count": 8}]`
- Recommendation: Preserve Bricklayers four raw daub -> mudbrick workflow; explain AoG straw alternative when producing the raw daub. Drygrass reward remains perishable AoG hay; replace reward with game:thatch if intended to supply building fiber, or retain with explicit feed meaning. [B,X] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### C — `efchefstricks/efchefstricks-baking::make-crumb-feed`
- Source: `content/efchefstricks/assets/questline/questline/chapters/efchefstricks-baking.json`
- Current prose: Bread crumbs alone in the crafting grid make bread crumb feed. You can't eat it, but many animals will, and it's a cheap way to keep livestock fed.
- Current tasks: `[{"type": "obtain", "item": "efchefstricks:breadcrumbfeed", "count": 4}]`
- Recommendation: Bread crumb feed remains a separate feed, not AoG drygrass/straw. Preserve obtain target; qualify broad animal feeding advice against loaded trough dietary rules. AoG trough patch does not itself establish breadcrumb-feed support for all species. [A,X]

### C — `expandedfoods/expandedfoods-baking::roast-grain`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-baking.json`
- Current prose: Put grain in a hot clay oven and take it out once it's roasted. Roasted grain goes into porridge and pilaf, and keeps longer than raw grain.
- Current tasks: `[{"type": "obtain", "item": "expandedfoods:roastedgrain-*", "count": 4, "unchecked": true}]`
- Recommendation: Keep expandedfoods:roastedgrain-* target; culinary grain must first be hulled from AoG seeds. Preserve the Expanded Foods heating route, not fresh bundle roasting. [H,X]

### C — `expandedfoods/expandedfoods-farming::press-oil`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`
- Current prose: Fill the fruit press with flax grain, sunflower seeds or soybeans and press it. Cooking oil fries breaded food and enriches dough.
- Current tasks: `[{"type": "obtain", "item": "expandedfoods:foodoilportion-*"}]`
- Recommendation: Keep existing output/processing route. Use shelled legumes or hulled culinary grain (flax/sunflower) rather than raw bundles/planting bags; link revised harvest steps. [H,X]

### D — `expandedfoods/expandedfoods-farming::grow-soybeans`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`
- Current prose: Plant soybean seeds in farmland and harvest eight soybeans. Expanded Foods turns them into oil, soy milk and soy sauce, each of which takes plenty of beans.
- Current tasks: `[{"type": "obtain", "item": "game:legume-soybean", "count": 8}]`
- Recommendation: Replace straight harvest wording: ripe soybean yields artofgrowing:grainbundle-soybean, hold right-click to shell to game:legume-soybean; that food item is now plantable. Keep legume obtain x8 target. [H]

### C — `expandedfoods/expandedfoods-farming::soak-soybeans`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`
- Current prose: Seal soybeans in a barrel with a litre of water for each. Three days later they're soaked, ready to become soy sauce or soy milk.
- Current tasks: `[{"type": "obtain", "item": "expandedfoods:soyprep-soaked", "count": 8}]`
- Recommendation: Keep soaked soybean goal; first shell harvested bundles to game:legume-soybean. Subsequent water soak is Expanded Foods processing, not AoG flax retting. [H,X]

### C — `expandedfoods/expandedfoods-farming::culture-soybeans`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`
- Current prose: Mix the soybean powder with a grain, such as spelt, rice or flax, in the crafting grid or the mixing bowl.
- Current tasks: `[{"type": "obtain", "item": "expandedfoods:soyprep-cultured", "count": 8}]`
- Recommendation: Keep existing output/processing route. Use shelled legumes or hulled culinary grain (flax/sunflower) rather than raw bundles/planting bags; link revised harvest steps. [H,X]

### D — `expandedfoods/expandedfoods-farming::brew-soy-sauce`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`
- Current prose: Seal cultured soybeans with a litre of brine each in a barrel for a week, then press the slurry in the fruit press. A litre of soy sauce takes about seven; it seasons meals and kneaded foods.
- Current tasks: `[{"type": "obtain", "item": "expandedfoods:soysauce"}]`
- Recommendation: Soy sauce processing outcome is unchanged; replace AoG planting reward game:seeds-soybean with game:legume-soybean or explicitly test legacy seed planting. Include shelling prerequisite link, not a fictitious new soy sauce recipe. [H,X] AoG makes game:legume-soybean plantable; prefer that for planting rewards; legacy seeds may still resolve. [H]

### C — `expandedfoods/expandedfoods-kitchen::roast-meat`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-kitchen.json`
- Current prose: Put raw meat in a lit firepit and take it out once it's cooked. Cooked meat fills you up and won't make you sick.
- Current tasks: `[{"type": "clayform", "item": "aculinaryartillery:saucepan-*-raw"}, {"type": "obtain", "item": "game:@(redmeat|bushmeat|poultry)-cooked", "unchecked": true}]`
- Recommendation: Preserve Expanded Foods obtain-based override and its saucepan task; AoG firepit construction is the upstream fix, not reason to rewrite this cooked meat target. [F]

### C — `expandedfoods/expandedfoods-kitchen::power-mixing-bowl`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-kitchen.json`
- Current prose: Craft a mixing bowl with a table and a wooden axle into a powered mixing bowl, and connect a turning axle to its bottom. It kneads on its own, and puts what it makes beside it, or into a hopper.
- Current tasks: `[{"type": "place", "block": "aculinaryartillery:poweredmixingbowl-*"}]`
- Recommendation:  Reward is already hulled culinary grain, a processing bypass but not a missing item. [H]

### C — `expandedfoods/expandedfoods-stone-age::cook-roots`
- Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-stone-age.json`
- Current prose: Break a cut cattail again to dig up its root, faster with a shovel. Roast the root on a lit firepit: it's plain, but it keeps you going when nothing else will.
- Current tasks: `[{"type": "cook", "item": "expandedfoods:cookedveggie-cattailroot-charred"}]`
- Recommendation: Expanded Foods charred root outcome remains the override; preserve it and route through working AoG firepit. Do not restore vanilla cooked-root matcher. [F]

### C — `vanilla/arms-and-armor::make-crude-shield`
- Source: `content/vanilla/assets/questline/questline/chapters/arms-and-armor.json`
- Current prose: Six sticks and three cattail tops, papyrus tops or bamboo stakes make a crude shield. Hold it in your offhand and Sneak to block. See the <a href="handbook://craftinginfo-armor">armor guide</a>.
- Current tasks: `[{"type": "obtain", "item": "game:shield-crude"}]`
- Recommendation: Retain fresh cattailtops/papyrustops/bamboo recipe; no cached patch establishes reed drying; retain the existing reed input and verify intended storage behavior. No AoG shield recipe replacement shown. [R]

### D — `vanilla/arms-and-armor::make-improvised-armor`
- Source: `content/vanilla/assets/questline/questline/chapters/arms-and-armor.json`
- Current prose: Firewood, rope and dry grass make improvised body armor, with a knife in the crafting grid. It breaks after a few hits, but it can save your life.
- Current tasks: `[{"type": "obtain", "item": "game:armor-body-improvised-wood"}]`
- Recommendation: Add AoG straw recipe using firewood, knife and game:thatch; do not claim AoG recipe consumes rope: its JSON does not. Preserve game:armor-body-improvised-wood output and retain valid vanilla alternatives. [B]

### C — `vanilla/baking::grind-flour`
- Source: `content/vanilla/assets/questline/questline/chapters/baking.json`
- Current prose: Put grain in the quern and turn it.
- Current tasks: `[{"type": "obtain", "item": "game:flour-*", "count": 4}]`
- Recommendation: Retain game:flour-* obtain target and quern action; explain that AoG seed bags first need knife-hulling to game grain. Do not infer seed bags grind directly just from their edible status. [H]

### C — `vanilla/baking::eat-well`
- Source: `content/vanilla/assets/questline/questline/chapters/baking.json`
- Current prose: Your character panel shows five food groups: fruit, vegetables, grain, protein and dairy. Keeping all of them full raises your maximum health, so keep a varied larder.
- Current tasks: `[{"type": "obtain", "item": "game:fruit-*", "count": 8, "name": "questline:name-any-fruit"}, {"type": "obtain", "item": "game:vegetable-*", "count": 8, "name": "questline:name-any-vegetable"}, {"type": "obtain", "item": "game:bread-*-perfect", "count": 4}]`
- Recommendation: Keep current fruit/vegetable/bread targets for this non-breeding cache. Add grain-processing link; inspect future breeding addon separately rather than replacing all vegetable matchers now. [H,V]

### C — `vanilla/beekeeping::raid-wild-hive`
- Source: `content/vanilla/assets/questline/questline/chapters/beekeeping.json`
- Current prose: Wild bee hives hang in trees and hide in hollow logs. Breaking one gives honeycomb, but angers the bees and ends that colony. Leave one standing if you want to catch a swarm.
- Current tasks: `[{"type": "obtain", "item": "game:honeycomb", "count": 2}]`
- Recommendation:  Reward remains reed; AoG storage patch has a suspicious target filename, but no proven drying transition; keep existing recipe input. [R]

### C — `vanilla/beekeeping::make-skep`
- Source: `content/vanilla/assets/questline/questline/chapters/beekeeping.json`
- Current prose: A skep is woven from cattail or papyrus tops and sealed with clay, in the crafting grid. It's a home for bees.
- Current tasks: `[{"type": "obtain", "item": "game:skep-*"}]`
- Recommendation: Retain cattail/papyrus+clay recipe and game:skep-* target. No cattail drying transition is proven; reward x6 is still the existing valid reed item, not straw. [R] Reward remains reed; AoG storage patch has a suspicious target filename, but no proven drying transition; keep existing recipe input. [R]

### C — `vanilla/beekeeping::squeeze-honey`
- Source: `content/vanilla/assets/questline/questline/chapters/beekeeping.json`
- Current prose: Hold honeycomb over an open container, such as a bowl or bucket, and squeeze it to get honey and beeswax. A fruit press does it faster. Each comb gives a fifth of a litre.
- Current tasks: `[{"type": "obtain", "item": "game:honeyportion"}]`
- Recommendation:  Reward remains reed; AoG storage patch has a suspicious target filename, but no proven drying transition; keep existing recipe input. [R]

### C — `vanilla/beekeeping::make-candle`
- Source: `content/vanilla/assets/questline/questline/chapters/beekeeping.json`
- Current prose: Cook three beeswax and one flax fiber in a pot over the fire to make a candle.
- Current tasks: `[{"type": "obtain", "item": "game:candle", "count": 2}]`
- Recommendation: Keep candle recipe/fiber goal; link fully processed AoG flax rather than obtaining fibers from harvesting. No AoG candle replacement shown. [L]

### D — `vanilla/building::make-roof`
- Source: `content/vanilla/assets/questline/questline/chapters/building.json`
- Current prose: Roofing comes in many kinds: thatch, sod over boards, boards alone, or clay shingles. Make eight pieces of any of them and put a roof over your head.
- Current tasks: `[{"type": "obtain", "item": "game:slantedroofing-*", "count": 8}]`
- Recommendation: Add AoG straw roofing recipe and artofgrowing:slantedroofing-* output namespace (plus ridge/tip/corner if selected), alongside original game filter. Do not assume the original game:slantedroofing-* pattern matches the AoG output: it does not. OneRoof is installed and can add competing recipes; require final registry verification. [B,X]

### C — `vanilla/clay-and-fire::form-bowl`
- Source: `content/vanilla/assets/questline/questline/chapters/clay-and-fire.json`
- Current prose: Hold clay, then shift and right-click the ground to start clay forming. Pick the bowl, and add clay with right-click and remove it with left-click, layer by layer.
- Current tasks: `[{"type": "clayform", "item": "game:bowl-*-raw"}]`
- Recommendation: Clayforming goal unchanged; game:drygrass reward now means hay. Prefer game:thatch if reward is intended as straw kiln starter; both are accepted kiln inputs. [G,K] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### D — `vanilla/clay-and-fire::fire-pottery`
- Source: `content/vanilla/assets/questline/questline/chapters/clay-and-fire.json`
- Current prose: Raw clay must be fired before it's any use. Make a pit kiln: shift and right-click to set the raw pieces on the ground, add dry grass, sticks and firewood, and light it. Wait for it to burn out.
- Current tasks: `[{"type": "obtain", "item": "game:bowl-*-fired"}]`
- Recommendation: Replace exclusive dry-grass wording with the patched kiln first layer: base drygrass OR added game:thatch (patch quantity 2 at buildMats/grass/1), then base sticks/firewood; do not invent agedgrass support or total layer counts. Preserve fired pottery tasks. Do not suggest fresh grass. [K]

### C — `vanilla/clay-and-fire::make-bricks`
- Source: `content/vanilla/assets/questline/questline/chapters/clay-and-fire.json`
- Current prose: Four clay make a raw brick in the crafting grid. Fire the raw bricks in a pit kiln. Fired bricks, set in mortar, build walls that last.
- Current tasks: `[{"type": "obtain", "item": "game:rawbrick-*", "count": 8}, {"type": "obtain", "item": "game:burnedbrick-*", "count": 8}]`
- Recommendation: Keep fired brick target; link revised kiln loading with drygrass or the added straw alternative rather than duplicating obsolete first-layer instructions. [K]

### C — `vanilla/clay-and-fire::cook-meal`
- Source: `content/vanilla/assets/questline/questline/chapters/clay-and-fire.json`
- Current prose: Put the pot in a lit firepit with ingredients inside it, wait for it to cook, and take it out. A mixed meal fills you up far better than its parts.
- Current tasks: `[{"type": "cook", "item": "game:claypot-*-cooked", "name": "questline:name-any-pot-meal"}]`
- Recommendation: Outcome/recipe unchanged by AoG; verify cooked output reporting against the AoG firepit. Questline uses InventorySmelting output interception rather than a hard-coded firepit domain for cooked food. [F,Q]

### C — `vanilla/copper-age::make-charcoal`
- Source: `content/vanilla/assets/questline/questline/chapters/copper-age.json`
- Current prose: Dig a pit, fill it with full stacks of firewood and cover it with blocks that don't burn, leaving the top of one stack open. Build a firepit on that stack, light it, and seal it within half an hour. See the <a href="handbook://craftinginfo-charcoalburning">charcoal burning guide</a>.
- Current tasks: `[{"type": "obtain", "item": "game:charcoal", "count": 16}]`
- Recommendation: Keep charcoal target; construction uses AoG drygrass firepit route, so reference revised make-fire and preserve charcoal-pit process pending native check. [F]

### D — `vanilla/copper-age::make-scythe`
- Source: `content/vanilla/assets/questline/questline/chapters/copper-age.json`
- Current prose: Smith a scythe head and fit it to a stick. A scythe cuts grass and harvests grain over a wider area than a knife.
- Current tasks: `[{"type": "obtain", "item": "game:scythe-*"}]`
- Recommendation: Retain game:scythe-*; add that AoG replaces ItemScythe behavior and leaves harvest layers/crop bundles rather than promising instantly usable drygrass or grain. Cross-link grass drying/threshing; seed reward remains game:seeds-spelt. [G,H]

### D — `vanilla/farming::gather-seeds`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: Wild crops grow here and there. Harvesting them gives seeds to plant.
- Current tasks: `[{"type": "obtain", "item": "game:seeds-*", "count": 4}]`
- Recommendation: Rewrite wild-crop harvest as collection/processing, not always immediate seeds: grain heads must be rubbed/threshed and vegetables can need a later seed-bearing stage. Keep game:seeds-* goal as processed seed endpoint. ManualHarvesting is installed; final interaction must be checked with it. [H,X]

### D — `vanilla/farming::harvest-grain`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: Plant seeds on tilled farmland, within three blocks of water if you can, or water it. Harvest when the crop is fully grown.
- Current tasks: `[{"type": "obtain", "item": "game:grain-*", "count": 16}]`
- Recommendation: Replace direct grain-drop claim with mature crop -> artofgrowing:grainbundle-TYPE-wet -> dry -> place on ground and thresh to game:seeds-TYPE and straw -> knife in grid to game:grain-TYPE when culinary grain is needed. Preserve final game:grain-* x16 task, add process milestones rather than switching it to seed bags. Non-grain early crop stages can drop only drygrass. [H]

### D — `vanilla/farming::grow-vegetables`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: Plant carrots, onions, turnips, parsnips or cabbages. Each crop draws on one of the soil's three nutrients, shown on the farmland's tooltip: rotate crops so the soil can recover.
- Current tasks: `[{"type": "obtain", "item": "game:vegetable-*", "count": 12, "name": "questline:name-any-vegetable"}]`
- Recommendation: Teach harvesting food before the terminal seed stage; carrot stages 6-10 give vegetables, 11 gives seeds/rot, with best food yield at 7 in this archive. Do not tell players to wait until final stage for edible crop. Preserve game:vegetable-* output in this cache (no breeding addon). [V]

### C — `vanilla/farming::make-quern`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: A quern grinds grain into flour. Two sticks and four full blocks of granite, andesite, basalt or peridotite make one, with a hammer and chisel in the crafting grid. A rock block comes out whole once everything around it has been dug away.
- Current tasks: `[{"type": "obtain", "item": "game:quern-*"}]`
- Recommendation: Quern crafting/output unchanged; its game:grain-spelt reward is already processed culinary grain, so it intentionally bypasses drying/threshing/hulling. Retain unless progression design prohibits that shortcut. [H] Reward is already hulled culinary grain, a processing bypass but not a missing item. [H]

### D — `vanilla/farming::grow-pumpkin`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: A pumpkin plant spreads a vine, and the pumpkins grow on the ground beside it, so leave it room. Cut a pumpkin into slices with a knife in the crafting grid.
- Current tasks: `[{"type": "obtain", "item": "game:pumpkin-fruit-4"}, {"type": "obtain", "item": "game:vegetable-pumpkin"}]`
- Recommendation: Teach AoG pumpkin fruit interaction/selection and separate seeds from hollowed fruit; preserve game:vegetable-pumpkin goal only after verifying its resolved harvest/interaction path. Class AOGBlockPumpkin and patched pumpkin crop/fruit make generic vanilla maturity instructions insufficient. Do not invent a seed-processing count from the asset name. [V]

### D — `vanilla/farming::full-harvest`
- Source: `content/vanilla/assets/questline/questline/chapters/farming.json`
- Current prose: Keep several fields: grain, vegetables and flax, rotated and fertilized. Below 10°C crops grow slowly and below 0°C not at all, so the harvest before winter matters.
- Current tasks: `[{"type": "obtain", "item": "game:grain-*", "count": 32}, {"type": "obtain", "item": "game:vegetable-*", "count": 24, "name": "questline:name-any-vegetable"}]`
- Recommendation: Add completed drying/threshing/hulling and distinguish food harvest versus seed harvest; retain game grain/vegetable outcomes in this non-breeding pack. Review seed-soybean reward: AoG makes game:legume-soybean itself plantable, so that is the appropriate AoG planting reward; game:seeds-soybean may still exist, so this is a semantic correction, not demonstrated missing item. [H,V] AoG makes game:legume-soybean plantable; prefer that for planting rewards; legacy seeds may still resolve. [H]

### C — `vanilla/husbandry::make-trough`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: Three planks make a small trough, for chickens, hares and other small animals. Fill it with grain or vegetables: fed animals breed, and hungry ones lose weight over winter.
- Current tasks: `[{"type": "place", "block": "game:trough-*-small-*"}]`
- Recommendation: Keep game:trough-*-small*; seed bags are added for chicken-* (flax, rye, rice, spelt, sunflower, amaranth and pumpkin). Link shelling/hulling distinction and verify loaded species rules. Do not copy large trough straw or grass entries onto the small trough. [A]

### D — `vanilla/husbandry::make-large-trough`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: Pigs, sheep and goats eat from a large trough, made from five planks. Animals are drawn to a full trough, which helps when herding them in.
- Current tasks: `[{"type": "place", "block": "game:trough-*-large-*"}]`
- Recommendation: Preserve game:trough-*-large* place goal; expand feed instructions to AoG fresh grass, base drygrass (hay), added straw, straw blocks and seed bags as patched. Do not treat every feed as nutritionally equivalent; fresh grass and straw require different quantityPerFillLevel values. BetterHusbandry and LivestockWelfare may further modify resolved feed rules. [A,X]

### D — `vanilla/husbandry::breed-animals`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: Keep a male and a female of the same kind in the pen and their trough full, and in time they have young. Animals bred this way grow tamer each generation. Tick this off when the first young are born.
- Current tasks: `[{"type": "checkbox"}]`
- Recommendation: Rewrite vague grain-only continuation into species-appropriate feed plus hay reserve/drying/storage. Keep the multiply-animals checkbox, do not auto-grant from owning grass; verify actual reproduction as the quest asks. Grain game:grain-* still appears among feed alternatives; seed bags are added, not universally substituted. [A]

### D — `vanilla/husbandry::make-henbox`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: Five planks and dry grass make a henbox. Hens lay in it rather than on the ground, and a broody hen sits on three eggs until they hatch, if there's a rooster about and the hens are well fed.
- Current tasks: `[{"type": "place", "block": "game:henbox*"}]`
- Recommendation: Keep game:henbox-* target; add AoG straw/game:thatch nest material route. Existing drygrass reward is feed, not durable straw; prefer game:thatch reward if it supplies nesting. [B,A] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### C — `vanilla/husbandry::make-basket-trap`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: A basket of cattail or papyrus tops and a stick make a basket trap. Bait it with food the animal likes and it may catch chickens, hares and many young animals.
- Current tasks: `[{"type": "obtain", "item": "game:baskettrap-*"}]`
- Recommendation: Trap outcomes unchanged; AoG storage-patch targeting and seed-versus-grain distinctions make bait advice worth checking. No evidence all seed bags are acceptable bait: retain tested bait instead of guessing. [R,H]

### C — `vanilla/husbandry::make-crate-trap`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: A reinforced crate trap is built from planks and bronze or better nails and strips. It catches larger animals than a basket trap, but tiny baits like grain won't do.
- Current tasks: `[{"type": "obtain", "item": "game:trapcrate-wood"}]`
- Recommendation: Trap outcomes unchanged; AoG storage-patch targeting and seed-versus-grain distinctions make bait advice worth checking. No evidence all seed bags are acceptable bait: retain tested bait instead of guessing. [R,H]

### C — `vanilla/husbandry::melt-fat`
- Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`
- Current prose: Pigs, sheep, goats, deer, bears and raccoons leave raw fat when you harvest them. Cook it in a pot over the fire and it sets into lumps of rendered fat, used for pelts, the fruit press and sealing crocks.
- Current tasks: `[{"type": "obtain", "item": "game:fat-rendered", "count": 4}]`
- Recommendation: Outcome/recipe unchanged by AoG; verify cooked output reporting against the AoG firepit. Questline uses InventorySmelting output interception rather than a hard-coded firepit domain for cooked food. [F,Q]

### C — `vanilla/kitchen::roast-meat`
- Source: `content/vanilla/assets/questline/questline/chapters/kitchen.json`
- Current prose: Put raw meat in a lit firepit and take it out once it's cooked. Cooked meat fills you up and won't make you sick.
- Current tasks: `[{"type": "obtain", "item": "game:poultry-raw"}, {"type": "cook", "item": "game:poultry-cooked"}]`
- Recommendation: Food output remains valid; use supported AoG firepit and previously dried tinder. No source evidence that AoG itself changes this food outcome or forces a new cook task. [F]

### C — `vanilla/kitchen::cook-stew`
- Source: `content/vanilla/assets/questline/questline/chapters/kitchen.json`
- Current prose: A stew needs two portions of meat, and takes vegetables or eggs as extras. Every slot of the pot you use must hold the same number of portions.
- Current tasks: `[{"type": "obtain", "item": "game:poultry-raw", "count": 2}, {"type": "cook", "item": "game:claypot-*-cooked", "name": "questline:name-any-pot-meal"}]`
- Recommendation: Preserve cooked-pot/recipe filters. AoG cooking patches add vegetables/legumes rather than deleting ordinary food; optional breeding-sized vegetables are not active in this cache. Link firepit setup; recipe composition remains the existing one unless final registry says otherwise. [P,V]

### C — `vanilla/kitchen::cook-soup`
- Source: `content/vanilla/assets/questline/questline/chapters/kitchen.json`
- Current prose: Pour a portion of water into the pot, then add vegetables, and meat if you have it. Soup stretches a few vegetables a long way.
- Current tasks: `[{"type": "obtain", "item": "game:vegetable-*", "count": 3, "name": "questline:name-any-vegetable"}, {"type": "cook", "item": "game:claypot-*-cooked", "name": "questline:name-any-pot-meal"}]`
- Recommendation: Preserve cooked-pot/recipe filters. AoG cooking patches add vegetables/legumes rather than deleting ordinary food; optional breeding-sized vegetables are not active in this cache. Link firepit setup; recipe composition remains the existing one unless final registry says otherwise. [P,V]

### C — `vanilla/kitchen::cook-porridge`
- Source: `content/vanilla/assets/questline/questline/chapters/kitchen.json`
- Current prose: Porridge is two to four portions of grain, with fruit, vegetables or honey as extras. Grain alone barely feeds you; as porridge it fills a bowl.
- Current tasks: `[{"type": "obtain", "item": "game:grain-*", "count": 4}, {"type": "cook", "item": "game:claypot-*-cooked", "name": "questline:name-any-pot-meal"}]`
- Recommendation: Preserve game:claypot-*-cooked and recipe=porridge matching; use culinary game:grain-* after hulling. The AoG porridge patch adds vegetable alternatives only: handbook prose about porridge from unhulled seeds is NOT proven by this JSON. Add a processing cross-link, do not replace ingredient with seeds without runtime proof. [H,P]

### C — `vanilla/preservation::pickle-vegetables`
- Source: `content/vanilla/assets/questline/questline/chapters/preservation.json`
- Current prose: Put vegetables in a barrel with a litre of brine each, and seal it. They take about two weeks. Pickled vegetables keep far longer than fresh, and curdle milk for cheese.
- Current tasks: `[{"type": "obtain", "item": "game:pickledvegetable-*", "count": 4, "name": "questline:name-any-pickled-vegetable"}]`
- Recommendation: Keep game:pickledvegetable-* in this cache; AoG adds possible wild/sized variants under addon pathways but does not establish removal of ordinary pickles. Link crop food-stage timing if helpful. [V,P]

### D — `vanilla/stone-age::make-firestarter`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Two sticks and a little dry grass make a firestarter in the crafting grid. It's how you light fires until you have something better.
- Current tasks: `[{"type": "obtain", "item": "game:firestarter"}]`
- Recommendation: Retain game:firestarter outcome; teach dried tinder or AoG straw alternative, and do not claim fresh cut grass is ready. ManualFirestarter/Firestarters are installed and own ignition interaction; do not replace their mechanics with a guessed vanilla click sequence. Consider changing the drygrass reward to straw only if it is meant as durable tinder rather than animal feed. [F,G,X] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### C — `vanilla/stone-age::knap-shovel`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Knap a shovel head, then put it and a stick in the crafting grid. A shovel digs soil, sand and clay far faster than your hands.
- Current tasks: `[{"type": "knap", "item": "game:shovelhead-*"}, {"type": "obtain", "item": "game:shovel-*"}]`
- Recommendation:  Reward remains reed; AoG storage patch has a suspicious target filename, but no proven drying transition; keep existing recipe input. [R]

### D — `vanilla/stone-age::cut-grass`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Cutting tall grass with a knife gives dry grass: kindling, bedding and much else.
- Current tasks: `[{"type": "obtain", "item": "game:drygrass", "count": 10}]`
- Recommendation: Replace the immediate dry-grass claim: ordinary knife cutting yields artofgrowing fresh grass (artofgrowing:grass) or leaves a hay layer; teach drying and obtaining game:drygrass before fire. Retain the final drygrass obtain count, but add a preceding fresh-grass/drying milestone. Drygrass is not straw/game:thatch. [G]

### C — `vanilla/stone-age::gather-reeds`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Cattails grow in shallow water and on wet shores. Break them, faster with a knife, to get the tops; what's left keeps its root, and grows back.
- Current tasks: `[{"type": "obtain", "item": "game:cattailtops", "count": 10}]`
- Recommendation: AoG intends to add storage/handbook data to cattailtops, but its target path spells catttailtops. Keep existing game:cattailtops recipe/obtain filters; no cached transition proves fresh reed turns into straw. Do not incorrectly replace cordage/basket input with straw. [R] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### C — `vanilla/stone-age::first-hunt`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Chickens are easy prey. Larger animals fight back: keep your distance until you're better armed.
- Current tasks: `[{"type": "kill", "entity": "game:chicken-*"}]`
- Recommendation:  Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### C — `vanilla/stone-age::ground-storage`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Hold an item, then shift and right-click flat ground to set it down: up to four pots or bowls fit in a block, and firewood stacks into a pile. Tools lean against a wall with shift, ctrl and right-click. See the <a href="handbook://gamemechanicinfo-groundstorage">ground storage guide</a>. Tick this off once you've stored something.
- Current tasks: `[{"type": "checkbox"}]`
- Recommendation: Basic sneak-right-click pile task stays manual, but explicitly teach AoG grass/grain/ flax piles and Ctrl+Shift+RMB conversion. This is now a processing prerequisite for drying, cereal threshing and hay blocks, not merely convenience storage; do not claim ordinary ground storage interaction is enough for every AoG action. [G,H,L]

### D — `vanilla/stone-age::make-fire`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Shift and right-click the ground with dry grass to start a firepit, add four firewood, then hold right-click on it with the firestarter until it catches.
- Current tasks: `[{"type": "ignite", "block": "game:firepit-*"}]`
- Recommendation: Normal drygrass interaction constructs artofgrowing firepits. Extend the ignite filter from game:firepit-* to support artofgrowing:firepit-*; preserve vanilla alternative. Explain dried-grass or straw tinder before four firewood. Final runtime filter must use exact domain artofgrowing without spaces (artofgrowing). [F,G]

### C — `vanilla/stone-age::make-basket`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Ten cattails make a hand basket in the crafting grid. Put it in one of your bag slots for more room to carry.
- Current tasks: `[{"type": "obtain", "item": "game:basket-normal-*"}]`
- Recommendation: AoG intends to add storage/handbook data to cattailtops, but its target path spells catttailtops. Keep existing game:cattailtops recipe/obtain filters; no cached transition proves fresh reed turns into straw. Do not incorrectly replace cordage/basket input with straw. [R]

### D — `vanilla/stone-age::hay-bed`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Eight dry grass make a hay block, and three hay blocks make a bed. Sleeping through the night is safer than wandering in the dark.
- Current tasks: `[{"type": "obtain", "item": "game:bed-hay-*"}]`
- Recommendation: Add AoG thatch-bed alternative: three artofgrowing:thatchhay-normal-ud blocks -> artofgrowing:bed-thatch-head-north; extend the obtain bed filter if this is the intended pack early bed. The game haybale grid recipe is explicitly disabled in patches/drygrass.json; teach pile conversion (Ctrl+Shift+RMB) for hay/straw blocks instead of the old eight-grass grid claim. Never silently replace the vanilla quest for AoG-absent players. [B]

### D — `vanilla/stone-age::make-torch`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: A stick and dry grass make a torch. Light it at a burning fire. Torches light the way at night and in caves.
- Current tasks: `[{"type": "obtain", "item": "game:torch-basic-*", "count": 2}]`
- Recommendation: Retain game:torch-* task; teach two straw/game:thatch plus a stick as AoG additional recipe, lighting at the now-supported firepit. Existing drygrass torch route is not proved removed. Do not use fresh grass as torch material. [F]

### C — `vanilla/stone-age::cook-roots`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Break a cut cattail again to dig up its root, faster with a shovel. Roast the root on a lit firepit: it's plain, but it keeps you going when nothing else will.
- Current tasks: `[{"type": "cook", "item": "game:vegetable-cookedcattailroot"}]`
- Recommendation: Food output remains valid; use supported AoG firepit and previously dried tinder. No source evidence that AoG itself changes this food outcome or forces a new cook task. [F]

### D — `vanilla/stone-age::build-shelter`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Five dry grass and four soil make ten blocks of cob in the crafting grid. Raise walls and a roof around your bed before the nights grow cold.
- Current tasks: `[{"type": "place", "block": "game:cob-*", "count": 20}]`
- Recommendation: Preserve game:cob-* place target; add AoG straw/game:thatch ingredient route. Existing drygrass recipe is not shown disabled. [B]

### C — `vanilla/stone-age::make-rope`
- Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`
- Current prose: Rope is twisted from cattail or papyrus tops, or from wild vines, in the crafting grid. Tongs, ladders and much else need it.
- Current tasks: `[{"type": "obtain", "item": "game:rope"}]`
- Recommendation: AoG intends to add storage/handbook data to cattailtops, but its target path spells catttailtops. Keep existing game:cattailtops recipe/obtain filters; no cached transition proves fresh reed turns into straw. Do not incorrectly replace cordage/basket input with straw. [R] Reward remains reed; AoG storage patch has a suspicious target filename, but no proven drying transition; keep existing recipe input. [R]

### D — `vanilla/textiles::grow-flax`
- Source: `content/vanilla/assets/questline/questline/chapters/textiles.json`
- Current prose: Plant flax seeds in farmland and harvest the grown crop. Flax gives fibers as well as seeds and grain.
- Current tasks: `[{"type": "obtain", "item": "game:flaxfibers", "count": 16}]`
- Recommendation: Replace instant-fiber harvesting claim. Mature flax -> artofgrowing:grainbundle-flax-wet; dry the bundle then thresh on ground to obtain seeds and flaxbundle-dry stalks. Ret flaxbundle-dry in water to flaxbundle-wet, wash to flaxbundle-clear using water, soften by held interaction to flaxbundle-soft, then hold soft flax with ridge in offhand to obtain game:flaxfibers. Retain final fibers x16 goal; add distinct processing milestones and a non-circular rough-ridge route (can use rope). [L]

### C — `vanilla/textiles::spin-twine`
- Source: `content/vanilla/assets/questline/questline/chapters/textiles.json`
- Current prose: Four flax fibers make a length of flax twine, in the crafting grid. Twine also mends clothing a little.
- Current tasks: `[{"type": "obtain", "item": "game:flaxtwine", "count": 4}]`
- Recommendation: Four fibers -> twine stays valid; fiber prerequisite now means fully processed flax, not crop drop. Reward of four fibers is a deliberate processing bypass, not invalid item. [L] Reward is already fully processed fiber, a bypass but not a missing item. [L]

### C — `vanilla/wider-world::relight-fire`
- Source: `content/vanilla/assets/questline/questline/chapters/wider-world.json`
- Current prose: Rain and snow put out firepits, torches and forges and cool hot metal. Relight a doused fire with a torch, and roof over the ones that matter. See the <a href="handbook://gamemechanicinfo-weather">weather guide</a>. Tick this off once you have.
- Current tasks: `[{"type": "checkbox"}]`
- Recommendation: Keep weather checkbox and original extinguishing advice; include AoG firepit in ignition test matrix rather than hard-coding vanilla firepit domain. [F]

### C — `vanilla/wider-world::make-poultice`
- Source: `content/vanilla/assets/questline/questline/chapters/wider-world.json`
- Current prose: Four horsetail and two cattail or papyrus tops make a poultice. Hold it and right-click to heal your wounds.
- Current tasks: `[{"type": "obtain", "item": "game:poultice-*"}]`
- Recommendation: Keep game:poultice-* target and reed-based recipe; AoG cattail storage patch has a suspicious filename but no demonstrated poultice replacement or reed-drying requirement. Inspect resolved cattail item rather than rewriting healing input to straw. [R]

### D — `vanilla/winter::stock-firewood`
- Source: `content/vanilla/assets/questline/questline/chapters/winter.json`
- Current prose: Winter is long and cold. Keep plenty of firewood where you can reach it, under a roof.
- Current tasks: `[{"type": "obtain", "item": "game:firewood", "count": 64}]`
- Recommendation: Keep firewood goal, but reassess game:drygrass x16 reward: this is perishable hay, not evergreen tinder. Replace with game:thatch if straw emergency fire/kiln material is intended; otherwise explicitly identify hay and teach storage. [G] Reward is now perishable hay/feed; keep deliberately, or use game:thatch if straw tinder/building material was intended. [G]

### D — `vanilla/winter::stock-grain`
- Source: `content/vanilla/assets/questline/questline/chapters/winter.json`
- Current prose: Nothing grows in winter. Keep grain in storage vessels, for bread and porridge and to fill the troughs.
- Current tasks: `[{"type": "obtain", "item": "game:grain-*", "count": 64}]`
- Recommendation: Keep processed game:grain-* x64 for bread/porridge; distinguish it from plantable seed bags and crop bundles. Trough feeding has additional seed/hay alternatives, so do not tell players to hull all their breeding/planting stock. Add stored hay/straw preparation before winter; field hay drying stops below 8 C and resets below -1 C. [G,H,A]

### C — `vanilla/winter::cellar-food`
- Source: `content/vanilla/assets/questline/questline/chapters/winter.json`
- Current prose: Store vegetables in your cellar. Raw vegetables keep best in a storage vessel there.
- Current tasks: `[{"type": "obtain", "item": "game:vegetable-*", "count": 16, "name": "questline:name-any-vegetable"}]`
- Recommendation: Keep game:vegetable-* in this cache: ordinary crop outputs remain game namespace. AoG brewing-sized/sized crop items would need additional matchers only with breeding addon; do not install hypothetical namespace migrations. [V]

### D — `vanilla/winter::winter-larder`
- Source: `content/vanilla/assets/questline/questline/chapters/winter.json`
- Current prose: Before the snow comes, gather cured meat and pickles that will last until spring.
- Current tasks: `[{"type": "obtain", "item": "game:*-cured", "count": 8, "name": "questline:name-any-cured-meat"}, {"type": "obtain", "item": "game:pickledvegetable-*", "count": 8, "name": "questline:name-any-pickled-vegetable"}]`
- Recommendation: Keep meat/pickles tasks; add separate reserve for livestock hay/seed feed and durable straw/tinder. Current completion checks do not demonstrate animal winter readiness. Do not count perishable drygrass inventory alone as a safe winter reserve. [G,A]

## Exhaustive chapter inventory: all records, including unaffected justifications

Rows are partitioned by authored module/chapter, not by a guessed active loadout. U means no local rewrite required by AoG; it does not deny upstream progression impact. `Upstream` lists transitive directly changed quest IDs through authored requires (union of same-ID optional variants); it is a conservative dependency view, not an active-provider runtime graph.

### `betterruins/ruins` — 22 records
Source: `content/betterruins/assets/questline/questline/chapters/betterruins-ruins.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `explore-ruin` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `explore-megastructure` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `find-waystone` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `find-blueprint` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: betterruins:br-schematic-*. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `find-hidden-passage` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `find-hidden-tomb` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `buy-hideout-map` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: betterruins:locatormap-undergroundruins. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `find-hideout` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `visit-forlorn-tower` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-forlorn-bastion` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-university` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-crossroads` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-mansion` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-panopticon` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-dome-mall` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-coal-mine` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-abandoned-mine` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-huaca` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-sunrift` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-calix` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-halite-quarry` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |
| `visit-forgotten-village` | U | Exploration/location/trade contract; no AoG crop, fiber, feed, tinder or block-namespace replacement in this local goal. Target: visit. | — |

### `bricklayers/bricklayers-building` — 7 records
Source: `content/bricklayers/assets/questline/questline/chapters/bricklayers-building.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `cut-small-bricks` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:smallstonebrick-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `lay-small-bricks` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:smallstonebricks-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-tile-cement` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:cement-tile. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `lay-clay-tiles` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:claytiles-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `lay-stone-tiles` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:stonetiles-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-polishing-set` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:polishingset-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `polish-tiles` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:stonerawtileshiny-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `bricklayers/bricklayers-clay-and-fire` — 4 records
Source: `content/bricklayers/assets/questline/questline/chapters/bricklayers-clay-and-fire.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-mudbricks` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `lay-mudbricks` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:mudbricks-*. | `cut-grass`, `fire-pottery`, `make-firestarter`, `make-mudbricks` |
| `form-clay-tiles` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:clayrawtile-raw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `fire-clay-tiles` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:clayrawtile-burnt-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `bricklayers/bricklayers-glass-and-kilns` — 13 records
Source: `content/bricklayers/assets/questline/questline/chapters/bricklayers-glass-and-kilns.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `grind-quartz-powder` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: em:powdered-ore-quartz. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-frit` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:frit-mix-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `bake-frit` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:frit-baked-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `grind-frit` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:frit-ground-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-colored-glass` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glassbatch-plain-*, game:@glass-(green|blue|violet|red|yellow|brown|pink). | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-glazing-base` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glazingbase-clear. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-glazing` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glazing-clear-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `glaze-bowl` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glazedbowl-burnt-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `glaze-bricks` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glazedbricks-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `glaze-planter` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:glazedplanter-burnt-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `gather-porcelain-powders` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: em:powdered-ore-boneash, em:powdered-stone-granite, bricklayers:powdered-ceramic-light. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-porcelain` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: game:clay-white. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `fire-porcelain` | U | Bricklayers stone/ceramic/glaze process unchanged locally; if firing is involved use revised kiln/firepit setup. AoG does not replace this output. Target: bricklayers:porcelainbowl-burnt-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `charcoalkiln/charcoalkiln-copper-age` — 6 records
Source: `content/charcoalkiln/assets/questline/questline/chapters/charcoalkiln-copper-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `smith-draft-shutter` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: charcoalkiln:draftshutter-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-kiln-parts` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: charcoalkiln:kilndoor-*, charcoalkiln:chimney-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-charcoal-kiln` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: charcoalkiln:kilndoor-*, charcoalkiln:chimney-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `fire-charcoal-kiln` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `upgrade-charcoal-kiln` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: charcoalkiln:kilnliningkit-*, charcoalkiln:heatingkit-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-industrial-kiln` | U | Dedicated Charcoal Kiln process; AoG ground-firepit construction does not replace this kiln/door/torch goal. Target: charcoalkiln:retortdoor-*, charcoalkiln:retorthearth-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `efchefstricks/efchefstricks-baking` — 1 records
Source: `content/efchefstricks/assets/questline/questline/chapters/efchefstricks-baking.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-crumb-feed` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `efchefstricks/efchefstricks-farming` — 1 records
Source: `content/efchefstricks/assets/questline/questline/chapters/efchefstricks-farming.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `wash-eggshells` | U | Chef Tricks salt/eggshell process unchanged locally; no AoG direct recipe/item replacement identified. Target: efchefstricks:washedeggshell. | `cut-grass`, `fire-pottery`, `make-firestarter`, `make-henbox` |

### `efchefstricks/efchefstricks-preservation` — 2 records
Source: `content/efchefstricks/assets/questline/questline/chapters/efchefstricks-preservation.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `crystallize-salt` | U | Chef Tricks salt/eggshell process unchanged locally; no AoG direct recipe/item replacement identified. Target: efchefstricks:saltcrystal-damp. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `dry-salt-crystal` | U | Chef Tricks salt/eggshell process unchanged locally; no AoG direct recipe/item replacement identified. Target: efchefstricks:saltcrystal-dry. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `efmealsmodule/efmealsmodule-kitchen` — 1 records
Source: `content/efmealsmodule/assets/questline/questline/chapters/efmealsmodule-kitchen.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `mix-salad` | U | Meal-module mixing process unchanged; normal vegetables remain available without the breeding addon. Target: checkbox. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |

### `expandedfoods/expandedfoods-baking` — 2 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-baking.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `roast-grain` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-breadcrumbs` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:breadcrumbs-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `expandedfoods/expandedfoods-brewing` — 7 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-brewing.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `boil-syrup` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:fruitsyrupportion-*. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `form-bottle` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:bottle-clay-*-raw, aculinaryartillery:bottle-clay-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-bottle-rack` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:bottlerack-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-vinegar` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: game:vinegarportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `age-wine` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:strongwineportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `fine-wine` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:potentwineportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `age-spirit` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:strongspiritportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `expandedfoods/expandedfoods-cheesemaking` — 2 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-cheesemaking.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `pasteurize-milk` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:pasteurizedmilkportion. | `breed-animals`, `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter`, `make-large-trough` |
| `make-yogurt-starter` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:yogurt-starter. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |

### `expandedfoods/expandedfoods-farming` — 7 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-farming.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `press-oil` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `grow-soybeans` | D | See detailed recommendation above; correct local AoG route. | `gather-seeds` |
| `soak-soybeans` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-soybeans`, `make-firestarter` |
| `grind-soybeans` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:soyprep-powdered. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-soybeans`, `harvest-grain`, `make-firestarter` |
| `culture-soybeans` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-soybeans`, `harvest-grain`, `make-firestarter` |
| `brew-soy-sauce` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-soybeans`, `harvest-grain`, `make-firestarter` |
| `make-soy-milk` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:soymilk-edible. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-soybeans`, `harvest-grain`, `make-fire`, `make-firestarter` |

### `expandedfoods/expandedfoods-kitchen` — 11 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-kitchen.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `roast-meat` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `crack-egg` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:eggshell. | `cut-grass`, `fire-pottery`, `make-firestarter`, `make-henbox` |
| `tap-tree` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:spile-*, expandedfoods:*sapportion. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-mixing-bowl` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:mixingbowl-*. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `cut-nuggets` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:meatnugget-*-raw. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `render-lard` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:lard. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `boil-tree-syrup` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:treesyrupportion-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `knead-pasta` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:pasta-cut. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter`, `make-henbox` |
| `knead-sausage` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:sausage-*-raw. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `cast-cauldron` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:cauldronminimold-*-raw, aculinaryartillery:cauldronmini-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `power-mixing-bowl` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter`, `make-henbox` |

### `expandedfoods/expandedfoods-preservation` — 6 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-preservation.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-hardtack` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:hardtack-*-raw, expandedfoods:hardtack-*-bake1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-meat-rack` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: aculinaryartillery:meathooks-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `dry-age-meat` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:agedmeat-*-normal. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `water-glass-eggs` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:limeegg-chicken. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-henbox` |
| `ferment-fish` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:fermentedfish-slop. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `press-fish-sauce` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: expandedfoods:fishsauce. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `expandedfoods/expandedfoods-stone-age` — 1 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-stone-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `cook-roots` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `make-fire`, `make-firestarter` |

### `expandedfoods/expandedfoods-waterways` — 1 records
Source: `content/expandedfoods/assets/questline/questline/chapters/expandedfoods-waterways.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `cook-fish` | U | Expanded Foods food/container process unchanged locally; crop shelling/hulling and firepit setup are upstream, not a replacement to this outcome. Target: game:fish-cooked. | — |

### `fromgoldencombs/fromgoldencombs-beekeeping` — 14 records
Source: `content/fromgoldencombs/assets/questline/questline/chapters/fromgoldencombs-beekeeping.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `expand-apiary` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: game:skep-*. | — |
| `form-clay-hive` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:ceramicbroodpot-*-raw, fromgoldencombs:hivetop-*-raw. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `fire-clay-hive` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:ceramicbroodpot-*-notop, fromgoldencombs:hivetop-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `set-clay-hive` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:ceramicbroodpot-*-notop. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `harvest-clay-hive` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:hivetop-*-harvestable. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `wax-boards` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:langstrothside-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-frame-rack` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:framerack-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-hive-supers` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:langstrothsuper-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-hive-base` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:langstrothbase-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-brood-box` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:langstrothbroodtop-*, fromgoldencombs:langstrothbrood-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `wax-linen` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: game:linen-waxed-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `cut-liners` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:frameliner. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `make-bee-frames` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: fromgoldencombs:beeframe-*-empty. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `assemble-langstroth` | U | Hive/frame/wax process unchanged; pit-kiln material and fresh-reed/linen production are upstream, not a new hive outcome. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `hexsmech/industry` — 34 records
Source: `content/hexsmech/assets/questline/questline/chapters/hexsmech-industry.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-iron-pipes` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:pipe-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `craft-hearth` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:reverberatoryhearth-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `form-casting-bed` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:cast-bulkingot-*-raw. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-bellows-input` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:bellowsinput-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-casting-chamber` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:castingbed-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-reverb` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:reverberatoryhearth-*, hexsmech:bellowsinput-*, hexsmech:coveredpipe-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `power-bellows` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:linkage-heavy-*, game:bellows-large-*, game:axlearm-wood-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `hull-castiron` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:ingot-castiron, hexsmech:castironwall. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-fettling` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:fettling-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-rabble` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:rabble-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-finery` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:finerybasin-*, hexsmech:feedstockinput-*, hexsmech:foundrydoor-*, hexsmech:fireboxdoor-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `puddle-iron` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:ironbloom-wrought. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-vat` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:vataccess-*, hexsmech:castiron-firebox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `brew-sulfuric-acid` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:acid-full-sulfuric. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-retort` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:retortaccess-*, hexsmech:retortbuffer-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `reduce-aluminium` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:ingot-aluminium. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-boiler` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:pump-iron, hexsmech:boileraccess-*, hexsmech:fluidtank. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-engine` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:engineaccess-*, hexsmech:castironflywheel-*, hexsmech:castironcylinder-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-seep-pick` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:seeppick-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-pumpjack` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:pumpjackaccess-*, hexsmech:pumpjackwellhead. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-slitting-mill` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:slittingmill-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-distillation` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:distillationtoweraccess-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-cracker` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:crackeraccess-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-combustion` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:castironcombustionchamber-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-reaction-chamber` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:reactionchamberaccess-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `draw-wire` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:drawplate-*, hexsmech:spooler-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-dynamo` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:dynamo-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `string-power-line` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:connector-lv-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-battery-box` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:batterybox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `run-heat-box` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:heatbox-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-extruder` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:extruder-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-arc-furnace` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:arcfurnaceaccess-*, hexsmech:electrodereceptacle, hexsmech:steelwall. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-titanium` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:ingot-titanium. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `pour-stainless` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: game:ingot-stainlesssteel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `hexsmech/hexsmech-mechanical-power` — 4 records
Source: `content/hexsmech/assets/questline/questline/chapters/hexsmech-mechanical-power.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `crank-by-hand` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:handcrank-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-castiron-axles` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:castironaxle-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-dog-clutch` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: hexsmech:castirondogclutch-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `run-belt-drive` | U | Mechworks machine/industrial process; no AoG replacement to this goal. Earlier charcoal, clay or textile supply is an upstream dependency, not a new machine recipe. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `seafarer/provisions` — 25 records
Source: `content/seafarer/assets/questline/questline/chapters/seafarer-provisions.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-saltpan` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:saltpan-raw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `harvest-sea-salt` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:saltpan-*-empty, game:salt. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-preptable` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:preptable-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `salt-meat` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:saltedmeat-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `dry-salted-meat` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:driedsaltedmeat-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `slack-meat` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:slackedmeat-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-dryingframe` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:dryingframe-*. | — |
| `grow-sugarcane` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:sugarcane. | `gather-seeds`, `harvest-grain` |
| `press-cane` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:canejuiceportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `boil-molasses` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:molassesportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-sugar` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:sugar. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `candy-fruit` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:candiedfruit-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `distill-rum` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:spiritportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `form-griddle` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:claygriddle-raw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-griddle` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:claygriddle-clay, seafarer:griddlehearthbase-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `sear-meat` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:searedmeat-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `grow-corn` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:corn. | `gather-seeds`, `harvest-grain` |
| `dry-corn` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:driedcorn. | `gather-seeds`, `harvest-grain` |
| `make-mudrake` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:mudrake-wooden. | — |
| `burn-shells` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: game:lime. | — |
| `shuck-clams` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:premiumfish-raw. | — |
| `nixtamalize-corn` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:nixtamal. | `gather-seeds`, `harvest-grain` |
| `grind-masa` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:masa. | `gather-seeds`, `harvest-grain` |
| `make-tortilla` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:tortilla-corn. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `roll-burrito` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:burrito-cooked. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `seafarer/seafarer-waterways` — 9 records
Source: `content/seafarer/assets/questline/questline/chapters/seafarer-waterways.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-logbarge` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:boat-logbarge-*. | — |
| `ride-logbarge` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:boat-logbarge-*. | — |
| `make-raftsail` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:raftsail. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `season-planks` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: game:plank-seasoned. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cook-varnish` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:varnishportion-marine. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `varnish-planks` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: game:plank-varnished. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `oil-canvas` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:oiled-canvas. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `sew-sail` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:oiled-canvas-sail. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `build-outrigger` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:boat-outrigger-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `seafarer/seafarer-wider-world` — 1 records
Source: `content/seafarer/assets/questline/questline/chapters/seafarer-wider-world.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `visit-port` | U | Seafarer-specific crop/ship/salt/griddle process; no Seafarer mod in cache and no AoG Seafarer patch found. Retain optional content; runtime coexistence remains unverified. Target: seafarer:*. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |

### `tailorsdelight/tailorsdelight-arms-and-armor` — 4 records
Source: `content/tailorsdelight/assets/questline/questline/chapters/tailorsdelight-arms-and-armor.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-longbow` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:bow-long. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-jerkin` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:armor-body-jerkin-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-leather-armor` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:armor-body-sewn-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-gambeson` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:armor-body-sewn-linen. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `tailorsdelight/tailorsdelight-leatherwork` — 6 records
Source: `content/tailorsdelight/assets/questline/questline/chapters/tailorsdelight-leatherwork.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-buttons` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:buttons-*. | — |
| `leather-strips` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:leatherstrips-plain. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-backpack` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:backpack-normal. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `dark-leather` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:leather-darkbrown. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-awl` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:awlthorn-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-buttons` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:mold-raw-buttons, tailorsdelight:buttons-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `tailorsdelight/tailorsdelight-mechanical-power` — 1 records
Source: `content/tailorsdelight/assets/questline/questline/chapters/tailorsdelight-mechanical-power.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-sails` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:sail. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `tailorsdelight/tailorsdelight-riding` — 4 records
Source: `content/tailorsdelight/assets/questline/questline/chapters/tailorsdelight-riding.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-saddle` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:hoovedwearables-middleback-saddle1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-bridle` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:hoovedwearables-head-bridle*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-saddlebags` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:hoovedwearables-lowerbackside-saddlebags1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-pillion` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:hoovedwearables-lowerbackside-pillion-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `tailorsdelight/tailorsdelight-textiles` — 6 records
Source: `content/tailorsdelight/assets/questline/questline/chapters/tailorsdelight-textiles.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `knap-awl` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:awl-*. | — |
| `make-needle` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:needle-*. | — |
| `make-sewing-kit` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:sewingkit. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-sack` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: game:linensack. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `dye-thread` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:twine-blue. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `checkered-cloth` | U | Tailor recipe/output remains the same; AoG changes how base flax fiber is produced, not this downstream sewing/armor/sail outcome. Target: tailorsdelight:checkeredcloth-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/arms-and-armor` — 20 records
Source: `content/vanilla/assets/questline/questline/chapters/arms-and-armor.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `smith-falx` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:blade-falx-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `knap-arrowheads` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:arrowhead-*. | — |
| `make-bow` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:bow-*. | — |
| `make-arrows` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:arrow-*. | — |
| `make-bowstave` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:bowstave-*-raw. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-longbow` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:bow-long. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-sling` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:sling. | — |
| `make-crude-shield` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `make-round-shield` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:shield-woodmetal. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-improvised-armor` | D | See detailed recommendation above; correct local AoG route. | — |
| `make-wood-lamellar` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-lamellar-wood. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-improvised-armor` |
| `make-copper-lamellar` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-lamellar-copper. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-improvised-armor` |
| `make-jerkin` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-jerkin-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-leather-armor` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-sewn-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-brigandine` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-brigandine-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-chain-armor` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-chain-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-scale-armor` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-scale-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-plate-armor` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-plate-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-steel-plate` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-plate-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-gambeson` | U | Weapon/armor outcome unchanged; flax twine supply changes are upstream rather than a new weapon recipe. Target: game:armor-body-sewn-linen. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `vanilla/baking` — 5 records
Source: `content/vanilla/assets/questline/questline/chapters/baking.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `grind-flour` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-dough` | U | Dough/oven/bread/pie contract unchanged; seed hulling to culinary grain is upstream. Target: game:dough-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `bake-bread` | U | Dough/oven/bread/pie contract unchanged; seed hulling to culinary grain is upstream. Target: game:bread-*-perfect. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `bake-pie` | U | Dough/oven/bread/pie contract unchanged; seed hulling to culinary grain is upstream. Target: game:pie-perfect. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `eat-well` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-fire`, `make-firestarter` |

### `vanilla/beekeeping` — 9 records
Source: `content/vanilla/assets/questline/questline/chapters/beekeeping.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `raid-wild-hive` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `make-skep` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `plant-flowers` | U | Honey/wax/hive behavior unchanged; reed storage-patch targeting and flax fiber processing are separate upstream issues. Target: game:flower-*. | — |
| `populate-skep` | U | Honey/wax/hive behavior unchanged; reed storage-patch targeting and flax fiber processing are separate upstream issues. Target: game:skep-*-populated-*. | — |
| `harvest-honey` | U | Honey/wax/hive behavior unchanged; reed storage-patch targeting and flax fiber processing are separate upstream issues. Target: game:honeycomb. | — |
| `expand-apiary` | U | Honey/wax/hive behavior unchanged; reed storage-patch targeting and flax fiber processing are separate upstream issues. Target: game:skep-*. | — |
| `squeeze-honey` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `collect-beeswax` | U | Honey/wax/hive behavior unchanged; reed storage-patch targeting and flax fiber processing are separate upstream issues. Target: game:beeswax. | — |
| `make-candle` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |

### `vanilla/brewing` — 14 records
Source: `content/vanilla/assets/questline/questline/chapters/brewing.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-metal-rod` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:rod-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `gather-resin` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:resin. | — |
| `make-fruit-press` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:fruitpress-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `press-juice` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:juiceportion-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `ferment-drink` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:ciderportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `find-lead` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:nugget-galena. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-soldering-iron` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:solderingiron. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-copper-plates` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:metalplate-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `alloy-solder` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:ingot-leadsolder. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cut-solder` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:solderbar-tin. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-boiler` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:verticalboiler-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-condenser` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:condenser-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `distill-spirit` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:spiritportion-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `aqua-vitae` | U | Press/barrel/distillation contract unchanged; culinary grain sourcing and heat supply are upstream. Target: game:alcoholportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `vanilla/bronze-age` — 13 records
Source: `content/vanilla/assets/questline/questline/chapters/bronze-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-prospecting-pick` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:prospectingpick-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-tin` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:nugget-cassiterite. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `alloy-bronze` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-tinbronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `bronze-anvil` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:anvil-*bronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `bronze-pickaxe` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:pickaxe-*bronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `smith-bronze` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:*-tinbronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `bronze-axe` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:axe-felling-*bronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-bismuth` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:nugget-bismuthinite. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-zinc` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:nugget-sphalerite. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `alloy-bismuth-bronze` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-bismuthbronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-gold` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:nugget-nativegold. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-silver` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:nugget-nativesilver. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `alloy-black-bronze` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-blackbronze. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/building` — 18 records
Source: `content/vanilla/assets/questline/questline/chapters/building.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-boards` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:plank-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-door` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:door-solid-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-ladder` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:ladder-wood-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-fence` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:woodenfence-*, game:woodenfencegate-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-roof` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-nails` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:metalnailsandstrips-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-chest` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:chest-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-oil-lamp` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:oillamp-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-chisel` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:chisel-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cut-stone-bricks` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:stonebrick-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `grind-lime` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:lime. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `burn-quicklime` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:quicklime. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `slake-lime` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:slakedlimeportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-plaster` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:plaster-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `mix-mortar` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:mortar. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `lay-stone-bricks` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:stonebricks-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-barrel` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:barrel. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-table` | U | Stone/wood/mortar building contract unchanged; AoG straw/roofing changes tracked separately. Target: game:table-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/cheesemaking` — 7 records
Source: `content/vanilla/assets/questline/questline/chapters/cheesemaking.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `collect-milk` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:milkportion. | `breed-animals`, `cut-grass`, `fire-pottery`, `make-firestarter`, `make-large-trough` |
| `curdle-milk` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:curdledmilkportion. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `make-cottage-cheese` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:cottagecheeseportion. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `press-cheese` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: checkbox. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `wax-cheese` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:cheese-waxedcheddar-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `age-cheddar` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:cheese-cheddar-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `age-blue-cheese` | U | Milk/rennet/cheese contract unchanged; linen remains the same item after AoG flax processing. Target: game:cheese-blue-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter`, `make-large-trough` |

### `vanilla/clay-and-fire` — 16 records
Source: `content/vanilla/assets/questline/questline/chapters/clay-and-fire.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `find-clay` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:clay-*. | — |
| `find-fireclay` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:clay-fire. | — |
| `form-bowl` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `form-pot` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:claypot-*-raw. | — |
| `form-vessel` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:storagevessel-*-raw. | — |
| `form-oven` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:clayoven-north. | — |
| `fire-pottery` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `make-firestarter` |
| `fire-pot` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:claypot-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `place-oven` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:clayoven-*. | — |
| `make-bricks` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-jug` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:jug-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-watering-can` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:wateringcan-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cook-meal` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-planter` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:clayplanter-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `place-vessel` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:storagevessel-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-shingles` | U | Clayforming/container/oven contract unchanged; revised pit-kiln input layer is upstream. Target: game:shingle-burned-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/copper-age` — 20 records
Source: `content/vanilla/assets/questline/questline/chapters/copper-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-pan` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:pan-wooden. | — |
| `make-charcoal` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `find-copper` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:nugget-nativecopper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `form-crucible` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:crucible-*-raw. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `form-mold` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:toolmold-*-raw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-tongs` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:tongs. | — |
| `fire-metalwork` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:crucible-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-tool` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:*head-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `form-ingot-mold` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:ingotmold-*-raw. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-pickaxe` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:pickaxe-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-axe` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:axe-felling-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-hammer` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:hammer-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-ingot` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:ingot-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-forge` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:forge. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-anvil` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:anvil-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `first-smithing` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:*-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-saw` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:saw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `smith-knife` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:knife-generic-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-scythe` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-shovel` | U | Metalworking output unchanged; firepit namespace and kiln loading are upstream prerequisites. Target: game:shovel-copper. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/farming` — 11 records
Source: `content/vanilla/assets/questline/questline/chapters/farming.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `knap-hoe` | U | Soil/hoe/fertility contract unchanged; AoG harvest-stage/process changes are handled in the harvest quests. Target: game:hoehead-*. | — |
| `gather-seeds` | D | See detailed recommendation above; correct local AoG route. | — |
| `make-compost` | U | Soil/hoe/fertility contract unchanged; AoG harvest-stage/process changes are handled in the harvest quests. Target: game:compost. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-hoe` | U | Soil/hoe/fertility contract unchanged; AoG harvest-stage/process changes are handled in the harvest quests. Target: game:hoe-*. | — |
| `harvest-grain` | D | See detailed recommendation above; correct local AoG route. | `gather-seeds` |
| `grow-vegetables` | D | See detailed recommendation above; correct local AoG route. | `gather-seeds`, `harvest-grain` |
| `make-quern` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `grow-pumpkin` | D | See detailed recommendation above; correct local AoG route. | `gather-seeds`, `harvest-grain` |
| `grind-bonemeal` | U | Soil/hoe/fertility contract unchanged; AoG harvest-stage/process changes are handled in the harvest quests. Target: game:bonemeal. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `gather-saltpeter` | U | Soil/hoe/fertility contract unchanged; AoG harvest-stage/process changes are handled in the harvest quests. Target: game:saltpeter. | `gather-seeds`, `harvest-grain` |
| `full-harvest` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `grow-pumpkin`, `grow-vegetables`, `harvest-grain`, `make-firestarter` |

### `vanilla/glass-and-kilns` — 15 records
Source: `content/vanilla/assets/questline/questline/chapters/glass-and-kilns.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `find-quartz` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:ore-quartz. | — |
| `mold-refractory` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:refractorybrick-raw-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `lay-fireclay-bricks` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:claybricks-good-fire. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-hatch` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:cokeovendoor-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-lantern` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:lantern-*. | — |
| `make-glass` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:glass-*. | — |
| `fire-refractory` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:refractorybrick-fired-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-coke-oven` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:cokeovendoor-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-panes` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:glasspane-leaded-*. | — |
| `lay-refractory` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:refractorybricks-good-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-gratings` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:refractorybrickgrating-good-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-coke` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:coke. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-kiln-door` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:doorkiln-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-kiln` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: game:doorkiln-*, game:refractorybrickgrating-good-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `fire-kiln` | U | High-temperature material/kiln contract unchanged; pit-kiln straw alternative does not replace this output. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `vanilla/husbandry` — 12 records
Source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `build-pen` | U | Animal capture/breeding/milk output unchanged locally; AoG feed supply changes are upstream. Target: game:*fence-*. | — |
| `make-trough` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-bucket` | U | Animal capture/breeding/milk output unchanged locally; AoG feed supply changes are upstream. Target: game:woodbucket. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-large-trough` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `breed-animals` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter`, `make-large-trough` |
| `milk-animal` | U | Animal capture/breeding/milk output unchanged locally; AoG feed supply changes are upstream. Target: game:milkportion. | `breed-animals`, `cut-grass`, `fire-pottery`, `make-firestarter`, `make-large-trough` |
| `make-henbox` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `collect-eggs` | U | Animal capture/breeding/milk output unchanged locally; AoG feed supply changes are upstream. Target: game:egg-chicken-raw. | `cut-grass`, `fire-pottery`, `make-firestarter`, `make-henbox` |
| `make-basket-trap` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `make-crate-trap` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `melt-fat` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-cleaver` | U | Animal capture/breeding/milk output unchanged locally; AoG feed supply changes are upstream. Target: game:cleaver-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/iron-age` — 17 records
Source: `content/vanilla/assets/questline/questline/chapters/iron-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `build-bellows` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:bellows-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `find-iron` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:nugget-limonite. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-borax` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:powder-borax. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `find-meteorite` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:stone-meteorite-iron. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `fire-fireclay-bricks` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:burnedbrick-fire. | — |
| `build-bloomery` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:bloomerybase-*. | — |
| `make-bloom` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:ironbloom. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `refine-bloom` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:ingot-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-iron` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:*-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-tongs` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:tongsmetal-standard-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `coat-head` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:*head-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-anvil-parts` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:anvilpart-base-iron, game:anvilpart-top-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-waterwheel` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:waterwheel-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-metal-windmill` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:windmillrotor-metal-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `quench-head` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `fuse-anvil` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: checkbox. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-meteoric` | U | Metalworking/refractory output unchanged; revised firing supply is upstream. Target: game:*-meteoriciron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `vanilla/kitchen` — 5 records
Source: `content/vanilla/assets/questline/questline/chapters/kitchen.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `roast-meat` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `serve-meal` | U | Cooking/utensil contract unchanged locally; use corrected AoG firepit and processed crops as applicable. Target: game:bowl-*-meal. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cook-stew` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-fire`, `make-firestarter` |
| `cook-soup` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cook-porridge` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/leatherwork` — 14 records
Source: `content/vanilla/assets/questline/questline/chapters/leatherwork.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `get-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-raw-*. | — |
| `make-limewater` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:limewaterportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `weak-tannin` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:weaktanninportion. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `salt-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-salted-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `soak-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-soaked-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `strong-tannin` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:strongtanninportion. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `scrape-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-scraped-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `prepare-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-prepared-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-leather` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:leather-normal-plain. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-backpack` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:backpack-normal. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `leather-boots` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:clothes-foot-*leather-boots. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `oil-hide` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-oiled-*. | — |
| `cure-pelt` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:hide-pelt-*. | — |
| `fur-hat` | U | Leather/pelt/tannin contract unchanged; linen/twine inputs remain the same processed items. Target: game:clothes-head-furhat*. | — |

### `vanilla/mechanical-power` — 18 records
Source: `content/vanilla/assets/questline/questline/chapters/mechanical-power.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `tap-resin` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:resin. | — |
| `make-sails` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:sail. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `smith-pulverizer-metal` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:poundercap-*, game:metalplate-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `form-helve-mold` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:toolmold-*-raw-helvehammer. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-rotor` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:windmillrotor-wood-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-axle` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:woodenaxle-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-gears` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:angledgears-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `cast-helve-head` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:helvehammerhead-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-windmill` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:windmillrotor-wood-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `connect-power` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:woodenaxle-*, game:angledgears-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-pulverizer-parts` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:pounder-*, game:pulverizertoggle-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-helve` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:helvehammer-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-grinding-wheel` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:grindingwheel-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `power-quern` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:quern-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `build-large-gear` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:largegear3. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-pulverizer` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:pulverizerframe-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-helve-hammer` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:helvehammerbase-*, game:woodentoggle-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `crush-quartz` | U | Mechanical part/action unchanged; linen-production cost changes upstream, not the target item. Target: game:crushed-quartz. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/orchards` — 8 records
Source: `content/vanilla/assets/questline/questline/chapters/orchards.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `take-bush-cutting` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:fruitingbushcutting-*. | — |
| `take-tree-cutting` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:fruittree-cutting. | — |
| `make-flowerpot` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:flowerpot-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-greenhouse` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:glass-*. | — |
| `plant-bush-cutting` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:fruitingbushcutting-*. | — |
| `plant-tree-cutting` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:fruittree-cutting. | — |
| `graft-cutting` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: game:fruittree-cutting. | — |
| `greenhouse-bonus` | U | Tree/berry/greenhouse contract unchanged; AoG crop harvest does not replace orchard outputs. Target: checkbox. | — |

### `vanilla/preservation` — 10 records
Source: `content/vanilla/assets/questline/questline/chapters/preservation.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `find-salt` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:salt. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `cure-meat` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:*-cured. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-brine` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:brineportion. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `pickle-vegetables` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `form-crock` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:crock-*-raw. | — |
| `fire-crock` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:crock-*-fired. | — |
| `seal-crock` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: checkbox. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-shelf` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:shelf-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `build-cellar` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: checkbox. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `stock-cellar` | U | Salt/barrel/crock/cellar contract unchanged; ordinary game vegetables and pickles remain valid in cache. Target: game:crock-*-fired. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/riding` — 9 records
Source: `content/vanilla/assets/questline/questline/chapters/riding.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `smith-nails` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:metalnailsandstrips-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `trap-elk-calf` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: checkbox. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-saddle` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:hoovedwearables-middleback-saddle1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-bridle` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:hoovedwearables-head-bridle*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `break-in-elk` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:semitameddeer-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `ride-elk` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:tameddeer-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-saddlebags` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:hoovedwearables-lowerbackside-saddlebags1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-bone-flute` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:instrument-flute1. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-pillion` | U | Mount/tack contract unchanged; feed supply and flax supply are upstream. Target: game:hoovedwearables-lowerbackside-pillion-leather. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `vanilla/steel-age` — 11 records
Source: `content/vanilla/assets/questline/questline/chapters/steel-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `lay-furnace-floor` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:refractorybrickgrating-good-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `build-furnace` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:stonecoffinsection-*. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-iron-door` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:metaldoor-s*-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `stock-iron` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `wall-furnace` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:refractorybricks-good-*, game:metaldoor-s*-iron. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `blister-steel` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-blistersteel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `forge-steel` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:ingot-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `smith-steel` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:*-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-steel-tools` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:pickaxe-steel, game:axe-felling-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `coat-steel-head` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:*head-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `make-steel-anvil` | U | Local target is outside AoG replacement surface; no changed item/filter/recipe identified in the inspected AoG archive. Target: game:anvilpart-base-steel, game:anvilpart-top-steel. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |

### `vanilla/stone-age` — 24 records
Source: `content/vanilla/assets/questline/questline/chapters/stone-age.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `gather-flint` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:flint. | — |
| `gather-sticks` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:stick. | — |
| `forage` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:fruit-*. | — |
| `knap-axe-head` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:axehead-*. | — |
| `knap-knife` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:knifeblade-*. | — |
| `knap-spear` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:spearhead-*. | — |
| `make-firestarter` | D | See detailed recommendation above; correct local AoG route. | `cut-grass` |
| `make-axe` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:axe-*. | — |
| `make-knife` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:knife-generic-*. | — |
| `make-spear` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:spear-generic-*. | — |
| `knap-shovel` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `chop-wood` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:firewood. | — |
| `make-club` | U | Tool/forage/storage contract is not directly replaced by AoG; altered grass/reed/fire steps are tracked separately. Target: game:club-generic-wood. | — |
| `cut-grass` | D | See detailed recommendation above; correct local AoG route. | — |
| `gather-reeds` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `first-hunt` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `ground-storage` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `make-fire` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `make-firestarter` |
| `make-basket` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `hay-bed` | D | See detailed recommendation above; correct local AoG route. | `cut-grass` |
| `make-torch` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `make-fire`, `make-firestarter` |
| `cook-roots` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `make-fire`, `make-firestarter` |
| `build-shelter` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `hay-bed` |
| `make-rope` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |

### `vanilla/textiles` — 14 records
Source: `content/vanilla/assets/questline/questline/chapters/textiles.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `grow-flax` | D | See detailed recommendation above; correct local AoG route. | `gather-seeds`, `harvest-grain` |
| `spin-twine` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-linen` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:linen-*. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-sewing-kit` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:sewingkit. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-sack` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:linensack. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-cloth` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:cloth-plain. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `sew-shirt` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:clothes-upperbody-*. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `sew-pants` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:clothes-lowerbody-*. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `make-woad-dye` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:dye-woad. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `dye-woad` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:cloth-blue. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `crush-alum` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:crushed-alum. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `mordant-cloth` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:cloth-mordant. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |
| `make-yellow-dye` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:dye-yellow. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `dye-cloth` | U | Downstream twine/linen/cloth/dye contract unchanged after fully processed game:flaxfibers becomes available. Target: game:cloth-yellow. | `cut-grass`, `fire-pottery`, `gather-seeds`, `grow-flax`, `harvest-grain`, `make-firestarter` |

### `vanilla/waterways` — 15 records
Source: `content/vanilla/assets/questline/questline/chapters/waterways.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `make-wormgrunter` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:wormgrunter. | — |
| `make-fishing-pole` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:fishingpole-simple-*. | — |
| `bait-pole` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:fishingpole-simple-*. | — |
| `catch-fish` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:fishraw-*. | — |
| `fillet-fish` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:fish-raw. | — |
| `cook-fish` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:fish-cooked. | — |
| `make-oar` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:oar-crude-*. | — |
| `make-raft` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:boat-raft-*. | — |
| `ride-raft` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:boat-raft-*. | — |
| `make-rollers` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:roller. | — |
| `make-plumb-square` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:plumbandsquare. | — |
| `build-sailboat` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:boat-sailed-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-ratlines` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:ratlines. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-boat-seat` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:boatseat-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-anchor` | U | Fishing/boat outcome unchanged; cordage and cooking supply changes are upstream. Target: game:anchor-stone. | `cut-grass`, `fire-pottery`, `make-firestarter` |

### `vanilla/wider-world` — 11 records
Source: `content/vanilla/assets/questline/questline/chapters/wider-world.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `find-rusty-gears` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:gear-rusty. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `visit-trader` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: *:*. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `mine-stone` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:rock-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `find-limestone` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:stone-limestone. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `kill-drifter` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:drifter-*. | — |
| `find-temporal-gear` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:gear-temporal. | — |
| `survive-storm` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: checkbox. | — |
| `relight-fire` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `make-fire`, `make-firestarter`, `make-torch` |
| `make-poultice` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | — |
| `make-bandage` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:bandage-clean. | `gather-seeds`, `grow-flax`, `harvest-grain` |
| `soak-bandage` | U | Exploration/healing/weather target unchanged; upstream fire/textile supply changes are separately listed. Target: game:bandage-alcoholed. | `gather-seeds`, `grow-flax`, `harvest-grain` |

### `vanilla/winter` — 6 records
Source: `content/vanilla/assets/questline/questline/chapters/winter.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `stock-firewood` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `make-fire`, `make-firestarter` |
| `stock-grain` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter` |
| `cellar-food` | C | See detailed recommendation above; retain endpoint, clarify context/reward. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `make-pelt` | U | Clothing/temperature contract unchanged locally; AoG winter feed/drying concerns are separate. Target: game:hide-pelt-*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `dress-warm` | U | Clothing/temperature contract unchanged locally; AoG winter feed/drying concerns are separate. Target: game:clothes-*fur*. | `cut-grass`, `fire-pottery`, `make-firestarter` |
| `winter-larder` | D | See detailed recommendation above; correct local AoG route. | `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-fire`, `make-firestarter`, `stock-firewood`, `stock-grain` |

### `wool/wool-husbandry` — 2 records
Source: `content/wool/assets/questline/questline/chapters/wool-husbandry.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `shear-animal` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:fleece-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `make-firestarter`, `make-large-trough` |
| `make-shears` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: game:shears-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `make-firestarter`, `make-large-trough` |

### `wool/wool-textiles` — 5 records
Source: `content/wool/assets/questline/questline/chapters/wool-textiles.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `wash-fleece` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:fibers-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `spin-wool` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:twine-wool-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `weave-wool` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:cloth-wool-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `make-kneedles` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:kneedle-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |
| `dye-wool` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:cloth-wool-blue. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |

### `wool/wool-winter` — 1 records
Source: `content/wool/assets/questline/questline/chapters/wool-winter.json`

| Quest ID | Class | Local decision / unaffected justification | Upstream direct-change IDs |
|---|---|---|---|
| `knit-sweater` | U | Wool/shearing/knitting process, not AoG flax processing; husbandry nutrition is upstream. Target: wool:clothes-upperbodyover-sweater-*. | `breed-animals`, `cut-grass`, `fire-pottery`, `gather-seeds`, `harvest-grain`, `make-firestarter`, `make-large-trough` |

## Coverage totals by module

| Module | Authored records | D | C | U | In cached Mods? |
|---|---:|---:|---:|---:|---|
| betterruins | 22 | 0 | 0 | 22 | No (authored optional content still audited) |
| bricklayers | 24 | 1 | 0 | 23 | Yes / base game |
| charcoalkiln | 6 | 0 | 0 | 6 | No (authored optional content still audited) |
| efchefstricks | 4 | 0 | 1 | 3 | Yes / base game |
| efmealsmodule | 1 | 0 | 0 | 1 | Yes / base game |
| expandedfoods | 37 | 2 | 7 | 28 | Yes / base game |
| fromgoldencombs | 14 | 0 | 0 | 14 | Yes / base game |
| hexsmech | 38 | 0 | 0 | 38 | No (authored optional content still audited) |
| seafarer | 35 | 0 | 0 | 35 | No (authored optional content still audited) |
| tailorsdelight | 21 | 0 | 0 | 21 | Yes / base game |
| vanilla | 322 | 22 | 32 | 268 | Yes / base game |
| wool | 8 | 0 | 0 | 8 | Yes / base game |

## Replacement implementation and verification recommendations (NOT executed)

- Material caveat: straw and drygrass both use the same 4320 fresh + 448 transition Perish parameters in this cache. Recommendations to give straw instead of hay are about purpose/naming/recipe use, NOT evidence straw lasts longer. One stack of either is not a measured winter feeding budget; compute portions for actual livestock before claiming readiness.
1. Preserve the existing IDs; introduce AoG-aware quest replacements gated on **artofgrowingpatch** and keep AoG-absent vanilla chapter behavior. Respect competing ExpandedFoods, Bricklayers and TailorsDelight overrides. Do not use generic modid artofgrowing as the only gate for this specific unofficial cached pack.
2. Support normal AoG and vanilla firepit matchers; unit tests for exact domains and valid ignite states, native placement/ignite/cook/smelt tests. Do not solve mismatch by a broad unscoped `*:firepit-*` that completes too early.
3. Fresh profile/day-one journey: knife -> fresh grass/layer -> drygrass -> firestarter -> four firewood -> light -> roots/torch. Also test straw alternative and no-reward bootstrap, so reward drygrass does not conceal broken drying instructions.
4. Wet/cold conditions: rain resets, 8 C stop, -1 C reset, ground piles versus field layer and water; verify persistence through reload and passage of time. Confirm handbook timing mismatch before publishing a fixed hour promise.
5. Crop journeys with ManualHarvesting active: wild seeds, grain bundle extraction/hulling, soybean shelling/planting, vegetable food-stage versus terminal seed-stage, pumpkin harvest; record actual resolved item codes and quantities without treating randomized output as fixed.
6. Complete flax journey: wet flax grain bundle -> dry -> ground thresh -> dry flax stalks -> wet in water -> wash clear -> soft -> offhand ridge -> fibers -> twine -> linen; prove rough ridge can bootstrap from rope. Confirm timers with actual cache settings and no cheat-supplied fibers.
7. Animal winter feed matrix with BetterHusbandry/LivestockWelfare and Chef Tricks: normal trough large/small + correct species + fresh grass/hay/straw/seeds/culinary grain/breadcrumb feed (test agedgrass as an unproven case, not presumed supported); check portions and spoil/drying transitions. NaturalFertilizer and Wool drygrass recipes must not be accidentally broken.
8. Export final merged recipes/assets to settle coexistence/additive recipe and OneRoof issues. Test AoG absent, AoG present alone with required core, full cache, and optional override combinations. No native acceptance claims are made in this audit.
9. Only after evidence approval edit chapters, localization and tests in an implementation worktree; regenerate any derived mirrors, validate progress migration semantics, and update all shared-ID translations. This read-only audit made none of those changes.

## Audit artifacts and limitations

- Requested deliverable: `<research-scratch>/aog-impact-research.md` (this report).
- Supporting scratch artifacts: `aog-audit-source/inventory.json`, `classified-inventory.json`, `build_report.py`, cached DLL copies and decompiled directories; ilspycmd installed only into scratch `aog-audit-tools/`. No repository files were created or modified.
- Scope excludes live world state, active merged registry and native gameplay. Report distinguishes proven source changes, additive alternatives, stale config uncertainty, absent optional mods and recommended acceptance checks.
- Every authored quest record was parsed and enumerated; direct recommendation keys were asserted to exist; classifications are disjoint; totals computed from parsed data, not manual counting.
