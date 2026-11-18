# Native test runner integration

The original commands in the upstream `CLAUDE.md` predate content extraction and install only the framework. They are not sufficient for this fork. This document supersedes those native staging examples without modifying the protected instruction file.

- Install the framework plus `content/vanilla` for vanilla-dependent native tests, BookTests and Gallery.
- Stage each optional questbook together with its actual gameplay provider and prerequisites. Installing gameplay providers alone no longer installs their quest definitions.
- Expanded Foods screenshots require `content/expandedfoods` in addition to vanilla and the gameplay mods.
- Chef's Tricks and Meals Module questbooks also need Expanded Foods gameplay and questbook packages.
- For Toolsmith native tests, build/install `compat/toolsmith` as well as core and Toolsmith. When using the inspected VsTestkit runner, use `--mods <checkout>/compat/toolsmith/bin/Release` for the adapter output; do not use `--mod` for this different output convention.

`scripts/screenshots.sh` stages vanilla for both inherited scenarios and Expanded Foods for its provider scenario. Its shell/staging behavior has been checked against upstream VsTestkit runner sources; native game execution has not been performed. It still requires a genuinely configured Cairn/VsTestkit environment and gameplay providers.

Use the local test ZIPs and `local-testing.md` for manual acceptance. Native rendering/eating, old saves, multiplayer and provider runtime behavior remain unverified until run in a real game.
