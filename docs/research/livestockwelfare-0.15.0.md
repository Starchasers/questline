# Retained Livestock Welfare 0.15.0 — verified research

Baseline: `/home/brunette/.hermes/cache/scratch/woodworking-tutorial/modpack` (ZIP without extension), SHA-256 `daafd4c1cb217b2553711128adfbd71511f5f0734cfb2927a6c4ffea02e0bb2d`. Manifest: Pszczoly 1.0, game 1.22.7, Client export. This is the supplied historical pack, **not** the later 1.4.0 baseline.

Official source: https://github.com/ReginArtDesign/livestockwelfare/tree/c1df75afabbbbb638b87da0255f0a40e65b79785. Exact supplied LW and BH assemblies were decompiled statically; no bundled code executed or repo edited.

## Provider/config fingerprints

| Provider/member | SHA-256 |
|---|---|
| `betterhusbandry 1.4.0` / `betterhusbandry_1.4.0.zip` | `4b9f6daf8e4e9ef6e8fe4c18f57fcfe05eb7e842908e42a86ec1e940aeb2d861` |
| `butchering 1.14.3` / `butchering_1.14.3.zip` | `8332a390c42677ab4376e8817ef93e8835b3f074e9cd3fe534ff32a8d5508862` |
| `catchlivestock 0.2.4` / `Catch Livestock_0.2.4.zip` | `5443b3207981de5f0502c20ce3e3f358bc58e69ea241a61517d0d7ba406b38fd` |
| `genelib 3.2.1` / `genelib_3.2.1.zip` | `a222d7b1d6f30f2b7479703bd14a1d0bb994d7fc3829ef757bf7c0625ff28165` |
| `livestockwelfare 0.15.0` / `livestockwelfare_0.15.0.zip` | `f1c41843b32ae9ccd20c42b38a4c518755369ea08e2249b30df041f4734ad065` |
| `naturalfertilizer 1.5.1` / `naturalfertilizer-v1.22.0-1.5.1.zip` | `639776fccb7ffeaef2c1d4c0a2752045c0084bfc2e82ba71e345027b57e1ec9b` |
| `config/ModConfig/livestockwelfare.json` | `4e98781c4f09aebf1f7ed6eebd323f8e1938fc5b3739d72470b6b17ec7354641` |
| `config/ModConfig/betterhusbandry.json` | `a1a6246ac724e1afb4e4582be82b1f63df003dd2a02e759f660cd1489b8414e8` |

LW DLL SHA-256: `17f4b9dca236d9fc27fbb9727352988083ceb5c3d307e729552b7e26c694f860`. All listed provider hashes match manifest: True.

## Critical corrections

- `Breeding.Enabled=false` disables **only timing/portion/growth JSON rewrites**, not all welfare and **not the clean-bedding gate**. `RequireBedding=true` is independently read by `LivestockBedding.Settings`; its pregnancy/birth Harmony patches are installed unconditionally server-side. This is the most important retained breeding distinction.
- No LW/BH mutual blocker or required companion provider appears in LW modinfo/startup. Do not invent an incompatibility blocker. BH coexistence is a shared-generation semantic interaction, not a demonstrated loader failure.
- `petai`, `wolftaming`, `feralkinship`, `feralkinshipcompanions` are all absent from enabled manifest. **Feral Kinship Companions** is `feralkinshipcompanions`; it is not Feral Kinship (`feralkinship`), Wolf Taming (`wolftaming`), BH or Catch Livestock. Optional compatibility code/config entries do not install those providers. Vanilla-wolf care is separate.
- BH offline protection does not suspend LW needs: `Safety.PauseWhenNoPlayerNearby=false`; all LW death permissions true.
- Genelib 3.2.1 is present; LW avoids replacing a texture source owned by another mod. Visible dirt is not a universal completion criterion.

## Quest coverage matrix

Each row is a teaching milestone, not necessarily a separate mandatory quest. Config values below are retained values, not upstream defaults. Detailed source lines and full exact configs are in the JSON companion.

