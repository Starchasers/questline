# Pszczoly questbook: progression map

How a player actually progresses in the Pszczoly 1.4.1 modpack, as read from the mod files and configs. Companion documents: [mod-inventory.md](mod-inventory.md) and [chapter-plan.md](chapter-plan.md).

Item codes come from recipe, item-type and lang files inside the mod zips. They have **not** been validated against a running game; validate them with `/questline snapshot` and `tools/packcheck` before authoring. Codes with `{…}` or `*` stand for variants.

## 1. Tier ladder

What each vanilla tech tier unlocks across the whole pack. Vanilla tool tiers: stone 1, copper 2, bronze 3, iron 4, steel 5.

### Stone

| System | Unlocks |
|---|---|
| Tools | Knapped heads assembled **in hand** (head + stick, then a binding of dry grass or reed tops). Whetstone. Crude handle carved from firewood. |
| Wood | Chopping block: log → half-logs → firewood → sticks. No planks yet. |
| Fire | Firestarter (two diagonal sticks), tinder minigame, staged Art of Growing firepit, stick roasting, torches that die in wind and in the backpack. |
| Walls | Loose soil falls (block gravity is on). Packed dirt (`game:packeddirt`), cob and mud brick stay put. A closed hole in the ground is already a cellar. |
| Land | Dry grass from yellow standing grass, or green grass mown and dried; threshing grain with a stick; wooden hayfork; bales; manure and weak fertilizer. |
| Animals | Carcass, flint skinning hook, primitive butcher table, meat slabs, smoke rack, straw bedding, grooming, trust and generations. |
| Craft | Flint awl, bone needle, spindle, rough ridge for flax, hide and reed bags. |
| Combat | Stone javelin (the better hunting weapon thrown), spear, stone mace, wood lamellar, hide jerkin, crude shield, sling. |
| Travel | Crude walking stick, reed boat, dugout, movement skills, trails. |
| Community | Coins mint and banknotes, tabletop games, hand-to-hand giving. |

### Clay

| System | Unlocks |
|---|---|
| Kitchen | Saucepan, mixing bowl, clay bottles, roasting dish, tea, broths, lard, kneaded foods, liquid egg meals. |
| Land | Clay waterer for livestock, ceramic hive, slurry and mature fertilizer (needs a barrel). |
| Dairy | Settling milk, cream scoop, skim milk. |
| Materials | Coloured clay, mud bricks, clay tiles, tar pot for birch tar. |
| Textiles | Fleece washing in lime water, wool twine. |
| Metal prep | Crucible, tool and ingot molds, tableware molds. |

### Copper

| System | Unlocks |
|---|---|
| Metal | Ore smashed with a stone in hand, first cast heads (pickaxe, hammer), then hammer and anvil smashing, cold-worked copper. |
| Wood | Saw → paired sawhorses → planks and support beams; debarking for tanning bark; pit saw, bark spud, maul. |
| Tools | Toolsmith workbench and grindstone, carved handle, grips, treatments, leather and glue bindings. |
| Building | Scaffolding, OneRoof roofs, chisel, Stone Harvesting, hand planer, stone bake oven (needs copper plate). |
| Kitchen | Meat rack and dry ageing, spile and syrups, small cauldron, butter churn, cheese kettle, tongs for braising, metal smoking rack. |
| Land | Flail, metal hayfork, scythe, shears, horse tack. |
| Craft | Metal awls and buttons, buckles and belts, quivers, armourer kits. |
| Storage | Resource bin, racks, food cupboard, carts and sleds, tool belt. |
| Community | Shop register and stalls, notice board, cartography table, heraldry workbench. |
| Combat | Copper weapons with Armory handles, copper lamellar, light copper shield. |

### Bronze

| System | Unlocks |
|---|---|
| Metal | Bronze alloys, prospecting with shared readings, pewter, reforging worn heads. |
| Power | Windmill, quern and pulverizer in practical use; crushed and powdered materials. |
| Materials | Frit, glazes, glazed ceramics, porcelain. |
| Building | Pantograph, path maker, door tool, stone and ashlar roads. |
| Combat | Bronze weapons, chain and brigandine. |
| Community | Trader phone. |

