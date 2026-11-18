# Development notes

Runtime contracts and test traps, moved from the inherited `CLAUDE.md`. Read [AGENTS.md](../AGENTS.md) first. Historical lab paths below are examples, not available infrastructure or fresh verification.

## Layout and ownership

- `questline/Model/`: definitions, `requires` trees/converter, progress and quest states; shared by client/server.
- `questline/Server/`: `QuestLoader`, `QuestEngine`, `QuestEditor`, trackers and station patches. Server owns registry, progress, parties, claims, sync and saves.
- `questline/Graph/`: recipe edges, JSON serialization and in-game graph building.
- `questline/Network/`: channel `questline`; register messages in identical order on both sides.
- `questline/Client/`: client registry, book tabs/editor, canvas, chapter rail and HUD. `BookStyle`/`BookLayout` own shared typography, colors and sizing.
- `questline/assets/questline/questline/chapters/`: every chapter, shipped in the one mod. `VanillaQuestlineTests` checks reachability, guide links, problems and layout.
- Integration chapter files (`<modid>-<chapter>.json`) still `extends` a base chapter and keep `requiresMod`. Matching quest IDs replace base records; page blocks use keys such as `<id>-<modid>`.
- `compat/toolsmith/`: optional executable provider adapter; no Toolsmith hooks in core.
- `tools/packcheck/`: offline loader/checks against `/questline snapshot`; `PACKCHECK` excludes the game graph builder.
- `tests/`: VsTestkit suites. `tests/fixtures/Mods/qltest` is owned, committed test content, not a downloaded dependency.

Clients receive registry JSON when playing, then state changes. They send claim/checkbox requests; the server decides outcomes.

## Loading, graph and patches

- Register the `questline/` asset folder as an `AssetCategory` in `StartPre`; unknown categories are silently skipped.
- `AssetsFinalize` precedes `StartServerSide`. Load the registry in `StartServerSide`, after assets exist.
- Loader/check code reads `IGameFacts`, never the running game directly. `ServerFacts` and `PackFacts` must report identical fixture problems (`PackCheckTests`).
- Apply station patches separately (`StationPatches.Apply`). One failing hook must not disable unrelated hooks. API signatures differ even between 1.22 point releases: `InventoryCraftingGrid.ConsumeIngredients` returns its recipe in 1.22.7, not 1.22.6. CI targets 1.22.7; the inherited lab used 1.22.6 for some runs.
- Dedicated-server test compilation cannot reference `HarmonyLib` directly: it lacks `0Harmony`. Use reflection and `StationPatches.Attached()` for counts.
- Ignite hooks cover every lightable loaded block (`StationPatches.IgniteTargets`), crediting its pre-ignition code. Check `OnTryIgniteBlock` before crediting `OnTryIgniteBlockOver`; shift-held torches also call the latter on unlightable blocks. Patch counts vary with loaded mods.
- An ingot represents its metal in the graph; casting accepts anything melting into it. Do not enforce ordering as though only ingots count.
- Dedicated clients lack server-side entity behavior configuration. Butchering drops are server-only; milking/pickup use game defaults when needed. `MultiplayerTests` compares client/server graph counts.
- Build game-facing graph data on the main thread in small `GraphBuild` tick steps: mod APIs are not thread-safe. `GraphTests.TheGraphIsBuiltInSmallSteps` covers yielding.
- Pure checks/index work uses worker-thread `GraphIndex`, built once per graph. Historical full-pack indexing took about 15 s; reload checks then took milliseconds. Tests wait for `Engine.GraphChecksDone`; planner waits for `QuestClient.GraphReady`. Accessing `Graph` early finishes the build synchronously.

## Native UI