| Milestone / status | Actual mechanic + config | BH coexistence / authoring caution | Evidence |
|---|---|---|---|
| Know your herd / read needs / active | Age and needs in hover text; sneak + empty-hand right-click reports age/status. Sheep, goats, pigs, chickens and vanilla wolves have direct patches; optional mod species are conditional, not proof of installed animals. **Values:** `{"OldAgeFraction":0.75}` | BH displays bloodline/trust separately and writes effective vanilla generation; do not equate bloodline with age or LW health. | [age](#evidence-age), [startup](#evidence-startup) |
| Keep a clean, uncrowded pen / active | Remove Natural Fertilizer droppings, LW muck/dog poop and ground-stored rot. Dirt moves filth toward environmental dirt exponentially; it is not a fixed daily filth increase. Kept adults can deposit muck; chicks/nursed babies are kept clean. IsKept means generation >= Hygiene.MuckMinGeneration (1), origin=playerplaced, or a nonempty Pet AI owner; it is not synonymous with any nearby wild animal. **Values:** `{"Hygiene.Enabled":true,"DroppingScanRadius":3,"DirtPerDropping":0.05,"DirtPerMuckLevel":0.03,"DirtPerRotItem":0.01,"MuckChancePerDay":0.15,"MuckCrowdingBonus":0.15,"MuckMinGeneration":1,"CrowdingRadius":4,"CrowdingFreeAnimals":6,"DirtPerExtraAnimal":0.1,"FilthAdaptHours":24,"FilthCleanHours":96}` | LW IsKept and muck generation checks read vanilla generation, which BH recomputes from bloodline + floating care modifiers summed then truncated to integer; care can change eligibility without a new birth. | [hygiene](#evidence-hygiene), [safety](#evidence-safety), [binary-kept](#evidence-binary-kept) |
| Brush a dirty adult / active | Dry grass or grooming brush; hold right-click on groomable adults. Grooming removes 0.25 filth per completed use, not disease directly. Chickens self-clean; nursed babies do not need brushing. Shovels harmless to supported animals (shove instead of damage). **Values:** `{"GroomFilthReduction":0.25,"GroomItemUseChance":0.5,"ShovelsHarmless":true,"SelfCleaningSpecies":["chicken"],"drygrass.groomSeconds":2}` | LW grooming is not BH RegisterInteract: BH patches petting, milking and optional shearing. Do not promise brushing awards BH trust. | [groom](#evidence-groom), [hygiene](#evidence-hygiene) |
| Recognize, isolate and support a sick animal / active | Daily illness probability = .25*(filth² + weatherStress²), doubled when old. Same-species contagion within radius 3. Recovery daily chance = .35*(1-filth)*(1-weatherStress), then 6-day immunity. Sick animals lose normal regeneration and breeding; kept sick animals take damage and may collapse. Cleaning/shelter improve odds, not an instant medicine cure. HarmPerDay/SickDamagePerDay are normalized to 17 reference max-health and scale to the animal max-health, not fixed absolute HP across species. **Values:** `{"SicknessChancePerDay":0.25,"OldAgeSicknessMultiplier":2,"ContagionRadius":3,"ContagionChancePerDay":0.1,"RecoveryChancePerDay":0.35,"ImmunityDays":6,"SickDamagePerDay":3,"CollapseHealthFraction":0.3}` | High BH effective generation/trust is not immunity and does not bypass LW sickness, damage or LW breeding cooldown blocks. | [disease](#evidence-disease), [safety](#evidence-safety) |
| Provide a roof and a tolerable climate / active | Rain/snow, temperature and sleeping outside build stress. Animals seek shelter, may get heat-listless/lose appetite; extreme stress harms kept animals, illness risk rises, breeding can stop. Petting reduces LW weather stress with its own cooldown. HarmPerDay/SickDamagePerDay are normalized to 17 reference max-health and scale to the animal max-health, not fixed absolute HP across species. **Values:** `{"Weather.Enabled":true,"RainStress":0.35,"SnowStress":0.45,"RoofColdFactor":0.5,"SleepOutsideStress":0.3,"StressAdaptHours":12,"NoBreedingAboveStress":0.5,"HarmAboveStress":0.8,"HarmPerDay":2,"SeekShelterRadius":24,"PetStressReduction":0.2,"PetCooldownHours":2}` | BH petting and LW stress relief coexist but have distinct timers/effects. Food condition and trust do not replace a roof. | [weather](#evidence-weather) |
| Supply reachable clean drinking water / active | Walk to fresh natural water or consume water from supported placed containers/waterer. Natural water is free; container volume is consumed. Salt/boiling/tainted water is not universally drinkable. A thirsty animal cannot be fixed just by feeding. HarmPerDay/SickDamagePerDay are normalized to 17 reference max-health and scale to the animal max-health, not fixed absolute HP across species. **Values:** `{"Thirst.Enabled":true,"ThirstPerDay":0.8,"WarmAboveC":20,"HotSunMultiplier":1.5,"SeekWaterAboveThirst":0.2,"SeekWaterRadius":16,"DrinkAboveThirst":0.25,"RemoteDrinkAboveThirst":0.6,"DrinkRadius":6,"NoBreedingAboveThirst":0.6,"HarmAboveThirst":0.95,"HarmPerDay":3,"LitresPerFullDrink":{"sheep":1,"goat":1,"pig":1.5,"chicken":0.1,"dog":0.5}}` | BH feed-care scoring is not thirst. LW thirst breeding/regen/damage penalties remain active. | [thirst](#evidence-thirst) |
| Raise young with their mother / active | Keep nursing babies near a suitable female. Mother health/stress affects milk; sick mothers can infect young. Nourishment can slow growth or cause harm. Babies learn trough feeding after time with mother; chicks follow a hen rather than needing mammalian milk. HarmPerDay/SickDamagePerDay are normalized to 17 reference max-health and scale to the animal max-health, not fixed absolute HP across species. **Values:** `{"Babies.Enabled":true,"NursingDistance":10,"NourishAdaptHours":6,"HungerPerDay":0.6,"LearnTroughWithMotherDays":2,"SickMotherMilk":0.5,"StressedMotherMilkLoss":0.5,"SickMotherContagionPerDay":0.3,"SlowGrowthBelow":0.5,"HarmBelow":0.15,"HarmPerDay":2}` | Breeding.Enabled=false does NOT disable LW baby nourishment/growth penalties. BH care bonuses are not a replacement for nursing. | [babies](#evidence-babies) |
| Hand-feed an orphan / teach the trough / active | Use supported milk/food on a nursing baby; three hand-feedings teach trough use. Babies are excluded from ordinary chicken treat setup. Keep orphan care separate from adult feeding. **Values:** `{"HandFeedingsToLearnTrough":3,"HandFeedMilkLitres":0.5,"HandFeedMilkNourishment":0.35,"HandFeedFoodNourishment":0.2,"NourishmentPerPortion":0.25}` | No direct BH ownership conflict found; full-pack runtime not tested. | [babies](#evidence-babies), [handfeed](#evidence-handfeed), [treats](#evidence-treats) |
| Give chickens dry sand / active | Daytime chickens seek dry sand within 10 blocks, with air above and no rain falling on the sand. Bath when filth >= .1 or 20 hours since last bath; 12-second bath resets filth to zero. After 2 unbathed days environmental target is at least .5. Chickens are not brush targets. **Values:** `{"DustBathing":true,"DustBathBlockCodes":["game:sand-*","game:sandwavy-*"],"DustBathRadius":10,"DustBathAboveFilth":0.1,"DustBathEveryHours":20,"DustBathSeconds":12,"UnbathedDays":2,"UnbathedFilth":0.5,"SelfCleaningHours":12}` | A tame/trusting chicken still needs dust-bathing access. SelfCleaningHours is the fallback when DustBathing=false, not the active bath interval. | [dust](#evidence-dust), [hygiene](#evidence-hygiene) |
| Lead chickens with grain / hand-feed / active | Hold food matching the chicken creatureDiet to lure it; hand feeding consumes one item, adds 1 hunger saturation and updates lastMealEatenTotalHours, with one-hour cooldown. Not an all-species LW lure. **Values:** `{"Treats.Enabled":true,"AnimalCodes":["game:chicken-*"],"FollowRadius":10,"FollowDistance":1.5,"HandFeedCooldownHours":1}` | Treats can contribute to feeding/breeding state and BH last-fed data, but do not call BH RegisterInteract. Do not claim a direct BH trust bonus for each grain. | [treats](#evidence-treats) |
| Build a weatherproof chicken coop / active-optional | LW coop kit places ordinary blocks: raised 5×5 coop, ramps 2 long, two hen boxes, rear gate. Recipe uses eight ingredient cells ×8 planks =64 planks plus two hen boxes. It is a building shortcut, not a new egg machine or required structure; hand-built coops work. **Values:** `{"Breeding.Enabled":false,"coop.Width":5,"coop.Depth":5,"coop.RampLength":2,"coop.henboxes":2}` | No BH timer replacement is provided by the coop; egg/breeding conditions remain those of actual entity behaviors. | [coop](#evidence-coop), [breeding](#evidence-breeding) |
| Plan a replacement generation / active | Lifespans randomized in game-calendar years; old at 75% of personal lifespan. Old animals infertile; old-age death enabled. Read age rather than treating effective generation as biological age. Pre-existing/wild adults get an assumed starting age in the first half of life; babies retain birth-age across grow-up. Do not promise historical birth dates for imported adults. **Values:** `{"OldAgeFraction":0.75,"OldAnimalsInfertile":true,"DieOfOldAge":true,"lifespan_years":{"sheep":[3,5],"goat":[4,6],"pig":[3,4],"chicken":[2,3],"dog":[5,7]}}` | BH generation changes do not rejuvenate LW birth date or erase old-age infertility. | [age](#evidence-age), [safety](#evidence-safety) |
| Breed healthy animals without inventing LW timings / retained-base-breeding | LW runtime rewriting of portions, pregnancy, rest and grow-up timings is disabled. Retained numbers are dormant presets, NOT effective pack breeding rates. LW sickness/age/weather/thirst can still hold breeding cooldown ahead of the current time. **Values:** `{"Breeding.Enabled":false,"dormant_species_presets":"Full exact values in JSON config; sheep/goat 10 portions,20 pregnancy days,4–11 rest,14 grow; pig 10,25,6–11,7; chicken 4,null,0–3,8.3."}` | BH effective generation still participates in base-game generation-dependent behavior; BH does not itself make the dormant LW timing overrides active. | [breeding](#evidence-breeding), [safety](#evidence-safety), [disease](#evidence-disease), [binary-timing](#evidence-binary-timing) |
| Use clean bedding for kept mammal mating / active-independent-gate | IMPORTANT: RequireBedding is true and the bedding Settings getter does not test Breeding.Enabled. Kept females with vanilla multiply must mate on clean straw bedding; 15-second mating, search radius16. Birth soils LW bedding and mother/newborn stay there for 1 day. Therefore disabling the timing rewrite does NOT disable bedding requirement. **Values:** `{"Breeding.Enabled":false,"Breeding.RequireBedding":true,"BeddingRadius":16,"MatingSeconds":15,"NewbornDays":1,"BeddingBlockCodes":["livestockwelfare:strawbedding-clean"]}` | BH recomputed vanilla generation can change LW IsKept and therefore whether bedding gate applies. Hens use multiplybase, not this EntityBehaviorMultiply pregnancy gate; do not teach straw bedding as a hen egg requirement. | [bedding](#evidence-bedding), [startup](#evidence-startup), [binary-bedding](#evidence-binary-bedding), [binary-startup](#evidence-binary-startup) |
| Maintain BH care and effective generation / active-bh | BH stores bloodline separately; effective vanilla generation = int(max(0, bloodline + feed modifier + interaction modifier)), i.e. truncation after summing, NOT separate rounding. Feed and interaction modifiers each bounded -3..3. Daily good care +.03, decay .2, condition thresholds .95/.75; interaction grace1 day, generation decay multiplier .5, interaction memory30 days. Offline protection early-returns the entire BH daily update when recorded recent interactors are all offline and its protection check passes; it does not suspend LW needs. Feed condition thresholds .95/.75 are actually hardcoded in BH ApplyFeedAxis (retained config happens to match), not read from those threshold config fields. **Values:** `{"feedFloor":-3,"feedCeiling":3,"feedGrowthPerDay":0.03,"feedDecayPerDay":0.2,"feedGoodWeightThreshold":0.95,"feedOkWeightThreshold":0.75,"interactFloor":-3,"interactCeiling":3,"interactGrowthPerDay":0.03,"interactDecayPerDay":0.2,"interactGraceDays":1,"interactgenerationDecayMultiplier":0.5,"interactMemoryDays":30,"offlineFullProtect":true,"offlineGraceDays":7}` | Pet after at least .6s, milking, optional ShearLib DoShear register BH interactions. Keep bloodline and temporary effective generation explicit. | [bh-generation](#evidence-bh-generation), [bh-interaction](#evidence-bh-interaction) |
| Understand ongoing welfare risk / active-warning | All six LW lethal permissions are enabled and PauseWhenNoPlayerNearby=false. Do not promise offline invulnerability from BH config. Loaded simulated animals can age, become ill, thirst or starve; individual LW needs cap catch-up, which is not global suspension. **Values:** `{"AnimalsCanDie":true,"OldAgeCanKill":true,"DiseaseCanKill":true,"ExposureCanKill":true,"ThirstCanKill":true,"MalnutritionCanKill":true,"PauseWhenNoPlayerNearby":false,"PlayerRadius":64}` | BH offlineFullProtect=true does not govern LW safety. PlayerRadius64 is inactive while pause flag is false. | [safety](#evidence-safety), [age](#evidence-age), [bh-generation](#evidence-bh-generation) |
| Optional raised-wolf welfare and guardianship / conditional-vanilla-wolves | Dogs.Enabled=true; kept vanilla wolves get LW dog care. Bond .5 initial,+.1 pet (2h cooldown),-.08/day without company; lonely below .25, loyal above .75; guard herd/garden, bark, help hunts, spare kept animals/players, lure pups. Dog bowls craftable. External companion trips/commands/beds need the actual external provider and are not proven available here. **Values:** `{"Dogs.Enabled":true,"StartBond":0.5,"BondPerPet":0.1,"PetCooldownHours":2,"BondLossPerDay":0.08,"CompanyRadius":8,"LonelyBelowBond":0.25,"LoyalAboveBond":0.75,"GuardHerd":true,"GuardRadius":12,"GuardGarden":true,"Bark":true,"HelpHunt":true,"TripAftermath":true,"BedCodes":["petai:petnest-*","feralkinshipcompanions:foxbed-*"]}` | BH is not Pet AI or Feral Kinship Companions. Those IDs must not be conflated; none of petai, wolftaming, feralkinship, feralkinshipcompanions are enabled in this retained export. | [dogs](#evidence-dogs), [safety](#evidence-safety) |

## Exact climate/lifespan/timing reference

```json
{
  "Species": {
    "sheep": {
      "LifespanYearsMin": 3.0,
      "LifespanYearsMax": 5.0
    },
    "goat": {
      "LifespanYearsMin": 4.0,
      "LifespanYearsMax": 6.0
    },
    "pig": {
      "LifespanYearsMin": 3.0,
      "LifespanYearsMax": 4.0
    },
    "chicken": {
      "LifespanYearsMin": 2.0,
      "LifespanYearsMax": 3.0
    },
    "dog": {
      "LifespanYearsMin": 5.0,
      "LifespanYearsMax": 7.0
    },
    "giantboar": {
      "LifespanYearsMin": 4.0,
      "LifespanYearsMax": 6.0
    },
    "greathorn": {
      "LifespanYearsMin": 4.0,
      "LifespanYearsMax": 6.0
    },
    "giantredriver": {
      "LifespanYearsMin": 3.0,
      "LifespanYearsMax": 5.0
    },
    "cow": {
      "LifespanYearsMin": 5.0,
      "LifespanYearsMax": 8.0
    }
  },
  "Breeding": {
    "Enabled": false,
    "RequireBedding": true,
    "BeddingRadius": 16,
    "MatingSeconds": 15.0,
    "NewbornDays": 1.0,
    "BeddingBlockCodes": [
      "livestockwelfare:strawbedding-clean"
    ],
    "Species": {
      "sheep": {
        "PortionsToBreed": 10.0,
        "PregnancyDays": 20.0,
        "RestDaysMin": 4.0,
        "RestDaysMax": 11.0,
        "GrowUpDays": 14.0
      },
      "goat": {
        "PortionsToBreed": 10.0,
        "PregnancyDays": 20.0,
        "RestDaysMin": 4.0,
        "RestDaysMax": 11.0,
        "GrowUpDays": 14.0
      },
      "pig": {
        "PortionsToBreed": 10.0,
        "PregnancyDays": 25.0,
        "RestDaysMin": 6.0,
        "RestDaysMax": 11.0,
        "GrowUpDays": 7.0
      },
      "chicken": {
        "PortionsToBreed": 4.0,
        "PregnancyDays": null,
        "RestDaysMin": 0.0,
        "RestDaysMax": 3.0,
        "GrowUpDays": 8.3
      }
    }
  }
}
```

Weather species cold-below/hot-above °C: `{"default":{"ColdBelowC":-2.0,"HotAboveC":30.0},"sheep":{"ColdBelowC":-10.0,"HotAboveC":27.0},"goat":{"ColdBelowC":-6.0,"HotAboveC":32.0},"pig":{"ColdBelowC":2.0,"HotAboveC":26.0},"chicken":{"ColdBelowC":0.0,"HotAboveC":30.0},"dog":{"ColdBelowC":-12.0,"HotAboveC":28.0},"giantboar":{"ColdBelowC":-8.0,"HotAboveC":27.0},"greathorn":{"ColdBelowC":-15.0,"HotAboveC":25.0},"giantredriver":{"ColdBelowC":6.0,"HotAboveC":33.0},"cow":{"ColdBelowC":-15.0,"HotAboveC":26.0}}`. Baby sensitivity shifts: ColdSensitivityC=5, HeatSensitivityC=2.

## Evidence locators

### Evidence age
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockAge.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockAge.cs))
L21: `const string LifespanAttr = "lwLifespanYears";`; L39: `public override void Initialize(EntityProperties properties, JsonObject attributes)`; L41: `base.Initialize(properties, attributes);`; L64: `int DaysPerYear => entity.World.Calendar.DaysPerYear;`; L79: `if (!attrs.HasAttribute(LifespanAttr) && Aging is { } aging)`; L81: `double lifespan = aging.LifespanYearsMin + rand.NextDouble() * (aging.LifespanYearsMax - aging.LifespanYearsMin);`; L82: `attrs.SetDouble(LifespanAttr, lifespan);`; L98: `double lifespan = attrs.GetDouble(LifespanAttr, 2);`

### Evidence hygiene
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockHygiene.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockHygiene.cs))
L147: `UpdateSelfCleaning();`; L148: `if (SelfCleaning && entity is EntityAgent agent && Settings is { DustBathing: true })`; L183: `bool KeptClean => baby && !entity.WatchedAttributes.GetBool(EntityBehaviorLivestockNursing.OrphanAttr);`; L193: `bool SelfCleaning => entity.WatchedAttributes.GetBool(SelfCleaningAttr);`; L194: `const string SelfCleaningAttr = "lwSelfCleaning";`; L196: `void UpdateSelfCleaning()`; L198: `bool selfCleaning = livestockwelfareModSystem.Config?.Hygiene.SelfCleaningSpecies is { } list && Array.IndexOf(list, species) >= 0;`; L199: `if (selfCleaning != SelfCleaning) entity.WatchedAttributes.SetBool(SelfCleaningAttr, selfCleaning);`

### Evidence disease
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockHygiene.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockHygiene.cs))
L219: `LivestockUtil.SetRegenBlocked(entity, "sick", IsSick);`; L382: `double chancePerDay = livestockwelfareModSystem.Config?.Dogs.PoopChancePerDay ?? 0;`; L423: `double chancePerDay = settings.MuckChancePerDay * (1 + extraAnimals * settings.MuckCrowdingBonus);`; L464: `double chancePerDay = settings.SicknessChancePerDay * (filth * filth + weather * weather);`; L467: `chancePerDay *= settings.OldAgeSicknessMultiplier;`; L475: `if (Roll(settings.RecoveryChancePerDay * (1 - Filth) * (1 - WeatherStress), hours))`; L477: `Recover(settings.ImmunityDays);`; L481: `LivestockUtil.BlockBreeding(entity);`

### Evidence dust
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockHygiene.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockHygiene.cs))
L148: `if (SelfCleaning && entity is EntityAgent agent && Settings is { DustBathing: true })`; L150: `if (!entity.WatchedAttributes.HasAttribute(LastDustBathAttr)) entity.WatchedAttributes.SetDouble(LastDustBathAttr, entity.World.Calendar.TotalHours);`; L151: `LivestockUtil.AddAiTask(agent, AiTaskLivestockDustBath.Code, DustBathPriority, walkSpeed, 0.5, 1,`; L152: `(taskConfig, aiConfig) => new AiTaskLivestockDustBath(agent, taskConfig, aiConfig));`; L270: `if (DustBathes(settings) && hours >= CatchUpBathHours && WantsDustBath(settings) && FindDustBath(settings, _ => false) != null) DustBathed();`; L271: `if (DustBathes(settings)) UpdateNoDustBath(settings);`; L293: `if (DustBathes(settings) && HoursSinceDustBath > settings.UnbathedDays * 24) dirt = Math.Max(dirt, settings.UnbathedFilth);`; L294: `double adaptHours = dirt > filth ? settings.FilthAdaptHours : SelfCleaning && !settings.DustBathing ? settings.SelfCleaningHours : settings.FilthCleanHours;`

### Evidence groom
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/CollectibleBehaviorGroom.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/CollectibleBehaviorGroom.cs))
L27: `float groomSeconds = 2;`; L41: `groomSeconds = properties["groomSeconds"].AsFloat(2);`; L49: `entitySel?.Entity is { Alive: true } e && e.GetBehavior<EntityBehaviorLivestockHygiene>() is { CanBeGroomed: true } hygiene ? hygiene : null;`; L69: `return secondsUsed < groomSeconds;`; L79: `if (byEntity.World.Side != EnumAppSide.Server || secondsUsed < groomSeconds - 0.1f) return;`; L83: `bool groomed = hygiene.Groom(settings.GroomFilthReduction * filthMultiplier);`; L93: `else if (!creative && byEntity.World.Rand.NextDouble() < settings.GroomItemUseChance)`; L114: `bool Sneaking(EntityAgent byEntity) => !needsSneak || byEntity.Controls.ShiftKey;`

### Evidence weather
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockShelter.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockShelter.cs))
L18: `/// the cold. Stress counts towards sickness (see EntityBehaviorLivestockHygiene), stops breeding`; L27: `const string StressAttr = "lwWeatherStress";`; L62: `double targetStress;`; L114: `public float Stress => entity.WatchedAttributes.GetFloat(StressAttr);`; L116: `/// <summary>Stresses the animal at once (e.g. a dog back from a trip); it fades like weather stress, and petting helps.</summary>`; L117: `public void AddStress(float amount) => entity.WatchedAttributes.SetFloat(StressAttr, Math.Clamp(Stress + amount, 0, 1));`; L150: `if (Stress > 0) entity.WatchedAttributes.SetFloat(StressAttr, 0);`; L173: `UpdateStress(settings, hours);`

### Evidence thirst
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockThirst.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockThirst.cs))
L46: `const float SeekWaterPriority = 1.36f;`; L54: `LivestockUtil.AddAiTask(agent, AiTaskLivestockSeekWater.Code, SeekWaterPriority, walkSpeed, 0.25, 0.5,`; L55: `(taskConfig, aiConfig) => new AiTaskLivestockSeekWater(agent, taskConfig, aiConfig));`; L97: `&& FindDrinkTarget(settings.SeekWaterRadius, _ => false) is { } target)`; L99: `DrinkFrom(target.Container);`; L103: `double drinkAbove = settings.WalkToWater ? Math.Max(settings.DrinkAboveThirst, settings.RemoteDrinkAboveThirst) : settings.DrinkAboveThirst;`; L110: `double rate = settings.ThirstPerDay;`; L134: `if (water.Container != null) DrinkFrom(water.Container);`

### Evidence babies
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockNursing.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockNursing.cs))
L31: `const string NourishedAttr = "lwNourished";`; L35: `const string KnowsTroughAttr = "lwKnowsTrough";`; L53: `const float FullNourished = 0.95f;`; L82: `tasks.OnShouldExecuteTask += task => task is not AiTaskSeekFoodAndEat || KnowsTrough;`; L86: `bool KnowsTrough => LivestockUtil.BabySettings == null || entity.WatchedAttributes.GetBool(KnowsTroughAttr);`; L88: `public float Nourished => entity.WatchedAttributes.GetFloat(NourishedAttr, 1);`; L133: `double milk = mother == null ? 0 : MilkQuality(mother, settings);`; L156: `if (withMother >= settings.LearnTroughWithMotherDays * 24) attrs.SetBool(KnowsTroughAttr, true);`

### Evidence handfeed
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/CollectibleBehaviorHandFeed.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/CollectibleBehaviorHandFeed.cs))
L10: `/// piglet that cannot suckle feeds it by hand (see EntityBehaviorLivestockNursing.HandFeed). The baby`; L15: `public class CollectibleBehaviorHandFeed : CollectibleBehavior`; L19: `const float FeedSeconds = 1.5f;`; L24: `public CollectibleBehaviorHandFeed(CollectibleObject collObj) : base(collObj) { }`; L29: `if (!byEntity.Controls.ShiftKey || entitySel?.Entity is not { } entity) return null;`; L30: `if (entity.GetBehavior<EntityBehaviorLivestockNursing>() is { } nursing)`; L32: `return nursing.WantsHandFeeding && nursing.CanHandFeedWith(slot.Itemstack) ? entity : null;`; L39: `entitySel?.Entity is { } entity && (entity.HasBehavior<EntityBehaviorLivestockNursing>() || LivestockTreats.TakesTreats(entity));`

