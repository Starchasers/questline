# Better Husbandry 1.4.0 — retained-pack evidence ledger and Questline integration map

## Scope and identity

This is **Better Husbandry**, modid `betterhusbandry`, author Tyeia, not Detailed Animals. The supplied `.../woodworking-tutorial/modpack` is an outer ZIP file, not a directory. Evidence was read from its exact nested archives and configs. The accompanying integration is content-only. This is static source/asset research, not a live-game compatibility test.

Retained `evpack.json`: Pszczoly 1.0, description `Pszczoly server 13.11.2026`, created `2026-11-12T20:50:19.3284355Z`, game **1.22.7**, Kind **Client**, IncludesModConfig true. These are retained exported settings, not proof of the currently running server settings.

| Archive | evpack state | Computed SHA256 (matches manifest) |
|---|---|---|
| `mods/betterhusbandry_1.4.0.zip` | enabled, bundled, 1.4.0 | `4b9f6daf8e4e9ef6e8fe4c18f57fcfe05eb7e842908e42a86ec1e940aeb2d861` |
| `mods/livestockwelfare_0.15.0.zip` | enabled, bundled, 0.15.0 | `f1c41843b32ae9ccd20c42b38a4c518755369ea08e2249b30df041f4734ad065` |

Also enabled: ShearLib 1.3.0 (`shearlib`), Wool & More 1.9.6 (`wool`), `equusferus`, `equusdestrier`, `naturalfertilizer`, `dairyplus`, `catchlivestock`, `configlib`. No Detailed Animals entry was found in the manifest inspection.

## Reproducible evidence locations

Scratch extraction root: `/home/brunette/.hermes/cache/scratch/bh-evidence/`.

- `betterhusbandry.json`, `livestockwelfare.json`, `evpack.json`: exact copied nested export files.
- `betterhusbandry_1.4.0/`: exact nested archive extraction; includes modinfo, DLL/PDB, JSON patches/config/localization.
- `bh-source/betterhusbandry/`: ILSpy decompilation of **the retained 1.4.0 DLL**, not a guessed upstream branch/tag.
- `livestockwelfare_0.15.0/`, `lw-source/livestockwelfare/`: corresponding exact Welfare extraction/decompilation.

Tools used: retained `woodworking-tutorial/tools/ilspycmd` with retained `woodworking-tutorial/dotnet`; both decompilations exited successfully. Decompiled `//IL_...` annotations reflect unavailable reference typing, not a runtime error observed here. Method logic cited below is visible in the exact DLL decompilation. No upstream lookup was necessary.

Evidence shorthand: **BH-E** = `bh-source/betterhusbandry/EntityBehaviorbetterhusbandry.cs`; **BH-H** = `HarmonyPatches.cs`; **BH-S** = `betterhusbandryModSystem.cs`; **LW-** paths are under `lw-source/livestockwelfare/`.

## Mechanics ledger — actual code versus marketing/config names

