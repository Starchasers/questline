# Tiny edible quest reward options

Research findings informed the subsequently approved Quest Cookie implementation: retain rewards but replace resource payouts with a tiny custom edible. This note is not implementation or runtime-test evidence. Hard requirement: the reward must not be usable in further crafting, cooking, planting, or processing—not merely be unobtainable through crafting.

## Findings

| Candidate | Verified vanilla facts | Further-use check | Decision |
|---|---|---|---|
| Walnut seed | Raw edible: **40 satiety, protein, never spoils**. [Cooking: Raw edibles](https://wiki.vintagestory.at/Cooking/en#Raw_edibles) | **Plantable:** the tree page documents seed propagation and lists walnut seeds in its growth table. This can provide a walnut tree and therefore wood/resources, not just a snack. [Tree: Propagation](https://wiki.vintagestory.at/Tree/en#Propagation) Walnut is absent from the cooking-pot ingredient table, which says unlisted ingredients cannot be used in pot meals; that is wiki-level evidence only, not an asset/runtime audit of every recipe or processing path. [Cooking: Meal food values](https://wiki.vintagestory.at/Cooking/en#Meal_food_values) | **Fails** the no-further-use requirement because planting is a verified use. |
| Cherry | Raw edible: **40 satiety, fruit**; meal ingredient value **60**. Fruit table gives **2 days fresh**, followed by **12 hours transition** (storage/environment can modify spoilage). [Cooking](https://wiki.vintagestory.at/Cooking/en#Meal_food_values), [Fruit: Fruit Trees](https://wiki.vintagestory.at/Fruit/en#Fruit_Trees) | **Cooking is verified:** cherry is explicitly a meal ingredient. Fruit documentation also describes pie/jam, pressing into juice, fermentation/distillation, mash feed, and rot/compost pathways; these broader category descriptions are not a cherry-specific asset audit. Cherry trees propagate through **cuttings**, not an evidenced ability to plant the edible cherry itself. [Fruit: Usage](https://wiki.vintagestory.at/Fruit/en#Usage), [Fruit tree: Growing fruit trees](https://wiki.vintagestory.at/Fruit_tree#Growing_fruit_trees) | **Fails** because it is a verified cooking ingredient; low raw satiety does not make it progression-neutral. |
| Vanilla cookie/biscuit | **No vanilla cookie/biscuit verified.** The official cooking page documents bread and pie as the two baked foods; official-wiki searches for cookie/biscuit did not establish a vanilla item. [Cooking: Baking](https://wiki.vintagestory.at/Cooking/en#Baking) | No actual cookie asset was available to inspect, so no nutrition, item code, or absence of downstream uses can be certified. | **Not a verified vanilla option.** Do not present a proposed custom biscuit as existing vanilla content. |

For scale, the wiki lists blueberry and currants at **80** raw satiety, but cranberry at **60**: “berries are 80” has exceptions. These are ingredients rather than a solution to the strict requirement. [Cooking: Raw edibles](https://wiki.vintagestory.at/Cooking/en#Raw_edibles)

## Evidence limits

These findings use the official wiki, not a complete installed-game asset audit. A bounded local discovery under `/home/brunette`, `/opt`, and `/mnt` did not locate an available game asset tree; it was not an exhaustive host or remote-server search. The tree page itself is marked last verified for **1.20.7**; wiki content is not a guarantee for the project's target game build. No existing vanilla item is certified here as satisfying the no-further-use constraint. Missing documentation/search results establish **unverified absence**, not proof that an item or recipe cannot exist.

## Safest proposal, subject to approval

A **custom standalone, quest-only tiny biscuit** is the most controllable design, not an implemented feature or verified vanilla fact. Give it deliberately tiny, explicitly agreed satiety and no downstream utility. “Noncraftable” alone is insufficient: it also must not be an ingredient or processing input.

Before claiming compliance, audit the target game build and enabled modpack for exact-code and wildcard recipe matches; cooking-pot/pie eligibility; planting behaviors; grinding, crushing, heating/baking, pressing, barrel and other processing; fuel/feed uses; and spoilage into useful rot/compost. A nonspoiling item avoids the rot pathway. Verify these exclusions in runtime tests, including negative interactions. Keep the item isolated from generic ingredient attributes/behaviors that could admit it to other systems. Only implement or substitute rewards after explicit approval.
