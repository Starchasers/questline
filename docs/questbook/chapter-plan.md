# Pszczoly questbook: chapter plan

Proposed book structure and quest candidates for the Pszczoly 1.4.1 modpack. This is a planning document: no quest JSON exists for it yet. Companion documents: [mod-inventory.md](mod-inventory.md) and [progression.md](progression.md).

Decisions already taken: clean-slate chapter design, full progression coverage, content edited directly in this fork, English only.

## 1. How to read the tables

| Column | Meaning |
|---|---|
| **Quest** | Working title. **[G]** marks a chapter milestone (gear shape). |
| **Task** | Questline task type and target. `obtain` is the default "make it" task. `check` is a checkbox (honour system) where nothing can be detected. `+u` means `unchecked: true` (mod machine the recipe graph cannot see). |
| **After** | Prerequisite quests, by title. Prerequisites only suggest an order (locking is open). |
| **Path** | A bold prefix (`**Grains** ·`) puts the quest on a named path inside the chapter; paths run side by side. |
| **Optional** | `*(optional)*` marks a side branch that nothing depends on. |
| **Source** | `new`, or the upstream quest ID reused (`=`) or rewritten (`~`). `S#` refers to a stuck point in [progression.md](progression.md). |

Item codes are from mod files and still need validation with `/questline snapshot` and `tools/packcheck`.

## 2. Design constraints from the Questline format

- **Rewards.** Every item reward collapses to one quest cookie. Only **stage rewards** have an effect, so milestones should grant stages (`stone`, `clay`, `copper`, `bronze`, `iron`, `steel`) if anything is to be gated.
- **Locking** is open by default: prerequisites are a suggested order. Only mod, stage and `discovered` gates really lock.
- **Detection gaps** → checkbox or `obtain`: breeding, taming, trust, shearing, chiselling, prospecting, barrel sealing, kiln firing, what meal is in a pot, quenching, surviving a storm, reviving a player, movement skills, in-world multi-step builds.
- **Mod machines** (saucepan, mixing bowl, butcher table, sawhorses, cheese kettle) are invisible to the `craft` task: use `obtain`, with `+u` where the recipe graph complains.
- **Toolsmith** in-hand and workbench crafts only count as `craft` through `compat/toolsmith`; `obtain` on the finished tool is the safe default.
- **Liquids** count by the litre in carried containers, so broth, cream, syrup and dye quests can use `obtain`.
- **No attribute matching.** Meals in pots, custom banners and Toolsmith part quality cannot be told apart.
- **Pattern names.** Wildcard tasks whose matches share no word need an explicit `name` key.
- **Visit tasks** need a structure lang key and the worldgen code; surface only.
- **Multiplayer.** `mode: party` pools progress in a party; `mode: server` pools across everyone. Seven players share this server, so communal builds are good server quests.

## 3. Book structure

Thirty-one chapters in six groups. `Order` leaves gaps for later additions. Chapters marked **age** set `age: true` and label quests elsewhere with the age they depend on.

| Order | Chapter | Group | Entry tier | Main mods |
|---|---|---|---|---|
| 10 | First Days (age) | Ages | stone | Toolsmith, Immersive Woodworking, Manual Firestarter, Firestarters, Art of Growing, Real Smoke, Stick Roast |
| 20 | Clay & Fire (age) | Ages | clay | vanilla, Dana Tweaks, Culinary Artillery |
| 30 | Copper Age (age) | Ages | copper | Immersive Ore Crush, Toolsmith, Juicy Ores |
| 40 | Bronze Age (age) | Ages | bronze | ProspectTogether, Pewter |
| 50 | Iron Age (age) | Ages | iron | vanilla |
| 60 | Steel Age (age) | Ages | steel | vanilla |
| 110 | Toolsmithing | Workshop | stone | Toolsmith |
| 120 | Woodworking | Workshop | stone | Immersive Woodworking, Seasoned Firewood |
| 130 | Materials & Ceramics | Workshop | clay | Expanded Matter, Bricklayers |
| 140 | Rooms & Shelter | Workshop | stone | vanilla rooms, Real Smoke, OneRoof, Scaffolding, Bricklayers, Millwright |
| 150 | Mechanical Power | Workshop | bronze | vanilla, Millwright, Immersive Woodworking |
| 160 | Storage & Hauling | Workshop | stone | Purposeful Storage, Containers Bundle, Carry On, ToolBelt, Cartwrights Caravan |
| 210 | Fields & Harvest | Land | stone | Art of Growing, Natural Fertilizer |
| 220 | Orchards & Bees | Land | stone | From Golden Combs, Manual Harvesting |
| 230 | Livestock | Land | stone | Livestock Welfare, betterhusbandry, genelib, Catch Livestock, Wool |
| 240 | Horses & Riding | Land | copper | Equus, Jaunt |
| 250 | Butchery & Hunting | Land | stone | Butchering, Rustic Cookery, BloodTrail |
| 310 | Cooking | Kitchen | stone | Culinary Artillery, Expanded Foods, Meals, Rustic Cookery, Manual Dishes |
| 320 | Baking | Kitchen | clay | Manual Dough, Stone Bake Oven, Expanded Foods |
| 330 | Dairy | Kitchen | clay | DairyPlus |
| 340 | Preservation & Cellar | Kitchen | clay | Expanded Foods, Chef's Tricks, FoodShelves |
| 350 | Brewing & Drink | Kitchen | clay | Expanded Foods, Simple Tea, Tankards, SlowTox |
| 410 | Textiles & Tailoring | Craft | stone | Art of Growing, Tailor's Delight, Wool, Dressmakers |
| 420 | Leatherwork | Craft | copper | Immersive Woodworking, Tailor's Delight, Expanded Matter |
| 430 | Arms & Armor | Craft | stone | Combat Overhaul, Armory, Quivers and Sheaths |
| 510 | Survival & the Unknown | World | stone | Downed, Temporal Symphony, Mists of Stability, Firestarters |
| 520 | Overland Travel | World | stone | Walking Stick, movement mods, trails, Cartography Table, Spyglass |
| 530 | Waterways | World | stone | Rough Seas, Rivers, Watersheds |
| 540 | Traders | World | stone | vanilla traders, BetterTraders, Trader Phone |
| 545 | Player Economy | World | stone | Coins, Vinconomy, Hand to Hand, Notice Board, Tabletop Games |
| 550 | Home & Decor | World | stone | Heraldry, Window Display, Wind Chimes, Kevin's Furniture, Pewter, Chisel Tools, paths and slabs |

## 4. Chapters and quest candidates

### 4.1 Ages

#### First Days (order 10, age)

The pack's first days differ from vanilla at almost every step, so this chapter is the most important one. It covers S1–S3, S6–S10, S12, S13.

