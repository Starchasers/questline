# Questline Toolsmith compatibility (optional, MIT)

Install `questlinetoolsmith.dll`, `modinfo.json` and `LICENSE` together in their own ZIP or mod directory on the server, alongside the updated Questline framework and Toolsmith. Do not include Questline's DLL or game dependencies in this ZIP. No client install is required. This adapter has no quest/content assets and no compile-time Toolsmith dependency.

It reports finished in-hand tools and workbench outputs as **craft** progress, preserving the original collectible code and stack count. Existing craft quests and retroactive craft history use the same core engine path. Questline alone retains all generic station trackers but intentionally no longer observes Toolsmith's non-grid assembly. Installing/removing this adapter does not migrate or reset progress.

`QuestlineApi.Report` and the `questline:report` event remain custom-task-only. The additive `ReportCraft(IServerPlayer, AssetLocation, int)` is for trusted server-side trackers: null/uninitialized, nonpositive amounts, invalid locations and wildcard codes are rejected. Its boolean indicates input acceptance, not quest completion. Call once per real output on the server thread. No engine changes are required.

The adapter uses its own Harmony owner, attaches each hook independently with warnings, restores workbench player attribution on success or exceptions, and removes only its own hooks at disposal. The workbench output hook requires successful attribution attachment. Missing/moved provider methods degrade with a warning rather than disabling core tracking.

## Build and checks

```sh
dotnet build compat/toolsmith/QuestlineToolsmith.csproj -c Release -p:VINTAGE_STORY=/path/to/game
python compat/toolsmith/tests/regression.py
dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY=/path/to/game
```

Installable files are emitted to `compat/toolsmith/bin/Release/mod/`. Package only the DLL, metadata and license, not tests or dependent binaries. The adapter requires Questline **0.15.0 or newer**, containing `ReportCraft` and no competing core Toolsmith hooks. An older unmodified 0.14.0 is unsupported and is rejected by the declared minimum dependency.

Checks use real compiled Questline/game/Harmony assemblies with synthetic provider target methods. Engine reporting is intercepted to verify exact forwarded type/code/player/count without starting a game world. They verify API rejection and existing custom semantics, workbench credit, absent attribution, exception cleanup, nested attribution restoration (including inner exceptions), null outputs, unchanged in-hand bundles, successful synthetic in-hand replacement, skipped output-hook attachment when the attribution hook is absent, and isolated unpatching. The successful in-hand check intercepts `EntityPlayer.Player` for an uninitialized synthetic entity: this verifies adapter forwarding only, not real player lookup or Toolsmith assembly semantics. The absent-hook check deliberately removes attribution before retrying output attachment; it does not simulate every provider ABI failure or verify startup warning logs.

**Native acceptance remains a release gate.** These checks do **not** prove native Toolsmith ABI compatibility, completed in-hand attribution in a world, quests advancing, history persistence, or reload behavior. Run `tests/ToolsmithTests.cs` with a supported game/testkit, real Toolsmith, this adapter, and the qltest fixtures; require execution (not skips) of the separate adapter hook test plus both successful native craft paths and the no-recipe path. Run the core `StationTests.EveryPatchAttachesOnce` separately; its expected count intentionally excludes provider methods. Also verify craft history survives save/reload and optional-adapter removal/reinstallation does not reset progress.
