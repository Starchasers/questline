# Pszczoly questbook: mod inventory

Every mod in `modpack/evpack.json` (Pszczoly 1.4.1, game 1.22.7, 148 mods), classified by how much questbook content it deserves. Companion documents: [progression.md](progression.md) (how the pack progresses) and [chapter-plan.md](chapter-plan.md) (book structure and quest candidates).

Source: the mod zips (modinfo, lang, recipes, handbook pages) and `modpack/config/ModConfig`. Nothing here was tested in game; mods marked *DLL only* were read from strings in the binary and are best guesses.

**Tier** is the earliest vanilla tech tier at which the mod's content becomes reachable: stone, clay, copper, bronze, iron, steel. **Chapter** names refer to [chapter-plan.md](chapter-plan.md).

## 1. Progression mods

These have a chain of their own and drive whole chapters or large parts of one.

| Mod ID | Name, version | What it adds | Tier | Chapter | Handbook page |
|---|---|---|---|---|---|
| `toolsmith` | Toolsmith 1.2.19 | Multi-part tools (head, handle, binding, grip, treatment), sharpness, whetstones, grindstone, workbench, reforging. Grid tool assembly is **off** in this pack. | stone | First Days, Toolsmithing | `toolsmith-items*` (via Modpack Guide) |
| `immersivewoodworking` | ImmersiveWoodworking 1.3.13 | Chopping block, paired sawhorses, pit saw, bark spud, maul, bark and birch tar chain, powered sawmill and chopper. Vanilla firewood, plank, debark and log-tannin recipes are **off**. | stone | First Days, Woodworking, Leatherwork, Mechanical Power | mod handbook pages |
| `immersiveorecrush` | ImmersiveOreCrush 2.2.5 | Smash ore chunks lying on the ground with a stone in hand or a metal hammer, or on the anvil. Grid nugget recipe is **off**. | stone | Copper Age | – |
| `artofgrowingpatch` | Art of Growing 1.2.2 | Farming overhaul: green and dry grass, mowing and drying, grain bundles and threshing, seed crops for root vegetables, flax retting chain, staged firepit, bales, straw roofing. | stone | First Days, Fields & Harvest, Textiles & Tailoring | "Art of Growing" and "Crops" tabs |
| `butchering` | Butchering 1.14.3 | Carcasses, skinning hook, butcher table (three tiers), blood, offal, sinew, prime meat, smoking rack, glue. Field harvesting gives about half. | stone | Butchery & Hunting | `butcheringguide`, `butcheringinfo` |
| `livestockwelfare` | Livestock Welfare 0.16.0 | Thirst, shelter, hygiene, straw bedding for breeding, grooming, ageing, coop kit, waterer. | stone | Livestock | `livestockwelfare-guide` |
| `aculinaryartillery` | A Culinary Artillery 2.0.0-dev.29 | Kitchen tools: saucepan, mixing bowl, rolling pin, bottles and stoppers, spile, meat rack, cauldrons, powered mixing bowl. Egg cracking. | stone | Cooking, Preservation & Cellar, Brewing & Drink | `aculinaryartilleryguide`, `kneadingmixingguide`, `simmeringguide` |
| `expandedfoods` | Expanded Foods: Core 2.0.0-dev.17 | Broths, lard, oils, syrups, sausage, pemmican, hardtack, pasta, dumplings, aged meat, yogurt, soy and fish sauce, aged wines and spirits. | stone | Cooking, Baking, Preservation & Cellar, Brewing & Drink | `expandedfoodsguide`, `…2`, `…4`, `…5` |
| `efchefstricks` | Expanded Foods: Chef's Tricks 1.0.0-dev.6 | Non-food uses: crumb feed, oil and lard as lubricant, resin from spiles, salt crystals, eggshell lime. | clay | Preservation & Cellar, Livestock, Mechanical Power | `efchefstricksguide` |
| `efmealsmodule` | Expanded Foods: Meals 1.0.0-dev.9 | New pot meals and mixing-bowl meals (salad, cold pasta, yogurt meal). Scrambled eggs need liquid egg. | clay | Cooking | `expandedfoodsguide3` |
| `dairyplus` | DairyPlus 2.0.0 | Cream, butter, ghee, cheese kettle, curds, mozzarella, feta, tofu, soy milk. | clay | Dairy | `creamguide`, `butterguide`, `mozzaguide` |
| `rusticcookery` | Rustic Cookery 1.2.0 | Meat slabs, smoke rack and hooks, roasting dish, braising, pot roast, egg dishes. | stone | Butchery & Hunting, Cooking | mod handbook pages |
| `stonebakeoven` | Stone Bake Oven 1.4.0 | Multiblock stone oven (heat source, grills, baking and cooking tops). | copper | Baking | `stone-bake-oven-title` |
| `fromgoldencombs` | From Golden Combs 2.1.0 | Ceramic hive, Langstroth hive, frames, pollination bonus. | clay | Orchards & Bees | `fromgoldencombsguide`, `…pollination`, `…langstrothguide` |
| `wool` | Wool & More 1.9.6 | Shearing, fleece washing, wool twine and cloth, knitting, wool dyeing. | clay | Livestock, Textiles & Tailoring | `wool:gamemechanicinfo-woolknitting`, shearing page |
| `tailorsdelight` | Tailor's Delight 2.2.2 | Awls, needles, spindle, buttons, leather strips, coloured leather and cloth. Replaces vanilla backpack, sewing kit, saddle and armour recipes. | stone | Textiles & Tailoring, Leatherwork | mod handbook pages |
| `dressmakers` | Dressmakers 1.8.0 | Grid recipes for vanilla clothing sets, many class-locked. | copper | Textiles & Tailoring | – |
| `em` | Expanded Matter 3.8.3 | Crushed and powdered ores, stones and metals; ash, lye, alum, borax, gypsum; extra dye and hide routes; ore panning. | copper | Materials & Ceramics, Leatherwork | mod handbook pages |
| `bricklayers` | Bricklayers 3.3.4 | Coloured clay, porcelain, tiles, mud bricks, small stone bricks, frit and glazing, coloured glass, coloured shingles. | clay | Materials & Ceramics, Rooms & Shelter | `bricklayers:craftinginfo-coloredclay`, `-glazedceramics`, `-coloredglass` |
| `millwright` | Millwright 1.3.5 | Reinforced and vertical windmill rotors, sail types, brake, improved axle passthrough. | iron | Mechanical Power | – |
| `combatoverhaulfork` | Combat Overhaul 0.18.9 | Directional melee, parry and block, zone damage, bows and slings, armour recipes with armourer kits. Vanilla armour grid recipes are **off**. | stone | Arms & Armor | mod handbook pages |
| `armoryfork` | Combat Overhaul: Armory 1.11.4 | Weapon handles, weapon families per tier, light and heavy shields, lamellar to plate armour. | stone | Arms & Armor | – |
| `quiversfork` | Quivers And Sheaths 0.9.32 | Belts, buckles, quivers, sheaths, bandoliers, slings. | copper | Arms & Armor | – |
| `roughseas` | Rough Seas 5.0.1 | Reed boat, dugout, coracle, bark canoe, currach, outrigger; hull damage, bailing, mooring, surf. | stone | Waterways | `roughseas-goingtosea`, `-weather`, `-vessels`, `-surf`, `-mooring`, `-swimming` |
| `cartwrightscaravan` | Cartwrights Caravan 1.9.1 | Pulled carts, sled, wheelbarrow, market stall, canopies and inserts. | copper | Storage & Hauling | – |
| `coins` | Coins 0.1.0 | Mint, named currencies, banknotes, wallet. | stone | Player Economy | – |
| `vinconomy` | Vinconomy 6.0.3 | Shop register and stalls, buy orders, ledger, catalogue. | copper | Player Economy | mod handbook pages |
| `coinage` | Coinage 2.4.0 | Punch, planchets, trussell and anvil die, struck coins, coin press. | bronze | none (left out by decision) | – |
| `equusferus` | Equus: Wild Horses 2.0 1.0.6 | Wild horses with genetics, saddle-breaking, tack. | copper | Horses & Riding | – |
| `equusdestrier` | Equus: Medieval Horses 1.1.2 | Destriers bought from a Stablemaster, destrier tack and metal barding. | copper | Horses & Riding | – |
| `chiseltools` | chiseltools 1.17.9 | Hand planer, wedge, pantograph, path maker, door tool, ladder maker, paintbrush, chiselled furniture. | copper | Home & Decor | `chiseltools:chiseltools-guide` |
| `pewter` | Pewter 1.5.0 | Pewter alloy, tableware molds, bowls, crocks, jugs, candle lamps. | bronze | Bronze Age, Home & Decor | – |
| `foodshelves` | FoodShelves 3.1.1 | Food shelves, baskets, jars, barrel racks, cooling cabinet, ice keeper, meat freezer, cut ice. | stone | Preservation & Cellar | `foodshelvesguide` |
| `naturalfertilizer` | Natural Fertilizer 1.5.1 | Dung and manure, weak fertilizer piles, slurry and mature fertilizer. | stone | Fields & Harvest | – |