### Evidence treats
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/LivestockTreats.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/LivestockTreats.cs))
L12: `/// Treats (see TreatSettings): which animals follow food and take it from the hand, and the feeding`; L19: `const string NextTreatAttr = "lwNextTreatHours";`; L24: `public static TreatSettings? Settings =>`; L28: `/// Server: whether this animal takes treats (TreatSettings.AnimalCodes). Orphaned babies are fed`; L29: `/// by hand their own way (EntityBehaviorLivestockNursing).`; L33: `bool takes = Settings is { } settings && Diet(entity) != null && !entity.HasBehavior<EntityBehaviorLivestockNursing>()`; L34: `&& settings.AnimalCodes.Any(code => WildcardUtil.Match(new AssetLocation(code), entity.Code));`; L57: `entity.World.Calendar.TotalHours < entity.WatchedAttributes.GetDouble(NextTreatAttr) ? "livestockwelfare:handfeed-full" : null;`

### Evidence coop
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/ItemChickenCoop.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/ItemChickenCoop.cs))
L22: `// Outside size of the coop itself: Width across the pop hole, Depth away from it. The ramp`; L23: `// leads up to it from the clicked spot, RampLength blocks in front; the same steps lead up to`; L25: `public const int Width = 5, Depth = 5, RampLength = 2;`; L27: `enum Part { Air, Planks, Stairs, Slab, Post, Gate, HenBox }`; L50: `string? error = TryBuild(api.World, rampFoot, forward, Variant["wood"]);`; L60: `slot.TakeOut(1);`; L72: `public static string? TryBuild(IWorldAccessor world, BlockPos rampFoot, Vec3i forward, string wood)`; L122: `block.Replaceable >= 6000`

