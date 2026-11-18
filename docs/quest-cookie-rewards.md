# Quest Cookie reward policy

## Shipped behavior

- Pay material rewards only as `questline:questcookie` through this fork's quest claim path, including milestone quests and authored resource-choice rewards. Each shipping quest that previously paid resources now pays **one** cookie. Leave rewardless quests rewardless.
- Apply the shared `RewardPolicy.Apply` policy at both boundaries: reload projects a detached registry before sending client definitions; claim applies the policy again. Before normalization, loader, projection and claim enforce an explicit, case-sensitive `item`/`stage`/`choice` allowlist across the entire authored reward tree. Require nonblank stages and at least one option per choice. Reject nested choices: the claim protocol supports only top-level picks. Reject invalid trees even with `ItemRewards` false; do not normalize them into apparently valid payouts. Legacy material metadata cannot authorize payouts. Only the effective cookie collectible must exist.
- Resolve every selected cookie collectible before consuming hand-ins, creating/marking a claim record, or granting stages. Refuse a claim when the cookie is missing; allow retry after restoring the asset, never fallback to the authored item. Dispatch only a normalized one-cookie item or a validated stage.
- Collapse item bundles and item-only choices to one cookie. Retain stage grants. Keep stage-bearing choices as choices, replacing material options with cookies. Third-party mixed stage/material trees can pay one cookie per material-bearing list/selected branch; there is no unconditional one-cookie cap across arbitrary stage choices.
- Use `ItemRewards: false` to opt out of item rewards while retaining stages. Keep legacy `GearRewards` for configuration/source compatibility only: it cannot scale, suppress, or restore cookie payouts. Reload after reward-configuration changes.
- Preserve task counts, consumption flags, completed/claimed state, personal/server/party claim ownership, quest IDs and links without reset or migration. Do not reopen claimed quests or confiscate/convert existing inventory resources.
- Treat original chapter JSON and prose as authored metadata, not payout authority. The editor can still show/edit authored rewards, but those resources cannot bypass the policy. Player-facing book reward slots use effective server definitions.

## Item and artwork

Use the engine's plain `Item` class for the cookie: satiety **10**, food category
`NoNutrition`, health **0**. The item has no custom behaviors, attributes,
food/feed tags, fuel properties, planting properties, transition/perish rules,
or processing/baking/smelting definitions. It cannot spoil into rot, so it
supplies no cookie-to-rot-to-compost pathway. Neither the framework nor its
content packages supply cookie crafting recipes, cooking ingredients, or
transformation outputs. Ordinary eating is the intended functional use; normal
engine hunger timing is not an added custom buff.

Regenerate `textures/item/questcookie.png` with the command below. This original,
hand-authored pixel art comes from `verification/rewards/generate_texture.py`,
uses no third-party image inputs, and is distributed under the repository's
MIT license.

```sh
python verification/rewards/generate_texture.py
```

## Scope of the no-other-use guarantee

Limit the guarantee to **definitions and payout code supplied here**. Other mods
can make the cookie eligible for another use through a broad namespace/code
wildcard recipe (for example `*:*`), an explicit `questline:questcookie` reference,
a generic "any edible" cooking rule, a feed rule, or an asset patch. The isolated
code and absence of fuel/feed/processing properties prevent ordinary
property-driven paths; they cannot stop unrelated mods from matching the item
by code or adding rules.

Do not claim the cookie is universally uncraftable/unprocessable in every
modpack. To verify that stronger claim, inspect the **actual loaded and expanded
recipe/cooking/feed/processing registries**, including wildcard matches and
patches, then test native interactions in the target game/modpack. This change
neither patches third-party recipes nor globally overrides their matching rules.
No native/modpack certification was performed here.

## Verification and limits

Run the dependency-free headless regression executable with the installed
.NET 10 SDK and game SDK assemblies:

```sh
VINTAGE_STORY=/path/to/vintage-story dotnet run --project verification/rewards/RewardTests.csproj
```

The executable references production framework code. It checks:

- All **521** shipping rewarded quest records, including **39** milestone records.
- Material-choice/bundle collapse, source nonmutation, non-reward quest fields, serialized client definitions, idempotence, configuration, persisted progress, and the item asset contract.
- Real `QuestEngine.Claim` execution against interface doubles: incomplete/repeated claims; successful and missing hand-ins; personal/server/party ownership; shared consume-once; stage rewards; stage-bearing choices; unknown/custom/null/case-mismatched reward rejection with items enabled and disabled; nested-choice rejection without exceptions or mutation; missing-cookie refusal/retry without fallback; and inventory-overflow dispatch.
- A literal legacy progress JSON fixture through real `LoadProgress`, claim, `SaveProgress`, registry reprojection, then `LoadProgress` again. Completed/claimed/consumed flags, stages and history survive without payout replay. This fixture injects registry reprojection by reflection; it does not execute native asset reload.
- Item nutrition JSON deserialization with the real game API type.

The headless player double uses the SDK's `MonoMod.Utils` access-check attribute
to handle an inaccessible abstract `IPlayer` method in this game SDK. It modifies
no installed SDK files. These doubles are not a running game.

Historical results below record earlier verification, not new runs:

- Initial behavioral RED: **3 passed, 6 failed**, after extracting old scaling/filtering into the testable registry projection but before changing behavior. Failures included original rusty-gear payout surviving, milestone bundles retaining three payouts, legacy scaling removing payouts, original resources surviving serialization, shipping resources surviving, and the missing cookie asset.
- Initial policy GREEN: **15 passed, 0 failed**.
- Reward-review behavioral RED: **15 passed, 4 failed**. It reproduced unknown reward acceptance, a nested-choice null-item exception, and missing-cookie acceptance, plus a hand-in fixture initialization issue.
- Final GREEN: **21 passed, 0 failed**, after fixing the fixture's SDK dirty-slot callback seam and production validation/preflight bugs, then adding overflow/legacy-save cases.
- Additional recorded commands: `Composition: 12 passed, 0 failed`; `23 runtime checks passed` for the Toolsmith adapter; Release framework build with **0 warnings, 0 errors**.

Do **not** read these checks as proof of in-game item loading, rendered UI
appearance, eating/satiety execution, native inventory overflow, native recipe
exclusion, or multiplayer delivery. VsTestkit was unavailable; native validation
remains outstanding. The recorded
`dotnet build tests/questline.tests.csproj -c Release --no-restore` attempt failed
on missing `VsTestkit.Runtime`/`VsTestkit` references (**1 warning, 402 errors**).
That was not a native test run. The directly affected EngineTests and
VanillaQuestlineTests payout/choice expectations were updated to cookies, but
those native suites were not executed.