### Iron

| System | Unlocks |
|---|---|
| Metal | Bloomery, iron anvil, iron plates and nails. |
| Power | Reinforced rotors, improved axle passthrough, powered sawmill and chopper, powered mixing bowl. |
| Materials | Coloured glass from bloomery glass batches. |
| Building | Ladder maker, paintbrush, block swapper. |
| Combat | Arming sword, halberd, plate pieces. |
| Land | Langstroth hive (needs many boards, wax and glue rather than iron, but lands here in practice), destrier barding. |

### Steel

| System | Unlocks |
|---|---|
| Tools | Steel nails-and-strips binding (best), flint and steel firestarter. |
| Combat | Poleaxe, warhammer, full plate, steel barding. |
| Kitchen | Nothing new; end-game is aged potent spirits, SoulStorm brew, cold storage. |

## 2. System chains

### 2.1 Tools (Toolsmith)

1. Knap a head (`game:axehead-flint`, `game:knifeblade-flint` …).
2. Head in main hand, handle (`game:stick`, bone) in offhand, hold right-click.
3. Hold the pair, put a binding in the offhand (dry grass, cattail tops, twine), hold right-click.
4. Knap `toolsmith:whetstone-{chert|granite|andesite|basalt|peridotite}` and hone; near-full sharpness stops head and handle wear.
5. Carve `toolsmith:crudehandle` (knife + firewood).
6. Copper: `toolsmith:grindstone-{rock}-north` (planks + rock) and `toolsmith:workbench-north` (planks, with a saw as tool).
7. `toolsmith:handle` carved from a support beam; `toolsmith:carpentedhandle` with `toolsmith:sandpaper`.
8. Treatment (fat, beeswax, oil; dries 12–48 h), then a grip (twine, cloth, leather, sturdy leather).
9. Better bindings: `toolsmith:fabricstrips-{rawhide|cloth|leather|sturdy|wool}`, rope, `butchering:sinew-dry`, glues, then metal nails and strips up to steel.
10. Reforge worn metal heads at the workbench and forge.

Toolsmith's tool regex also covers the Immersive Woodworking pit saw, maul and bark spud, the hayfork, awl and the OneRoof hammer, so those are probably assembled in hand too.

### 2.2 Wood (Immersive Woodworking, Seasoned Firewood)

1. `immersivewoodworking:choppingblock` (axe + placed log). Log → `immersivewoodworking:halflog` → firewood; firewood → sticks.
2. Seasoned firewood: knife + 2 firewood → prepared → `fseasonedfirewood:fseasonedfirewood` after 96 h → aged after 200 h.
3. Copper saw. Build two `immersivewoodworking:sawhorse` in the world, side by side (stick, stick, rope each).
4. Saw from the end for planks or support beams (tool mode); debark from the side for `immersivewoodworking:bark-tan-green`.
5. Smith `immersivewoodworking:pitsaw-{metal}`, `barkspud-{metal}`, `maul-{metal}`.
6. Bark: dry it, crush it in the quern (`barkcrushed`) for tannin; birch bark in a `perforatedpot` over a clay pot, sealed and fired in a pit kiln, gives tar (a resin substitute); bast rope; medicinal brew.
7. Powered `sawmill-frame-north` (carriage, sash, crankshaft, levers, `sawmillblade-{metal}`) and `chopper-frame-north`.

### 2.3 Fire and smoke

1. `game:firestarter` from two diagonal sticks.
2. Build the firepit in stages: 1 straw (`artofgrowing:firepit-construct1` to `construct4`) or 1 dry grass (vanilla `game:firepit`), then 4 firewood.
3. Place separate tinder, sneak, stay still and alternate clicks until it glows; carry it to the pit.
4. Conditions: above 10 °C and no rain or wind for the plain firestarter; bow drill and torch from 5 °C; quartz or spyglass lens around midday under clear sky; flint and steel in any weather.
5. Ventilate: Real Smoke fills rooms. A chimney is a column of non-solid blocks capped with a chimney block.

### 2.4 Ore and metal