### Evidence breeding
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/LivestockBreeding.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/LivestockBreeding.cs))
L21: `if (!settings.Enabled) return;`; L35: `Set(multiply, "portionsEatenForMultiply", breeding.PortionsToBreed);`; L36: `Set(multiply, "pregnancyDays", breeding.PregnancyDays);`; L37: `Set(multiply, "multiplyCooldownDaysMin", breeding.RestDaysMin);`; L38: `Set(multiply, "multiplyCooldownDaysMax", breeding.RestDaysMax);`; L42: `if (breeding.GrowUpDays is not { } growUpDays) continue;`; L48: `double factor = growUpDays * HoursPerDay / longest;`; L53: `grow.Token["hoursToGrow"] = Math.Max(1, grow["hoursToGrow"].AsDouble(96) * factor);`

### Evidence bedding
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/LivestockBedding.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/LivestockBedding.cs))
L12: `/// Straw bedding for breeding (BreedingSettings.RequireBedding): kept animals only get pregnant`; L29: `const string SoiledCode = "livestockwelfare:strawbedding-soiled";`; L32: `public static BreedingSettings? Settings =>`; L33: `livestockwelfareModSystem.Config?.Breeding is { RequireBedding: true } settings ? settings : null;`; L36: `public static bool Applies(Entity entity) =>`; L37: `Settings != null && entity.HasBehavior<EntityBehaviorLivestockShelter>() && LivestockUtil.IsKept(entity);`; L53: `/// <summary>Straw bedding, clean or soiled: a mother stays on hers after the birth soiled it.</summary>`; L104: `harmony.Patch(AccessTools.Method(typeof(EntityBehaviorMultiply), "TryGetPregnant"),`

