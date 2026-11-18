# Framework fork contract

## Source and licensing

Baseline: dizzyd/questline commit `9a2fd4e2b2e24046de08c7a86aff335294558939` (v0.14.0). Preserve the upstream MIT license and attribution. Fork framework version: 0.15.0. Keep the `questline` mod ID, asset namespace and public compatibility identities to avoid silently changing quest/save identifiers. Do not install the upstream and fork simultaneously.

## Approved requirements

1. One repository containing the framework, independently installable vanilla quest content, independently installable optional mod questbooks, and optional executable provider adapters.
2. Preserve original chapter files, quest prose, tasks, IDs, dependencies, pages, links, positions and intentional replacement definitions. Existing quests must retain their behavior except the approved reward substitution.
3. Original request to remove all quest rewards was superseded by explicit user approval: retain claiming functionality and replace item/resource payouts with a custom tiny edible Quest Cookie.
4. Cookie design: quest-only acquisition, tiny satiety, no buffs/healing, no recipes or downstream crafting/cooking/planting/processing/fuel/feed uses supplied by this project. Avoid spoilage into useful materials. Do not claim immunity to arbitrary external mod recipes; inspect the actual enabled modpack for wildcard interactions before release.
5. Preserve stage progression, hand-in consumption, shared claims and one-time claim safeguards. Do not silently change stages or task completion into rewards.
6. Use separate implementing and reviewing agents, address findings, and perform final integration verification. Static and synthetic tests are not native-game acceptance.
7. Publication awaits the user's empty GitHub repository URL. No remote publication authorized to an assumed repository.

## Structural baseline

56 chapter files, 532 source quest records, 589 tasks, 516 distinct quest IDs, including 16 intentional replacement IDs. Packages: vanilla, Better Ruins, Bricklayers, Charcoal Kiln, EF Chef's Tricks, EF Meals Module, Expanded Foods, From Golden Combs, Hex's Machinery, Seafarer, Tailor's Delight and Wool. Toolsmith requires a separate executable adapter.

## Architecture boundaries

Reuse the native cross-mod loader and existing engine. Preserve legacy chapter asset domains and filenames. Keep extension/base replacement semantics; ambiguous competing extensions must not depend on discovery order. Retain existing public API meaning; integration APIs are additive. Shared translations currently remain in the framework to avoid same-path language asset collisions; this is an explicit ownership limitation, not a fully independent localization split.

## Acceptance evidence

- Byte-level upstream content comparisons and dependency-valid optional-package combinations.
- Real framework/adapter compilation against available game assemblies.
- Actual loader conflict/permutation tests and reward policy tests.
- Package manifest/membership/license/checksum validation and deterministic repackaging.
- Independent specification and code-quality reviews, with fixes re-reviewed.
- Native client/server loading, actual provider compatibility, reward claiming/eating/negative-use interactions, old-save progress and multiplayer persistence remain release gates until exercised with a supported game/Testkit setup. Missing VsTestkit is a blocker to those checks, not evidence they pass.
