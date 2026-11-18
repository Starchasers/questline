# Packaging verification

Read this as **historical local evidence**, not a current test report.

## Art of Growing integration verification

An independent output directory was built against .NET 10 and Vintage Story
1.22.7 assemblies after adding `content/artofgrowing`. Core and Toolsmith builds
both returned **0 warnings, 0 errors**. The exact manifest-derived set was
**15 ZIPs**: framework, thirteen content addons, and Toolsmith. All fifteen
`SHA256SUMS` digests were independently recomputed and matched. The separate
`questlineartofgrowing_0.14.0.zip` contained all 29 expected entries: root manifest,
root MIT license, twenty JSON patch files, four extension chapters and three
English locale files; no DLLs or provider binaries.

This is local package and offline composition evidence, not a native gameplay
run or a completed GitHub Actions run. See [AoG integration](artofgrowing.md) for
public-source 404/cache limits, full impact audit and open native gates.

## Earlier packaging hardening evidence

The earlier recorded runs used the external .NET SDK at
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

That historical pre-AoG snapshot contained **14 artifacts** in `Releases/` (the
current catalog adds the separate AoG ZIP; see the integration evidence above):

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