| Mechanic | Exact active behavior | Evidence | Quest consequence |
|---|---|---|---|
| Independent bloodline | First server initialization captures existing watched `generation` into `betterhusbandry.bloodline`, only if missing. | BH-E Initialize lines 172–185 | Teach inherited generation separately from care-adjusted generation. |
| Effective generation | Writes watched `generation = (int)max(bloodline + feedMod + interactMod, 0)`. Integer cast truncates nonnegative fractional progress. No separate new taming subsystem. | BH-E RecomputeEffectiveGeneration 298–302 | An improvement need not immediately change the visible integer. Do not equate bloodline with current trust. |
| Care axis: feeding | Once per daily callback, reads watched `animalWeight` (default 1). At weight >=0.95 add 0.03; 0.75 <= weight <0.95 hold; weight <0.75 subtract 0.2; clamp [-3,3]. This is condition/body weight, **not an item-fed counter**. | BH-E ApplyDailyUpdate/ApplyFeedAxis 213–264; exact config | Daily husbandry/condition observation is manual. A trough placement/food obtain task cannot prove feeding or healthy condition. |
| Threshold config bug | Config exposes/sanitizes `feedGoodWeightThreshold=0.95`, `feedOkWeightThreshold=0.75`, but ApplyFeedAxis uses hardcoded 0.95f/0.75f, not those config fields. Retained values happen to match code. | BH-E 253–261; betterhusbandryConfig.cs | Avoid promising changed thresholds work in 1.4.0. |
| Care axis: interaction | Petting lasting at least 0.6 seconds and completed player milking record the last interaction and player UID. This does not immediately add points. | BH-H Patch_OnPet 26–39, Patch_OnMilk 11–24; BH-E RegisterInteract 194–205 | Manual petting/milking observation; repeated spam is not instant taming. |
| Shearing hook | When assembly `vs_shearlib` exists, reflectively patches `ShearLib.EntityBehaviorShearable.DoShear`. The mod passes its callback in the **prefix** position, although its class/method is named Postfix. Callback only tests player/server and presence of BH behavior; no successful fleece result test. | BH-S 128–140; BH-H Patch_OnShear 67–78 | Describe as recognized shearing interaction, not proof of successful harvest. Live hook compatibility remains a release gate. |
| Interaction growth | On daily callback: interaction within one game day adds 0.03, clamped [-3,3]. | BH-E ApplyAxis 266–295 | Routine care over time, not one-off pet = fully tame. |
| Neglect/grace | If last action is older than a day, hold while either last interaction or last decay is within `one day + interactGraceDays + current generation * interactgenerationDecayMultiplier` game days; otherwise subtract 0.2 and record last decay. Retained grace=1, generation multiplier=0.5. | BH-E 268–294 | Explain neglect/maintenance, with generation-dependent breathing room. Decay is not necessarily every day; last-decay grace also applies. |
| Player memory/offline protection | Tracks player UID -> interaction hour in `betterhusbandry.recentInteractions`. If dictionary nonempty and none of its players are online, `offlineFullProtect=true` returns before **both** care updates/recompute. No interaction history means no such protection. | BH-E 91–100, 194–205, 213–249 | Protection is tied to remembered carers, not all animals or server population. Never advertise universal offline animal safety. |
| Memory pruning nuance | Old UID entries (>30 game days) are removed inside ApplyAxis, after the offline early return. Full protection can skip the very code that prunes memory. `offlineGraceDays=7` does not limit protection when full protection is true. | BH-E 226–243, 272–279; exact config | Do not promise the protection expires after 7 or 30 days under these settings. |
| Inheritance | Prefix on `EntityBehaviorMultiply.GiveBirth` temporarily replaces mother watched generation with **bloodline**; postfix restores the previously saved effective generation. Intended offspring inheritance excludes temporary feed/interaction bonuses. | BH-H Patch_GiveBirth 41–65 | Observe offspring/bloodline manually. Do not teach that temporary trust bonuses become inherited bloodline. Egg/reproduction behavior outside this patched GiveBirth path needs native verification; do not overgeneralize every species. |
| Persistence/despawn | On despawn sets watched `generation` back to Bloodline. Daily update and initialization recompute effective generation. | BH-E 172–191, 244–248 | Runtime event order matters; offline protection is not a complete persistence/compatibility guarantee. |
| Inspectability | Tooltip explicitly prints `Bloodline Generation:` plus trust descriptions from InteractMod and time since interaction. Admin `/betterhusbandry` (`/bh`) `attr` and `setattr` exist and require controlserver privilege. | BH-E GetInfoText 113–170; BH-S 100–121 | Player quest can ask to inspect tooltip; admin debug commands are QA tools, not progression objectives. |
| Timing/config reload | Registers approximately one game-day callback, visits loaded entities with BH behavior (no explicit Alive filter in this loop); reloads config every 45 real seconds and adjusts callback for time-speed changes. | BH-S RegisterDailyCareTickListener 323–337, OnConfigReloadTick 340+, OnDailyCareTick near end | Do not claim continuous, all-unloaded-animal simulation or instantaneous config/care effects. |

### Exact retained Better Husbandry settings

```json
{"version":2,"feedFloor":-3.0,"feedCeiling":3.0,"feedGrowthPerDay":0.03,"feedDecayPerDay":0.2,"feedGoodWeightThreshold":0.95,"feedOkWeightThreshold":0.75,"interactFloor":-3.0,"interactCeiling":3.0,"interactGrowthPerDay":0.03,"interactDecayPerDay":0.2,"interactGraceDays":1.0,"interactgenerationDecayMultiplier":0.5,"interactMemoryDays":30,"offlineFullProtect":true,"offlineGraceDays":7}
```

All care axes are active (neither neutralized with zero bounds/rates). There is no BH master enabled flag inside this config; the enabled mod manifest/patch installation activates it.

## Item, block and entity-code ledger

**BH adds no itemtypes, blocktypes, recipes, or new animal definitions.** Its asset top-level directories are only `config`, `lang`, `patches`. Never invent `betterhusbandry:feed`, brushes, troughs, milk, breeding items or a Detailed Animals namespace.

`assets/betterhusbandry/patches/vanilla.json` adds behavior `betterhusbandry` to **both client/server** for these exact entity *asset paths* (not final variant entity codes):