1. Find ore (Juicy Ores makes veins visible; ProspectTogether shares readings).
2. Smash chunks lying on the ground: with a loose stone in hand before the first metal hammer (read from the mod code, not tested), then with any metal hammer, on the anvil or under a helve hammer. The knapped OneRoof hammer probably does **not** work: it is not the vanilla hammer class the mod hooks.
3. Charcoal, crucible, molds, cast head, assemble as in 2.1.
4. Anvil; Toolsmith cold-works copper.
5. Bronze alloys, pewter (`game:ingot-pewter`: tin 80–95 %, lead 5–10 %, copper 1–5 %).
6. Iron: bloomery, bloom refining, iron anvil, quenching (vanilla 1.22).
7. Steel: cementation furnace, coke.

### 2.5 Fields (Art of Growing, Natural Fertilizer)

1. Grass has two standing forms. Yellow `artofgrowing:talldrygrass-*` (old or snow-covered grass, and small wild patches) cuts straight to `game:drygrass`. Green grass cuts to a mown layer of fresh grass (`artofgrowing:grass`), which dries in about a day where it lies or in a pile, or at once in a firepit slot. A knife mows one block, a scythe an area; a hayfork gathers many layers. A dried layer left lying regrows after about 8 days.
2. Grain: wild or planted, a ripe plant gives `artofgrowing:grainbundle-{type}-wet`. Shift-place the bundles on the ground to dry (in a bag they rot to straw first), then thresh with a stick or `artofgrowing:flail`: one bundle gives one `game:seeds-{type}` and one `game:thatch`. The seed is what you sow.
3. Knife + seeds → `game:grain-{type}` for eating and milling. One way only, so keep seed back.
4. Vegetables: harvest at the mature stage for food; yield falls afterwards, and the final withered stage gives about 3 seeds and no food. A carrot, onion, turnip or parsnip planted back as a seedling grows about 2 seeds. Cabbage has no seedling. Wild plants give food or seed depending on their stage. Soil rules are vanilla: moisture from nearby water, fertility by soil grade, three nutrients.
5. Pumpkins: place and cut with a knife or cleaver.
6. Bales: stack dry grass or straw and press with rope (`game:hay-normal-ud`, `artofgrowing:thatchhay-normal-ud`).
7. Fertilizer: shovel dung into `naturalfertilizer:manure`; pile with grass → `weakfertilizer`; barrel slurry + dry grass, sealed 240 h → `maturefertilizer`.

### 2.6 Flax and textiles (Art of Growing, Tailor's Delight, Wool, Dressmakers)

1. `artofgrowing:flaxbundle-dry` → soak in water (`-wet`) → clean in a barrel (`-clear`) → crumple (`-soft`) → work with a ridge in the offhand (`artofgrowing:ridge-rough`) → flax fibers.
2. `tailorsdelight:spindle-wood` spins twine more efficiently (clothier trait).
3. `tailorsdelight:awl-{flint|bone|metal}` and `tailorsdelight:needle-bone`; buttons of clay, horn or metal.
4. Sewing kit, sack, backpack and saddle use the Tailor's Delight recipes.
5. Wool: shear a generation 1+ animal → `wool:fleece-*` → lime water barrel 18 h → `wool:fibers-*` → `wool:twine-wool-*` → cloth; knit with `wool:kneedle-{wood|bone}`.
6. Mordant and dye; Dressmakers clothing sets (many class-locked).

### 2.7 Leather

1. Hide from the butcher table.
2. Soak: lime water 20 h, or borax 18 h, or Expanded Matter lye and soda routes.
3. Scrape with a knife.
4. Tannin **only from bark**: sawhorse debarking (or Culinary Artillery oak bark) → weak tannin 72 h → strong tannin 108 h.
5. Leather → Tailor's Delight strips and bundles, darker and coloured leather.

### 2.8 Hunting and butchery (Butchering, Rustic Cookery)

