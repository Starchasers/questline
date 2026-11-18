# CI and release verification

## Pull requests and development builds

`.github/workflows/ci.yml` runs on pull requests, pushes to `main`/`master`,
manual dispatch, and calls from the release workflow. The stable check name is
**Build and offline suites** (GitHub may prefix it with the calling job for a
release run). Configure the normal PR check as required in repository branch
protection; a workflow file alone cannot enable branch protection.

The Ubuntu job installs Python 3.12 and .NET SDK 10.0.302, then downloads the
Vintage Story 1.22.7 **official stable Linux server**, using the existing upstream
URL convention:

```text
https://cdn.vintagestory.at/gamefiles/stable/vs_server_linux-x64_1.22.7.tar.gz
```

The archive's observed SHA-256 and toolchain versions are recorded in the test
artifact. This records the downloaded build input; it is not an independently
trusted, pre-pinned SDK checksum. We do not cache or redistribute game binaries
inside the artifacts. A stable semantic-version-only release workflow input can
select a different official server version; it is not a shell expression or URL.

Checkout includes Git history because the content extraction tests read upstream
commit `9a2fd4e2b2e24046de08c7a86aff335294558939` directly from Git objects.

### Automated gates

Commands below run from the repository root with `VINTAGE_STORY` pointing to the
extracted server directory and `dotnet` on `PATH`:

```sh
python3 -m unittest discover -s tools/packaging -v
python3 -m unittest discover -s tests -p 'test_content_extraction.py' -v
python3 tools/lang/check.py
python3 compat/toolsmith/tests/regression.py
sh ./build.sh
dotnet run --project verification/composition/CompositionTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project verification/rewards/RewardTests.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
dotnet run --project compat/toolsmith/tests/AdapterChecks.csproj -c Release -p:VINTAGE_STORY="$VINTAGE_STORY"
(cd Releases && sha256sum --check SHA256SUMS)
```

CI additionally compares ZIP names and checksum entries to every owned package's
`modinfo.json`, requiring exactly **14**: framework, 12 content packs, and optional
Toolsmith adapter. The core and adapter compile against real game assemblies;
content packs are independently validated and packaged. No build-only fixture,
game assembly, or external provider is shipped.

Use a clean output directory for local package-set verification. The packager
intentionally preserves unrelated output files, so an old core ZIP in `Releases`
will correctly fail CI's exact-set check. A local alternative is
`sh ./build.sh --output /path/to/new-output-directory` and verifying that directory.

Bash pipelines preserve failing test exit statuses (`pipefail`); logs are uploaded
with `always()` even when a gate fails. Later verification/build steps are skipped
after a failure. A failed check is not evidence that those later suites ran.

### Downloadable outputs

Successful runs upload two artifacts, retained for 14 days:

- **questline-packages**: all 14 individually installable ZIPs and `SHA256SUMS`.
- **questline-test-results**: text logs for each executed suite, build/checksum
  output, source commit, server archive checksum, and toolchain versions. Logs are
  not fabricated JUnit/TRX reports: the executable suites use their own assertions
  and nonzero exit status.

GitHub's artifact download is an **outer ZIP wrapper**. Extract that wrapper once;
install only the selected **inner mod ZIPs**. Do not install the wrapper itself,
and do not unpack individual mod ZIPs into one combined mod. Check integrity with
`sha256sum --check SHA256SUMS` from the extracted package artifact directory.

## Release behavior and permissions

`.github/workflows/release.yml` calls the exact same verification job. A manual
run only builds and uploads artifacts, including when manually run against a tag.
Only a **push of a `v*` tag**, after successful verification, can publish. The
framework manifest version must equal the tag without the leading `v`; content
and adapter packages retain their own manifest versions.

The publisher downloads the verified artifacts from its own workflow run (no
rebuild), rechecks all 14 ZIP checksums, attests every ZIP, then attaches all 14
ZIPs and `SHA256SUMS` to the GitHub release. The publisher reads back all 15
release assets, downloads them again, and checks their hashes against the verified
checksum file. Notes include checksums and recorded build inputs. It refuses to overwrite an existing release rather than replacing
assets silently. The trusted tag publisher checks out metadata only; it does not
execute repository build/test scripts with a write token.

PR/build jobs have explicit `contents: read` only, no secrets and no persisted
checkout credentials. Only the tag publisher receives `contents: write`,
`id-token: write`, and `attestations: write`. Action versions are pinned to verified
upstream release commit SHAs. No `pull_request_target` or privileged workflow-run
consumer executes PR code.

## Remote setup and remaining acceptance

- Enable GitHub Actions and allow the pinned official `actions/*` actions under
  repository/organization policy. Fork pull requests may need maintainer approval.
- Require **Build and offline suites** in branch protection/rulesets after its first
  run; protect release tag creation so only trusted maintainers can publish.
- Artifact provenance needs GitHub's OIDC/attestation service and appropriate
  repository support/policy (especially for private repositories). Release creation
  must be allowed by organization policy. These are not exercised by local tests.
- Runners require access to the official server CDN, .NET downloads, NuGet, and
  GitHub artifact services. An unavailable official SDK download is a real CI
  failure, not permission to substitute synthetic game assemblies.
- Native VsTestkit tests in `tests/questline.tests.csproj` are **not executed** by
  these offline gates. A supported VsTestkit/runtime and real providers are not
  supplied by this repository. The synthetic Toolsmith checks do not prove the
  real provider ABI, player attribution in-world, or save/reload behavior. Follow
  `compat/toolsmith/README.md` for native acceptance; also complete reward gameplay,
  persistence, and multiplayer acceptance before claiming native readiness.
- A green local run validates commands and package bytes, not hosted action
  execution, upload/download behavior, branch protection, or release permissions.
  Verify the exact PR-head run and its downloadable artifacts on GitHub before
  treating remote CI setup as complete.
