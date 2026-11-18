# Build and deterministic mod packaging

Run `build.sh` to build the framework first, then every discovered `compat/*` code
project, and package each mod in its own ZIP. Treat `content/*` directories as
content-only mods. Add a manifest to every immediate directory under `content/`
or `compat/`; discovery uses no curated package list.

## Requirements and usage

- Install Python 3.10+. Packaging uses only the standard library, not pip or Cake.
- Install the .NET 10 SDK for code builds. Set `DOTNET` to its executable path if
  it is not on PATH.
- Install the Vintage Story SDK separately and set `VINTAGE_STORY` to its directory.
  The build checks required game assemblies before building; it never redistributes them.

```sh
export VINTAGE_STORY=/path/to/vintage-story
export DOTNET=/path/to/dotnet # optional when dotnet is on PATH
sh ./build.sh
sh ./build.sh --configuration Debug --output /path/to/artifacts
python3 -m unittest discover -s tools/packaging -v
```

Run from any working directory; the script locates the repository itself. The
legacy `dotnet run --project CakeBuild -- ...` command forwards to the same Python
entry point without Cake, Newtonsoft, or game assembly dependencies. Do not use
old Cake task names or `--skipJsonValidation`; neither is supported.
`--configuration Release` is supported. JSON validation cannot be bypassed.

To package built assemblies without a .NET/game SDK, supply **exactly one**
explicit mapping per discovered code mod. Replace these paths with actual outputs:

```sh
sh ./build.sh --package-only \
  --assembly questline=questline/bin/Release/Mods/mod/questline.dll \
  --assembly questlinetoolsmith=compat/toolsmith/bin/Release/mod/questlinetoolsmith.dll
```

Use ordinary builds for releases: package-only cannot establish assembly freshness.
Code builds use each project's actual `.csproj` and `TargetPath`, not a guessed
assembly filename. Keep exactly one code project per code-mod directory. Declare
framework references in each compat project, as in
`compat/toolsmith/QuestlineToolsmith.csproj`. Use normal MSBuild ProjectReferences
for code-to-code dependencies beyond framework-first ordering; packaging does not
create dependency relationships.

## Artifact contract

- Write `Releases/<modid>_<version>.zip` with root-level modinfo, optional modicon,
  the root MIT `LICENSE` (including the original copyright), and recursively owned
  `assets/` with legacy asset namespaces unchanged. Each code mod also contains
  exactly its built TargetPath DLL. Content archives contain no assemblies.
- Package no recursive copies of `bin`, publish folders, or test outputs. Do not
  implicitly include PDBs, game DLLs, dependencies, caches, or sources.
- Sort entries; use fixed 1980-01-01 ZIP timestamps, Unix regular-file mode 0644,
  DEFLATE level 9, and no directory entries. Read back each archive to check exact
  membership, payload bytes, and CRC before atomically replacing its named output.
- Limit `SHA256SUMS` to **this invocation's discovered artifacts**. Retain unrelated
  files and older versions in the output directory without advertising them as
  current. Replace same-name archives and SHA256SUMS.
- Validate all manifests/assets before writing archives. Each archive replacement
  is atomic; the multi-archive batch is not a transactional filesystem commit.
- Require unique lowercase alphanumeric mod IDs, three-component versions
  (optional SemVer prerelease), appropriate code/content type, and dependency maps.
  Prerelease identifiers must be nonempty ASCII alphanumeric/hyphen components;
  numeric identifiers cannot have leading zeros. Apply the same rules to dependency
  minimums. Build metadata (`+...`) is unsupported. Require every addon to declare
  `questline` and satisfy internal dependency minimum versions. Empty dependency
  versions mean any installed version, matching game modinfo conventions. Local
  validation does not check external mod availability or versions.
- Accept strict UTF-8 JSON with an optional BOM. Reject duplicate keys, comments,
  trailing commas, and non-finite numbers, including nested floating-point overflow
  such as `1e999` and `-1e999`, not just literal `NaN`/`Infinity`. Accept finite
  values such as `1e308`. Syntax checks do not establish native JSON-patch semantics
  or content gameplay correctness.
- Fail closed on unsafe/control-character names, case collisions, symlinks,
  private/generated asset paths, additional executable payloads, private key
  markers, and embedded home-directory paths. Block dotenv path components `.env`
  and `.env.*` case-insensitively in files and directories; `.environment.txt` is
  not a dotenv-family name. Reject line-oriented assignments whose variable name
  contains TOKEN, PASSWORD, SECRET, API_KEY, or ACCESS_KEY, including assignments
  with optional `export` and whitespace. Do not treat comments/prose or JSON
  gameplay `token` properties as dotenv assignments. This focused payload check
  is not a complete secret scanner or historical Git audit.
- Check executable headers regardless of filename extension: PE, ELF, and all eight
  Mach-O/thin/universal 32/64-bit byte-order signatures. Reject the shared CAFEBABE
  Java class header as unowned executable content; it does not uniquely identify
  Mach-O. Do not reject a PNG/JPEG merely because these byte sequences appear later
  in its image data.

Treat package tests as mechanics checks: their assembly bytes are **synthetic**.
Exercise actual core/compat builds separately. Neither building nor packaging proves
native client/server behavior; VsTestkit and in-game smoke tests remain separate
gates. Expect repeat ZIP bytes only for the same payload and Python/zlib
implementation, not across zlib implementations. Build output determinism also
requires a consistent SDK/compiler and unchanged sources.
