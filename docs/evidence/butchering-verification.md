# Butchering verification receipt

Executed in the independent `questline-butchering` clone, against the official Vintage Story 1.22.7 assemblies and .NET 10 SDK. No files in `questline-framework` were edited or built.

| Gate | Actual result |
|---|---|
| Primary export identity | Pszczoly 1.2.0; archive SHA-256 `239c31aef93c0960bfb87c8d5e8a2dd0add2d4287ce18836ca36abdefbf4ac9d` |
| Primary evidence readback | Export archive hash and all 30 ledger member hashes verified |
| Packaging unittest suite | 32 passed |
| Content/extraction unittest suite | 7 passed; historical assets byte-identical |
| Core localization checker | All languages: zero errors; existing `addon-efchefstricks` English warnings |
| Toolsmith source regression | 3 passed |
| Release framework/adapter builds | Both succeeded, zero warnings/errors |
| Production-loader composition | 13 passed; including 17 shipped replacements and Butchering present/absent, exactly 14 new IDs |
| Reward claim suite | 21 passed; 536 rewarded quest definitions exercised |
| Synthetic Toolsmith runtime adapter | 23 checks passed |
| Complete package set | 15 independently installable ZIPs, all SHA256SUMS entries verified |
| Repeat full build | Identical SHA256SUMS (`cmp` exited zero) |
| Whitespace | `git diff --check` clean |

The new content tests were first executed before implementation and failed for the missing chapter/replacement; the complete suite passes with the addon. An independent source/content reviewer found the missing chapter-title key, incorrect knife icon shorthand and consumed knife preparation omission. All three were corrected; title/icon contracts now have regressions.

This is offline verification, not live native acceptance. No full modpack client/server, native GUI layout, VsTestkit, spoilage timer or real interaction playthrough was run. The gameplay claims are bounded to archived asset/recipe/config and decompiled DLL inspection. Synthetic adapter checks are not an installed Toolsmith receipt. The historical srMi9 URL was not fetched as a currently available source; locally cached export identity is documented in the research. Human translation remains pending; addon English is the fallback.