| Quest | Task | After | Source |
|---|---|---|---|
| Gather flint and sticks | obtain `game:flint` ×3, `game:stick` ×6 | – | = gather-flint, gather-sticks |
| Forage fruit or mushrooms | obtain `game:fruit-*` or `game:mushroom-*` ×8 | – | ~ forage; mushrooms added, needs a `name` key |
| Knap a knife blade and an axe head | knap | Gather flint | = knap-knife, knap-axe-head |
| Assemble your first tools in hand | obtain knife, axe | Knap | ~ make-knife, make-axe (S1) |
| Knap a whetstone and hone a tool *(optional)* | obtain `toolsmith:whetstone-*` | Assemble | new (S2); side branch, leads to Toolsmithing |
| Set up a chopping block | place `immersivewoodworking:choppingblock` | Assemble | new (S3) |
| Split firewood | obtain `game:firewood` ×8 | Chopping block | ~ chop-wood |
| Fell a tree safely | check | Assemble | new (S10) |
| Cut standing dry grass | obtain `game:drygrass` ×4 | Assemble | ~ cut-grass (S13); yellow grass (`artofgrowing:talldrygrass-*`) and snow-covered grass cut straight to dry grass |
| Mow green grass | obtain `artofgrowing:grass` ×8 | Assemble | new (S13); green grass gives fresh grass, not dry |
| Dry fresh grass | obtain `game:drygrass` ×10 | Mow green grass | new (S13); about a day in a pile or left where it was mown, or at once in a firepit slot |
| Make a firestarter | obtain `game:firestarter` | Gather sticks | ~ make-firestarter |
| Build the firepit | place `game:firepit-*` or `artofgrowing:firepit-construct1` | Split firewood, dry grass | new (S8); 1 dry grass or straw, then 4 firewood |
| Kindle and carry tinder | ignite firepit | Build the firepit, Firestarter | ~ make-fire (S6, S7) |
| Roast on a stick | obtain `stickroast:roastingstick` | Kindle | new |
| Make torches | obtain torch ×2 | Kindle | ~ make-torch; wind and backpack put them out |
| Knap a spear and a shovel | obtain | Knap | = make-spear, knap-shovel |
| Weave a reed basket | obtain `game:basket-normal-*` | Assemble | = make-basket; first bag, 3 slots |
| Sleep on a hay bed | obtain bed | Dry grass | = hay-bed |
| Pack dirt for walls | obtain `game:packeddirt` ×12 | Shovel | new (S12); loose soil falls, packed dirt, cob and mudbrick do not |
| Build a ventilated shelter **[G]** | place `game:packeddirt` ×20; check for chimney | Pack dirt, Kindle | ~ build-shelter (S9); reward stage `stone` |
| Dig a first cellar | check | Shelter | ~ build-cellar; moved to the first days, details in Rooms & Shelter |

#### Clay & Fire (order 20, age)

| Quest | Task | After | Source |
|---|---|---|---|
| Find clay | obtain clay ×20 | – | = find-clay |
| Form bowl, pot, vessel | clayform | Find clay | = form-bowl, form-pot, form-vessel |
| Fire a pit kiln **[G]** | obtain fired bowl | Form, dry grass or straw | ~ fire-pottery; the kiln takes dry grass or straw (2 straw per layer, confirmed in the Art of Growing patch); reward stage `clay` |
| Cook a pot meal | cook `claypot-*-cooked` | Fire | = cook-meal |
| Form a crucible and tool molds | clayform | Fire | from copper-age form-crucible, form-mold |
| Find fire clay | obtain ×30 | Find clay | = find-fireclay |
| Bricks and shingles | obtain | Fire | = make-bricks, make-shingles |
| Jug, watering can, planter, storage vessel | obtain / place | Fire | = make-jug, make-watering-can, make-planter, place-vessel |

#### Copper Age (order 30, age)

Covers S11.

| Quest | Task | After | Source |
|---|---|---|---|
| Pan or find copper | obtain copper nuggets | – | ~ make-pan, find-copper |
| Spot an ore vein | check | – | new (Juicy Ores) |
| Smash ore with a stone | obtain nuggets ×40 | Find copper | new (S11); a loose stone held in hand breaks chunks lying on the ground. Read from the mod code, verify in game |
| Burn charcoal | obtain charcoal | Split firewood | ~ make-charcoal (tinder on the pit) |
| Make tongs | obtain | – | = make-tongs |
| Cast a pickaxe head and a hammer head | smelt | Smash ore, Charcoal, molds | ~ cast-tool |
| Assemble copper tools | obtain pickaxe, hammer | Cast | ~ make-pickaxe, make-hammer (S1) |
| Smash ore with a hammer | check | Assemble copper tools | new (S11); any metal hammer, no tier limit |
| Cast ingots | smelt | Cast | = cast-ingot |
| Build a forge and cast an anvil | place / obtain | Ingots | = build-forge, cast-anvil |
| First smithing **[G]** | smith | Forge, Anvil | = first-smithing; reward stage `copper` |
| Smith a saw blade | smith, obtain saw | First smithing | ~ make-saw (leads to Woodworking) |
| Nails and a chest | obtain | First smithing, Planks | = make-nails, build-chest; moved from building |
| Smash ore on the anvil | check | First smithing | new |
| Cold-work copper | check | First smithing | new (Toolsmith) |
| Smith a knife, scythe, shears, chisel | smith | First smithing | = smith-knife, make-scythe, make-chisel |

#### Bronze Age (order 40, age)

| Quest | Task | After | Source |
|---|---|---|---|
| Make a prospecting pick | obtain | First smithing | = make-prospecting-pick |
| Share a prospecting reading | check (party) | Prospecting pick | new (ProspectTogether) |
| Find tin, zinc, bismuth, gold, silver, lead | obtain | Prospecting pick | = find-* |
| Alloy bronze | smelt | Find tin | = alloy-bronze |
| Bismuth and black bronze | smelt | Find … | = alloy-bismuth-bronze, alloy-black-bronze |
| Bronze anvil | obtain | Alloy bronze | = bronze-anvil |
| Smith bronze tools **[G]** | smith | Alloy bronze | = smith-bronze; reward stage `bronze` |
| Alloy pewter | obtain `game:ingot-pewter` | Find tin, lead | new |
| Reforge a worn head | check | Smith bronze | new (points to Toolsmithing) |

#### Iron Age (order 50, age)

Mostly vanilla; reuse upstream with wording fixes.

| Quest | Task | After | Source |
|---|---|---|---|
| Find iron ore, meteorite, borax | obtain | Smith bronze | = find-iron, find-meteorite, find-borax |
| Fire-clay bricks and bloomery | obtain / place | – | = fire-fireclay-bricks, build-bloomery |
| Bellows | obtain | Leather | = build-bellows |
| Smelt and refine a bloom | smelt, smith | Bloomery | = make-bloom, refine-bloom |
| Smith iron | smith | Refine | = smith-iron |
| Coat and quench a head | craft, check | Smith iron | = coat-head, quench-head |
| Fuse an iron anvil **[G]** | check | Smith iron, borax | = fuse-anvil; reward stage `iron` |
| Meteoric iron | smith | Fuse anvil | = smith-meteoric |
| Glass and lantern | obtain | Bloomery | from glass-and-kilns find-quartz, make-glass, make-lantern |
| Coke oven and beehive kiln | place, check | – | from glass-and-kilns build-coke-oven, build-kiln, fire-kiln |

#### Steel Age (order 60, age)

| Quest | Task | After | Source |
|---|---|---|---|
| Refractory bricks | obtain | Coke oven | from glass-and-kilns |
| Build the cementation furnace | place | Refractory | = lay-furnace-floor, build-furnace, wall-furnace |
| Blister steel → steel **[G]** | obtain | Furnace | = blister-steel, forge-steel; reward stage `steel` |
| Steel tools and anvil | smith | Steel | = smith-steel, make-steel-tools, make-steel-anvil |
| Flint and steel | check | Steel | new (Firestarters) |

### 4.2 Workshop

#### Toolsmithing (order 110)

Four parallel paths, one per tool part, plus upkeep. Each row is one step up; stat figures are from `ToolsmithPartsStats.json` (durability factor). Part swaps cannot be detected, so most rows hold the material and tick a checkbox.