## 2. Mechanic mods

Few or no items, but they change how the game is played. Each gets one teaching quest, or a note inside another quest's text.

| Mod ID | Name, version | What it changes | Tier | Chapter | Handbook page |
|---|---|---|---|---|---|
| `manualfirestarter` | Manual Firestarter 0.1.3 | Firestarter from two diagonal sticks; ignition is a tinder minigame, and the hot tinder is carried to the target. | stone | First Days | First Steps tutorial |
| `firestarters` | FireStarters 1.4.6 | Weather, temperature and time-of-day gates on ignition; bow drill, lens, flint and steel; torches go out in wind and in the backpack. | stone | First Days, Survival & the Unknown | Firestarters environment guide |
| `realsmoke` | Real Smoke 1.3.1 | Smoke fills rooms, smothers fires and can suffocate; chimneys needed. | stone | First Days, Rooms & Shelter | `realsmokeguide` |
| `fallingtree` | Falling Tree 0.5.2 | Felled trees topple and deal impact damage. | stone | First Days | – |
| `coreofartspatch` | Core of Arts 1.2.2 | Library for the Arts mods; liquid mixing; vanilla meals accept more vegetables. | – | Cooking (note) | `artsguides-liquidmixing` |
| `manualdough` | Manual Dough 1.1.8 | Knead dough in hand from flour and water (or blood). *DLL only.* | stone | Baking | – |
| `manualdishes` | Manual Dishes 0.1.2 | Used bowls and pots need washing at water. *DLL only.* | clay | Cooking | – |
| `manualharvesting` | Manual Harvesting 0.1.0 | Pick fruit by hand from fruit-tree branches. *DLL only.* | stone | Orchards & Bees | – |
| `slowtox` | SlowTox 5.1.0 | Gradual intoxication with buffs at low levels and damage when overdone. | clay | Brewing & Drink | – |
| `betterhusbandry` | betterhusbandry 1.4.0 | Feed and interaction modifiers, trust scale, bloodline generation. | stone | Livestock | – |
| `genelib` | Genelib 3.2.1 | Genetics, animal profile, inbreeding, nest boxes and incubation. | stone | Livestock, Horses & Riding | – |
| `jaunt` | Jaunt 3.3.1 | Gaits, stamina, saddle breaks; call flute. | copper | Horses & Riding | – |
| `catchlivestock` | Catch Livestock 0.2.4 | Pick up tamed (generation 1+) animals with Ctrl + right-click. | stone | Livestock | – |
| `bloodtrail` | BloodTrail 1.2.13 | Wounded animals leave a trail. | stone | Butchery & Hunting | – |
| `immersivecorpsedrop` | Immersive Corpse Drop 1.0.4 | Harvested corpses drop items on the ground. | stone | Butchery & Hunting (note) | – |
| `downed` | Downed 2.9.4 | Downed state for 300 s; no self-revive; others can revive, drag or carry. | stone | Survival & the Unknown | – |
| `temporalsymphony` | Temporal Symphony 2.3.2 | Audiovisual storm warnings, reworked bell and rift weather. | stone | Survival & the Unknown | – |
| `mistsofstability` | Mists of Stability 0.2.1 | Coloured mist shows temporal stability; gated behind a gear necklace. | stone | Survival & the Unknown | – |
| `carryon` | Carry On 1.14.3 | Carry chests, barrels, anvils, querns and vessels; back slot. | stone | Storage & Hauling | – |
| `toolbelt` | ToolBelt 0.3.6 | Belts give 2 or 4 tool slots. | copper | Storage & Hauling | – |
| `handtohand` | Hand to Hand 1.0.7 | Hand an item to another player (receiver holds R). | stone | Player Economy | – |
| `crawlanddive` | Crawl&Dive 0.2.5 | Crawl through one-block gaps, dive, slide. | stone | Overland Travel | – |
| `catchledge` | Catch Ledge 0.7.1 | Grab and hang from ledges with empty hands. | stone | Overland Travel | – |
| `climbmountain` | Climb Mountain 0.2.4 | Climb stone and ore faces at a stamina cost. | stone | Overland Travel | – |
| `vaultandroll` | Vault And Roll 0.1.2 | Vault obstacles; timed roll halves fall damage. | stone | Overland Travel | – |
| `chargedjump` | ChargedJump 1.2.3 | Charged jump from a crouch; sprint jump is off. | stone | Overland Travel | – |
| `sprintmomentum` | Sprint Momentum 0.2.1 | Acceleration and inertia by surface. | stone | Overland Travel (note) | – |
| `trailmodmaro` | Natural Trail Mod 1.3.21 | Player-made trails that decay; trowel and cairn. | stone | Overland Travel | – |
| `rivers` | Rivers 5.0.3 | River networks with current (pushes swimmers, not boats). | – | Waterways | – |
| `watersheds` | Algernons Watersheds 7.0.6 | Streams and erosion; well pulley; streams drive water wheels. | copper | Waterways, Mechanical Power | – |
| `quietroughseas` | Kuboczoch: Quiet Rough Seas 1.7.0 | Rough Seas tuning: rivers don't push boats, stronger paddling. | – | Waterways (note) | – |
| `prospecttogether` | ProspectTogether 2.2.1 | Prospecting readings on the map, shared with the group. | copper | Bronze Age | – |
| `stoneharvesting` | Stone Harvesting 1.2.2 | Cut full rock blocks out of a face with hammer and chisel. | copper | Home & Decor | – |
| `sawchiseling` | Saw Chiseling 0.1.2 | Chisel wood with a saw. | copper | Home & Decor | – |
| `danatweaks` | Dana Tweaks 4.1.0 | Many small rules: rain collection, firepit heats oven, planks in pit kiln, extra clayforming batches, year-round pumpkin carving, auto-closing doors, drifters can't open doors. | – | notes in several chapters | – |
| `bettertraders` | BetterTraders 0.2.2 | More trader structure variants in worldgen. | – | Traders | – |
| `juicyores` | Juicy Ores 1.0.2 | Ore blocks show protruding nodules. | – | Copper Age (note) | – |
| `barkbeetle` | Bark Beetle 1.0.6 | Resin logs make a sound. | – | Woodworking (note) | – |
| `clickuptorches` | Click Up Torches 1.1.1 | Right-click picks up placed torches. | stone | First Days (note) | – |

