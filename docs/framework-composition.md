# Framework composition and addon author contract

Build independent content assets, not one monolithic quest pack. Content can
own a questline, append to an installed chapter, or intentionally replace one
quest in a chapter. Do not use file order as a priority system.

## Discovery and precedence

1. Discover questline assets (`assets/<domain>/questline/questline.json`) in **ordinal domain** order. Existing activation rules (`requiresMod`, `yieldsTo`, `replacesDefault`) still apply.
2. Discover chapter assets (`assets/<domain>/questline/chapters/*.json`) in **ordinal domain, then filename** order. If a provider reports different texts for the same asset identity, use ordinal JSON text as the final deterministic tie-breaker. The asset manager normally exposes one resolved asset per identity.
3. Keep the first discovered installed chapter for duplicate non-extension chapter IDs; report the ignored copy. This deterministic compatibility behavior is not a supported override mechanism.
4. Apply editor working copies over installed chapters with the same ID, or add them as new chapters. Traverse working domains and filenames ordinally. If several working files claim one ID, the last ordinal working copy wins, preserving editor precedence. Use the same stable domain traversal for working language overlays.
5. Compose active extensions **after editor copies**. A single extension record with an existing qualified quest ID replaces that quest **in place**; a new qualified ID is appended. Preserve file-internal quest and art order. Extension discovery order orders unrelated appended records/art; it does not select a winner between competing replacements.
6. Keep registry/UI presentation separate: sort chapters and questlines by authored `order`, then **ordinal ID**, independent of server culture. Existing alias collisions are deterministic too: the last chapter in registry order wins. Do not use aliases to resolve extension conflicts. Discovery neither reorders arrays inside content files nor introduces a UI-priority field.

Include an extension only when its `requiresMod` predicates pass and its target
chapter is active. Extensions of inactive targets stay inactive; report
nonexistent targets. Merge quest records and art only. Extension metadata,
such as aliases, is not automatically merged into the target.

## Conflict policy: fail closed, never last-loaded-wins

Before applying any extension records, group all applicable records by
**(target chapter ID, qualified quest ID)**:

- **One record:** apply the existing base-to-one-extension replacement or addition unchanged.
- **More than one record, base/editor quest exists:** keep the base/editor quest and apply none of the competing records.
- **More than one record, no base/editor quest exists:** omit the ambiguous added quest and apply none of the competing records.
- Compose other records and extension art normally. Do not discard the whole chapter.

Treat repeated records within one extension file as ambiguous, even when
identical. An extension cannot silently replace a quest added by another
extension: both records share the conflict key. Ignore inactive extensions
when checking conflicts. Global duplicate quest IDs across distinct chapters
still follow the existing duplicate-quest validation policy; this conflict key
does not permit cross-chapter replacement.

Emit one stable diagnostic per conflict. Name the target, qualified quest ID,
**all contributing asset paths**, retained/disabled outcome, and remediation.
Report conflicts and source paths in ordinal order. Example:

```text
questline:kitchen: ambiguous extension quest questline:roast-meat from addonone:questline/chapters/kitchen.json, addontwo:questline/chapters/kitchen.json; base quest retained. Remove competing records or give additions unique qualified ids; only one extension may supply a quest per target chapter.
```

Fix competing replacements by removing one record, or supply a compatibility
content package that selects one replacement and keeps competing records
inactive. Renaming filenames/domains to win load order is not a fix. Give
independent additions distinct addon-qualified quest IDs.

## Linking a third-party addon

- Install the framework and the content package that owns the target chapter. Declare actual mod dependencies in the addon `modinfo.json`; do not assume the framework ships that chapter.
- Put addon-owned assets under **your own domain**. Extracted compatibility packages retain historical `questline:` IDs for save compatibility; new third-party addons must not use that as a reason to share their namespace.
- Fully qualify every cross-addon link. Unqualified chapter/quest IDs and requirement references use the **asset domain**, not the extension target's domain.
- Set `extends` to the target chapter's qualified ID, not an extension file ID. Extensions are neither standalone chapters nor chained extension targets.
- Use your own quest ID for additions. To replace a quest intentionally, use its original qualified ID explicitly and check that no other active addon supplies that record for that target.
- Use `requiresMod` to gate conditional mechanics by availability. It is positive-only, not a priority or mutual-exclusion rule, and cannot choose between two installed competing addons.
- Point `requires` and other ID links at actual quest/chapter/stage IDs. Dependency declarations do not rewrite references. Keep public IDs stable across releases; use the owning chapter's supported aliases when renaming its quests.
- Give a standalone addon questline its own `questline.json` and chapters with the correct `questline` ID. Use `yieldsTo`/`replacesDefault` for questline activation, not extension conflict resolution.

Minimal addition to another package's chapter:

```json
{
  "id": "myaddon:kitchen-extension",
  "extends": "questline:kitchen",
  "requiresMod": ["myaddon"],
  "quests": [
    {
      "id": "myaddon:prepare-special-meal",
      "pos": [0, 0],
      "tasks": [{ "type": "checkbox", "count": 1 }],
      "requires": { "quest": "questline:roast-meat" }
    }
  ]
}
```

Use this example for linking and composition only. It neither defines rewards
nor changes reward handling.

## Executable verification

Run with .NET 10 and a Vintage Story SDK/game installation:

```sh
dotnet run --project verification/composition/CompositionTests.csproj -c Release \
  -p:VINTAGE_STORY=/path/to/vintagestory
```

The dependency-free console harness invokes the **real `QuestLoader`**, using
`IGameFacts` and logger test doubles and real temporary editor files. It executes
the loader rather than substituting regex assertions. Coverage includes:

- Exhaustive small discovery/conflict permutations and discovery under two cultures.
- Inactive extensions, stable duplicate diagnostics, editor precedence, and qualified cross-addon links.
- 12 seeded shuffles of all 51 retained chapter files (469 quest records, 520 tasks and 453 distinct quest IDs).
- All **16 intentional base-to-one-extension replacements** in the real content, including tasks, prose, and prerequisites.

Game existence/lang lookups use permissive mocks. This verifies composition,
not a native client/server or full gameplay smoke test.

Historical registry tie-breaking evidence: the added real-loader regression was
RED (**9 passed, 1 failed**) with culture-sensitive ID sorting and GREEN after
explicit ordinal comparers. The recorded suite result was **12 passed, 0 failed**;
this is not a new run.

A snapshot shared across `en-US` and `tr-TR` checks authored-order/ordinal-ID
chapter and questline presentation and the alias collision winner for `I`/`i`
across input permutations. Direct assertions also preserve base/extension art
payload and authored art order despite quest conflicts, and check same-domain
`I.json`/`i.json` working-file winners across cultures and file creation orders.
Every test restores `CurrentCulture` and `CurrentUICulture` in `finally`, even
on failure. Registry presentation order remains separate from asset discovery
order.

Removing shipped packages does not delete existing `ModConfig/questline/working/`
copies, saved progress, installed old ZIPs or previous build output. Editor copies
still participate under the precedence rules above; removal is not a progress
migration or an automatic working-copy cleanup.
