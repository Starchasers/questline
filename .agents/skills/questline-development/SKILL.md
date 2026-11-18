---
name: questline-development
description: Use when changing Questline framework, content composition or optional provider integration. Preserve identities, server authority and native game boundaries.
---

# Questline development

1. Read [repository rules](../../../AGENTS.md), relevant tests and [composition](../../../docs/framework-composition.md). Classify the change as framework, content, provider, UI or documentation.
2. Keep framework in `questline/`, content in `content/*`, executable Toolsmith hooks in `compat/toolsmith/`. Optional providers must be absent safely; do not add another quest engine or bundle gameplay mods.
3. Trace identity before moving assets. Preserve asset domains, chapter filenames, quest/task IDs, replacement records, extension targets and shared language ownership. Match dependencies to actual manifests, not inferred namespaces.
4. Trace server-owned progress and claim paths. Retain scoped grants, one-time hand-in consumption, duplicate-claim prevention, party/server semantics and saved history. Reward changes require explicit scope.
5. Keep loader/check logic behind `IGameFacts`. Native API and Harmony changes need supported-version source/assembly evidence; never guess item codes or provider ABI.
6. For UI, read [development notes](../../../docs/development-notes.md): client thread, grid, packet timing, history, pause behavior and bounded main-thread work. Check 960×600 plus 115% and 150% text scale.
7. Select [verification](../questline-verification/SKILL.md). Test missing/present providers, composition, reload and existing saves where affected. Distinguish synthetic/offline results from native evidence.

For a documentation-only task, inspect these contracts but leave runtime files and mod content unchanged.