### Evidence dogs
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/EntityBehaviorLivestockDog.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/EntityBehaviorLivestockDog.cs))
L17: `/// crop eaters off the garden (see AiTaskLivestockDogGuard), and not hunting the player's own`; L35: `const string FkcAwayKey = "feralKinshipExpeditionAway";`; L36: `const string FkcTripAttr = "feralKinshipRetainedNativeExpeditionV1";`; L37: `static readonly string[] FkcAwayPhases = { "Leaving", "Suspended", "Returning", "Resuming" };`; L73: `static DogSettings? Settings =>`; L78: `// stay could be cancelled from 1.9 on, so CanGuard is false while one of those is active.`; L79: `const float GuardPriority = 2.2f;`; L94: `// switch targets on the way, which StopSparedHunts catches.`

### Evidence safety
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/LivestockUtil.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/LivestockUtil.cs))
L30: `public static void BlockBreeding(Entity entity)`; L36: `if (multiply.GetDouble("totalDaysCooldownUntil") >= blockUntil) return;`; L38: `multiply.SetDouble("totalDaysCooldownUntil", blockUntil);`; L43: `public static bool CanKill(string cause)`; L50: `OldAgeDeathCause => safety.OldAgeCanKill,`; L51: `DiseaseDeathCause => safety.DiseaseCanKill,`; L52: `ExposureDeathCause => safety.ExposureCanKill,`; L53: `ThirstDeathCause => safety.ThirstCanKill,`