- `game:entities/animal/mammal/hooved/sheep-adult`, `sheep-baby`
- `game:entities/animal/mammal/hooved/goat-adult`, `goat-baby`
- `game:entities/animal/mammal/hooved/pig-adult`, `pig-baby`
- `game:entities/animal/mammal/hare-adult`, `hare-baby`
- `game:entities/animal/bird/chicken-adult`, `chicken-baby`

It does **not** add the behavior to vanilla elk/deer. A BH patch does not itself add pettable/milkable/shearable capability: the animal must already support the relevant interaction. Avoid instructing players to pet every patched species indiscriminately.

Active optional BH patches by retained manifest:

- `equusferus`: `equusferus:entities/ferus/ferus`, `ferus-unhandled`, `ferus-wild`.
- `equusdestrier`: `equusdestrier:entities/destrier/destrier`, `destrier-unhandled`.

Other supplied compatibility patches are dormant here because their dependency modids are not enabled: equus, pegasus, monoceros, draconis, talonborne, feverstonewilds, medievalexpansion / medievalexpansionpatch, wolftaming, moreanimals, and the various FOTSA family mods. Welfare's config mentioning cow/dog/giant species does not install BH support for them.

Existing Questline codes that remain useful, **not new BH content**:

| Code/pattern | Kind | Honest automatic evidence |
|---|---|---|
| `game:*fence-*` | placed block pattern | fence placement only, not a closed safe pen |
| `game:trough-*-small-*`, `game:trough-*-large-*` | placed blocks | trough placement only, not filling/eating |
| `game:woodbucket` | obtained item | possession, not milking |
| `game:milkportion` | obtained item | possession of milk, not provenance or a completed milking |
| `game:henbox*` | placed block | placement, not nesting success |
| `game:egg-chicken-raw` | obtained item | egg possession, not egg-laying observation |
| `game:baskettrap-*`, `game:trapcrate-wood` | obtained items | trap possession, not capture |
| `game:shears-*` | smith item | making shears, not shearing |
| `wool:fleece-*` | obtained item (existing Wool addon) | fleece possession, not successful shearing of a cared-for animal |
| `livestockwelfare:strawbedding-clean`, `livestockwelfare:strawbedding-soiled` | Welfare blocks, exact source constants | placed bedding can be detected; mating/birth/cleanliness cannot be inferred from possession |
| `naturalfertilizer:dung-*`, `naturalfertilizer:smallpoop-*`, `naturalfertilizer:chickenpoop-*` | Welfare configured hygiene scan patterns | dirt sources, not BH recipes or rewards |

The existing vanilla/Wool Questline code patterns above were verified in repository quest JSON, not freshly resolved against a native 1.22.7 item registry. Keep native code resolution as a release gate.

## Livestock Welfare interactions: important conflict ledger

### Enabled retained systems

`Hygiene.Enabled`, `Weather.Enabled`, `Thirst.Enabled`, `Babies.Enabled`, `Dogs.Enabled`, `Treats.Enabled` are true. OldAgeFraction=.75, OldAnimalsInfertile=true, DieOfOldAge=true. All Safety death switches are true (AnimalsCanDie, OldAgeCanKill, DiseaseCanKill, ExposureCanKill, ThirstCanKill, MalnutritionCanKill). `Safety.PauseWhenNoPlayerNearby=false`.

- Weather can block breeding at stress >=0.5; pet stress reduction .2 with 2 game-hour cooldown. Roof/shelter seeking, sleeping under roof, heat appetite loss active.
- Thirst can block breeding at >=0.6; natural-water drinking and walking to water active. Water consumption is species-specific.
- Hygiene uses Natural Fertilizer droppings, crowding, muck and rot; disease/old age can also stop breeding.
- Babies require nourishment/maternal care; may need hand feeding and learning the trough. These are **Welfare mechanics**, not BH feeding-counter mechanics.
- Treat following is configured for `game:chicken-*`; do not treat Welfare chicken treats or dog bonding as BH trust state.

### Critical: `Breeding.Enabled=false` DOES NOT disable bedding requirements in 0.15.0

This deserves explicit treatment rather than a simplistic disabled-feature list:

