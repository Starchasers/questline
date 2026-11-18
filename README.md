# Questline framework fork

A modular quest framework for Vintage Story, derived from dizzyd/questline v0.14.0 under the MIT license. The framework retains the `questline` identity for quest/save compatibility. **Never install this fork alongside upstream Questline.**

## Fork layout and verification

- **Framework:** `questline/`, version 0.15.0. Ships no quest chapters.
- **Questbooks:** 13 independent content packages: `content/vanilla/`, eleven original optional integrations, and `content/artofgrowing/`. Install only the integrations you use.
- **Executable adapters:** `compat/toolsmith/`, optional and separate from quest content.
- **Rewards:** original material payouts become Quest Cookies; stage grants and claiming remain supported.
- **Translations:** original shared text still lives in the framework. Independent localization ownership for the original packages is not implemented; new Art of Growing prose belongs to the addon's `questlineartofgrowing` domain.

Native game/client/server acceptance is pending. Compilation, offline checks and synthetic Harmony tests do not prove in-world compatibility. Intermediate archives are **not validated releases**.

The optional [Art of Growing integration](docs/artofgrowing.md) uses the actual
provider mod ID **`artofgrowingpatch`**, not its `artofgrowing` asset domain.
**The supplied `srMi9` upload returns 404: the inspected AoG 1.2.2 + Core 1.2.2
cache cannot be asserted to equal the current pack.** The [532-record impact
matrix](docs/artofgrowing-impact-audit.md), [crop-process evidence](docs/artofgrowing-crop-research.md)
and [graph/verification contract](docs/artofgrowing.md) document the evidence and
limits. Native gameplay has not been run.

## Developer guides

Start with [CONTRIBUTING.md](CONTRIBUTING.md). AI assistants must also read [AGENTS.md](AGENTS.md) and the [AI workflow](docs/ai-workflow.md).

| Task | Guide |
| --- | --- |
| Check approved scope and compatibility boundaries | [Fork contract](docs/fork-contract.md) |
| Select packages and dependencies; preserve content identity | [Content packages](docs/content-packages.md) |
| Build deterministic archives | [Build and packaging](docs/build-packaging.md) |
| Understand CI and release gates | [CI](docs/ci.md) |
| Author addons and resolve extension conflicts | [Framework composition](docs/framework-composition.md) |
| Change payouts safely | [Cookie reward policy](docs/quest-cookie-rewards.md) |
| Install a test build and run smoke checks | [Local testing](docs/local-testing.md) |
| Stage native tests and screenshots | [Native testing](docs/native-testing.md) |
| Review recorded implementation evidence | [Packaging verification](docs/packaging-verification.md), [phase findings](docs/phase1-findings.md), [edible reward research](docs/edible-reward-options.md) |

## Status

The features below are inherited capabilities, not proof of native acceptance for this fork. The upstream roadmap covered every phase except the VS Quest importer. The fork separates that content from the framework; use the guides above for current packaging and release gates.

### Content and progression

- Load chapters from any mod's `assets/<domain>/questline/chapters/`; merge and validate them at load. Disable and report a broken quest, not its whole chapter.
- Express `requires` as a tree of `all`, `any`, `atLeast`, quest IDs and mod gates. In `ModConfig/questline.json`, `Locking` defaults to `"open"`: prerequisites suggest an order but every quest can start immediately. `"strict"` locks quests until their required quests are done. Both modes still enforce mod, stage and discovery gates.
- With the vanilla questbook installed, get 322 quests in 25 chapters: knapping through steel, mechanical power, kilns, farming, husbandry, beekeeping, cheese, brewing, textiles, leather, boats, riding, arms and armor. It links every vanilla guide and teaches mechanics, not story.
- Optional questbooks add 194 quests for Expanded Foods (with A Culinary Artillery and its modules), Hex's Mech, Seafarer, Bricklayers, Charcoal Kiln, Wool, Tailor's Delight, From Golden Combs and Better Ruins, including its ruins, hidden places and far story locations reached through maps. Install both the gameplay mod and its questbook. Chapter files can `extend` a base chapter and replace a quest whose mechanic changes.
- Chapters marked `"age": true` label quests elsewhere with the age reached through their prerequisites. The default questline uses stone, clay and fire, copper, bronze, iron and steel; a chapter's late branch carries that age's icon.
- Quest modes support personal progress, pooled party progress with one claim per member, and pooled server progress. Server quests can use `"claim": "first"`. Create parties in the Party tab; disable them with `"Parties": false`.

### Tasks, history and rewards

