# Phase 1 findings

Historical findings from the rendering spike and investigation of the design doc's open
questions, followed by later-phase results. Source paths are relative to the workspace root.
Sources were checked against the 1.22.0 trees; runtime measurements used game 1.22.6.

## Rendering spike: both gates passed

`tests/BookSpikeTests.cs`, client tier on vsclient.home (GTX 1060):

| Gate | Recorded result |
|---|---|
| 500-node tree pans and zooms smoothly | 15 s tour across the whole tree, zoom 0.2–2.3: frame 16.3 ms avg, 16.7 ms p95 (vsync-bound, 60 fps). Canvas alone: 1.3 ms avg, 4.4 ms p95, 9.8 ms max over 921 frames |
| A handbook page renders inside the book without patches | The copper anvil's vanilla page (61 rich-text components, recipe slideshows and links) composed in the book's Reference tab; item links navigated inside the book and Back returned |

`questline/Client/GuiElementQuestCanvas.cs` drew edges and node frames as two meshes in canvas
units with the engine's GUI shader. Pan and zoom changed only the model-view matrix.
Per-node drawing covered only visible item icons (`RenderItemstackToGui`) and labels.
Labels used cached text textures, generated at most 8 per frame.

First-zoom label generation caused the worst canvas frames. Long dummy item-name titles
overlapped at zoom 1; real quest titles needed a width limit or show-on-hover.

## Hosting the handbook (Reference tab)

Item pages needed no Harmony patches:

- Call the public `new GuiHandbookItemStackPage(capi, stack).ComposePage(composer, bounds, allStacks, openDetailPageFor)`.
  Retrieve `allStacks` with `ObjectCacheUtil.TryGet<ItemStack[]>(capi, "handbookallstacks")`;
  the handbook sets it at `LevelFinalize` (`VSSurvivalMod/Systems/Handbook/SurvivalHandbook.cs:74`).
- Route item-icon clicks through `openDetailPageFor` to keep navigation inside the book.
- Construct pages as needed: construction is cheap; `GetHandbookInfo` scans recipes per page at compose time.
- Re-parse guide-page `GuiHandbookTextPage.Text` with `VtmlUtil.Richtextify`. Do not reuse cached
  components: disposing a rich-text element disposes them.
- Subscribe to `ModSystemSurvivalHandbook.OnInitCustomPages` for the handbook's full page list,
  including guides.
- Reroute H with `capi.Input.SetHotKeyHandler("handbook", ...)`; its hotkey is `"handbook"`.
  Replace `capi.LinkProtocols["handbook"]` to reroute `handbook://` links.

**Build the recipe graph separately.** "Created by" and "used in" existed only as rich-text
components; no per-item recipe structure was retained (`CollectibleBehaviorHandbookTextAndExtraInfo`,
its `add*Info` methods). The underlying public lookups (`World.GridRecipes`,
`FastSearchRecipesByIngredient`, `GetSmithingRecipes()` etc.) supported a separate scan of the
same sources. This brought planner and validator work forward from phase 4.

## Crafting hooks (phase 2's cost)

Three engine event-bus events needed no Harmony:
`"onitemcrafted"`, `"onitemknapped"`, `"onitemclayformed"`. Each carried a tree with `itemstack`
and `byentityid`. Subscribe through `sapi.Event.RegisterEventBusListener`, as vanilla's tutorial
system did (`VSSurvivalMod/Systems/Handbook/Tutorial/ModSystemTutorial.cs:81`).

| Station | Hook | Gap |
|---|---|---|
| Grid crafting | `onitemcrafted` | Shift-click reports only the last batch's quantity |
| Knapping | `onitemknapped` | Not fired when the output is a placed block |
| Clay forming | `onitemclayformed` | Not fired for ground-storable outputs — most pottery |
| Anvil | Harmony: `BlockEntityAnvil.CheckIfFinished` | Prefix saves the recipe (cleared on finish); player is null for helve hammers |
| Firepit, cooking pot | Harmony: `ItemSlot.TryPutInto` filtered to the output slots | Credit on take, via `op.ActingPlayer` |
| Tool / ingot molds | Harmony: `TryTakeContents` / `TryTakeIngot` | Prefix saves the contents |
| Bloomery | Harmony: `BlockEntityBloomery.OnBlockBroken` | Its inventory is `internal` |
| Barrel | Harmony: remember the sealer from `OnReceivedClientPacket`, credit on unseal | No player at completion |

The design doc's "one patch per station" estimate held for anvil, molds, heat stations and
barrel. The three events covered the rest, except that each listed event gap also needed a
patch. `CollectibleObject.OnCreatedByCrafting` and `MatchesGridRecipe` fired on preview, not
on take, so neither could credit a player.

## Phase 2: station-patch findings

All stations were patched in `questline/Server/StationPatches.cs`; event-bus listeners were
removed. The grid patch counted every shift-click batch. Knapping and clay-forming patches
covered outputs omitted by their events.

Point-release internals differed: `InventoryCraftingGrid.ConsumeIngredients` returned the
consumed recipe in 1.22.7 but `void` in 1.22.6. A postfix reading `__result` failed to attach
on 1.22.6; under `PatchAll`, this took down the entire mod. The fix attached patches individually
and read the public `MatchingRecipe` field in a grid prefix instead.