## 3. Small content mods

One or two optional quests each, usually inside a broader chapter.

| Mod ID | Name, version | What it adds | Tier | Chapter | Handbook page |
|---|---|---|---|---|---|
| `stickroast` | Stick Roast 0.1.0 | Roast meat or fish on a stick over a fire. | stone | First Days | – |
| `tseasonedfirewood` | SeasonedFirewood 1.2.12 | Prepared, seasoned and aged firewood with longer burn. | stone | Woodworking | – |
| `simpletea` | Simple Tea 1.2.0 | Four kinds of tea brewed in a pot. | clay | Brewing & Drink | `simpleteaguide` |
| `tankardsandgoblets` | Tankards, Goblets and More! 1.4.4 | Tankards, goblets, wine bottles, demijohns. | stone | Brewing & Drink | – |
| `pagoldsilver` | Pewter Additions: Gold and Silver 1.1.0 | Gold and silver tableware. | bronze | Home & Decor | – |
| `oneroof` | One Roof Mod 1.12.0 | Roof blocks from shingles, thatch, slate, metal; also a knapped stone hammer that fits almost no recipe in the pack. | stone | Rooms & Shelter | – |
| `scaffolding` | Scaffolding 1.3.1 | Climbable scaffolding. | copper | Rooms & Shelter | – |
| `morepathsandstairs` | MorePathsAndStairs 2.0.0 | Dirt paths, stone and ashlar roads, steps and stairs. | stone | Home & Decor | – |
| `terrainslabs` | Terrain Slabs 1.0.17 | Slabs of soil, rock, sand, gravel and more. | stone | Home & Decor | – |
| `kevinsfurniture` | kevinsfurniture 1.9.0 | Furniture, leaded windows, wardrobe, four-burner stove, thermometer. | copper | Home & Decor | – |
| `heraldry` | Heraldry 2.0.0 | Heraldry workbench; customise items with dye. | copper | Home & Decor | – |
| `heraldrybanners` | Heraldry: Banners 2.0.0 | Custom banners. | copper | Home & Decor | – |
| `capes` | Heraldry: Capes 2.0.0 | Custom capes. | copper | Home & Decor | – |
| `windowdisplay` | Window Display 1.1.4 | Custom windows with display shelves. | copper | Home & Decor | – |
| `windchimes` | Wind Chimes 1.5.4 | Wood, metal and crystal chimes. | stone | Home & Decor | – |
| `tabletopgames` | Tabletop Games 4.0.1 | Boards, chess, checkers, shogi, go, dice, cards. | stone | Player Economy | starter and custom-piece pages |
| `noticeboard` | Notice Board 3.0.4 | Notice board with map-pinned notices. | copper | Player Economy | – |
| `remotetradercheckmod` | Trader Phone 0.8.0 | Check a trader's stock remotely; needs a temporal gear. | bronze | Traders | – |
| `kscartographytable` | K's Cartography Table 2.0.4 | Cartography table and quill; share waypoints and explored map. | copper | Overland Travel | `sharingwaypointsguide` |
| `spyglass` | Spyglass 0.6.1 | Spyglass (also works as a fire lens). | copper | Overland Travel | – |
| `walkingstick` | Adventurer's Walking Stick 3.0.12 | Walking sticks from crude to specialised variants. | stone | Overland Travel | – |
| `purposefulstorage` | PurposefulStorage 2.3.1 | Resource bin, wardrobes, weapon, firewood, rope and pelt racks, apothecary cabinet. | copper | Storage & Hauling | – |
| `containersbundle` | Containers Bundle 1.4.1 | Baskets, boxes, crates, food cupboard, metal cabinet, strongbox. | stone | Storage & Hauling, Preservation & Cellar | – |
| `morepiles` | More Piles 3.0.1 | Ground piles for more item types. | stone | Storage & Hauling (note) | – |
| `sortablestorage` | Sortable Storage 3.0.0 | Sort button on containers. | – | Storage & Hauling (note) | – |
| `shelfobsessed` | Shelf Obsessed 2.2.1 | More items fit on shelves. | – | Storage & Hauling (note) | – |
| `immersivelanterns` | Immersive Lanterns 0.4.1 | Lanterns and chimes sway. | – | Home & Decor (note) | – |