| Quest | Task | After | Source |
|---|---|---|---|
| **Handles** · Stick or bone handle | check | First tools | new; factor 1.0, bone allows a grip |
| **Handles** · Crude handle | obtain `toolsmith:crudehandle` | Firewood | new; knife + firewood, allows a grip |
| **Handles** · Carved handle | obtain `toolsmith:handle` | Support beams | new; factor 1.2, can be treated |
| **Handles** · Professional handle | obtain `toolsmith:carpentedhandle` | Sandpaper | new; factor 1.5; sandpaper needs sand, pitch glue, parchment |
| **Bindings** · Grass or reed binding | check | First tools | new; factor 1.0 |
| **Bindings** · Twine binding | obtain flax twine | Flax | new; 1.2 |
| **Bindings** · Rawhide strips | obtain `toolsmith:fabricstrips-rawhide` | First hunt | new; 1.25, stone age |
| **Bindings** · Rope or sinew | obtain `game:rope` or `butchering:sinew-dry` | Butcher a carcass | new; 1.25 |
| **Bindings** · Cloth strips | obtain `toolsmith:fabricstrips-cloth` | Linen | new; 1.3 |
| **Bindings** · Pitch glue | obtain `game:glueportion-pitch-hot` | Resin | new; 2.0, the strong early choice; hide and sinew glue match it |
| **Bindings** · Copper nails and strips | obtain `game:metalnailsandstrips-copper` | First smithing | new; 1.4 |
| **Bindings** · Leather strips | obtain `toolsmith:fabricstrips-leather` | Leather | new; 1.5 |
| **Bindings** · Bronze nails and strips | obtain | Smith bronze | new; 1.7 |
| **Bindings** · Iron nails or sturdy strips | obtain | Smith iron | new; 1.8 |
| **Bindings** · Steel nails and strips | obtain | Steel | new; 2.2, the best |
| **Grips** · Twine grip | check | Crude handle | new; handle wears 5 % less often |
| **Grips** · Cloth grip | check | Linen | new; +10 % speed |
| **Grips** · Leather grip | check | Leather | new; +20 % speed |
| **Grips** · Sturdy leather grip | check | Smith iron | new; +30 % speed |
| **Treatments** · Fat | check | Carved handle | new; +20 % handle life, must dry |
| **Treatments** · Beeswax | check | Wax | new; +50 % |
| **Treatments** · Oil | check | Oil press | new; +65 % (flax, olive or seed oil) |
| **Upkeep** · Whetstone *(optional)* | obtain `toolsmith:whetstone-*` | First tools | new (S2) |
| **Upkeep** · Grindstone | obtain `toolsmith:grindstone-*` | Planks | new |
| **Upkeep** · Tool workbench | obtain `toolsmith:workbench-north` | Planks, saw | new |
| **Upkeep** · Swap a worn part | check | Workbench | new |
| **Upkeep** · Reforge a head | check | Smith bronze | new |
| Master tool **[G]** | check | Professional handle, Steel nails, Sturdy grip, Oil | new |

#### Woodworking (order 120)

Covers S4.

| Quest | Task | After | Source |
|---|---|---|---|
| Split sticks | obtain stick | Chopping block | new |
| Season firewood | obtain `fseasonedfirewood:fseasonedfirewood` | Split firewood | new |
| Make rope for trestles | obtain rope ×2 | – | = make-rope |
| Build paired sawhorses | place `immersivewoodworking:sawhorse` ×2 | Rope, Saw | new (S4) |
| Saw planks | obtain planks | Sawhorses | ~ make-boards |
| Saw support beams | obtain support beam | Sawhorses | new |
| Debark a log | obtain `immersivewoodworking:bark-tan-green` | Sawhorses | new (leads to Leatherwork) |
| Smith a pit saw, bark spud, maul | obtain | First smithing | new |
| Tap resin; listen for resin logs | obtain resin | – | = tap-resin (Bark Beetle note) |
| Birch tar | obtain `immersivewoodworking:barktar` +u | Clay pot | new |
| Bast rope and medicinal bark | obtain | Debark | new |
| Powered sawmill **[G]** | place `immersivewoodworking:sawmill-frame-north` | Mechanical Power | new |
| Powered chopper | place `immersivewoodworking:chopper-frame-north` | Mechanical Power | new |

#### Materials & Ceramics (order 130)

| Quest | Task | After | Source |
|---|---|---|---|
| Coloured clay pottery | obtain | Pit kiln | new (Bricklayers) |
| Mud bricks, clay tiles | obtain | – | = bricklayers mudbrick and tile quests |
| Crush and powder | obtain `em:crushed-*`, `em:powdered-ore-quartz` | Pulverizer, quern | ~ crush-quartz |
| Ash, lye and potash | obtain +u | Barrel | new (Expanded Matter) |
| Alum, borax, gypsum | obtain | Powder | ~ crush-alum |
| Glaze base | obtain `bricklayers:glazingbase-clear` | Powder | = bricklayers glazing chain |
| Frit: mix, bake, grind | obtain `bricklayers:frit-ground-*` | Glaze base | = bricklayers |
| Glaze a bowl **[G]** | obtain `bricklayers:glazedbowl-burnt-*` | Frit | = bricklayers |
| Porcelain | obtain | Powder | = bricklayers |
| Coloured glass | obtain | Bloomery | = bricklayers |
| Quicklime, plaster, mortar | obtain | Quern | = grind-lime, burn-quicklime, slake-lime, make-plaster, mix-mortar |
| Pan for ore | check | – | new (Expanded Matter panning) |

#### Rooms & Shelter (order 140)

Built around rooms the game recognises and rewards: a cellar, a ventilated room with a chimney, a greenhouse, a barn. Decoration is left to Home & Decor.

| Quest | Task | After | Source |
|---|---|---|---|
| **Walls** · Packed dirt | obtain `game:packeddirt` | Shovel | new (S12); 6 soil → 6 |
| **Walls** · Cob | obtain `game:cob-none` | Dry grass | ~ build-shelter |
| **Walls** · Mud bricks | obtain `game:mudbrick-*` | Clay, sand | = bricklayers mudbrick |
| **Walls** · Stone bricks and mortar | obtain / place | Chisel, lime | = cut-stone-bricks, mix-mortar, lay-stone-bricks |
| **Walls** · Door and ladder | obtain | Planks | = make-door, make-ladder |
| **Roof** · Thatch roof | obtain `oneroof:oneroof-thatch*` | Dry grass or straw | new |
| **Roof** · Shingle roof | obtain `oneroof:oneroof-*clay-*` | Shingles | new |
| **Roof** · Scaffolding | obtain `scaffolding:scaffolding-*` | Planks | new |
| **Cellar** · Dig a first cellar | check | Shelter | ~ build-cellar; a closed 1×2×1 hole already counts |
| **Cellar** · Storage vessel in the cellar | place storage vessel | Pit kiln | = place-vessel, cellar-food |
| **Cellar** · A walk-in cellar | check | Door | new; up to 7×7×7, walls of soil, brick or stone, no skylight |
| **Cellar** · Shelves and crocks | obtain shelf | Planks | = make-shelf; leads to Preservation & Cellar |
| **Cellar** · Stock the cellar **[G]** | – | Walk-in cellar, Crocks | = stock-cellar |
| **Chimney** · Vent your fire | check | Shelter | new (S9) |
| **Chimney** · Build a chimney | check | Vent your fire | new (S9); a column of open blocks capped with a chimney block |
| **Chimney** · Smokehouse | check | Chimney, smoke rack | new; a room that holds smoke for the rack |
| **Greenhouse** · Glass | obtain glass | Bloomery | = make-glass |
| **Greenhouse** · Build a greenhouse | place glass ×12 | Glass | = build-greenhouse |
| **Greenhouse** · Feel the bonus | check | Greenhouse | = greenhouse-bonus |
| **Barn** · Roofed animal shelter | check | Roof | new (S21); leads to Livestock |
| **Barn** · Sealed axle passthrough | obtain `millwright:improvedaxlepassthrough*` | Windmill | new; power through a wall without breaking the room |

#### Mechanical Power (order 150)