1. Kill, ideally with a thrown stone javelin (`armory:javelin-plain-*`: flint head over a stick).
2. Pick up the carcass (a bag slot; the butchery bag is optional and moves carcasses to the inventory).
3. Hang on `butchering:butcherhook-flint-north` (knapped `butchering:hook-flint`), skin with a knife, let it bleed into a bucket 2 to 4 blocks below (`butchering:bloodportion`); a saucepan probably works too.
4. Move to `butchering:butchertable-{primitive|simple|advanced}-north` and butcher: prime meat, offal, sinew, fur, bone, marrow.
5. Large animals give `rusticcookery:meatslab-{redmeat|bushmeat}-raw`; slice with a knife or cleaver.
6. Smoke on `rusticcookery:smokerack-east` with `smokehook` (needs real smoke), or on the metal `butchering:smokingrack-{metal}-north`.
7. Barrel work: clean offal, blood sausage, hide and sinew glue.

### 2.9 Livestock (Livestock Welfare, betterhusbandry, genelib, Catch Livestock)

1. Pen with a roof within reach, a water source or `livestockwelfare:waterer-fired`, and feed.
2. Daily care (feed, pet, milk) raises trust and generation gain.
3. Breeding needs `livestockwelfare:strawbedding-clean` under a roof and low stress; replace soiled bedding after a birth.
4. Shovel muck, groom with dry grass or `livestockwelfare:groomingbrush`.
5. Generation 1+ animals can be picked up and sheared.
6. Coop kit `livestockwelfare:chickencoop-{wood}`, nest boxes `genelib:nestbox`.
7. Animals age; plan replacements.

### 2.10 Horses (Equus, Jaunt)

1. Find wild horses (`equusferus:wildhorse-*`).
2. Saddle `equusferus:saddle-*` and bridle; mount repeatedly to use up saddle breaks (about 15).
3. Call flute `jaunt:instrument-flute`.
4. Destriers: buy `equusdestrier:voucher-destrier` from a Stablemaster; breed; craft barding from plates, chains and `schematics-destrier`.

### 2.11 Kitchen (Culinary Artillery, Expanded Foods, Rustic Cookery, DairyPlus)

1. Stick roast → pot meals → wash dishes.
2. `aculinaryartillery:saucepan-{colour}-fired`: simmer broth, lard, syrup.
3. `aculinaryartillery:mixingbowl-*` and `rollingpin-*`: knead sausage, pemmican, hardtack, pasta, dumplings.
4. Crack eggs into a container for liquid egg.
5. Roasting dish and tongs: braise, pot roast (finish in the oven).
6. Manual dough → clay oven → stone bake oven.
7. Meat rack with large hooks: dry-aged meat.
8. Spile: maple or birch sap → syrup; pine resin.
9. Dairy: settle milk 24 h → cream scoop → churn butter → cheese kettle → curds, mozzarella, feta.
10. Cauldrons; salt crystals from brine.
11. Bottles, corks and sealing wax; aged wines and spirits; SoulStorm brew.
12. Powered mixing bowl.

### 2.12 Bees (From Golden Combs)

1. Vanilla skep and flowers (at least 3 near each hive).
2. `fromgoldencombs:ceramicbroodpot-*` + `hivetop-*`, populated from a skep; harvest the honey pot with a knife.
3. Langstroth: waxed boards and linen, `frameliner`, `beeframe`, `framerack`, `langstrothsuper`, `langstrothbase`.
4. Pollination bonus 10 / 20 / 30 % for skep / ceramic / Langstroth.

### 2.13 Materials and ceramics (Expanded Matter, Bricklayers)

1. Pulverizer → `em:crushed-*`; quern → `em:powdered-*`.
2. Coloured clay pottery, mud bricks, tiles.
3. `bricklayers:glazingbase-clay` → `-clear`; frit mix → baked → ground; seal 48 h → `bricklayers:glazing-*` → glazed bowl.
4. Porcelain (bone ash + ground granite).
5. Coloured glass batches in a bloomery.

### 2.14 Combat (Combat Overhaul, Armory, Quivers and Sheaths)

1. Learn directional attacks, parry and block; melee stops on terrain.
2. `armory:handle-{short|medium|long}` + head for each weapon.
3. Armour by tier: wood lamellar and hide jerkin → copper lamellar → bronze chain or brigandine → iron plate → steel plate. Armourer kits `combatoverhaul:sewingkit-armor-*`.
4. Buckle `quiversandsheaths:part-buckle-*` → belt → quiver, sheath, holster.
5. Bandages and a recovery kit; nobody can self-revive.

