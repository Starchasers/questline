# Packaging verification

Executed locally against the external .NET SDK at
`/home/brunette/.hermes/cache/scratch/woodworking-tutorial/dotnet/dotnet`
(version supplied for this task: 10.0.404), with `VINTAGE_STORY` pointing to the
sibling `vs` directory. No game assemblies were copied into the repository.

## RED → GREEN

1. Created `tools/packaging/test_package.py` before implementation and ran
   `python3 -m unittest discover -s tools/packaging -v`.
   **RED**: import failed because `tools/packaging/package.py` did not exist.
2. Implemented the packager; the initial **15 tests passed**.
3. Added stricter regression cases before their fixes. **RED**: 23 tests ran,
   two errors: prerelease comparison incorrectly treated `rc.10` as older than
   `rc.2`; non-string manifest `type` raised AttributeError instead of ValueError.
4. Fixed both; **23 tests passed**. Added an unowned game-assembly override
   regression: **RED** (24 tests, one assertion failure), then enforced DLL names
   from the owning csproj. Final suite: **24 tests passed**. Test DLL payloads are explicitly
   synthetic; this is not a native game integration suite.

## Actual builds and artifacts

Ran `sh ./build.sh` using the explicit SDK environment. Both the core
`questline.csproj` and `compat/toolsmith/QuestlineToolsmith.csproj` built with
**0 warnings and 0 errors**. The latter builds against its actual framework
ProjectReference. The legacy dependency-free CakeBuild launcher was also exercised
with `dotnet run --project CakeBuild/CakeBuild.csproj -- --help`.

Repeated the complete real build/package entry point twice. The resulting
`Releases/SHA256SUMS` bytes were **identical** between those two runs. Independently
opened each advertised ZIP and checked checksum, manifest, expected DLL membership,
MIT LICENSE bytes, sorted unique names, CRC, fixed timestamp and mode.

Current snapshot: **14 artifacts** in `Releases/`:

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

`git diff --check` passed at this checkpoint. Rebuild after concurrent runtime/content
changes before treating this snapshot as final. No native VsTestkit or in-game test
was run; the unavailable native harness remains a separate acceptance limitation.
Nothing was committed or published.

## Independent packaging review follow-up

Added seven regression test methods **before** implementation changes, covering
all four reported defects plus accepted-file/valid-version boundary cases.
Exact command for RED and GREEN:

```sh
python3 -m unittest discover -s tools/packaging -v
```

- **RED:** `Ran 31 tests in 0.112s`; `FAILED (failures=36)`.
  Failing subtests: six dotenv-family paths, six ordinary-file secret assignments,
  eight executable signatures, four nested floating overflow cases, and twelve
  invalid prerelease versions across manifest/dependency fields. Existing
  NaN/Infinity rejection and safe-format boundary cases already passed.
- **GREEN:** `Ran 31 tests in 0.072s`; `OK`.
- Logs: `/home/brunette/.hermes/cache/scratch/packaging-review-{red,green}.log`.

Ran an actual build/package with the same external SDK via
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
Build/package logs are `packaging-review-build.log` and
`packaging-review-only.log` in the scratch directory. Artifacts stayed outside
repository Releases; no runtime/content sources were edited by this follow-up.
Native game behavior is still not verified by packaging tests. Nothing committed
or published.
