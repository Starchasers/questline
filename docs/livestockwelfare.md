# Livestock Welfare addon (draft)

Install Questline core, Questline Vanilla, **Livestock Welfare 0.15.0** and
`questlinelivestockwelfare_0.1.0.zip` on the server and clients. Build with the
normal `sh ./build.sh` workflow; packaging discovers the catalogued content mod.
No provider DLL, config, world or external asset is distributed. Better Husbandry
is optional, not a dependency. The draft targets the retained 1.22.7 export,
not every configuration or future provider version.

The separate **Livestock welfare** chapter contains sixteen manual care
milestones. The Vanilla husbandry chapter and its saved IDs remain unchanged.
No duplicate replacement IDs are introduced, so the separately authored Better
Husbandry addon can own its husbandry replacements without this pack silently
winning or disabling them. General vanilla birth/milking milestones are still
valid; welfare preparation belongs here rather than an unnecessary base rewrite.
All new locale keys are present in all 34 shared locale files; non-English files
currently use explicitly provisional English fallback text, not claimed human
translations.

## Care map

| Quest ID (`questline:`) | Player outcome |
| --- | --- |
| lw-read-herd | Inspect age and welfare; understand manual completion |
| lw-clean-pen | Remove waste/rot and reduce crowding |
| lw-shelter | Accessible shelter against temperature, rain, snow and stress |
| lw-water | Provide and observe reachable drinking water |
| lw-groom | Complete adult grooming, using the correct interaction |
| lw-sickness | Prepare clean isolation without deliberately inducing illness |
| lw-dustbath | Dry accessible chicken sand bath |
| lw-chicken-treat | Grain lure and sneak-use feeding interaction |
| lw-coop | Optional coop kit or equivalent hand-built accommodation |
| lw-bedding | Roofed accessible clean bedding; mating and birth cleanup |
| lw-healthy-breeding | Check live fertility gates, not disabled timing presets |
| lw-nursing | Nourishment, mother proximity and trough learning |
| lw-orphan | Rescue feeding and three-feed learning; no forced orphaning |
| lw-age | Read biological age and plan replacement stock |
| lw-safety | Understand enabled deaths and no-nearby-player behavior |
| lw-wolf-care | Optional kept-wolf care; no absent Pet AI/FKC promises |

There are no new rewards or event hooks. Checkboxes certify a player's action or
care-plan review; they do **not** prove provider state, survival or recovery.
Mother/young milestones require real animals when available; illness/orphan/wolf
planning deliberately does not require creating harm or owning a wolf.

## Better Husbandry coexistence

| Providers | Welfare chapter | Better Husbandry responsibilities |
| --- | --- | --- |
| Neither | Hidden | Vanilla milestones only |
| LW only | 16 manual quests | No BH mechanics assumed |
| BH only | Hidden | BH trust/handling, effective generation and wool remain BH-owned |
| LW + BH | 16 manual quests | BH care/handling alongside LW biological welfare; BH's conditional welfare bridge may appear |

`Breeding.Enabled=false` disables LW breeding timing rewrites, **not**
`RequireBedding=true`. Ordinary pregnancy bedding, roof/access/lying-together
checks still apply. LW biological age is not BH effective generation. BH trust
or its own offline care protection does not cancel LW thirst, disease, exposure,
nursing or death policies. Provider behavior is supported by static source and
retained assets/config; loader composition is not a live simulation proof.

## Reproduction

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tools/packaging -v
python3 tools/lang/check.py
# Optional exact-archive checks (not required in public CI):
LIVESTOCK_WELFARE_PACK=/path/to/retained-export python3 -m unittest discover -s tests -p test_livestockwelfare.py -v
# Optional actual sibling-addon JSON in the loader matrix:
BETTER_HUSBANDRY_QUESTLINE_ROOT=/path/to/questline-betterhusbandry dotnet run --project verification/composition/CompositionTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
```

Public CI runs content contracts, all four provider-availability states in the
real loader, randomized composition, translations and normal package validation.
Without the optional sibling path, the BH half is a **provider-availability**
check, not a test of unpublished BH addon files. The local verification supplied
that path and exercised the three actual sibling chapters. Check sibling content
again at its final revision; this is not a frozen cross-PR compatibility promise.

[Source research and full mechanics matrix](research/livestockwelfare-0.15.0.md)
and [exact evidence hashes](research/livestockwelfare-0.15.0-evidence.json) include
retained provider/config fingerprints. Official source snapshot:
`ReginArtDesign/livestockwelfare@c1df75afabbbbb638b87da0255f0a40e65b79785`.
Research and content were independently reviewed by two nested workers.

## Native caveats

No graphical game session or live animal simulation was run. Before removing
DRAFT: install the packaged addon in a copied 1.22.7 world with the exact provider
and retained config; open every link, inspect the 4x4 chapter layout at minimum
window/text scale, exercise grooming/feeding/water/roofed bedding/nursing and
confirm combined BH behavior and server/client persistence. Do not relabel static
source, headless real-loader checks or successful compilation as native evidence.