| Quest | Task | After | Source |
|---|---|---|---|
| Axle, gears, rotor | obtain | Resin, fat or oil | = make-axle, make-gears, make-rotor (oil and lard alternative) |
| Sails | obtain | Linen | ~ make-sails (Tailor's Delight recipe) |
| Build a windmill **[G]** (server) | place | Rotor, sails | = build-windmill |
| Power a quern | place | Windmill | = power-quern |
| Pulverizer | obtain | Bronze | = make-pulverizer |
| Helve hammer | place | Bronze | = build-helve-hammer; ore-smashing note |
| Large gear, grinding wheel | place | Windmill | = build-large-gear, build-grinding-wheel |
| Reinforced rotor | obtain `millwright:windmillrotor-*` | Iron plate | new |
| Wide sails and vertical rotor | obtain | Reinforced rotor | new |
| Brake and sealed axle passthrough | obtain `millwright:improvedaxlepassthrough*` | – | new |
| Water wheel on a stream | place | Smith iron | ~ build-waterwheel (Watersheds) |
| Powered mixing bowl | obtain `aculinaryartillery:poweredmixingbowl-*` | Windmill | = expandedfoods |

#### Storage & Hauling (order 160)

| Quest | Task | After | Source |
|---|---|---|---|
| **Bags** · Reed basket (3 slots) | obtain `game:basket-normal-*` | – | = make-basket |
| **Bags** · Hunter's backpack (4) | obtain `game:hunterbackpack` | Pelts | new; reed tops + pelts, stone age |
| **Bags** · Linen or wool sack (5) | obtain `game:linensack` or `wool:sack-wool-*` | Needle, linen | = tailorsdelight make-sack (S27) |
| **Bags** · Leather backpack (6) | obtain `game:backpack-normal` | Leather, buttons, awl | = tailorsdelight make-backpack (S27) |
| **Bags** · Sturdy backpack (8) | obtain `game:backpack-sturdy` | Sturdy leather | new |
| **Bags** · Mining bag (12, ore only) | obtain `game:miningbag` | Smith bronze | new |
| **Bags** · Sturdy mining bag (14) | obtain `game:miningbagsturdy` | Smith iron | new |
| **Bags** · Four good bags **[G]** | check | Leather backpack | new |
| **Belt** · Tool belt | obtain `game:clothes-waist-sturdy-belt` | Leather | new; 2 tool slots, heavy belt 4 |
| **At home** · Ground storage and piles | check | – | = ground-storage |
| **At home** · Carry a container | check | – | new (Carry On) |
| **At home** · Wicker basket and wooden box | obtain | – | new (Containers Bundle) |
| **At home** · Resource bin | obtain `purposefulstorage:resourcebin-*` | Planks | new |
| **At home** · Racks for tools, firewood, pelts | obtain | Planks | new |
| **At home** · Food cupboard | obtain `containersbundle:foodcupboard-*` | Nails | new |
| **At home** · Strongbox and metal cabinet | obtain | Smith iron | new |
| **Hauling** · Cart schematics | obtain `cartwrightscaravan:cartschematics-carts` | – | new |
| **Hauling** · Build a sled | obtain | Schematics | new |
| **Hauling** · Build a cart | obtain | Support beams | new |
| **Hauling** · Wheelbarrow and market stall | obtain | Cart | new |

### 4.3 Land

#### Fields & Harvest (order 210)

Art of Growing gives each kind of plant its own cycle, so the chapter runs as separate paths. Covers S13–S17. Art of Growing does not change soil rules; moisture and fertility are vanilla.

| Quest | Task | After | Source |
|---|---|---|---|
| **Soil and water** · Knap and assemble a hoe | obtain | First tools | ~ knap-hoe, make-hoe |
| **Soil and water** · Farm beside water | check | Hoe | new; farmland takes moisture from water a few blocks away, otherwise use a watering can |
| **Soil and water** · Bring in medium soil | obtain `game:soil-medium-*` ×8 | Shovel | new; medium fertility or better, low soil grows slowly |
| **Soil and water** · Read the three nutrients | check | Hoe | new; crops drain N, P or K (carrot K, onion and parsnip P, turnip N), so rotate |
| **Grass and hay** · Mow and dry grass | obtain `game:drygrass` ×32 | – | new (S13); a dried layer left lying regrows after about 8 days |
| **Grass and hay** · Wooden hayfork | obtain `artofgrowing:hayfork-wooden` | Sticks | new; gathers many layers at once |
| **Grass and hay** · Bale hay or straw | obtain `game:hay-normal-ud` | Rope | new; pile 8 on the ground and press with rope |
| **Grains** · Find wild grain | obtain `artofgrowing:grainbundle-*-wet` | – | new (S14); spelt, rye, rice, amaranth, flax |
| **Grains** · Dry the bundles on the ground | obtain `artofgrowing:grainbundle-*-dry` | Find wild grain | new (S14); shift-place them; in a bag they rot to straw first |
| **Grains** · Thresh with a stick | obtain `game:seeds-*`, `game:thatch` | Dry bundles | ~ harvest-grain (S14); one bundle gives one seed and one straw |
| **Grains** · Sow your seed | check | Thresh, Hoe | new; the threshed seed is what you plant |
| **Grains** · Harvest a planted field | obtain `artofgrowing:grainbundle-*-wet` ×16 | Sow | new; a ripe plant gives 7 to 14 bundles |
| **Grains** · Cut seed into cereal | obtain `game:grain-*` | Thresh | new (S15); knife + seed, one way only, so keep seed back |
| **Grains** · Eat from your own field | obtain flour or porridge | Cereal, Quern | = make-quern, grind-flour |
| **Grains** · Flail | obtain `artofgrowing:flail` | Leather, nails | new; threshes faster |
| **Vegetables** · Find wild vegetables or seeds | obtain `game:vegetable-*` or seeds | – | ~ gather-seeds; a wild plant gives food or seed depending on its stage |
| **Vegetables** · Plant seeds | check | Hoe | new |
| **Vegetables** · Harvest at maturity | obtain `game:vegetable-*` ×8 | Plant seeds | ~ grow-vegetables; yield falls after the mature stage |
| **Vegetables** · Let a plant wither for seed | obtain `game:seeds-carrot` or similar | Plant seeds | new (S16); the last stage gives about 3 seeds and no food |
| **Vegetables** · Plant a seedling | check | Harvest | new (S16); a carrot, onion, turnip or parsnip put back in the soil grows about 2 seeds |
| **Vegetables** · Keep a seed plot | check | Wither, Seedling | new (S16); set a few plants aside for seed each season |
| **Vegetables** · Scallions *(optional)* | obtain `artofgrowing:vegetable-scallions` | Onions | new; young onions give greens |
| **Other crops** · Cabbage | obtain cabbage, cabbage seeds | Plant seeds | new; no seedling, seed only from withered plants |
| **Other crops** · Pumpkin | obtain pumpkin slices | Hoe | ~ grow-pumpkin (S17); place the fruit and cut it with a knife |
| **Other crops** · Sunflower | obtain `game:seeds-sunflower` | Hoe | new; hold the head and rub out the seeds |
| **Other crops** · Soy and peanuts | obtain `game:legume-*` | Hoe | new; shell the pods in hand; the bean is both seed and food |
| **Other crops** · Flax | obtain `artofgrowing:flaxbundle-dry` | Thresh | ~ grow-flax; leads to Textiles |
| **Fertilizer** · Collect manure | obtain `naturalfertilizer:manure` | Shovel | new |
| **Fertilizer** · Weak fertilizer | obtain `naturalfertilizer:weakfertilizer` | Manure | new |
| **Fertilizer** · Mature fertilizer | obtain `naturalfertilizer:maturefertilizer` (mod machine) | Barrel | new |
| **Fertilizer** · Compost, bone meal, saltpeter | obtain | – | = make-compost, grind-bonemeal, gather-saltpeter |
| Oil press and food oil | obtain | – | = expandedfoods oil quests |
| Full harvest **[G]** | grain, vegetables and seed in store | – | ~ full-harvest |

#### Orchards & Bees (order 220)

Covers S34.

| Quest | Task | After | Source |
|---|---|---|---|
| Pick fruit by hand | check | – | new (Manual Harvesting) |
| Bush and tree cuttings; grafting | obtain / place | – | = take-*, plant-*, graft-cutting |
| Raid a wild hive | obtain honeycomb | – | = raid-wild-hive |
| Skep, flowers, populate | obtain / place | – | = make-skep, plant-flowers, populate-skep |
| Honey, wax, candle | obtain | Skep | = harvest-honey, squeeze-honey, collect-beeswax, make-candle |
| Ceramic hive | clayform / place | Populated skep | ~ fromgoldencombs clay hive quests (S34) |
| Harvest the honey pot | obtain | Ceramic hive | = fromgoldencombs |
| Pollination bonus | check | Ceramic hive | new |
| Waxed boards and linen | obtain +u | Wax, planks | = fromgoldencombs |
| Frames and rack | obtain | Waxed linen | = fromgoldencombs |
| Assemble a Langstroth hive **[G]** | check | Frames | = assemble-langstroth |

#### Livestock (order 230)

One common care path, then a path per animal, because each is caught and kept differently. Covers S21, S22. Livestock Welfare's breeding module is switched off in this pack's config, so whether bedding is still required to breed must be checked in game.

| Quest | Task | After | Source |
|---|---|---|---|
| **Care** · Build a roofed pen | place fence ×16; check | – | ~ build-pen |
| **Care** · Trough and feed | obtain | Planks or logs | = make-trough, make-large-trough |
| **Care** · Give them water | obtain `livestockwelfare:waterer-fired` | Pit kiln | new; a pond or bucket works too |
| **Care** · Earn an animal's trust | check | Pen | new (betterhusbandry); feed and pet daily |
| **Care** · Lay straw bedding | obtain `livestockwelfare:strawbedding-clean` | Dry grass | new (S21) |
| **Care** · Clean and groom | obtain `livestockwelfare:groomingbrush` | Flax fibers | new; shovel muck, groom with dry grass |
| **Care** · Breed a first generation **[G]** | check | Water, Bedding, Trust | ~ breed-animals (S21) |
| **Care** · Move a tame animal | check | Breed | new (S22); generation 1 and up, Ctrl + right-click |
| **Care** · Read the animal profile | check | Breed | new (genelib) |
| **Chickens** · Lure or trap a hen | obtain `game:baskettrap-*` | – | = make-basket-trap; hens follow held grain |
| **Chickens** · Hen box and eggs | obtain | Hen | ~ make-henbox, collect-eggs |
| **Chickens** · Nest box and coop kit | obtain `livestockwelfare:chickencoop-*` | Planks | new |
| **Chickens** · Crumb feed | obtain `efchefstricks:breadcrumbfeed` | – | = efchefstricks |
| **Hares** · Trap a hare | obtain `game:baskettrap-*` | – | new; basket trap, adults and young |
| **Hares** · Feed on vegetables | check | Trap a hare | new; small trough |
| **Pigs** · Trap a piglet | check | Basket trap | new; adult boars break traps, only piglets can be caught |
| **Pigs** · Raise it on scraps | check | Piglet | new; grain, fruit, vegetables or meat |
| **Sheep and goats** · Trap a lamb or kid | check | Basket trap | new; adults cannot be trapped; the basket trap works poorly on them |
| **Sheep and goats** · Crate trap | obtain `game:trapcrate-wood` | Smith bronze | = make-crate-trap; much better odds |
| **Sheep and goats** · Bucket and milk | obtain milk | Breed | = make-bucket, milk-animal; ewes and nannies after a birth |
| **Sheep and goats** · Shear a fleece | obtain `wool:fleece-*` | Breed, Shears | = wool shear quests (S22); generation 1 and up |

#### Horses & Riding (order 240)

| Quest | Task | After | Source |
|---|---|---|---|
| Find wild horses | check | – | new |
| Saddle and bridle | obtain `equusferus:saddle-*`, `bridle-*` | Leather, nails | ~ make-saddle, make-bridle |
| Break in a horse | mount `equusferus:wildhorse-*` | Saddle | new |
| Ride a tamed horse **[G]** | check | Break in | new |
| Call flute | obtain `jaunt:instrument-flute` | – | ~ make-bone-flute |
| Saddlebags, blanket, pillion | obtain | Ride | = make-saddlebags, make-pillion |
| Hitching post | obtain | Planks | new |
| Visit a Stablemaster | trade `equusdestrier:*` | – | new |
| Destrier barding | obtain | Smith iron | new |
| Elk: trap, break in, ride | check / mount | Crate trap | = trap-elk-calf, break-in-elk, ride-elk |

#### Butchery & Hunting (order 250)

Covers S19, S20.

| Quest | Task | After | Source |
|---|---|---|---|
| Knap a javelin | obtain `armory:javelin-plain-*` | Flint, stick | new; preferred hunting weapon, hits harder thrown than the spear |
| First hunt | kill | Javelin | ~ first-hunt |
| Carry a carcass | obtain `butchering:dead*` | First hunt | new (S19); takes a bag slot, small animals fit anywhere |
| Butchery bag *(optional)* | obtain `butchering:butcherybag-primitive` | Rope, reeds | new; carcasses then go to the inventory |
| Knap a hook, build a skinning hook | obtain `butchering:butcherhook-flint-north` | – | new |
| Skin a carcass | obtain hide | Hook | ~ get-hide |
| Collect the blood | obtain `butchering:bloodportion` | Skin | new; a bucket 2 to 4 blocks under the hook; a saucepan probably works too, verify |
| Primitive butcher table | obtain `butchering:butchertable-primitive-north` | – | new |
| Butcher a carcass **[G]** | obtain `butchering:primemeat*`, sinew, offal | Table, Skin | new |
| Slice a meat slab | obtain `rusticcookery:meatslab-*-raw` | Butcher | new (S20) |
| Smoke rack and smoked slab | obtain `rusticcookery:meatslab-*-smoked` (mod machine) | Slab, fire | new |
| Render fat | obtain fat | Butcher | = melt-fat |
| Clean offal, blood sausage | obtain (mod machine) | Barrel | new |
| Sinew and hide glue | obtain `butchering:glueportion-*` | Butcher | new |
| Cleaver | obtain | First smithing | = make-cleaver |
| Metal hooks and smoking rack | obtain `butchering:smokingrack-*` | First smithing | new |
| Simple and advanced tables | obtain | Planks | new |

### 4.4 Kitchen

#### Cooking (order 310)

Covers S23, S24, S36.

| Quest | Task | After | Source |
|---|---|---|---|
| Wash your dishes | check | Pot meal | new (S36) |
| Meat stew | cook | Pot meal, meat | = cook-stew; vanilla, still a staple |
| Vegetable stew | cook | Pot meal, vegetables | new; vanilla recipe |
| Soup and porridge | cook | Pot meal | = cook-soup, cook-porridge |
| Fire a saucepan | obtain `aculinaryartillery:saucepan-*-fired` | Pit kiln | = expandedfoods saucepan |
| Simmer bone broth | obtain `expandedfoods:brothportion-bone` | Saucepan | new |
| Render lard | obtain lard | Saucepan | = expandedfoods lard |
| Rolling pin and mixing bowl | obtain | Saucepan | = expandedfoods mixing bowl |
| Smash and cut meat nuggets | obtain `expandedfoods:meatnugget-*` | – | = expandedfoods nuggets |
| Knead sausage or pemmican | obtain `expandedfoods:sausage-*` +u | Mixing bowl | = expandedfoods sausage |
| Crack an egg | obtain liquid egg | – | ~ crack-egg (S23) |
| Scrambled eggs the new way | check | Crack an egg | new |
| Mix a salad | check | Mixing bowl | = mix-salad |
| Roasting dish | obtain `rusticcookery:roastingdish-*-fired` | Pit kiln | new |
| Braise with tongs | check | Roasting dish, Tongs | new (S24) |
| Pot roast | check | Braise, oven | new |
| Tree syrup | obtain `expandedfoods:treesyrupportion-*` | Spile | = expandedfoods tap-tree, syrup |
| Small cauldron and cauldron | obtain | First smithing | = expandedfoods cauldron |
| Four-burner stove | obtain `kevinsfurniture:stove-*` | – | new |
| Eat well **[G]** | all main meals | – | ~ eat-well |

#### Baking (order 320)

| Quest | Task | After | Source |
|---|---|---|---|
| Grind flour | obtain flour | Quern, grain | = grind-flour (needs grain, not seeds) |
| Knead dough by hand | obtain dough | Flour | ~ make-dough (Manual Dough) |
| Form and place a clay oven | clayform, place oven | Fire clay | = form-oven, place-oven; moved from Clay & Fire |
| Bake bread | obtain bread | Clay oven | = bake-bread |
| Bake a pie | obtain pie | Bread | = bake-pie |
| Roast grain, breadcrumbs | obtain | – | = expandedfoods |
| Bread starter | obtain +u | Barrel | new |
| Hardtack | obtain `expandedfoods:hardtack-*` | Mixing bowl | = expandedfoods |
| Fresh pasta | obtain `expandedfoods:pasta-*` | Rolling pin | = expandedfoods pasta |
| Blood bread | obtain | Blood | new |
| Build a stone bake oven **[G]** | place `stonebakeoven:ovencontroller*`, grill, baking top | Copper plate | new |

#### Dairy (order 330)

Covers S26.

| Quest | Task | After | Source |
|---|---|---|---|
| Collect milk | obtain milk | Milk an animal | = collect-milk |
| Settle milk and skim cream | obtain `dairyplus:cream` | Barrel; `dairyplus:creamscoop` | new (S26) |
| Fruit vinegar | obtain +u | Barrel | new |
| Butter churn and butter | obtain `dairyplus:plungerchurn`, butter | Nails | new |
| Ghee | obtain | Butter | new |
| Cheese kettle | obtain `dairyplus:cheesekettle-*` | Solder, plates | new |
| Curds and whey | obtain +u | Kettle | new |
| Mozzarella | obtain `dairyplus:mozzaball*` | Curds | new |
| Feta, ricotta, halloumi | obtain | Curds | new |
| Cottage cheese, pressed cheese | obtain / check | – | = curdle-milk, make-cottage-cheese, press-cheese |
| Age cheddar **[G]** | obtain | Press | = age-cheddar, wax-cheese, age-blue-cheese |
| Pasteurise, yogurt | obtain | Saucepan | = expandedfoods |
| Tofu and soy milk | obtain | Soy | = expandedfoods soy; new tofu |

#### Preservation & Cellar (order 340)

The cellar itself is built in First Days and Rooms & Shelter; this chapter fills it.

| Quest | Task | After | Source |
|---|---|---|---|
| **Crocks** · Form and fire a crock | clayform, obtain `game:crock-*-fired` | Pit kiln | = form-crock, fire-crock |
| **Crocks** · Fill a crock from the pot | check | Pot meal | new; click a cooked pot with the crock, 4 servings |
| **Crocks** · Seal it | check | Fat or beeswax | = seal-crock; sealing slows spoilage tenfold |
| **Crocks** · Shelve it in the cellar | obtain shelf | First cellar | = make-shelf |
| **Crocks** · Pewter crock | obtain `pewter:crock-pewter` | Pewter | new |
| **Salt** · Halite | obtain `game:salt` | Quern | = find-salt |
| **Salt** · Fetch sea water | obtain `game:saltwaterportion` | Bucket | new |
| **Salt** · Boil sea water | obtain salt crystal (mod machine) | Small cauldron | new; 10 L per crystal; the saucepan holds only 5 L, enough for brine |
| **Salt** · Or evaporate it in a barrel | obtain `efchefstricks:saltcrystal-dry` | Barrel | = efchefstricks; sealed 240 h, then dried |
| **Salt** · Grind the crystal | obtain `game:salt` | Quern | new |
| **Keeping** · Brine, cured meat, pickles | obtain | Salt, barrel | = make-brine, cure-meat, pickle-vegetables |
| **Keeping** · Meat rack and dry-aged meat | obtain `aculinaryartillery:meathooks-*`, `expandedfoods:agedmeat-*` | Large hooks | = expandedfoods |
| **Keeping** · Water-glassed and pickled eggs | obtain | Barrel | = expandedfoods |
| **Keeping** · Fish sauce, soy sauce | obtain | Barrel | = expandedfoods |
| **Keeping** · Food shelves and baskets | obtain `foodshelves:*` | – | new |
| **Cold** · Cut ice | obtain `foodshelves:cutice` | Saw | new |
| **Cold** · Cooling cabinet and ice keeper | obtain | Glass | new |
| **Cold** · Meat freezer | obtain | Tin or zinc | new |
| Winter larder **[G]** | – | Crocks, salt, cellar | from winter: stock-firewood, stock-grain, winter-larder |

#### Brewing & Drink (order 350)

Covers S25.

| Quest | Task | After | Source |
|---|---|---|---|
| Brew tea | obtain `simpletea:teaportion-*-hot` | Pot | new |
| Wooden tankard | obtain `tankardsandgoblets:tankard-wood` | – | new |
| Fruit press and juice | obtain | – | = make-fruit-press, press-juice |
| Ferment a drink | obtain | Barrel | = ferment-drink |
| Clay bottles and corks | obtain `aculinaryartillery:bottle-clay-*`, `stopper-bark-cork` | Saucepan | = expandedfoods bottles |
| Seal it or lose it | check | Bottles | new (S25) |
| Vinegar on purpose | obtain | Ferment | = expandedfoods vinegar |
| Age strong wine | obtain `expandedfoods:strongwineportion*` | Seal | = expandedfoods wine aging |
| Know your limit | check | Ferment | new (SlowTox) |
| Still: boiler and condenser | obtain | Solder | = make-boiler, make-condenser and the solder chain |
| Distil spirit **[G]** | obtain | Still | = distill-spirit, aqua-vitae |
| Potent spirit | obtain | Distil | = expandedfoods aged spirit |
| SoulStorm brew | obtain `expandedfoods:soulstormbrew-*` | Distil | new |
| Goblets, wine bottles, demijohn | obtain | Glass | new |
| Bottle rack and barrel rack | obtain | – | = expandedfoods; FoodShelves |

### 4.5 Craft

#### Textiles & Tailoring (order 410)

Covers S18, S27, S28.

| Quest | Task | After | Source |
|---|---|---|---|
| Flint awl and bone needle | obtain `tailorsdelight:awl-flint`, `needle-bone` | – | = tailorsdelight awl, needles |
| Grow flax | obtain flax bundle | Hoe | ~ grow-flax |
| Ret and clean flax | obtain `artofgrowing:flaxbundle-clear` +u | Barrel | new (S18) |
| Ridge flax into fibers | obtain flax fibers; `artofgrowing:ridge-rough` | Ret | new |
| Spin twine | obtain twine; `tailorsdelight:spindle-wood` | Fibers | ~ spin-twine (S28 note) |
| Weave linen | obtain | Twine | = make-linen |
| Sewing kit | obtain | Needle | = tailorsdelight replacement (S27) |
| Buttons | obtain | – | = tailorsdelight |
| Sew a sack **[G]** | obtain `game:linensack` | Needle, linen | = tailorsdelight make-sack (S27); bag sizes continue in Storage & Hauling |
| Wash fleece, spin wool | obtain `wool:fibers-*`, `wool:twine-wool-*` | Shear | = wool |
| Weave wool cloth | obtain | Wool twine | = wool (clothier) |
| Knitting needles and a sweater | obtain | Wool twine | = wool knit-sweater |
| Woad and yellow dye | obtain | Barrel | = make-woad-dye, make-yellow-dye |
| Mordant and dye cloth | obtain | Alum | = mordant-cloth, dye-cloth, tailorsdelight dye thread |
| Sew a full outfit | obtain | Cloth | ~ sew-shirt, sew-pants (Dressmakers; party) |
| Dress warm | obtain | – | from winter: make-pelt, dress-warm |

#### Leatherwork (order 420)

Starts with pelts, which need only fat. Tanned leather comes later because tannin needs bark. Covers S5.

| Quest | Task | After | Source |
|---|---|---|---|
| **Pelts** · Oil a hide | obtain `game:hide-oiled-*` | Skin, fat | = oil-hide; fat + raw hide, no tannin or lime |
| **Pelts** · Cure a pelt | obtain `game:hide-pelt-*` | Oil a hide | = cure-pelt; 48 hours |
| **Pelts** · Fur hat and hunter's backpack | obtain | Pelt | = fur-hat; backpack in Storage & Hauling |
| **Pelts** · Pelt rack | obtain `purposefulstorage:peltrack-*` | Planks | new; cures twice as fast |
| **Pelts** · Oil hides in a barrel | check | Lard or food oil | new (Chef's Tricks) |
| **Leather** · Salt a hide for later | obtain | Salt | = salt-hide |
| **Leather** · Limewater or borax soak | obtain | – | = make-limewater, soak-hide |
| **Leather** · Scrape | obtain | Soak | = scrape-hide |
| **Leather** · Dry and crush bark | obtain `immersivewoodworking:barkcrushed` | Debark, quern | new (S5) |
| **Leather** · Weak and strong tannin | obtain | Bark | ~ weak-tannin, strong-tannin |
| **Leather** · Prepare the hide | obtain | Scrape, weak tannin | = prepare-hide |
| **Leather** · Make leather **[G]** | obtain | Prepare, strong tannin | = make-leather |
| **Leather goods** · Leather strips and bundles | obtain | Leather | = tailorsdelight |
| **Leather goods** · Dark and coloured leather | obtain | Leather | = tailorsdelight; Expanded Matter |
| **Leather goods** · Metal awl and buttons | smith | First smithing | = tailorsdelight |
| **Leather goods** · Boots | obtain | Leather | = leather-boots |

#### Arms & Armor (order 430)

Covers S29, S30.

| Quest | Task | After | Source |
|---|---|---|---|
| Learn to fight | check | – | new (directional attacks, parry) |
| Carve a weapon handle | obtain `armory:handle-short` | – | new |
| Stone mace or javelin | obtain | Handle | new |
| Sling and bullets | obtain | Rope | ~ make-sling |
| Bow and arrows | obtain | Rope | = make-bow, knap-arrowheads, make-arrows |
| Crude shield | obtain | – | = make-crude-shield |
| Wood lamellar | obtain `armory:armor-*-lamellar-wood-*` | Pelts, resin | ~ wood lamellar (S29) |
| Hide jerkin | obtain `combatoverhaul:armor-*-jerkin-hide-*` | Hide | new |
| Armourer kit | obtain `combatoverhaul:sewingkit-armor-*` | Nails | new (S29) |
| Buckle and belt | obtain `quiversandsheaths:belt-waist-*` | First smithing, leather | new (S30) |
| Quiver and sheath | obtain | Belt | new |
| Copper sword and lamellar | obtain | First smithing | ~ smith-falx, copper lamellar |
| Shields, light and heavy | obtain | – | ~ make-round-shield |
| Gambeson, leather armour | obtain | Linen, leather | = tailorsdelight replacements |
| Bronze chain or brigandine | obtain | Smith bronze | ~ brigandine, chain |
| Longbow | obtain | Leather | = tailorsdelight make-longbow |
| Iron plate and arming sword | obtain | Smith iron | ~ plate |
| Steel plate **[G]** | obtain | Steel | ~ make-steel-plate |
| Poleaxe or warhammer | obtain | Steel | new |

### 4.6 World

#### Survival & the Unknown (order 510)

Covers S7, S31.

| Quest | Task | After | Source |
|---|---|---|---|
| Keep a flame alive | check | Kindle | ~ relight-fire (S7) |
| Bow drill | check | Bow | new |
| Poultice and bandages | obtain | – | = make-poultice, make-bandage, soak-bandage |
| Recovery kit | obtain bandage ×4 | Bandages | new |
| Rescue a downed friend | check (party) | – | new (S31) |
| Kill a drifter | kill | Spear | = kill-drifter |
| Read the storm signs | check | – | ~ survive-storm (Temporal Symphony) |
| Find a temporal gear **[G]** | obtain | Drifter | = find-temporal-gear |
| See the mist | check | Temporal gear | new (necklace, verify) |
| Recover your things | check | – | new (corpse drop) |
| Rusty gears | obtain | – | = find-rusty-gears |

#### Overland Travel (order 520)

Covers S32.

| Quest | Task | After | Source |
|---|---|---|---|
| Crude walking stick | obtain `walkingstick:walkingstick-crude` | – | new |
| Crawl, vault, roll | check | – | new |
| Catch a ledge and climb rock | check | – | new (S32) |
| Wear a trail | check | – | new |
| Trowel and cairn | obtain `trailmod:trowel-*` | First smithing | new |
| Quill and cartography table | obtain `kscartographytable:cartographytable-*` | Planks | new |
| Share a map **[G]** (party) | check | Table | new |
| Spyglass | obtain `spyglass:spyglass-*` | Glass | new |
| Better walking sticks | obtain | – | new |
| Mine stone, find limestone | break / obtain | Pickaxe | = mine-stone, find-limestone |

#### Waterways (order 530)

Covers S33.

| Quest | Task | After | Source |
|---|---|---|---|
| Fishing: grunter, pole, bait, catch | obtain / craft | – | = waterways fishing quests |
| Fillet and cook fish | obtain | Catch | = fillet-fish; ~ cook-fish |
| Reed boat | obtain `roughseas:reedboat-*` | Reeds, rope | new |
| First crossing | mount | Reed boat | ~ ride-raft |
| Bail and repair | check | First crossing | new (S33) |
| Moor your boat | check | First crossing | new |
| Dugout | obtain `roughseas:dugout-*` | Axe, fire | new |
| Coracle or bark canoe | obtain | Hides or bark | new |
| Currach and outrigger | obtain | Laths | new |
| Read the weather and surf | check | – | new |
| Sailboat **[G]** | mount | Planks | = build-sailboat and parts |
| Well pulley | obtain `watersheds:wellpulley-*` | Rope, bucket | new |

#### Traders (order 540)

The wandering and settled traders of the world. They deal only in rusty gears; player money has no value to them.

| Quest | Task | After | Source |
|---|---|---|---|
| Rusty gears | obtain | – | = find-rusty-gears |
| Find a trader | visit `game:trader-*` | – | new; more building styles from BetterTraders |
| Buy something | trade `*:*` | Rusty gears | = visit-trader |
| Sell for gears | check | Find a trader | new; selling is not detectable |
| Know your traders **[G]** | check | Buy something | new; note who sells what on the map |
| Visit a Stablemaster | trade `equusdestrier:*` | – | new; also in Horses & Riding |
| Trader phone | obtain `remotetradercheckmod:remotetraderchecker-*` | Temporal gear | new; check stock from home |

#### Player Economy (order 545)

Trade between players, in money the group issues itself. Covers S35.

| Quest | Task | After | Source |
|---|---|---|---|
| Hand it over | check (party) | – | new (Hand to Hand) |
| Found a currency (server) | obtain `coins:mint-east`, `coins:banknote-1` | – | new |
| Wallet and change | obtain `coins:wallet` | Currency | new |
| Shop register and first stall | obtain `vinconomy:shopregister-*` | Copper plate | new |
| Make a sale **[G]** | check (party) | Register | new (S35); shops take loose notes only |
| Buy orders and a catalogue | check | Make a sale | new |
| Notice board | obtain `noticeboard:noticeboard-*` | Nails, parchment | new |
| Board and game pieces | obtain `tabletopgames:board-*` | – | new |

#### Home & Decor (order 550)

| Quest | Task | After | Source |
|---|---|---|---|
| Oil lamp and lantern | obtain | – | = make-oil-lamp, make-lantern |
| Wind chime | obtain `windchimes:windchime-*` | – | new |
| Custom window | obtain `windowdisplay:customwindow-*` | Planks | new |
| Furniture set | obtain `kevinsfurniture:*` ×3 | Planks | new |
| Heraldry workbench | obtain `heraldry:heraldryworkbench-*` | Cloth, chisel | new |
| Banner for the settlement **[G]** (server) | obtain `heraldrybanners:banner` | Workbench | new |
| Cape | obtain `capes:cape` | Workbench | new |
| Pewter tableware | obtain `pewter:bowl-pewter` | Pewter | new |
| Gold and silver tableware | obtain | Gold, silver | new |
| Flowerpot and planter | obtain | – | = make-flowerpot |
| Chiselled furniture | check | Chisel | new (Chisel Tools) |
| Hand planer and pantograph *(optional)* | obtain `chiseltools:handplaner-*` | First smithing | new; moved from building |
| Paths, roads and terrain slabs *(optional)* | obtain | – | new; moved from building |
| Harvest whole rock blocks *(optional)* | check | Chisel | new (Stone Harvesting) |

## 5. Coverage checks

**Stuck points.** Every S1–S36 from [progression.md](progression.md) appears in a `Source` cell or chapter note above.

**Upstream chapters** and where their quests go:

| Upstream chapter | Fate |
|---|---|
| stone-age | First Days (rewritten) |
| clay-and-fire | Clay & Fire |
| kitchen | Cooking |
| farming | Fields & Harvest |
| orchards, beekeeping | Orchards & Bees |
| copper-age | Copper Age (molds move to Clay & Fire) |
| building | Rooms & Shelter; chest to Copper Age; lime chain to Materials & Ceramics |
| baking | Baking |
| bronze-age | Bronze Age |
| husbandry | Livestock; hunting parts to Butchery & Hunting |
| textiles | Textiles & Tailoring |
| leatherwork | Leatherwork |
| mechanical-power | Mechanical Power |
| iron-age | Iron Age |
| glass-and-kilns | split: Iron Age, Steel Age, Materials & Ceramics |
| steel-age | Steel Age |
| preservation, winter | Preservation & Cellar; cellar itself to First Days and Rooms & Shelter; clothing to Textiles |
| cheesemaking | Dairy |
| brewing | Brewing & Drink |
| waterways | Waterways |
| riding | Horses & Riding |
| arms-and-armor | Arms & Armor (mostly rewritten) |
| wider-world | split: Survival, Overland Travel, Traders |
| bricklayers, expandedfoods, efchefstricks, efmealsmodule, fromgoldencombs, tailorsdelight, wool | folded into the chapters above; no longer optional add-ons |
| betterruins, hexsmech, seafarer, charcoalkiln | dropped (mods not in the pack) |

**Old roadmap** (`modpack/config/ModConfig/pszczoly/trees`, 23 trees): used for wording and task ideas only. Its trees map onto the chapters above (animals → Livestock and Orchards & Bees; equipment → Toolsmithing and Arms & Armor; exploration and travel → Overland Travel and Waterways; materials → Materials & Ceramics; decoration → Home & Decor; getting-started → First Days).

## 6. Multiplayer candidates

| Quest | Mode | Why |
|---|---|---|
| Build a windmill | server | One shared mill serves everyone. |
| Found a currency | server | The group agrees on one currency. |
| Banner for the settlement | server | Shared identity. |
| Share a map | party | Cartography table sharing. |
| Share a prospecting reading | party | ProspectTogether. |
| Rescue a downed friend | party | Needs two players. |
| Hand it over | party | Needs two players. |
| Sew a full outfit | party | Class-locked recipes; one clothier supplies the group. |
| Make a sale | party | Buyer and seller. |

Coinage (struck metal coins) is installed but deliberately has no quests.

## 7. Consequences for the fork when authoring starts

Editing content directly in this fork conflicts with several guards, each needing an explicit decision at that point:

1. `tests/test_content_extraction.py` freezes the 56 upstream chapter files byte-for-byte and expects 12 content packages; `docs/content-packages.json` lists them.
2. `tools/lang/check.py` requires every English key in all 33 other languages. English-only content needs that check relaxed or scoped.
3. `AGENTS.md` asks to preserve chapter filenames, quest and task IDs and saved progress unless a migration is approved. A clean-slate structure is such a migration; reused quests should keep their IDs, and renamed chapters can use `aliases`.
4. All item rewards become a quest cookie; if stages are used for age gating, `Locking` and stage rewards need a design pass.
5. Item codes in this plan must be validated with `/questline snapshot` and `tools/packcheck` in a game running the full pack.

## 8. Packaging and pull request split

**Decision: one mod.** All quest content ships inside the single `questline` mod. No per-mod content addons, no `requiresMod` gating, no extension files: the pack's mod list is fixed, so every chapter can assume every mod.

What that changes in the repo:

- The twelve packages under `content/` collapse into the core mod's chapter folder. Extension files are merged into their base chapters, with replacement quests applied in place and their IDs kept.
- Packages for mods not in the pack (Better Ruins, Charcoal Kiln, Seafarer, Hex's Machinery) are deleted.
- Build, packaging and CI drop the per-package zips and their counts; the byte-for-byte freeze test is replaced by a content test for the single book.
- English is the only maintained language; the 34-language parity check is scoped accordingly.
- Open draft PRs #4 to #8 build separate addons for mods this plan also covers. The chapters here are written independently and opened as their own PRs, so the two versions can be tested against each other. PR #2 is superseded by the consolidation step.
- Open question: `compat/toolsmith` is a separate code mod. It can stay separate or be folded into the core, since Toolsmith is always present.

Pull requests, each a draft against `main` in the repo's usual layout (outcome, quest map, existing quests changed, evidence, checks run, limits):

| # | Branch | Content |
|---|---|---|
| 1 | `docs/questbook-content-map` | The three documents in `docs/questbook/`. Docs only. |
| 2 | `refactor/single-mod-content` | Collapse `content/*` into the core mod, delete unused integrations, simplify build, CI and tests. No quest text or ID changes. |
| 3 | `refactor/chapter-structure` | The 31-chapter skeleton: orders, groups, quests moved to their new chapters, `aliases` for renamed chapters, stage rewards. No new quests. |
| 4 | `feat/first-days` | First Days, Clay & Fire. |
| 5 | `feat/metal-ages` | Copper to Steel, Toolsmithing. |
| 6 | `feat/woodworking-leather` | Woodworking, Leatherwork. Alternative to PR #5. |
| 7 | `feat/fields-and-bees` | Fields & Harvest, Orchards & Bees. Alternative to PR #6. |
| 8 | `feat/animals` | Butchery & Hunting, Livestock, Horses & Riding. Alternative to PRs #4, #7, #8. |
| 9 | `feat/kitchen` | Cooking, Baking, Dairy, Preservation & Cellar, Brewing & Drink. Split in two if large. |
| 10 | `feat/textiles-arms` | Textiles & Tailoring, Arms & Armor. |
| 11 | `feat/workshop` | Rooms & Shelter, Storage & Hauling, Materials & Ceramics, Mechanical Power. |
| 12 | `feat/world` | Survival, Overland Travel, Waterways, Traders, Player Economy, Home & Decor. |

PRs 2 and 3 must land in order before the rest; PRs 4 to 12 are independent of each other once the skeleton exists.

## 9. Suggested authoring order

1. **First Days** (with the first cellar), then **Copper Age**, **Woodworking**, **Fields & Harvest**, **Butchery & Hunting**, **Livestock**: the chapters where vanilla habits fail soonest.
2. Remaining age chapters and **Toolsmithing**, **Cooking**, **Textiles & Tailoring**, **Leatherwork**, **Arms & Armor**.
3. Kitchen side chapters, **Materials & Ceramics**, **Mechanical Power**, **Rooms & Shelter**.
4. World chapters and **Home & Decor**.