Recorded gate result: two processes on vsclient.home, game 1.22.6. The dedicated server held
all 8 patched methods; the client process held none. A server-side smithing finish reached
the client's book as progress.

## Phase 4: recipe graph and handbook

**Build from registries and item properties.** In 1.22, `RecipeBase.RecipeIngredients` and
`RecipeOutput` provided a common registry shape; `IRecipeIngredientBase.SatisfiesAsIngredient`
handled wildcards and tags. This covered grid, smithing, knapping, clay forming and barrel
recipes. Cooking pot recipes and alloys used separate classes.

Other handbook "Created by" entries came from collectible properties. The graph walked every
collectible, following `CollectibleBehaviorHandbookTextAndExtraInfo.addCreatedByInfo`: combustible
(smelt, cook, bake, fire), grinding, crushing, ore → nugget, transitions, juiceable, squeezable,
distillation, carburizing, beehive kiln, ground-stored processing, block drops, creature drops
and the harvestable behaviour's butchering drops. Vanilla 1.22.6 produced 20,622 edges in 366 ms.

Still absent at this phase: panning, charcoal pits, bloomery blooms (the graph had ore → ingot
by heat, not ore → bloom → ingot), quern and pulveriser chains beyond item properties, trader
stock, and world-generation-only sources. Client and server graphs matched for every recipe
kind; drops were not compared.

**Host guide pages by their page type.** Guides came from `config/handbook` assets and the list
supplied by `ModSystemSurvivalHandbook.OnInitCustomPages`. Plain `GuiHandbookTextPage` content
was re-read from `Text`. Subclasses (tutorial pages, meal recipe pages, mods') composed themselves
under "richtext", like item pages, and were hosted the same way. Extra content was prepended
to that rich text's components before composing.

The takeover replaced H keys (`handbook`, `selectionhandbook`) and link protocols
`handbook`/`handbooksearch` at `LevelFinalize`, after the handbook registered them.
`HotKey.Handler` and `capi.LinkProtocols` exposed the originals, allowing takeover to be disabled
without a restart.

## Phase 5: planner, checks and default questline

**Fix graph gaps exposed by content validation.** The validator's first real-content run found
meal outputs that matched no item and casting inputs restricted to ingots. The latter made a
quest for an ingot appear out of order after a quest casting copper. The fixes made cooking-pot
recipes produce the cooked pot and casting accept anything that melts into the metal. Both
faults were in the graph, not the questline. Loot vessels (via `Block.GetDropsForHandbook`) and
trader stock were included so loot-only items were not flagged as unobtainable.

**Prefer recipes over loot.** The first planner chose "find it" over recipes with missing
inputs. Since vessels could contain flint axes, it told players to find an axe. The revised
planner used a recipe whenever available and ranked loot vessels last among places to look.

**Use a worklist for obtainability.** Re-scanning every unfinished edge on each pass, including
wildcard matching, failed to finish in ten minutes on 21,000 edges. A code-keyed worklist that
matched each wildcard once took well under a second.

**Scale labels with zoom.** Fixed-size labels overlapped in a real chapter fitted below zoom 1.
Scaling labels kept them within the gaps. Opening zoom was capped at a minimum of 0.75, where
scaled text remained readable.

## All of vanilla

**Use guides as the coverage map.** Assigning vanilla's 32 handbook guides (`config/handbook`)
to chapters, then testing that each was linked from a quest, made "all of vanilla" checkable:
24 chapters, 322 quests.

**Add missing acquisition paths.** Water was reachable only through slush in a barrel, making
water-dependent barrel recipes appear impossible. A `fill` edge for filling a bucket from a
water block fixed this. Charcoal pits, coke ovens, panning, milking and picking up worms gained
edges in the same way. Casting had offered iron and steel anvils; it was restricted to metals
no hotter than the hottest fuel burns.

**Add task types and liquid counting.** `mount` covered rafts, sailboats and elk; `trade` patched
the trader's sale. `obtain` counted carried-bucket liquids by the litre. Claims still took back
only whole stacks, never liquid.

**Keep unsupported credit explicit.** Taming progress, trap catches, chiseling, prospecting
readings, fertilizing and watering, quenching, kiln firing, welding an anvil, and the meal held
in a pot could not be credited. Each became a checkbox or text in a neighbouring quest.

## Addons for other mods

**Support both extension and replacement.** A chapter file could `extend` a base chapter to put
mod quests beside the base quests they built on. An extension could also replace a base quest
with the same id when a mod changed the mechanic being taught. Expanded Foods made a firepit
char meat, breaking "Roast some meat" as written. Across the pack, Expanded Foods broke two
base quests outright; Tailor's Delight changed recipes behind twelve more without breaking
them. Reading the mods' patches was what exposed these changes.

**Run base checks with mods loaded before writing addons.** The modded snapshot exposed broken
base quests before any addon quest was written.

**Account for graph-invisible machines.** Mods' own machines were invisible to the graph, so
their outputs appeared as "nothing makes this". Authors had converted real tasks to checkboxes
to bypass this; `"unchecked": true` restored those tasks. Teaching the graph builder each mod's
recipe type remained the better solution, mod by mod.
