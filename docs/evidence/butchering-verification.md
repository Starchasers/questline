# Butchering verification receipt

## PR #4 conflict-resolution verification

Merged live `origin/main` at `ee7ba3a26ade50e024960321de42fa4daea7784b` into original feature head `15051df7639c91eb6d31aa7c856964fbf5013323` without rewriting history. Reconciled README and package documentation to retain the authored addon, its English-owned locale, and main's revised developer guides. Main's `CLAUDE.md` is unchanged. Original feature content, source ledger, research, directed map, catalogs, locales and runtime/composition tests remain intact.

Fresh local execution used the official cached Vintage Story 1.22.7 SDK, .NET SDK 10.0.302 (also checked 10.0.404), and Python 3.14.7. Packaging: 32 tests passed; content/extraction: 8 passed; Toolsmith source: 3 passed. Localization had zero errors, with only the existing Chef's Tricks English warnings. Both Release builds passed with zero warnings/errors. Production-loader composition: 13 passed, including 17 replacements and the Butchering present/absent contract. Reward claims: 21 passed, exercising 536 rewarded definitions. Synthetic adapter: 23 passed. All 15 ZIPs and checksum entries were read back; a repeat full build under SDK 10.0.302 produced identical `SHA256SUMS`. The cached primary archive and all 30 source ledger members were rehashed successfully.

The new release-count regression failed against the inherited release workflow's 14-ZIP assumption before correction. The release workflow and current CI documentation now agree on 15 ZIPs (core, 13 content packs, adapter) and 16 release assets including `SHA256SUMS`. No release publishing was executed. Hosted CI must be checked on the pushed merge commit; local results do not establish hosted execution. Native/full-pack acceptance and human translations remain pending.

## Historical original-feature receipt

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