- Enter the client thread (`await OnClient()`) before composing the book. Server-thread texture uploads have no GL context and can crash without logs.
- `Input.Click` changes world mouse state, not dialog elements. Dispatch presses as `BookTests.ClickAt` does.
- Reopening restores the last tab. Tests must select a known chapter/state.
- Use the book grid: aligned inset panels, row buttons through `AddRowButton`, text through `BookStyle`. Check screenshots at 960×600, the minimum test window.
- Dialog forms cannot scroll safely: input/dropdown frames are baked into the static texture. Use editor pages instead of moving bounds.
- Definitions arrive before editor packets after reload. Replace editor drafts only on `QuestClient.EditorChanged`; definitions alone leave old editor chapters.
- Editor tests use domain `qleditor` and clear its working copies plus `qltest` before each test.
- Dialog texture draws at z=50; text below it is hidden. Draw canvas art just above it.
- A `LinkTextComponent` constructed without the client API cannot follow links. Tests can dispatch `Capi.LinkProtocols["handbook"](link)` as a click does.
- Reading-mode canvas appends cross-chapter prerequisite stubs (`QuestCanvasNode.Stub`). An index beyond `canvasQuests.Count` is not a quest. Editor/plans have no stubs.
- Book history spans tabs, chapter, quest and page. Call `Remember()` before new navigation, like `SelectChapter`, `SelectQuest`, `OpenRef` and tab switches.
- Not every quest item has an exact handbook page: lantern materials and meals use particular stacks; pies may be absent. `ShowReference` falls back to item, kind, then search. `EveryQuestItemOpensAPage` checks this.
- `questline-back` (Backspace) is rebindable but has no hotkey handler. Book `OnKeyDown` reads it after `base.OnKeyDown` gives focused inputs priority; a global handler would fire while typing.
- Draw the book in the handbook layer (`DrawOrder` 0.2). Every show path calls `Show()` to raise it. L/H close only an `OnTop` book; otherwise bring it forward.
- Reference pauses singleplayer unless `noHandbookPause`/`GuiDialogQuestBook.NoPauseSetting` disables it. Paused servers cannot service `OnServer()`. Tests opening Reference first call `ReferenceTests.LeaveTheGameRunning()`.
- Use `BookStyle.TextScale` from player `TextSize`; editor temporarily resets scale to 1 for game-sized forms. Check 115% and 150% text sizes.

## Tasks, content and localization

These contracts inform runtime work; developer-doc edits must not change mod content.

- Query `Translations.Has`, not `Lang.HasTranslation`. The latter checks only the selected language, while `Lang.Get` falls back to English. The inherited German run reported 364 false missing-key problems.
- Keep language key coverage, `{0}` arguments and handbook links aligned; use the game's localized item names. Inherited guidance records 33 languages. `TranslationTests` and `tools/lang/check.py` enforce consistency; inspect current files before claiming a new count.
- `Locking` defaults open: prerequisites suggest order; mods, stages and discoveries lock quests. Strict-locking fixture suites call `Fixture.StrictLocking` before and `Fixture.RestoreLocking` after each test. New `Locked` assertions need the same isolation.
- “Make X” generally means obtain X, because provider machines do not emit grid-craft events. An obtain task for one unconsumed item uses `OnceIsEnough`; placing it later must not undo completion. Keep `craft` when state changes without code changes (`clayCovered` heads, baited poles). Use checkboxes when no reliable event exists.
- Pattern tasks name all matches via shared name or explicit `name` lang key; never display one variant as the whole pattern. `PatternTasksNameWhatTheyShare` checks this. Loaded addons can break common names, so test with real mods too.
- Visit tasks read placed `GeneratedStructures`, not worldgen configs. Recorded codes are domainless: `<schematic>/<structure>` for ruins/village buildings, `<structure>:<schematic>` for story locations, grouped dungeon pieces. `StructureCodes` restores config codes/domains. Remove records created with `VisitTests.Place` after tests.
- Ground storage does not call `DidPlaceBlock`; cooked pot meals share `claypot-*-cooked` with recipe attributes; planting/grafting use the same cutting. Quenching, kiln firing and anvil welding lack trackable player events. Existing content uses checkboxes.
- `GearRewards` and `ItemRewards` transform the server registry after loading, not source chapters; editor drafts retain pack rewards. Historically ordinary quests gave at most one gear (`GearRewardsAreSparingAndScale`), milestones more. The fork's current cookie policy is documented in [quest-cookie-rewards.md](quest-cookie-rewards.md); do not restore historical material rewards.
- Default layout uses columns 2 apart, rows 1.5 apart, in-chapter prerequisites to the left and no edges behind quests. Put entry quests beside what they unlock, not automatically in column 0.
- Graphs cannot inspect provider machines (Hex's Mech's furnaces, Expanded Foods' mixing bowl, Seafarer's prep table) or schematic-only loot such as Better Ruins blueprints. `"unchecked": true` skips production checks only there; the item code must still exist.
- Matcher targets can be regex, e.g. `game:@(redmeat|poultry)-cooked`. Use when wildcards include unintended variants. Look up actual variant codes; filenames are not proof.

