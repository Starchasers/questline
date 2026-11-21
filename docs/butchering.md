# Butchering player journey — addon 0.15.0

Install `questlinebutchering_0.15.0.zip` alongside Questline >=0.15.0, Questline Vanilla >=0.14.0 and Butchering >=1.14.3. Replaces only the vanilla `first-hunt` teaching page and adds 34 IDs across four chapter assets (35 definitions total). Hunting javelin removed by request; Armory is no longer a quest provider for this addon. Rustic Cookery adds three conditional meat/smoking quests.

## Progression and layout

The vertical working route starts at the primitive table: table → preparation → knapped flint component → primitive skinning hook → carcass → bled carcass → meat. Knapping must precede the primitive hook.

Three horizontal upgrade rows run rightward and only connect within the upgrade workshop: primitive → simple → advanced tables; flint → copper → bronze → iron components; primitive → copper → bronze → iron floor skinning hooks. Matching ceiling hooks are terminal mounting alternatives below their floor stations. Upgrade nodes never gate core processing or unrelated products. Bronze accepts tin, bismuth or black bronze; it does not force three redundant alloy stations.

Copper branches require `first-smithing`; bronze requires any of `alloy-bronze`, `alloy-bismuth-bronze`, `alloy-black-bronze`; iron requires `smith-iron`. All native metalworking pages are linked from the appropriate upgrade pages. Tier dependencies are curriculum order, not recipes consuming the previous workstation.

Clean offal, dry sinew, strong bones, butchery bag, prime cut and preservation are independent branches from meat processing. Blood sausage follows clean offal; sinew glue follows dry sinew; hide glue and Leatherworking links follow raw hide. No offal → sinew → prime-cut dependency exists. Hide pages link to hide preparation, limewater, tannins and leather making.

## Station rates and actual tiers

- Primitive table and primitive flint skinning hook: **80%** drop rate for their respective processing stages.
- Simple table, copper/bronze floor and ceiling skinning hooks: **100%**.
- Advanced iron table, iron floor and ceiling skinning hooks: **120%**.
- Components are ingredients, not independent yield-bearing stations. No flint ceiling or steel hook exists.
- Ceiling mounting uses the matching floor station plus a reusable wrench, is reversible and does not increase yield.

These are stage-specific drop-generation multipliers, not guaranteed individual drops. Skinning and table butchering use different reward sets; do not multiply their rates together. The retained configuration has both workstation multipliers at 1.0. Simple/advanced tables consume their tools during grid construction; there is no lower-table conversion recipe. Flint knapping produces two components; enabled metal smithing produces four from an ingot. The nugget single-hook recipe is disabled without SmithingPlus.

## Objective semantics and player language

All titles are plain nouns; descriptions teach actions without research versions or instrumentation disclaimers. Technical boundaries belong here: station/component obtain tasks observe carried outputs, not placement or personal manufacturing. Six existing grid-craft tasks credit real grid crafting; knapping, smithing and machine transitions are taught, not claimed as instrumented events. Liquids are counted as whole carried litres. Carcass equipment slots are not scanned, so use small carryable carcasses. Rare/class/species-dependent products never gate the working route.

All 35 icons and 34 automatic output targets have source-resolved examples in [the asset receipt](evidence/butchering-assets.json), checked against the [source ledger](evidence/butchering-sources.json). [Objective ledger](evidence/butchering-objectives.json), [website reconciliation](evidence/butchering-website-coverage.json), [verification history](evidence/butchering-verification.md).

## Verification boundary

Real-loader composition exercises absent/present providers, optional links, all hook tiers and all three bronze alternatives with Vintage Story wildcard matching. Static asset resolution does not establish a full-pack rendered layout, native station processing, multiplayer or persistence acceptance. English is the addon-owned fallback; human translations remain pending. No proprietary game binaries or mod archives are shipped in source.