1. `LW-LivestockBreeding.Apply` lines 15–20 returns when `Breeding.Enabled=false`. Thus the configured per-species portions, pregnancy days, rest days and growth-day overrides **are disabled**. Do not quote the exported 20/25-day pregnancy or 14/7/8.3-day growth values as active pack timing.
2. **`LW-LivestockBedding.Settings` lines 29–39 checks `RequireBedding`, NOT `Enabled`.** Retained `Breeding.RequireBedding=true`, radius=16, mating seconds=15, newborn days=1, bedding codes `[livestockwelfare:strawbedding-clean]`.
3. `livestockwelfareModSystem.StartServerSide` installs the bedding Harmony patches unconditionally. `TryGetPregnantPrefix` rejects pregnancy for an applicable kept shelter-behavior animal unless RecentlyMated (LivestockBedding lines 161–185). Usable bedding also requires rain-map roof coverage (74–80).
4. `GiveBirthPrefix` can soil clean bedding and set newborn-bed timing; it does not consult Enabled either (188–227). AI bedding task uses the same Settings accessor.

**Conclusion: only numerical breeding/growth overrides are definitely disabled; bedding/mating/newborn-bed mechanics remain code-enabled with this config.** Live reproduction smoke-testing is required before claiming exact practical behavior across species. Do not omit bedding from the retained-pack breeding guidance merely because Enabled is false.

### Cross-mod coupling, not demonstrated hard crash

- BH changes shared watched `generation`; Welfare `LivestockUtil.IsKept` lines 89–96 uses that same generation >= Hygiene.MuckMinGeneration (1), or playerplaced origin/owner. Thus BH care can move an animal across Welfare's kept threshold, influencing muck/bedding-related checks. A bloodline-0 animal with improved effective generation is not necessarily treated as wild by Welfare.
- Both patch `EntityBehaviorMultiply.GiveBirth`. BH temporarily rewrites generation to bloodline; Welfare clears mating and can soil bedding. No explicit inter-mod patch ordering was established here. Static code shows overlap; it does **not** establish a guaranteed crash or successful live coexistence.
- Welfare weather/thirst/health/age can prevent breeding even with good BH care. Feeding and petting do not override these gates. Build welfare troubleshooting into the breeding quest.
- BH offline protection only skips its own care update. It does not pause Welfare thirst, stress, disease, age or malnutrition; Welfare nearby-player pause is false. **Do not tell players their livestock are safe offline just because BH has full protection.**
- Welfare petting effects have their own states/cooldowns. BH interaction is a care timestamp with later daily growth. Do not merge the two into a single immediate trust award.

## Implemented journey and provider gates

All IDs below qualify to `questline:` (not a new mod or chapter domain). This is a separately packaged extension of `husbandry`. Existing vanilla tasks and prerequisites are never replaced by new manual gates.

```text
build-pen
  -> bh-inspect-bloodline [manual tooltip; inherited vs current]
    -> bh-feed-condition [manual access/condition; daily feeding axis]
      -> bh-interaction-routine [manual supported pet/milk; not spam]
        -> bh-observe-care-change [manual after daily round; no integer gain required]
          -> bh-welfare-readiness [manual, only with livestockwelfare]
        -> bh-offline-plan [manual; remembered carers, neglect and protection limits]
        + shear-animal -> bh-shearing-care [manual, only with wool + shearlib + questlinewool]

Unchanged vanilla routes retain make-trough, make-large-trough,
breed-animals and milk-animal IDs/tasks/rewards/prerequisites.
Their pages retain the old translated description and add provider-specific guidance.
```

No max-trust grind, forced starvation, new provider item codes, care automation or duplicated Wool tool/fleece journey. Equus support is explained in inspection guidance; vanilla elk remains untouched. Automatic placement/possession objectives keep their original evidence limits; new state observations are honest manual checkboxes without rewards.

| Composition | Available teaching | Scope/limit |
|---|---|---|
| BH absent | No BH records or overrides | Original husbandry pages/tasks remain |
| BH 1.4.0 | Five manual care nodes + four page-only replacements | Daily axes, tooltip, bloodline, inheritance, neglect, offline protection |
| BH + Welfare 0.15.0 | Adds bh-welfare-readiness | Breeding.Enabled=false does not disable RequireBedding; clean roofed beds, mating/newborn care; water, stress, health, age remain separate |
| BH + Wool + ShearLib + Questline: Wool | Adds bh-shearing-care | Existing Wool IDs stay owned by Wool; prefix records interaction, not harvest success |
| BH + Welfare + Wool + ShearLib | Both optional notes | Native GiveBirth ordering and ShearLib ABI still require gameplay checks |

### Existing-record impact/replacement map

Current source: `content/vanilla/assets/questline/questline/chapters/husbandry.json`. All IDs below remain unchanged.

