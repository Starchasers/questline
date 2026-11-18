# Tiny edible quest reward options

Historical research behind the subsequently approved Quest Cookie implementation: keep rewards,
replace resource payouts with a tiny custom edible. This note records neither implementation
nor runtime-test evidence.

**Requirement:** no further crafting, cooking, planting or processing use. Being unobtainable
through crafting alone does not qualify.

## Candidate findings

### Walnut seed — rejected: plantable

- Raw food: **40 satiety, protein, never spoils**.
  [Cooking: Raw edibles](https://wiki.vintagestory.at/Cooking/en#Raw_edibles)
- Verified further use: planting. The tree page documents seed propagation and includes walnut
  seeds in its growth table. A seed can yield a walnut tree, hence wood/resources, not just food.
  [Tree: Propagation](https://wiki.vintagestory.at/Tree/en#Propagation)
- Walnut is absent from the cooking-pot ingredient table, whose rule excludes unlisted ingredients
  from pot meals. This is wiki-level evidence, not an asset/runtime audit of every recipe or
  processing path. [Cooking: Meal food values](https://wiki.vintagestory.at/Cooking/en#Meal_food_values)

Planting alone fails the no-further-use requirement.

### Cherry — rejected: cooking ingredient

- Raw food: **40 satiety, fruit**. Meal ingredient value: **60**.
  [Cooking](https://wiki.vintagestory.at/Cooking/en#Meal_food_values)
- Fruit-table spoilage: **2 days fresh**, then **12 hours transition**; storage/environment can
  change these durations. [Fruit: Fruit Trees](https://wiki.vintagestory.at/Fruit/en#Fruit_Trees)
- Verified further use: cherry is explicitly a meal ingredient. Fruit documentation also describes
  pie/jam, pressing into juice, fermentation/distillation, mash feed and rot/compost pathways.
  Those category descriptions are not a cherry-specific asset audit.
  [Fruit: Usage](https://wiki.vintagestory.at/Fruit/en#Usage)
- Cherry trees propagate through **cuttings**. The cited evidence does not establish that the
  edible cherry itself can be planted.
  [Fruit tree: Growing fruit trees](https://wiki.vintagestory.at/Fruit_tree#Growing_fruit_trees)

Cooking use fails the requirement. Low raw satiety does not make cherry progression-neutral.

### Vanilla cookie/biscuit — unverified option

**No vanilla cookie/biscuit was verified.** The official cooking page lists bread and pie as
the two baked foods; official-wiki searches for cookie/biscuit did not establish a vanilla item.
[Cooking: Baking](https://wiki.vintagestory.at/Cooking/en#Baking)

No actual cookie asset was available to inspect. Nutrition, item code and absence of downstream
uses therefore could not be certified. Do not describe a proposed custom biscuit as vanilla content.

### Satiety comparison, not an alternative

The wiki lists blueberry and currants at **80** raw satiety, cranberry at **60**: “berries are 80”
has exceptions. These are ingredients, not a solution to the strict requirement.
[Cooking: Raw edibles](https://wiki.vintagestory.at/Cooking/en#Raw_edibles)

## Evidence limits

- Sources: official wiki, not a complete installed-game asset audit.
- Local discovery: bounded searches under `/home/brunette`, `/opt` and `/mnt` found no available
  game asset tree. They were not exhaustive host or remote-server searches.
- Version limit: the tree page was marked last verified for **1.20.7**. Wiki content does not
  guarantee behavior in the project's target game build.
- Conclusion: no existing vanilla item was certified as meeting the no-further-use constraint.
  Missing documentation/search results mean **unverified absence**, not proof that an item or
  recipe cannot exist.

## Historical proposal — subject to approval at the time

Use a **custom standalone, quest-only tiny biscuit** for the most controllable design. This was
a proposal, not an implemented feature or verified vanilla fact. Set deliberately tiny,
explicitly agreed satiety and exclude all downstream utility. “Noncraftable” is insufficient:
the item must also be unusable as an ingredient or processing input.

Before claiming compliance, the proposal required an audit of the target game build and enabled
modpack for:

- Exact-code and wildcard recipe matches; cooking-pot/pie eligibility; planting behaviors.
- Grinding, crushing, heating/baking, pressing, barrel and other processing.
- Fuel/feed uses and spoilage into useful rot/compost. A nonspoiling item avoids the rot pathway.

It also required runtime tests of these exclusions, including negative interactions, and isolation
from generic ingredient attributes/behaviors that could admit the item to other systems.
Implementation or reward substitution required explicit approval.