## Test harness traps

- The committed `qltest` fixture must be passed with an absolute `--mods` path. Without it, engine/book suites skip; skips are not passes.
- `MultiplayerTests` uses a dedicated server/client. Other suites are `[SingleplayerOnly]` because `OnServer()` requires a shared process. Multiplayer server calls use `Remote.Eval`; default usings include `Vintagestory.GameContent`.
- Graph/Reference suites reach the server directly, so remain singleplayer-only; multiplayer graph parity has its own suite.
- `--filter` is a plain substring, not a pattern. Bound stuck `run.sh` calls with `timeout`.
- Tests spell `VsTestkit.Testing.Gui` in full. A mod named `gui` adds a top-level `Gui` namespace that hides the class; a same-name alias cannot solve it.
- Core no longer embeds Toolsmith hooks. Follow [adapter checks](../compat/toolsmith/README.md) and install the adapter for real-provider tests. `ToolsmithTests` skips without the provider.
- Real-addon acceptance must cover provider-present and provider-absent loading, silent absence, replacements and pack-check snapshots. Native suites must not be replaced with ordinary `dotnet test`.

## Historical lab examples

These commands preserve inherited setup context, not a supported host or fresh result. Use [native-testing.md](native-testing.md) to establish the current harness first. The old design also referenced a private `questline-design-doc` memory; it is not a repository dependency. Checked-in findings are in [phase1-findings.md](phase1-findings.md).

The inherited client tier used `vsclient.home` and an absolute fixture path:

```bash
cd ~/src/anego-1.22/vstestkit
bash scripts/sync-linux.sh dizzyd@vsclient.home --mod ../questline/questline
ssh dizzyd@vsclient.home 'cd vstestkit-questline && bash scripts/run.sh mods/questline/tests \
  --mod mods/questline/questline \
  --mods "$HOME/vstestkit-questline/mods/questline/tests/fixtures/Mods" --client'
```

Swap `--client` for `--multiplayer` for the dedicated-server tier. Historical screenshots landed at `~/.cairn/games/1.22.6/questline-*.png`.

The old addon directory was `~/questline-addon-mods`; use it instead of fixtures for addon-content tests, then take `/questline snapshot`. For item lookup, the old harness kept a headless session (`run.sh ... --keep`) and queried it with `bash scripts/vstk eval`.

The full Dizzy's Best Pack targeted 1.22.7 in `~/vs-installs/1.22.7`, outside Cairn's default 1.22.6 slots. Mods lived in `~/questline-pack-mods`. Two mods refused 1.22.6, preventing world startup. Historical full-pack command:

```bash
env VINTAGE_STORY=$HOME/vs-installs/1.22.7 DOTNET_ROOT=$HOME/.cairn/runtimes/10.0.11-linux-x64 \
    PATH=$HOME/.cairn/runtimes/10.0.11-linux-x64:$PATH VSTK_BOOT_TIMEOUT=900 \
  bash scripts/run.sh mods/questline/tests --mod mods/questline/questline \
    --mods "$HOME/questline-pack-mods" --mods "$HOME/vstestkit-questline/mods/questline/tests/fixtures/Mods" --client
```

Historical Toolsmith fixture setup used `tests/fixtures/fetch.sh` and `--mods "$HOME/vstestkit-questline/mods/questline/tests/fixtures/Toolsmith"`. It stayed outside `fixtures/Mods` so other suites could run vanilla. Inspect the fetch script before downloading third-party binaries. Current modular tests also need the separately packaged adapter/content; old core-only commands do not establish fork acceptance.
