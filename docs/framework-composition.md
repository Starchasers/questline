# Framework composition and addon author contract

The framework loads independent quest content assets. It does not require one monolithic quest pack. Content can define its own questline, append to an installed chapter, or intentionally replace one quest in a chapter. File order is not a priority system.

## Discovery and precedence

1. Questline assets (`assets/<domain>/questline/questline.json`) are discovered by **ordinal domain** order. Existing activation rules (`requiresMod`, `yieldsTo`, `replacesDefault`) still apply.
2. Chapter assets (`assets/<domain>/questline/chapters/*.json`) are discovered by **ordinal domain, then filename** order. For providers reporting multiple different texts for an identical asset identity, ordinal JSON text is the final deterministic tie-breaker. Normally the asset manager exposes one resolved asset per identity.
3. Duplicate non-extension chapter IDs retain the first discovered installed chapter and report the ignored copy. This is deterministic compatibility behavior, not a supported override mechanism.
4. Editor working copies replace the installed chapter with the same ID, or add a chapter. Working domains and filenames are ordinal; if multiple working files claim one ID, the last ordinal working copy wins, preserving editor precedence. Working language overlays use the same stable domain traversal.
5. Active extensions are composed **after editor copies**. A single extension record with an existing qualified quest ID replaces that quest **in place**. A new qualified ID is appended. File-internal quest and art order is preserved. Extension discovery order determines the order of unrelated appended records/art, not which competing replacement wins.
6. Registry/UI presentation ordering remains separate: authored `order`, then **ordinal ID** for both chapters and questlines, independent of server culture. Existing alias collision behavior (last chapter in registry order wins) is therefore deterministic too; aliases are not an extension conflict-resolution mechanism. Discovery does not reorder arrays inside content files or introduce a new UI-priority field.

Only extensions whose `requiresMod` predicates pass and whose target chapter is active participate. An inactive target means its extensions are inactive too; a nonexistent target is reported. Extension metadata such as aliases is not automatically merged into the target; existing composition merges quest records and art only.

## Conflict policy: fail closed, never last-loaded-wins

Before any extension records are applied, the loader groups all applicable records by **(target chapter ID, qualified quest ID)**.

- **One record:** existing base-to-one-extension replacement or addition works unchanged.
- **More than one record, base/editor quest exists:** keep that base/editor quest; apply none of the competing records.
- **More than one record, no base/editor quest exists:** omit the ambiguous added quest entirely; apply none of the competing records.
- Other records and extension art still compose. The whole chapter is not discarded.

Repeated records within one extension file are ambiguous too, even if identical. An extension cannot silently replace a quest introduced by a second extension: those records share the same conflict key. Inactive extensions do not create conflicts. Global duplicate quest IDs across distinct chapters remain subject to the existing duplicate-quest validation policy; the extension conflict key does not invent cross-chapter replacement.

Each conflict produces one stable diagnostic naming the target, qualified quest ID, **all contributing asset paths**, retained/disabled outcome, and remediation. Conflicts and source paths are reported in ordinal order. Example:

```text
questline:kitchen: ambiguous extension quest questline:roast-meat from addonone:questline/chapters/kitchen.json, addontwo:questline/chapters/kitchen.json; base quest retained. Remove competing records or give additions unique qualified ids; only one extension may supply a quest per target chapter.
```

To fix competing replacements, remove one competing record or provide a compatibility content package that selects one replacement and ensures the competing records are not active. Renaming filenames/domains to win load order is not a fix. For independent additions, use distinct addon-qualified quest IDs instead.

## Linking a third-party addon

- Install the framework and the content package that owns the target chapter. Declare actual mod dependencies in the addon `modinfo.json`; do not assume the framework itself ships a particular chapter.
- Put addon-owned assets under **your own domain**. The extracted compatibility packages deliberately preserve historical `questline:` IDs for save compatibility; that is not a reason for new third-party addons to share their asset namespace.
- Unqualified chapter/quest IDs and requirement references are qualified against the **asset domain**, not against the extension target's domain. Use fully qualified IDs for every cross-addon link.
- Set `extends` to the target chapter's qualified ID, not an extension file ID. Extensions are not standalone chapters and are not chained extension targets.
- For an addition, use your own quest ID. For an intentional replacement, explicitly use the original quest's qualified ID and verify no other active addon supplies that same record for that target.
- Use `requiresMod` for conditional mechanics, but remember that it is a positive availability gate, not a priority or mutual-exclusion mechanism. It does not choose between two installed competing addons.
- `requires` and other ID links must name actual quest/chapter/stage IDs; a dependency declaration does not rewrite those references. Keep public IDs stable across releases; use the owning chapter's supported aliases when renaming its quests.
- A standalone addon questline needs its own `questline.json` and chapters with the correct `questline` ID. `yieldsTo`/`replacesDefault` control questline activation; they are not extension conflict resolution rules.

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

This example demonstrates linking and composition only. It does not define rewards or change reward handling.

## Executable verification

With .NET 10 and a Vintage Story SDK/game installation:

```sh
dotnet run --project verification/composition/CompositionTests.csproj -c Release \
  -p:VINTAGE_STORY=/path/to/vintagestory
```

The dependency-free console harness invokes the **real `QuestLoader`** with `IGameFacts` and logger test doubles, plus real temporary editor files. It does not substitute regex assertions for loader execution. Coverage includes exhaustive small discovery/conflict permutations, two cultures for discovery, inactive extensions, stable duplicate diagnostics, editor precedence, qualified cross-addon links, and 12 seeded shuffles of retained chapter files. The current content baseline is **51 chapter files, 469 quest records, 520 tasks and 453 distinct quest IDs**, after removal of Better Ruins, Charcoal Kiln and Seafarer. The real-content regression must continue to check all **16 intentional base-to-one-extension replacements**, including their tasks, prose, and prerequisites. Retained chapter bytes and generic structure/visit support are unchanged. Game existence/lang lookups are permissive mocks; this is composition verification, not a native client/server or full gameplay smoke test.

Historical verification before package removal used all 56 extracted chapter files. For ordinal registry tie breaking, the added real-loader regression was RED (**9 passed, 1 failed**) against culture-sensitive ID sorting and GREEN after the explicit ordinal comparers. That checkpoint reported **12 passed, 0 failed**; it is not a post-removal result. A snapshot shared across `en-US` and `tr-TR` verifies authored-order/ordinal-ID chapter and questline presentation plus the alias collision winner for `I`/`i`, across input permutations. Additional direct assertions preserve base/extension art payload and authored art order despite quest conflicts, and verify same-domain `I.json`/`i.json` working-file winners across cultures and file creation orders. Every test restores both `CurrentCulture` and `CurrentUICulture` in `finally`, even on failure. Registry presentation order is separate from asset discovery order.

Removing shipped packages does not delete existing `ModConfig/questline/working/`
copies, saved progress, installed old ZIPs or previous build output. Editor copies
still participate under the precedence rules above; removal is not a progress
migration or an automatic working-copy cleanup.
