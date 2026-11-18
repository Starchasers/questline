# Build and deterministic mod packaging

`build.sh` builds the framework first, then every discovered `compat/*` code project,
and produces one independent ZIP per mod. `content/*` directories are content-only
mods. Every immediate directory under `content/` or `compat/` must have a manifest;
there is no curated list to forget when adding a package.

## Requirements and usage

- Python 3.10+ (standard library only; no pip or Cake dependencies).
- .NET 10 SDK for code builds. Set `DOTNET` to an executable path if it is not on PATH.
- A separately installed Vintage Story SDK; set `VINTAGE_STORY` to its directory.
  Required game assemblies are checked before building and never redistributed.

```sh
export VINTAGE_STORY=/path/to/vintage-story
export DOTNET=/path/to/dotnet # optional when dotnet is on PATH
sh ./build.sh
sh ./build.sh --configuration Debug --output /path/to/artifacts
python3 -m unittest discover -s tools/packaging -v
```

The script locates the repository independently of the caller's working directory.
The legacy `dotnet run --project CakeBuild -- ...` invocation forwards to the same
Python entry point without Cake, Newtonsoft, or game assembly dependencies.
Old Cake task names and `--skipJsonValidation` are intentionally not supported;
`--configuration Release` remains supported. JSON validation cannot be bypassed.

To package already-built assemblies without a .NET/game SDK, provide **exactly one**
explicit mapping for each discovered code mod (use actual output paths):

```sh
sh ./build.sh --package-only \
  --assembly questline=questline/bin/Release/Mods/mod/questline.dll \
  --assembly questlinetoolsmith=compat/toolsmith/bin/Release/mod/questlinetoolsmith.dll
```

This mode cannot establish assembly freshness; ordinary builds are the release default.
Code projects are built using their actual `.csproj` and `TargetPath`, not a guessed
assembly filename. Compat projects must declare their own framework reference, as
`compat/toolsmith/QuestlineToolsmith.csproj` does. Only one code project is allowed
in each code-mod directory. Code-to-code dependencies beyond the framework-first
order must use normal MSBuild ProjectReferences; packaging does not invent them.

## Artifact contract

- Names: `Releases/<modid>_<version>.zip`; root-level modinfo, optional modicon,
  root MIT `LICENSE` (including the original copyright), and recursively owned
  `assets/` preserving legacy asset namespaces. Code mods additionally contain
  exactly their built TargetPath DLL. Content archives contain no assemblies.
- There is no recursive copying of `bin`, publish folders, or test outputs. PDBs,
  game DLLs, dependencies, caches and sources are not implicitly packaged.
- Sorted entries, fixed 1980-01-01 ZIP timestamps, Unix regular-file mode 0644,
  DEFLATE level 9, no directory entries. Every archive is read back to check exact
  membership, payload bytes and CRC before atomically replacing its named output.
- `SHA256SUMS` describes **only this invocation's discovered artifacts**. Unrelated
  files and older versions in the output directory are retained, not silently
  deleted or advertised as current. Same-name archives and SHA256SUMS are replaced.
- All manifests/assets are validated before archive writes. Each archive replacement
  is atomic; the whole multi-archive batch is not a transactional filesystem commit.
- Manifests require unique lowercase alphanumeric mod IDs, three-component versions
  (optional SemVer prerelease), appropriate code/content type and dependency maps.
  Prerelease identifiers must be nonempty ASCII alphanumeric/hyphen components;
  numeric identifiers cannot have leading zeros. The same validation applies to
  dependency minimums. Build metadata (`+...`) remains unsupported. Every
  addon must declare `questline`. Internal dependency minimum versions must be
  satisfied. Empty dependency versions mean any installed version, matching game
  modinfo conventions. External mod availability/versions are not verified locally.
- JSON is strict UTF-8 (optional BOM): duplicate keys, comments, trailing commas and
  non-finite numbers are rejected, including nested floating-point overflow such as
  `1e999` and `-1e999`, not just literal `NaN`/`Infinity`. Finite values such as
  `1e308` remain valid. Native JSON-patch semantics and content gameplay
  correctness are not inferred from syntax checks.
- Unsafe/control-character names, case collisions, symlinks, private/generated
  asset paths, additional executable payloads, private key markers and embedded
  home-directory paths fail closed. Dotenv path components `.env` and `.env.*`
  are blocked case-insensitively (files and directories); `.environment.txt` is not
  a dotenv-family name. Line-oriented assignments containing TOKEN, PASSWORD,
  SECRET, API_KEY or ACCESS_KEY in the variable name are rejected, including
  optional `export` and whitespace. Comments/prose and JSON gameplay `token`
  properties are not mistaken for dotenv assignments. This focused payload check
  is not a complete secret scanner or historical Git audit.
- Executable headers include PE, ELF and all eight Mach-O/thin/universal 32/64-bit
  byte-order signatures, independent of filename extension. The shared CAFEBABE
  Java class header is also rejected as unowned executable content, not claimed
  to uniquely identify Mach-O. Header matching does not reject a PNG/JPEG merely
  because it contains one of these byte sequences later in its image data.

The package tests use **synthetic** assembly bytes and verify mechanics only. Actual
core/compat builds must be exercised separately. Neither building nor packing proves
native client/server behavior; VsTestkit and in-game smoke tests are separate gates.
Repeat ZIP bytes are guaranteed for the same payload and Python/zlib implementation;
cross-zlib compressed byte identity is not promised. Build output determinism also
depends on the SDK/compiler and unchanged sources.