### 2.15 Travel and water

1. Walking stick, movement skills, trails with trowel and cairn.
2. Cartography table and quill to share waypoints.
3. Spyglass.
4. Boats: reed boat → dugout → coracle and bark canoe → currach and outrigger → vanilla sailboat. Carry repair materials and a bailer; moor to a post.
5. Carts and sleds on land.

### 2.16 Trade and community

1. Vanilla traders take only rusty gears; nothing in the pack changes that. Player money is a separate system.
2. `coins:mint-east`: found a currency, mint notes, make change.
2. Vinconomy `shopregister-*` plus a stall.
3. Notice board; trader phone.
4. Coinage (struck metal coins) is installed but left out of the questbook.

## 3. Stuck points

Where the pack differs from vanilla in a way that blocks a player who follows vanilla habits. Each should map to at least one quest ([chapter-plan.md](chapter-plan.md) carries the mapping).

| # | Stuck point | Cause | Chapter |
|---|---|---|---|
| S1 | Tools can't be assembled in the crafting grid. | Toolsmith config | First Days |
| S2 | Tools go blunt and wear in four separate ways. | Toolsmith | First Days, Toolsmithing |
| S3 | No grid firewood; use the chopping block. | Immersive Woodworking config | First Days |
| S4 | No grid planks or beams; sawhorses must be built in the world, side by side. | Immersive Woodworking config | Woodworking |
| S5 | No grid debarking and no tannin from logs; leather depends on bark. | Immersive Woodworking config | Leatherwork |
| S6 | Lighting a fire is a minigame with carried tinder. | Manual Firestarter | First Days |
| S7 | Fire won't start in cold, rain or wind; torches die in wind and in the backpack. | Firestarters | First Days, Survival |
| S8 | The firepit is built in stages. | Art of Growing | First Days |
| S9 | Smoke fills enclosed rooms and can kill. | Real Smoke | First Days, Building |
| S10 | Felled trees fall and hurt. | Falling Tree | First Days |
| S11 | No grid nuggets; ore must be smashed, with a stone in hand until the first metal hammer exists. | Immersive Ore Crush config | Copper Age |
| S12 | Loose soil falls; walls and roofs of raw dirt collapse. | World setting (block gravity) | First Days, Rooms & Shelter |
| S13 | Green grass gives fresh grass that must dry; only yellow standing grass cuts straight to dry grass. | Art of Growing | First Days, Fields & Harvest |
| S14 | Grain comes as wet bundles that must dry and be threshed. | Art of Growing | Fields & Harvest |
| S15 | Seeds are not food; cut them into grain with a knife. | Art of Growing | Fields & Harvest |
| S16 | Vegetables give seed only from withered plants or replanted seedlings. | Art of Growing | Fields & Harvest |
| S17 | Pumpkins are cut in the world. | Art of Growing | Fields & Harvest |
| S18 | Flax needs soaking, cleaning, crumpling and ridging. | Art of Growing | Textiles & Tailoring |
| S19 | Field harvesting gives about half; use hook and table. Carcasses take bag slots (small animals fit anywhere). | Butchering | Butchery & Hunting |
| S20 | Meat comes as slabs to slice. | Rustic Cookery | Butchery & Hunting |
| S21 | Animals need water, a roof and cleanliness, and may need bedding to breed (the breeding module is off in config; verify); they age and die. | Livestock Welfare | Livestock |
| S22 | Only generation 1+ animals can be picked up or sheared. | Catch Livestock, Wool | Livestock |
| S23 | Scrambled eggs and many recipes need liquid egg. | Culinary Artillery, EF Meals | Cooking |
| S24 | Braising needs tongs in the offhand. | Rustic Cookery | Cooking |
| S25 | Unsealed alcohol turns to vinegar. | Expanded Foods | Brewing & Drink |
| S26 | Skim milk won't make cheddar. | DairyPlus | Dairy |
| S27 | Backpack, sewing kit, saddle and more need awl, needle and buttons. | Tailor's Delight | Textiles & Tailoring |
| S28 | Many textile recipes are locked to the clothier or other class traits. | Wool, Dressmakers, Butchering | Textiles & Tailoring |
| S29 | Vanilla armour recipes are gone; armour needs kits and Armory recipes. | Combat Overhaul config | Arms & Armor |
| S30 | Belts and quivers need a smithed buckle. | Quivers and Sheaths | Arms & Armor |
| S31 | No self-revive; a downed solo player dies. | Downed config | Survival |
| S32 | Climbing only works on stone and ore; ledge grabs need empty hands. | Climb Mountain, Catch Ledge | Overland Travel |
| S33 | Boats leak and need bailing; rivers don't carry them. | Rough Seas, Quiet Rough Seas | Waterways |
| S34 | New hives need a populated skep and don't swarm. | From Golden Combs | Orchards & Bees |
| S35 | Traders take only rusty gears; player money is separate, and shops accept only loose notes. | Coins, Vinconomy | Player Economy |
| S36 | Used bowls and pots need washing. | Manual Dishes | Cooking |