| Existing ID | Impact | Treatment / impact rationale |
|---|---|---|
| `build-pen` | contextual care setup | retain 16 fence place task; explain it does not validate enclosure, safe spacing, access to food/water/roof. Welfare detail conditional. |
| `make-trough` | direct context for feeding axis | retain small trough place; page adds actual filling/eating and body-condition guidance, not automatic care credit. |
| `make-large-trough` | direct context | retain large trough place; feeding condition is observed, not proved by placing. |
| `breed-animals` | **direct material replacement** | retain checkbox; explain parent pair/offspring observation, inherited bloodline vs effective generation; retained Welfare bedding/mating and health/thirst/stress constraints conditional. Preserve legacy ID/references. |
| `milk-animal` | **direct material replacement** | preserve `game:milkportion` obtain but explicitly label possession-only; retain saved task identity; successful supported interaction is observed in the separate manual bh-interaction-routine. Completed milking records BH interaction, not instant score. |
| `make-bucket` | local task unchanged | keep `game:woodbucket` obtain; optional care-route note only. |
| `make-henbox` | local task unchanged | retain placement; optional poultry care context, no claim nest = breeding. |
| `collect-eggs` | local task unchanged | retain 6 eggs obtain; explicitly no birth/bloodline detection or egg provenance. |
| `make-basket-trap`, `make-crate-trap` | ancestor/setup context | retain item objectives; capture not observed. Catch Livestock interaction belongs to its own provider research. |
| `melt-fat`, `make-cleaver` | unaffected mechanics | no BH rewrite needed; don't broaden scope into butchering. |

Existing optional Wool extension `content/wool/assets/questline/questline/chapters/wool-husbandry.json`: `make-shears` smith `game:shears-*`, `shear-animal` obtain four `wool:fleece-*`. Preserve those IDs and provider ownership. Add conditional interaction teaching/manual acceptance, not a competing full chapter replacement. Fleece obtain is still not evidence of the ShearLib hook firing.

Vanilla riding `trap-elk-calf`, `break-in-elk` (`game:semitameddeer-*` mount), `ride-elk` (`game:tameddeer-*` mount) have **no direct BH patch** in this archive. Do not replace elk mechanics or declare every riding descendant BH-affected. Optional Equus Ferus/Destrier support is real but separate from vanilla elk.

Milk downstream processing/cheesemaking is ancestor exposure only unless its own text actually makes generation/care claims. BH adds no recipes or dairy products. Avoid replacing dairy/food content merely because milk-animal is an ancestor.

## Verification boundaries / release gates

Verified here: exact archive identities and hashes, retained enabled mods/config, exact DLL logic, entity patch targets, absence of BH items/blocks, existing Questline task codes/IDs, Welfare numerical-overrides-versus-bedding distinction.

Not verified: live 1.22.7 registration of every wildcard, actual pettable capabilities of every patched variant, native patch application against the final server pack, effective gameplay timing with server calendar/loaded chunks, ShearLib 1.3.0 hook invocation/results, offspring inheritance across every animal reproduction path, GiveBirth Harmony interop ordering. These must remain explicit draft/release gates; static decompilation is not a substitute for a live/native gameplay smoke test.

## Implemented scope

The implementation preserves every vanilla task, reward, position, prerequisite and saved ID. Four records receive provider-specific page blocks: make-trough, make-large-trough, breed-animals, milk-animal. Five manual BH observations form a side journey, without retroactively gating existing saved progress. Additive Welfare and Wool/ShearLib notes are provider-gated; they never replace Welfare or Wool IDs. New English strings are explicit fallbacks in all 34 locale files, not claimed translations.

Native release gates: resolve existing item/block patterns against the 1.22.7 registry; inspect minimum-window/text-scale layout; exercise daily care, relog/despawn and old-save claims; verify both GiveBirth Harmony patches and clean-bed mating across species; verify real ShearLib ABI and actual harvested fleece. Offline tests/builds do not prove any of these.

## Exact retained input hashes

- Outer evpack ZIP: `daafd4c1cb217b2553711128adfbd71511f5f0734cfb2927a6c4ffea02e0bb2d`.
- `config/ModConfig/betterhusbandry.json`: `a1a6246ac724e1afb4e4582be82b1f63df003dd2a02e759f660cd1489b8414e8`.
- `config/ModConfig/livestockwelfare.json`: `4e98781c4f09aebf1f7ed6eebd323f8e1938fc5b3739d72470b6b17ec7354641`.

Independent review corrected neglect grace to `dayDifference <= 1 + InteractionGracePeriodDays + generation*0.5`: with the retained one-day base grace, the threshold is **2 + generation*0.5 game days**, not one day. It also restored the original translated description as the first page block on all four overrides.
