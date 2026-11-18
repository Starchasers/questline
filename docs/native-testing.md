# Native test runner integration

Stage the modular fork's content explicitly. Historical upstream `CLAUDE.md` commands installed only the framework and predated content extraction; they are insufficient here. Use this guide for native staging and the repository's shared instructions for development rules.

## Stage required packages

- Install the single `questline` mod; it carries every chapter. No separate content packages exist.
- No chapter is gated on a mod. Quests that target a gameplay mod are disabled by the loader when that mod is absent, so install the full modpack for native runs.
- For Toolsmith native tests, build/install `compat/toolsmith`, core and Toolsmith. With the inspected VsTestkit runner, pass `--mods <checkout>/compat/toolsmith/bin/Release` for the adapter output—not `--mod`, which uses a different output convention.

## Screenshots and acceptance limits

`scripts/screenshots.sh` stages vanilla in both inherited scenarios and Expanded Foods in its provider scenario. Its shell/staging behavior was checked against upstream VsTestkit runner sources; no native game execution was performed. It still needs a configured Cairn/VsTestkit environment and gameplay providers.

For manual acceptance, use local test ZIPs and [local testing](local-testing.md). Native rendering/eating, old saves, multiplayer and provider runtime behavior remain unverified until exercised in a real game.