## 4. Cross-mod dependencies

- **Dry grass is a shared bottleneck.** Mowing (Art of Growing) feeds the firepit, straw bedding and grooming (Livestock Welfare), fertilizer (Natural Fertilizer), troughs and tool bindings (Toolsmith).
- **Support beams** from sawhorses feed carved tool handles, carts, sawmill frames and the notice board.
- **Bark** from sawhorses feeds tannin and therefore all leather: backpacks, belts, saddles, grips, armour.
- **Rope** gates sawhorses and bales, so early flax or reeds matter more than in vanilla.
- **A metal hammer** is needed by most hammer recipes in the pack. The knapped OneRoof hammer fits almost none of them (one cupboard recipe, perhaps offhand debarking), so it has no quest.
- **Butchering outputs** feed other mods: sinew and glue (Toolsmith bindings), blood (Manual Dough), slabs (Rustic Cookery), offal (Expanded Foods kneading).
- **Beeswax** feeds handle treatment, sealing wax, Langstroth boards, seasoned firewood and butter dishes.
- **Smoke** from Real Smoke drives Rustic Cookery smoke racks; the Art of Growing firepit needs its two compat patches for smoke and braising.
- **Generation 1+** gates both animal pickup and shearing.
- **Copper plate** gates the stone bake oven, cheese kettle and shop register.
- **Windmill power** gates practical powders, hence glazing, dyes and Expanded Matter chemistry.
- **Class traits** gate parts of Wool, Dressmakers, Tailor's Delight, Butchering and Combat Overhaul; on a group server these are natural party quests.

## 5. To verify in game

The files could not settle these. Check before writing the affected quests.

1. Whether a stone held in hand smashes ore chunks (the code suggests yes) and whether the OneRoof stone hammer does (probably not).
2. Whether the pit saw, maul, bark spud, hayfork, awl and OneRoof hammer need in-hand assembly under Toolsmith.
3. That a stone knife mows grass into a layer, and that yellow standing grass cuts straight to dry grass.
4. Whether fire can be started without sky access using the hand drill (the handbook and the mod text disagree).
5. Exact behaviour of Manual Dishes, Manual Harvesting and Manual Dough.
6. What From Golden Combs' `enabledInRoomOnly: true` does.
7. Which item is the "gear necklace" that reveals stability mist.
8. Vanilla 1.22 tier for tongs and shears, and whether quartz glass or bloomery glass comes first for the spyglass.
9. Whether Toolsmith in-hand assembly reports as a `craft` event through `compat/toolsmith`, or whether quests should use `obtain` on the finished tool.
10. Whether the Culinary Artillery saucepan output counts for the `cook` task (firepit output slot) or needs `obtain`.
11. Whether Livestock Welfare still requires straw bedding for breeding with its breeding module off.
12. Whether a saucepan under the skinning hook collects blood.
13. Which salt crystal code is live (`efchefstricks:` or `expandedfoods:`).
14. Worldgen structure codes for traders and the destrier tradepost, for `visit` tasks (`/questline structures`).
