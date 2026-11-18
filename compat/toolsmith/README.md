# Questline Toolsmith compatibility (optional, MIT)

Install this server-side adapter alongside Toolsmith and the updated Questline framework. Put `questlinetoolsmith.dll`, `modinfo.json` and `LICENSE` together in a separate ZIP or mod directory. Do not include Questline's DLL or game dependencies. Clients need no adapter install. The adapter contains no quest/content assets and has no compile-time Toolsmith dependency.

## Tracking contract

- Report finished in-hand tools and workbench outputs as **craft** progress, preserving collectible code and stack count. Existing craft quests and retroactive craft history use the same core engine path.
- Core Questline retains generic station trackers but no longer observes Toolsmith's non-grid assembly. Installing or removing the adapter does not migrate or reset progress.
- `QuestlineApi.Report` and the `questline:report` event remain custom-task-only. Use the additive `ReportCraft(IServerPlayer, AssetLocation, int)` only from trusted server-side trackers, once per real output on the server thread. It rejects null/uninitialized inputs, nonpositive amounts, invalid locations and wildcard codes. Its boolean means input accepted, not quest completed. No engine changes are required.

The adapter owns separate Harmony hooks, attaches each independently with warnings, and removes only its own hooks at disposal. Workbench player attribution is restored on success and exceptions; the output hook attaches only after attribution attaches successfully. Missing or moved provider methods warn rather than disabling core tracking.

## Build and checks

```sh
dotnet build compat/toolsmith/QuestlineToolsmith.csproj -c Release -p:VINTAGE_STORY=/path/to/game
python compat/toolsmith/tests/regression.py
dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY=/path/to/game
```

Package only the DLL, metadata and license from `compat/toolsmith/bin/Release/mod/`, not tests or dependent binaries. Require Questline **0.15.0 or newer** with `ReportCraft` and no competing core Toolsmith hooks. Unmodified 0.14.0 is unsupported; the declared minimum dependency rejects it.

### Synthetic coverage

Checks use real compiled Questline/game/Harmony assemblies with synthetic provider methods. They intercept engine reporting to verify exact forwarded type/code/player/count without a game world. Coverage includes:

- API rejection and unchanged custom-task semantics;
- workbench credit, absent attribution, exception cleanup and nested attribution restoration, including inner exceptions;
- null outputs, unchanged in-hand bundles and successful synthetic in-hand replacement;
- skipped output-hook attachment without an attribution hook, and isolated unpatching.

The successful in-hand check intercepts `EntityPlayer.Player` on an uninitialized synthetic entity. It proves adapter forwarding only, not real player lookup or Toolsmith assembly semantics. The absent-hook check removes attribution before retrying output attachment; it does not cover every provider ABI failure or verify startup warning logs.

### Native release gate

Synthetic checks do **not** prove native Toolsmith ABI compatibility, completed in-hand attribution in-world, quest progress, history persistence or reload behavior.

Before release:

1. Run `tests/ToolsmithTests.cs` with a supported game/testkit, real Toolsmith, this adapter and qltest fixtures. Require execution—not skips—of the separate adapter hook test, both successful native craft paths and the no-recipe path.
2. Run core `StationTests.EveryPatchAttachesOnce` separately. Its expected count intentionally excludes provider methods.
3. Verify craft history survives save/reload. Remove and reinstall the optional adapter; progress must not reset.