## 4. No quest content

Libraries, compatibility patches, interface, audio and visual mods. Listed so the inventory is complete; none needs a quest. Guide mods are sources for wording and handbook links.

| Mod ID | Name, version | Role |
|---|---|---|
| `kuboczochmodpackguide` | Kuboczoch Modpack Guide 1.4.0 | Pack handbook: 7 category directories and process guides. Main link target for quest text. |
| `kuboczochhandbookrefresh` | Kuboczoch Handbook Refresh 1.0.0 | Rewrites 27 handbook pages, including the Progression and Starter Survival guides. |
| `kuboczochwoodworkingtutorial` | Kuboczoch Woodworking Tutorial 1.3.0 | First Steps stages for the chopping block and firewood. |
| `manualfirestartertutorial` | Manual Firestarter Tutorial Patch 1.2.1 | First Steps stages for the tinder minigame. |
| `kuboczochtutorialskip` | Kuboczoch Tutorial Skip 1.0.1 | Skip button for the vanilla tutorial. |
| `kuboczochfoodhandbook` | Kuboczoch Food Handbook 0.3.1 | Groups food recipes by method in the handbook. |
| `kuboczochvisualmining` | Kuboczoch Visual Mining 1.0.4 | Mining animations and effects only. |
| `kuboczochaogcookerycompat` | Kuboczoch AoG Cookery Compatibility 1.0.0 | Rustic Cookery braising on the Art of Growing firepit. |
| `realsmokeartofgrowingfirepit` | Real Smoke & Art of Growing firepit patch 2.0.0 | Real Smoke emitter on the Art of Growing firepit. |
| `cartcarryonpatch` | Cartwrights Caravan and CarryOn Patch 1.0.1 | Carried containers ride in cart slots. |
| `windowdisplaypatches` | Window Display Patches 1.0.9 | Compatibility patches. |
| `placeonslabs` | Place on slabs 1.2.0 | Place items on slabs. |
| `cbr` | Chiseled Block Retention 2.0.1 | Chiselled blocks stay solid. |
| `immersivelight` | Immersive Light 0.2.7 | Light stops at walls. |
| `immersivefoliage` | Immersive Foliage 0.1.1 | Foliage bends and rustles. |
| `terraprety` | Terra Prety 7.11.1 | Landform and tree redesign. |
| `farseer` | Farseer 1.4.0 | Distant terrain rendering. |
| `cavesymphony` | Cave Symphony 1.2.2 | Cave ambience and events. |
| `footprints` | Footprints 1.2.16 | Cosmetic. |
| `footsteps` | Footsteps 1.0.3 | Cosmetic. |
| `stickstepsounds` | Stick Step Sounds 1.0.0 | Cosmetic. |
| `sungaze` | Sun Gaze 0.1.1 | Cosmetic. |
| `emotes` | Emotes 2.10.1 | Emotes. |
| `shearlib` | ShearLib 1.3.0 | Library (Wool). |
| `commercially` | Commercially 0.1.1 | Library (Vinconomy). |
| `commonlib` | CommonLib 2.8.0 | Library. |
| `configlib` | Config lib 1.13.2 | Library. |
| `jsonpatcheslib` | JSON Patches lib 1.5.9 | Library. |
| `vsimgui` | Dear ImGui 1.2.7 | Library. |
| `overhaullib` | Overhaul lib 2.0.10 | Library (Combat Overhaul). |
| `overhaulliblegacycompat` | Overhaul lib legacy compat 1.2.15 | Library (Combat Overhaul). |
| `playermodellib` | Player Model Library 1.25.0 | Library. |
| `attributerenderinglibrary` | Attribute Rendering Library 3.2.0 | Library (Heraldry, Notice Board, Tabletop). |
| `universaldisplaylib` | Universal Display Lib 1.5.0 | Library (Window Display). |
| `infinitumcore` | [Infinitum] Core 1.2.0 | Library. |
| `infinitumpickuphud` | [Infinitum] Pickup HUD 1.5.0 | Interface. |
| `infinitumprospectinghud` | [Infinitum] Prospecting HUD 1.1.0 | Interface: prospecting history. |
| `itempickupnotifier` | Item Pickup Notifier 2.3.0 | Interface. |
| `statushudcont` | Status HUD 4.4.0 | Interface. |
| `playerlistrevived` | PlayerListRevived 2.3.8 | Interface. |
| `extrainfo` | Extra Info 2.2.1 | Interface: block and handbook info. |
| `radialcrafting` | Radial Crafting 0.2.7 | Interface: radial crafting menu. |
| `egocaribautomapmarkers` | Auto Map Markers 5.0.3 | Interface: automatic map markers. |
| `handbookoptimizer` | Handbook Optimizer 0.19.2 | Performance. |
| `astroshandbookloadingfix` | Astro's Handbook Loading Fix 1.0.1-pre.1 | Fix. |
| `yangcoifix` | Clientside Drinkable Interaction Ordering Patch 5.0.0 | Fix. |
| `scrollbarcreativeinventorytabs` | Scrollable Creative Inventory Tabs 2.0.5 | Creative-mode interface. |
| `configureeverything` | Configure Everything 3.0.0 | Every module is disabled; no effect. |

## Notes

- **Stale configs.** `ModConfig` holds files for mods that are not installed (ImmersiveMining, SmithingPlus, ManualShingle, ManualToolCrafting, ManualScraping, HydrateOrDiedrate, VSRoofing, betterruins and others). Do not write quests from them.
- **Guide inaccuracies.** The author guide mods mention Manual Shingle and Manual Quenching (neither installed), say drifters open doors (Dana Tweaks disables it), and the Toolsmith handbook says grid assembly still works (it is off). Quest text should follow the installed mods and configs, not those pages.
- **Upstream Questline packages for mods not in this pack:** `betterruins`, `hexsmech`, `seafarer`, `charcoalkiln`. Their chapters are dropped.
