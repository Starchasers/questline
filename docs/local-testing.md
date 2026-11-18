# Local testing: modular Questline fork

These are test builds, not native-game-validated releases. Back up your world and ModData before installation. Target game dependency: Vintage Story 1.22.0 or newer within the supported 1.22 series; builds must record the actual SDK used.

## Install

1. Close Vintage Story/server. Use a copied test world and matching client/server mod sets.
2. Remove the original Questline ZIP/folder. This fork deliberately retains the `questline` mod ID; never install both.
3. Put `questline_0.15.0.zip` and `questlinevanilla_0.14.0.zip` in your Mods directory. Keep each mod ZIP intact; do not unpack it.
4. Add optional `questline<provider>_0.14.0.zip` files only for gameplay mods you actually have installed. These are quest definitions, not bundled gameplay mods. Consult `content-packages.md` for dependencies. Chef's Tricks and Meals Module questbooks also require the Expanded Foods questbook and gameplay mod.
5. Install `questlinetoolsmith_0.1.0.zip` only when using Toolsmith; it is a server-side compatibility adapter.
6. Start the copied world. Check startup logs for missing dependencies, asset collisions, disabled quests and Harmony errors before playing.

A downloadable bundle may contain these individual ZIPs in folders. Extract that outer bundle first; never put the outer bundle in Mods. Do not blindly install every optional addon.

## Smoke checks

- Open the book; verify vanilla chapters, descriptions, tasks, icons, page links and graph layout.
- With each installed provider, verify its chapters/extensions and replaced vanilla quests appear in the same shared book.
- Complete a normal quest and a milestone. Claim exactly one cookie for each original material-reward quest; never receive original resources. A repeated claim must give nothing.
- Eat the cookie: verify tiny satiety, no health/buff gain, correct name and texture. Check that it does not spoil.
- Try grid crafting, cooking, baking/heating, grinding, crushing, barrel processing, pressing, animal feed, fuel and planting against the actual enabled modpack. External wildcard recipes can introduce uses this project does not supply.
- Verify hand-in requirements still consume exactly once; missing hand-ins must not claim or consume unrelated items.
- Test personal, party and server claim scopes with multiple players. Save, close, reopen, and verify progress/claimed state survives.
- With real Toolsmith plus adapter, craft in hand and at a workbench; verify exact single task credit, correct player attribution, and history after reload.
- On a copied existing save, verify completed and previously claimed quests remain intact. Remove/reinstall optional content on the copy and check progress survives without silently remapping IDs.

Report game version, installed mod versions, exact artifact/checksum, client/server logs and reproduction steps. Automated compilation/headless checks do not replace these native checks.