- Track obtain, kill, mount (rafts, boats, elk), place, break, ignite, craft, knap, clayform, smith, cook, smelt, trade, visit, custom and checkbox tasks.
- Obtain counts liquids in carried buckets by the litre. Ignite covers firepits, forges, kilns and torches with any ignition source. Craft counts every shift-click batch; Toolsmith's in-hand and workbench outputs require the optional adapter. Cook tracks firepit output; smelt tracks molds and bloomeries; trade tracks trader purchases.
- Default quests usually require obtaining an item, so alternate production methods such as spindles and workbenches count. Craft tasks remain where crafting changes an item without changing its identity, such as a clay-coated head or baited pole. Multi-item tasks name their shared category ("any clay") or use a `name` language key ("any fruit").
- Visit counts standing inside a worldgen structure, once per structure. Use its worldgen code and that config file's domain (`game:trader-*`, `betterruins:largeforlornhopetower`); its place name uses `<domain>:structure-<code>`. Villages count each building. `/questline structures` lists structures at the player's position; `discovered` gates use visited places.
- Material payouts become a tiny Quest Cookie; each bundled quest with an original material reward gives one. Stage grants, claim ownership and hand-in consumption remain supported. `GearRewards` stays for configuration compatibility but cannot multiply cookies. `"ItemRewards": false` disables material payouts while retaining stages. See [policy and verification limits](docs/quest-cookie-rewards.md).
- `CreditEarlierWork` in `ModConfig/questline.json` credits work recorded since Questline was installed when a quest unlocks. The game supplies no earlier history. For older worlds, `/questline catchup [player]` completes only quests satisfied by items carried in the hotbar/backpack. It assumes no preceding quests, skips server quests and quests still gated by a mod, stage or discovery, and leaves rewards unclaimed in the book.
- Other mods can use `QuestlineApi` for custom tasks, stages and completion events, or the event bus without a Questline reference.

### Book and editor

- Open the book with L: chapter rail, pannable/zoomable tree, and quest pages with text, images, item rows and recipes. The Reference tab hosts handbook item pages.
- Locked quests list prerequisites with their chapters and links, plus open starting quests. Cross-chapter prerequisites appear beside their quest on the canvas. A chapter with nothing open explains what unlocks it. Backspace or the mouse back button retraces book navigation.
- Pin up to three quests below the minimap from the book or with `.questline pin <quest>`; list them with `.questline pins`. Set per-player notifications with `.questline toasts on|off`.
- Change per-player text size with A−/A+ beside the tabs or `.questline textsize <percent>`: 90, 100, 115 (default), 130 or 150.
- Chapter art supports backgrounds, images, labels and arrows. Quest nodes can be squares, circles, hexagons or gears at any size.
- Players with `questline.edit` (including admins) can add, move and link quests on the canvas, edit forms and export content-mod assets. Working copies stay in `ModConfig/questline/working/`, never installed mods. The Problems tab reports the last load's findings.
- The book uses 80% of the screen. Each chapter opens fitted to the whole chapter or to twenty quests around the player.

### Handbook, graph and planner

- The Reference tab replaces H and handbook links with one search across quests, guides and items. It groups item variants (woods, colours) into one row; item pages list variants and quests that require or reward the item. Search `@modid` for all items from a mod, or `@modid words` to filter them. Vanilla item and guide pages remain available.
- `.questline handbook off` restores the original handbook. In singleplayer, Reference pauses the game like the handbook; turn this off through the handbook's Pause game setting or `.questline pause off`. Other tabs keep the game running because claims and checkboxes require the server.
- The recipe graph scans handbook-known recipes and item properties: about 20,600 vanilla edges, built in under 400 ms. Inspect it with `/questline graph <item>` or `/questline graph export`.
- Use "Plan how to make this" on an item page to trace recipes back to carried items. `RevealLevel` in `ModConfig/questline.json` caps detail: `guide` shows every step/recipe, `hints` (default) shows what to get next without how, and `discovery` disables planning. Players may choose less detail.
- Graph checks flag unobtainable task items, wrong stations, items requested only later, and story items lacking a `{"discovered": ...}` gate in the default questline. The editor uses the graph to suggest prerequisites.

### Server commands

```text
/questline reload | complete <quest> [player] | unlock <quest> [player] |
catchup [player] | reset [quest] [player] | resetserver | export | graph <item> | structures | snapshot
```

Find a quest's ID at the foot of its page. Commands accept IDs without their domain (`cast-anvil`); when domains collide, the default questline's quest wins.

## Translations

All game-shipped languages are present in `questline/assets/questline/lang/`. These machine translations use the game's own item names but have not been checked by native speakers. Corrections are welcome.

Mirror every added or changed `en.json` line in every language. Run `python3 tools/lang/check.py` to check keys, arguments and handbook links.

## Checking a quest pack

`tools/packcheck` runs the server's checks outside the game: missing items/text, broken requirements, cycles, recipe-graph checks and spoilers.

1. In a game with the pack's dependencies installed, run `/questline snapshot`. It writes items, text and the recipe graph to `ModConfig/questline/questline-snapshot.json`.
2. Check the pack's folder or ZIP:

```bash
dotnet build tools/packcheck -c Release
dotnet tools/packcheck/bin/Release/net10.0/questline-packcheck.dll \
  --snapshot questline-snapshot.json --game "$VINTAGE_STORY" mypack/
```

The checker prints each problem and exits 1 if any quest would be disabled. `--strict` fails on any problem. `--game` resolves textures borrowed from the game.

## Building

For a Cairn installation:

```bash
export VINTAGE_STORY="$(ls -d ~/.cairn/games/1.22* | sort -V | tail -1)"
./build.sh
```

Archives land in `Releases/`. For explicit SDK paths, package-only mode and archive guarantees, use [build and packaging](docs/build-packaging.md).

## License

MIT; see [LICENSE](LICENSE). Preserve dizzyd/questline attribution.
