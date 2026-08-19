# Aikido security remediation — August 2026 batch

This documents a batch of fixes for findings from Aikido's security scan
(https://app.aikido.dev), tracked under BAI-440 / BAI-441. It follows the
same in-repo documentation pattern used for earlier Aikido remediation
passes in sibling repos (`baileyai`, `mcp-fhir-agent`, etc.) — a short
explanation of each vulnerability class and what was changed, rather than
leaving the reasoning only in a PR description.

This PR (BAI-440) covers the mechanical dependency and CI-hygiene fixes.
Code-level and Dockerfile fixes (path-handling review, non-root containers,
a documentation-example secret review) are in a follow-up PR tracked under
BAI-441, appended to this same file there.

## Dependency CVEs (`uv.lock`)

Mechanical `uv lock --upgrade-package <name>==<version>` bumps to the exact
patched versions Aikido flagged, re-resolved and verified against the test
suite:

| Package | From | To | Severity | Aikido ID(s) |
|---|---|---|---|---|
| anyio | 4.14.1 | 4.14.2 | Critical | AIKIDO-2026-889297 |
| huggingface-hub | 1.21.0 | 1.26.0 | High | AIKIDO-2026-587816 |
| aiohttp | 3.14.1 | 3.14.3 | High | AIKIDO-2026-168095, CVE-2026-69244, CVE-2026-59881, CVE-2026-69243 |
| transformers | 5.12.1 | 5.14.0 | Medium | AIKIDO-2026-295187, AIKIDO-2026-614493 |
| yarl | 1.24.2 | 1.24.5 | Medium | AIKIDO-2026-472816 |
| langsmith | 0.9.7 | 0.10.9 | Medium | AIKIDO-2026-890022, AIKIDO-2026-944829 |
| requests | 2.33.1 | 2.34.0 | Medium | AIKIDO-2026-106840 |
| h2 | 4.3.0 | 4.4.1 | Medium | CVE-2026-71554 |

No `pyproject.toml` constraint changes were required — the existing version
ranges already permitted these patched releases. Pinning to the exact
patched version (rather than a wider range) follows the workspace-wide
`pin-exact-patched-versions` convention: Root.io/Aikido use a `+aikido.N`
local-version label scheme that can sort unpredictably against a range
resolution, so an exact `==` pin is safer here too, and `uv lock
--upgrade-package` already resolves to an exact version in the lockfile.

## GitHub Actions: unpinned third-party action

`.github/workflows/build_and_test.yml` referenced
`pmeier/pytest-results-action@main` — a floating branch reference. Unlike a
version tag, `@main` re-resolves to whatever the latest commit on that
branch is at run time; if the upstream branch is compromised, force-pushed,
or the repo ownership changes, the next CI run would silently execute
different, unreviewed code with access to this repo's CI runner (secrets,
checkout contents, etc.).

Fixed by pinning to the immutable commit SHA behind the current `v0.9.0`
release tag (`fdc7f18d9934e38aca411ca9557e6577bd25ca9c`), with the version
kept as a trailing comment for readability. This is the standard
GitHub-recommended mitigation for third-party actions
(see `actions/checkout`, `actions/setup-python`, etc. in the same workflow,
which are already pinned to version tags — `@main` was the one outlier).