### Evidence startup
`/home/brunette/.hermes/cache/scratch/lw-audit/source/livestockwelfare/livestockwelfareModSystem.cs` ([pinned source](https://github.com/ReginArtDesign/livestockwelfare/blob/c1df75afabbbbb638b87da0255f0a40e65b79785/livestockwelfare/livestockwelfareModSystem.cs))
L42: `public override void AssetsFinalize(ICoreAPI api)`; L51: `MoveHygieneBeforeHealth(api);`; L52: `LivestockBreeding.Apply(api, LoadConfig(sapi).Breeding);`; L59: `static void MoveHygieneBeforeHealth(ICoreAPI api)`; L74: `public override void StartServerSide(ICoreServerAPI api)`; L76: `LoadConfig(api);`; L79: `beddingPatches = LivestockBedding.Patch(Mod.Info.ModID + ".bedding");`; L82: `// Needed by AssetsFinalize (breeding settings) and StartServerSide; loaded by whichever runs first.`

### Evidence bh-generation
`/home/brunette/.hermes/cache/scratch/lw-audit/bh-decompiled/betterhusbandry/EntityBehaviorbetterhusbandry.cs` (ILSpy of exact bundled assembly: decompiled)
L17: `public float FeedMod`; L29: `public float InteractMod`; L79: `public int Bloodline`; L91: `public Dictionary<string, double> RecentInteractions`; L123: `handler.AppendLiteral("Bloodline Generation: ");`; L124: `handler.AppendFormatted(Bloodline);`; L130: `if (InteractMod == num2)`; L134: `else if ((double)(InteractMod / num2) >= 0.75)`

### Evidence bh-interaction
`/home/brunette/.hermes/cache/scratch/lw-audit/bh-decompiled/betterhusbandry/HarmonyPatches.cs` (ILSpy of exact bundled assembly: decompiled)
L9: `public static class HarmonyPatches`; L11: `[HarmonyPatch(typeof(EntityBehaviorMilkable), "MilkingComplete")]`; L14: `[HarmonyPostfix]`; L15: `public static void Postfix(ItemSlot slot, Entity byEntity, Entity ___entity)`; L21: `___entity.GetBehavior<EntityBehaviorbetterhusbandry>()?.RegisterInteract(byEntity.World.Calendar.TotalHours, byEntity);`; L26: `[HarmonyPatch(typeof(EntityBehaviorPettable), "OnInteract")]`; L29: `[HarmonyPostfix]`; L30: `public static void Postfix(EntityAgent byEntity, Entity ___entity, float ___petDurationS)`

### Evidence binary-bedding
`/home/brunette/.hermes/cache/scratch/lw-audit/lw-decompiled/livestockwelfare/LivestockBedding.cs` (ILSpy of exact bundled assembly: decompiled exact LW 0.15.0 DLL)
L29: `public static BreedingSettings? Settings`; L33: `BreedingSettings breedingSettings = livestockwelfareModSystem.Config?.Breeding;`; L34: `if (breedingSettings == null || !breedingSettings.RequireBedding)`; L38: `return breedingSettings;`; L44: `if (Settings != null && entity.HasBehavior<EntityBehaviorLivestockShelter>())`; L46: `return LivestockUtil.IsKept(entity);`; L57: `BreedingSettings settings = Settings;`; L194: `if (Settings == null)`

### Evidence binary-timing
`/home/brunette/.hermes/cache/scratch/lw-audit/lw-decompiled/livestockwelfare/LivestockBreeding.cs` (ILSpy of exact bundled assembly: decompiled exact LW 0.15.0 DLL)
L17: `if (!settings.Enabled)`

### Evidence binary-startup
`/home/brunette/.hermes/cache/scratch/lw-audit/lw-decompiled/livestockwelfare/livestockwelfareModSystem.cs` (ILSpy of exact bundled assembly: decompiled exact LW 0.15.0 DLL)
L64: `LivestockBreeding.Apply(api, LoadConfig(val).Breeding);`; L103: `beddingPatches = LivestockBedding.Patch(((ModSystem)this).Mod.Info.ModID + ".bedding");`

### Evidence binary-kept
`/home/brunette/.hermes/cache/scratch/lw-audit/lw-decompiled/livestockwelfare/LivestockUtil.cs` (ILSpy of exact bundled assembly: decompiled exact LW 0.15.0 DLL)
L28: `private const string PetAiStatusAttr = "domesticationstatus";`; L89: `public static bool IsKept(Entity entity)`; L91: `if (((TreeAttribute)entity.WatchedAttributes).GetInt("generation", 0) < (livestockwelfareModSystem.Config?.Hygiene.MuckMinGeneration ?? 1) && !(((TreeAttribute)entity.Attributes).GetString("origin", (string)null) == "playerplaced"))`; L93: `ITreeAttribute treeAttribute = ((TreeAttribute)entity.WatchedAttributes).GetTreeAttribute("domesticationstatus");`

## Verification / limits

- Outer ZIP CRC: PASS. 17 coverage rows; source references validated to actual files/matching lines.
- Bundled LW asset files compared to pinned source: 50/50 byte-identical. Individual exceptions, if any, remain explicit in JSON.
- Official historical source and exact binary decompilation support the active-toggle conclusions; a reproducible binary build equivalence was not claimed.
- Static source and exact supplied-DLL decompilation, not a launched full-pack server.
- Client export does not prove server-deployed config, world settings, behavior merge success or runtime patch order.
- Genelib present: LW defers dirty-coat replacement if another texture source already owns appearance; absence of visible dirt is not evidence of disabled hygiene.
- Catch Livestock is an independent installed capture provider, not Pet AI/Feral Kinship; its capture controls were not audited in this LW/BH task.
- No hard LW/BH mutual disable, missing companion dependency or automatic BH-driven LW toggle found; this is not blanket runtime compatibility certification.

## Authored quest map

- `questline:lw-read-herd` — Read the herd
- `questline:lw-clean-pen` — A clean, uncrowded pen
- `questline:lw-shelter` — Shelter before the storm
- `questline:lw-water` — Reachable drinking water
- `questline:lw-groom` — Brush a dirty adult
- `questline:lw-sickness` — Prepare for sickness
- `questline:lw-dustbath` — Dry sand for chickens
- `questline:lw-chicken-treat` — Lead and feed a chicken
- `questline:lw-coop` — An optional ready-made coop
- `questline:lw-bedding` — Clean bedding before mating
- `questline:lw-healthy-breeding` — Healthy parents, not a timer exploit
- `questline:lw-nursing` — Keep young with their mother
- `questline:lw-orphan` — An orphan care plan
- `questline:lw-age` — Plan a replacement generation
- `questline:lw-safety` — Care does not pause with trust
- `questline:lw-wolf-care` — Optional care for raised wolves

All tasks are explicitly manual; no reward farming or custom event bridge. Other locales have English fallback text, not claimed translations. No existing quest IDs or base records are replaced: this independent care chapter complements birth/milking milestones and cannot collide with Better Husbandry replacement IDs. All links use qualified provider domain/type codes.
