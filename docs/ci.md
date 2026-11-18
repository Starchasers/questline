# CI and release verification

## Pull requests and development builds

Use `.github/workflows/ci.yml` for pull requests, pushes to `main`/`master`, manual
dispatch, and release-workflow calls. Require its stable check, **Build and offline
suites**, in repository branch protection. GitHub may prefix that name with the
calling job in release runs. The workflow file cannot enable branch protection.

The Ubuntu job installs Python 3.12 and .NET SDK 10.0.302, then downloads the
Vintage Story 1.22.7 **official stable Linux server** from the existing upstream
URL convention:

```text
https://cdn.vintagestory.at/gamefiles/stable/vs_server_linux-x64_1.22.7.tar.gz
```

Use the test artifact to inspect the archive's observed SHA-256 and toolchain
versions. That checksum records the downloaded input; it is not independently
trusted or pre-pinned. Artifacts do not cache or redistribute game binaries.
To select another official server version, supply a stable semantic version to
the release workflow input, not a shell expression or URL.

Keep Git history in checkout: content extraction tests read upstream commit
`9a2fd4e2b2e24046de08c7a86aff335294558939` directly from Git objects.

### Automated gates

Run these commands from the repository root. Point `VINTAGE_STORY` to the extracted
server directory and put `dotnet` on `PATH`:

```sh
python3 -m unittest discover -s tools/packaging -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tools/lang/check.py
python3 compat/toolsmith/tests/regression.py
sh ./build.sh
dotnet run --project verification/composition/CompositionTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project verification/rewards/RewardTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
(cd Releases && sha256sum --check SHA256SUMS)
```

CI also compares ZIP names and checksum entries with every owned package's
`modinfo.json`. It requires exactly **15** packages: the framework, 13 content packs,
and optional Toolsmith adapter. Core and adapter compile against real game
assemblies; content packs are validated and packaged independently. Packages ship
no build-only fixtures, game assemblies, or external providers.

Use a clean output directory for local package-set verification. The packager
preserves unrelated files, so an old core ZIP in `Releases` correctly fails CI's
exact-set check. Alternatively, run
`sh ./build.sh --output /path/to/new-output-directory` and verify that directory.

Bash pipelines use `pipefail` to preserve failing test exit statuses. Logs upload
with `always()`, even after a gate fails, but later verification/build steps are
skipped. Do not treat a failed check as evidence that later suites ran.

### Downloadable outputs

Download these two artifacts after a successful run; retention is 14 days:

- **questline-packages**: all 15 individually installable ZIPs and `SHA256SUMS`.
- **questline-test-results**: text logs for each executed suite, build/checksum
  output, source commit, server archive checksum, and toolchain versions. These
  are not fabricated JUnit/TRX reports; executable suites use their own assertions
  and nonzero exit status.

Extract GitHub's **outer ZIP wrapper** once, then install only the selected
**inner mod ZIPs**. Do not install the wrapper or unpack mod ZIPs into one combined
mod. From the extracted package artifact directory, check integrity with
`sha256sum --check SHA256SUMS`.

## Release behavior and permissions

Use `.github/workflows/release.yml` to call the same verification job. Manual runs
only build and upload artifacts, even when run against a tag. Publishing requires
both a **push of a `v*` tag** and successful verification. Match the framework
manifest version to the tag without its leading `v`; content and adapter packages
keep their own manifest versions.

The publisher downloads verified artifacts from its own workflow run without
rebuilding. It rechecks all 15 ZIP checksums, attests every ZIP, and attaches all
15 ZIPs plus `SHA256SUMS` to the GitHub release. It then reads back all 16 release
assets, downloads them again, and checks their hashes against the verified checksum
file. Release notes include checksums and recorded build inputs. The publisher
refuses to overwrite an existing release; it never silently replaces assets.
The trusted tag publisher checks out metadata only and does not execute repository
build/test scripts with a write token.

Keep PR/build jobs at explicit `contents: read`, with no secrets or persisted
checkout credentials. Only the tag publisher receives `contents: write`,
`id-token: write`, and `attestations: write`. Actions are pinned to verified
upstream release commit SHAs. Neither `pull_request_target` nor a privileged
workflow-run consumer executes PR code.

## Remote setup and remaining acceptance

- Enable GitHub Actions and permit the pinned official `actions/*` actions under
  repository/organization policy. Obtain maintainer approval for fork pull
  requests when required.
- Require **Build and offline suites** in branch protection/rulesets after its
  first run. Restrict release tag creation to trusted maintainers.
- Enable GitHub's OIDC/attestation service and required repository support/policy
  for artifact provenance, especially in private repositories. Ensure organization
  policy permits release creation. Local tests do not exercise these services or policies.
- Give runners access to the official server CDN, .NET downloads, NuGet, and GitHub
  artifact services. Treat an unavailable official SDK download as a CI failure;
  never substitute synthetic game assemblies.
- Run native acceptance separately. Offline gates do **not execute** native
  VsTestkit tests in `tests/questline.tests.csproj`; this repository supplies neither
  a supported VsTestkit/runtime nor real providers. Synthetic Toolsmith checks do
  not prove the real provider ABI, in-world player attribution, or save/reload
  behavior. Follow `compat/toolsmith/README.md` for native acceptance. Also complete
  reward gameplay, persistence, and multiplayer acceptance before claiming native readiness.
- Verify the exact PR-head run and its downloadable artifacts on GitHub before
  calling remote CI setup complete. A green local run validates commands and
  package bytes, not hosted action execution, upload/download behavior, branch
  protection, or release permissions.
