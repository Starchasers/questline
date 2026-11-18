# Local testing: modular Questline fork

**Use a copied world and back up ModData.** These test builds are not native-game-validated releases. Target Vintage Story 1.22.0 or newer within the supported 1.22 series, and record the actual SDK used for each build.

## Install

1. Close the game/server. Use a copied world with matching client/server mod sets.
2. Remove upstream Questline's ZIP/folder. Both versions use `questline`; never install them together.
3. Install `questline_0.15.0.zip` and `questlinevanilla_0.14.0.zip` in Mods. Keep individual mod ZIPs intact.
4. Add `questline<provider>_0.14.0.zip` only for installed gameplay mods. These packages contain quests, not the gameplay mods. Check [content dependencies](content-packages.md); Chef's Tricks and Meals Module need both the Expanded Foods questbook and gameplay mod.
5. Add server-side `questlinetoolsmith_0.1.0.zip` only when using Toolsmith.
6. Start the copied world. Inspect startup logs for missing dependencies, asset collisions, disabled quests and Harmony errors before playing.

If a download wraps these ZIPs in an outer bundle, extract the wrapper first. Never put that outer bundle in Mods or blindly install every optional addon.

## Smoke checks

### Content and payouts

- Open the book. Check vanilla chapters, descriptions, tasks, icons, page links and graph layout.
- For each installed provider, check its chapters/extensions and replaced vanilla quests appear in the shared book.
- Complete a normal quest and a milestone. Each original material-reward quest must pay exactly one cookie and no original resources. Repeating a claim must pay nothing.
- Eat a cookie. Check tiny satiety, no health/buff gain, correct name/texture and no spoilage.
- Check the enabled modpack for cookie use in grid crafting, cooking, baking/heating, grinding, crushing, barrels, pressing, animal feed, fuel and planting. External wildcard recipes may add uses this project does not supply.

### Claims, providers and persistence

- Check hand-ins consume exactly once. Missing hand-ins must neither claim nor consume unrelated items.
- Test personal, party and server claims with multiple players. Save, close and reopen; progress and claim state must survive.
- With real Toolsmith and the adapter, craft in hand and at a workbench. Require exact single task credit, correct player attribution and craft history after reload.
- On a copied existing save, preserve completed and previously claimed quests. Remove/reinstall optional content on that copy; progress must survive without silent ID remapping.

Report the game and installed mod versions, exact artifact/checksum, client/server logs and reproduction steps. Compilation and headless checks do not replace these native checks.
