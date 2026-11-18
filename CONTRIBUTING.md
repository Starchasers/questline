# Contributing

## Start

1. Read [AGENTS.md](AGENTS.md) and the relevant [developer guide](README.md#developer-guides).
2. Check `git status --short`; work on a focused branch. Use separate worktrees for concurrent work.
3. Define allowed files and acceptance checks. Prefer the smallest complete change. Keep developer-doc cleanup separate from mod content and gameplay changes.

## Choose checks

- **Docs only:** `git diff --check`, relative links/anchors, copied commands and final changed-file scope. Do not claim native validation.
- **Python tooling/content provenance:** run the four offline commands in [verification](.agents/skills/questline-verification/SKILL.md).
- **Framework, composition, rewards or adapter:** build with the supported SDK and run affected harnesses; see [build](docs/build-packaging.md) and [CI](docs/ci.md).
- **Game behavior, UI, multiplayer or persistence:** add the relevant [native checks](docs/native-testing.md), using a copied world. Check [local smoke tests](docs/local-testing.md) for installation and claims.

Use regression tests for behavior changes. Missing prerequisites and skipped tests are blockers or limits, not passing results. Do not commit generated ZIPs, credentials, proprietary binaries or local game paths as universal setup.

## Review and PR

- Keep identities, dependencies, translations, license notices and provenance intact. Document intentional compatibility changes and migrations.
- Review the whole diff, not only successful test output. Remove unrelated edits and unsupported claims.
- In the PR, state goal, scope, checks actually run, missing gates and risks. Include UI evidence for visible runtime changes and exact artifact/checksum for native runs.
- Use a draft while review or verification remains. Never merge or release without authorization; recheck CI on the exact pushed head.

## AI-assisted work

[AI workflow](docs/ai-workflow.md) explains rule ownership, local skills, source references and safe delegation. AI-generated changes receive the same review and verification as handwritten changes. Keep final prose concise and precise; never trade safety or technical meaning for fewer words.
