# Framework fork contract

## Source and licensing

Start from dizzyd/questline commit `9a2fd4e2b2e24046de08c7a86aff335294558939` (v0.14.0). Preserve its MIT license and attribution. Fork framework version: 0.15.0.

Keep the `questline` mod ID, asset namespace and public compatibility identities stable: changing them can silently change quest/save identifiers. Never install upstream and this fork together.

## Approved requirements

1. Keep the framework, independently installable vanilla and optional mod questbooks, and optional executable provider adapters in one repository.
2. Better Ruins, Charcoal Kiln and Seafarer quest packages are explicitly removed. Preserve retained original chapter files, quest prose, tasks, IDs, dependencies, pages, links, positions and intentional replacements. Change existing quest behavior only for the approved reward substitution.
3. Retain claiming and replace item/resource payouts with a custom tiny edible Quest Cookie. Explicit user approval superseded the earlier request to remove all quest rewards.
4. Make cookies quest-only, with tiny satiety and no buffs/healing. Supply no recipes or downstream crafting/cooking/planting/processing/fuel/feed uses, and avoid spoilage into useful materials. This does not guarantee immunity to arbitrary external recipes; inspect wildcard interactions in the enabled modpack before release.
5. Preserve stages, hand-in consumption, shared claims and one-time claim safeguards. Do not silently turn stages or task completion into rewards.
6. Separate implementing and reviewing agents, resolve findings, and verify final integration. Static and synthetic checks do not count as native-game acceptance.
7. The initial publication hold required the user's empty GitHub repository URL. The user has since authorized a new draft PR in [Starchasers/questline](https://github.com/Starchasers/questline), superseding that hold for this work. Do not infer authorization to publish elsewhere or create a release.

## Structural baseline

Current retained inventory: 51 chapter files, 469 source quest records, 520 tasks, 453 distinct quest IDs, including 16 intentional replacement IDs. Nine content packages: vanilla, Bricklayers, EF Chef's Tricks, EF Meals Module, Expanded Foods, From Golden Combs, Hex's Machinery, Tailor's Delight and Wool. With the framework and separate executable Toolsmith adapter, this is 11 artifacts.

Historical extraction baseline before removing Better Ruins, Charcoal Kiln and Seafarer: 56 chapter files, 532 source quest records, 589 tasks and 516 distinct quest IDs, including the same 16 intentional replacement IDs. Historical verification of that set does not establish post-removal verification.

Removal is a shipped-inventory change, not a migration or cleanup of existing `ModConfig/questline/working/` editor copies, saved progress, installed old packages or stale output archives. Generic structure discovery/visit support and third-party addon mechanisms remain intact.

## Architecture boundaries

- Reuse the native cross-mod loader and engine.
- Preserve legacy chapter domains, filenames and extension/base replacement semantics. Resolve ambiguous competing extensions independently of discovery order.
- Keep existing public API meaning; add integration APIs rather than changing existing semantics.
- Keep shared translations in the framework for now to avoid same-path language asset collisions. This ownership limitation is not an independent localization split.

## Acceptance evidence

Require:

- Byte-level upstream content comparisons and dependency-valid optional-package combinations.
- Real framework/adapter builds against available game assemblies.
- Real loader conflict/permutation checks and reward policy tests.
- Package manifest, membership, license and checksum checks; deterministic repackaging.
- Independent specification and code-quality reviews, with fixes re-reviewed.

Native client/server loading, real provider compatibility, reward claiming/eating/negative-use interactions, old-save progress and multiplayer persistence remain release gates. Exercise them with a supported game/Testkit setup. Missing VsTestkit blocks those checks; it does not make them pass.
