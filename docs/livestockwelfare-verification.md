# Livestock Welfare draft verification

Target: retained Vintage Story 1.22.7 export and LW 0.15.0. Source and configs
fingerprinted in `research/livestockwelfare-0.15.0-evidence.json`. This record is
headless/offline evidence, not native gameplay acceptance.

Actual local results:
- `LIVESTOCK_WELFARE_PACK=<retained export> python -m unittest discover -s tests -v`: **7 passed**, including exact retained export hash and provider handbook/asset checks.
- `python -m unittest discover -s tools/packaging -v`: **32 passed**.
- `python tools/lang/check.py`: exit **0**, with expected English-fallback warnings; no claimed translations.
- `python compat/toolsmith/tests/regression.py`: **3 passed**.
- Real-loader `verification/composition/CompositionTests.csproj`: **13 passed** both with and without `BETTER_HUSBANDRY_QUESTLINE_ROOT=/home/brunette/questline-betterhusbandry`. The optional run loads its actual three authored chapters. Both run addon absence plus all four LW/BH provider states and reversed file ordering; original extraction replacements remain valid.
- `verification/rewards/RewardTests.csproj`: **21 passed**, **521 rewarded quests** exercised.
- `compat/toolsmith/tests/AdapterChecks.csproj`: **23 runtime checks passed** (synthetic ABI, not actual Toolsmith gameplay).
- `sh ./build.sh`: core and Toolsmith adapter compiled against official 1.22.7 SDK with .NET 10.0.302, **0 warnings / 0 errors**; all **15** independent packages built.
- Package inventory equals catalog plus core and adapter; all SHA256SUMS entries verified; new addon ZIP CRC check succeeded.
- New artifact: `Releases/questlinelivestockwelfare_0.1.0.zip`, SHA-256 `3f0c89517955e9cd49be3ce0fb367ec5e458005ab96eb6469a0095ac60141049`.
- `git diff --check`: clean.

New artifact is locally built, ignored and not committed or uploaded. No provider
assemblies, proprietary assets or world data are redistributed. No protected
CLAUDE edits, merges or unrelated changes. Existing husbandry quests/IDs are
unchanged; all sixteen new tasks are honest manual checks without new rewards.

Nested review caught and corrected the coop's concrete `-oak` link, required
sneak/hold feeding gestures and roof/reach/lying-together maternity detail.
Future content changes invalidate those reviewed details and should be rechecked.

## Remaining native checks

No GUI/native world/server simulation was run. See `livestockwelfare.md` for the
copied-world checklist: actual links/UI layout, care actions, provider interaction,
multiplayer synchronization and persisted completion. The sibling BH addon is
parallel draft content, not a frozen release dependency; rerun against its final
commit. No claim is made that unloaded chunks simulate welfare or that BH offline
care protection suspends LW. Keep PR draft pending native acceptance.
