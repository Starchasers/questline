# Packaging verification

The original extraction and hardening execution snapshots later in this document
are historical. The post-removal checkpoint below is a separate local run.

## Current package target

The current clean-output target is **11 artifacts**: framework, nine content
packages (vanilla plus eight optional integrations), and the Toolsmith adapter.
The retained content contains 51 chapter files, 469 quest records, 520 tasks and
453 distinct quest IDs, including 16 intentional replacement IDs. Retained chapter
assets remain byte-for-byte unchanged; generic structure discovery/visit tasks
are not removed.

The three removed quest ZIPs listed in the historical snapshot below must not
appear in a new verified package set. The packager does not clean stale output;
use a new output directory and validate the exact ZIP/checksum set. Package removal
also does not clean existing `ModConfig/questline/working/` editor copies, saved
progress or installed old mod ZIPs.

## Post-removal local verification

Using the CI-matching .NET SDK 10.0.100 and Vintage Story 1.22.7 server SDK:

- RED before production removal: content suite **6 tests, 5 failures**; packaging
  suite **33 tests, 1 failure** (the inventory regression found 14 instead of 11).
- GREEN: packaging **33 passed**, content removal/preservation **6 passed**,
  translation consistency **1,197 English keys, zero errors across 34 locales**
  (31 existing English-text warnings), Toolsmith source **3 passed**,
  real-loader composition **12 passed**, headless rewards **21 passed**,
  synthetic Toolsmith adapter **23 runtime checks passed**.
- Both owned code packages built successfully, and the actual packager produced
  **11 ZIPs / 113 entries**, with 51 exact-source-byte chapter assets. Independently
  checked exact package membership, SHA256SUMS, licenses, CRC, asset and DLL bytes.
  A repeat packaging pass with identical assemblies produced identical ZIP bytes.
- All 51 retained chapters and the vanilla book manifest match immutable upstream
  blobs byte-for-byte. All nonremoved inherited locale values are preserved;
  150 exclusively removed-provider keys are absent from each of the 34 locales.

These are offline checks and builds, not a native VsTestkit/client/world run.
The generic native structure-mapping regression remains, without requiring the
removed Better Ruins chapter; it was not executed in this offline checkpoint.

## Historical execution environment

Read the following as **historical local evidence**, not a current test report. The recorded
runs used the external .NET SDK at
`/home/brunette/.hermes/cache/scratch/woodworking-tutorial/dotnet/dotnet`
(version supplied for that task: 10.0.404), with `VINTAGE_STORY` pointing to the
sibling `vs` directory. No game assemblies were copied into the repository.

## RED → GREEN

1. Created `tools/packaging/test_package.py` before implementation. Ran
   `python3 -m unittest discover -s tools/packaging -v`.
   **RED**: import failed because `tools/packaging/package.py` did not exist.
2. Implemented the packager. The initial **15 tests passed**.
3. Added stricter regression cases before fixing them. **RED**: 23 tests ran with
   two errors. Prerelease comparison treated `rc.10` as older than `rc.2`;
   non-string manifest `type` raised AttributeError instead of ValueError.
4. Fixed both errors: **23 tests passed**. Added an unowned game-assembly override
   regression: **RED** (24 tests, one assertion failure). Enforced DLL names from
   the owning csproj: **24 tests passed**. Test DLL payloads were explicitly
   synthetic; this was not a native game integration suite.

## Actual builds and artifacts

Ran `sh ./build.sh` with the explicit SDK environment. Both the core
`questline.csproj` and `compat/toolsmith/QuestlineToolsmith.csproj` built with
**0 warnings and 0 errors**. The adapter used its actual framework ProjectReference.
Also exercised the legacy dependency-free CakeBuild launcher with
`dotnet run --project CakeBuild/CakeBuild.csproj -- --help`.

Repeated the full real build/package entry point twice. Both runs produced
**identical** `Releases/SHA256SUMS` bytes. Independently opened every advertised
ZIP and checked its checksum, manifest, expected DLL membership, MIT LICENSE
bytes, sorted unique names, CRC, fixed timestamp, and mode.

That historical pre-removal snapshot contained **14 artifacts** in `Releases/`:

- `questline_0.15.0.zip`
- `questlinevanilla_0.14.0.zip`
- `questlinebetterruins_0.14.0.zip`
- `questlinebricklayers_0.14.0.zip`
- `questlinecharcoalkiln_0.14.0.zip`
- `questlineefchefstricks_0.14.0.zip`
- `questlineefmealsmodule_0.14.0.zip`
- `questlineexpandedfoods_0.14.0.zip`
- `questlinefromgoldencombs_0.14.0.zip`
- `questlinehexsmech_0.14.0.zip`
- `questlineseafarer_0.14.0.zip`
- `questlinetailorsdelight_0.14.0.zip`
- `questlinewool_0.14.0.zip`
- `questlinetoolsmith_0.1.0.zip`

`git diff --check` passed at that checkpoint. Rebuild after concurrent runtime/content
changes before treating the snapshot as final. No native VsTestkit or in-game test
ran; the unavailable native harness remained a separate acceptance limitation.
Nothing was committed or published.

## Independent packaging review follow-up

Added seven regression test methods **before** implementation changes. They covered
all four reported defects plus accepted-file and valid-version boundaries.
Used this exact command for RED and GREEN:

```sh
python3 -m unittest discover -s tools/packaging -v
```

- **RED:** `Ran 31 tests in 0.112s`; `FAILED (failures=36)`.
  Failing subtests covered six dotenv-family paths, six ordinary-file secret
  assignments, eight executable signatures, four nested floating overflow cases,
  and twelve invalid prerelease versions across manifest/dependency fields.
  Existing NaN/Infinity rejection and safe-format boundary cases already passed.
- **GREEN:** `Ran 31 tests in 0.072s`; `OK`.
- Logs: `/home/brunette/.hermes/cache/scratch/packaging-review-{red,green}.log`.

Ran a real build/package with the same external SDK via
`python3 tools/packaging/package.py --output
/home/brunette/.hermes/cache/scratch/packaging-review-build`, with `DOTNET` and
`VINTAGE_STORY` explicitly set as above. Both owned code projects built with
**0 warnings and 0 errors**. Then exercised package-only independently:

```sh
python3 tools/packaging/package.py --package-only \
  --assembly questline=questline/bin/Release/Mods/mod/questline.dll \
  --assembly questlinetoolsmith=compat/toolsmith/bin/Release/mod/questlinetoolsmith.dll \
  --output /home/brunette/.hermes/cache/scratch/packaging-review-only
```

Both invocations succeeded. Independently verified **14 ZIPs / 124 entries**:
CRC, LICENSE bytes, parsed manifests, owned DLL membership, sorted unique names,
SHA256SUMS, and byte-identical archives/checksums between build and package-only.
Build/package logs were `packaging-review-build.log` and
`packaging-review-only.log` in the scratch directory. Artifacts stayed outside
repository Releases; this follow-up edited no runtime/content sources.
Packaging tests did not verify native game behavior. Nothing was committed or
published. These results remain historical, not evidence of a new run.
