---
name: questline-verification
description: Use when validating Questline changes or preparing a PR. Select affected offline, build, synthetic and native checks; report evidence without overstating it.
---

# Questline verification

Read [CI](../../../.github/workflows/ci.yml) and [build guide](../../../docs/build-packaging.md) before running commands. Run from the repository root; do not silently install dependencies or download proprietary SDKs.

## Documentation-only

- Run `git diff --check`.
- Inspect every changed Markdown link, including anchors, relative skill links and README images. Check commands and versions against scripts/manifests.
- Inspect `git diff --name-only` against the allowed scope; no runtime, content, translation, asset, workflow or generated release changes.
- Run relevant lightweight checks below when available. Report missing tools, pre-existing failures and CI status separately.

## Offline: Python 3

```bash
python3 -m unittest discover -s tools/packaging -v
python3 -m unittest discover -s tests -p 'test_content_extraction.py' -v
python3 tools/lang/check.py
python3 compat/toolsmith/tests/regression.py
```

Extraction checks read pinned upstream Git blobs. Use full history before diagnosing missing objects as a content failure.

## Build and harnesses: .NET 10 + supported Vintage Story SDK

Set `VINTAGE_STORY` to an existing installation matching the task's supported SDK. CI records its exact SDK and game versions.

```bash
sh ./build.sh

dotnet run --project verification/composition/CompositionTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project verification/rewards/RewardTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
```

Build packaging rewrites generated output in `Releases/`; use an isolated workspace. Check complete package membership and `SHA256SUMS` as CI does. Synthetic adapter checks do not prove actual Toolsmith ABI or in-world credit.

## Native acceptance

Follow [native testing](../../../docs/native-testing.md) and [local testing](../../../docs/local-testing.md). Use copied worlds and matching client/server sets. Missing `VsTestkit.Runtime` blocks native acceptance; skipped fixture suites are not passes. Do not substitute ordinary `dotnet test`, compile success or a mock for a native run.

Report commit, commands, environment, pass/fail/skip results and missing gates. Link evidence to the exact artifact. Never reuse historical counts as a fresh result.
