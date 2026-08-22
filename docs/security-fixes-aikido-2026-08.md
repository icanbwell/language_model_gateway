# Aikido security remediation — August 2026 batch

This documents a batch of fixes for findings from Aikido's security scan
(https://app.aikido.dev), tracked under BAI-440 / BAI-441. It follows the
same in-repo documentation pattern used for earlier Aikido remediation
passes in sibling repos (`baileyai`, `mcp-fhir-agent`, etc.) — a short
explanation of each vulnerability class and what was changed, rather than
leaving the reasoning only in a PR description.

BAI-440 covers the mechanical dependency and CI-hygiene fixes below.
BAI-441 covers the code-level and Dockerfile fixes.

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

## Leaked-secret finding: fhir-query-builder SKILL.md — false positive

Aikido flagged a possible authorization token in a curl example in
`language-model-gateway-configs/.../fhir-query-builder/SKILL.md`. The value
was already `YOUR_TOKEN_HERE` — an unambiguous placeholder, not a real
credential — in both the curl and Python example blocks. No rotation is
needed. Reworded both occurrences to `<YOUR_API_TOKEN>` for extra clarity
and to close the finding.

## Path traversal: `output_file` passed directly to `open(..., "w")`

Three near-identical findings, all in CSV/TSV export helpers:
`github_pull_request_helper.py`'s `export_results`,
`jira_issues_helper.py`'s `export_results`, and
`confluence_helper.py`'s `write_results_to_csv`. Each takes an `output_file:
str` parameter and opens it for write with no path validation.

Traced every call site: none of these methods are wired into any LangChain
tool's `args_schema` exposed to the LLM, nor into any HTTP route or CLI
entrypoint — the only callers in the codebase are unit tests passing a
hardcoded `tmp_path`-derived filename. So today `output_file` is not
caller/request-influenced at all; there is no live path-traversal path to
exploit. Per the repo's own review guidance, genuinely internal/trusted
parameters get a documenting comment rather than speculative validation —
added a comment at each `open()` call site explaining this and stating the
requirement for path-containment validation (resolve to an absolute path,
confirm it stays inside an expected base directory) if any of these
methods is ever wired to a caller-supplied path in the future (e.g. an LLM
tool parameter).

## Docker containers running as root

### `pre-commit.Dockerfile` — bind-mount-aware non-root user

This image is invoked via `docker run -v "$(pwd):/sourcecode" ...`
(`pre-commit-hook`) — a bind mount, not a copy. Naively adding the
standard non-root `USER` pattern here breaks in two ways that a plain
`docker build` won't reveal:

- `git config --global --add safe.directory` writes to *root's*
  `.gitconfig`, which the new non-root user never sees, so git fails with
  "detected dubious ownership" the moment `USER` isn't root.
- A bind mount replaces `/sourcecode`'s ownership with the *host*
  directory's ownership, not the image's build-time `chown` — so a fixed,
  arbitrary in-image UID won't match the host caller's UID, and in-place
  auto-fixer hooks (`ruff --fix`, `end-of-file-fixer`) fail with permission
  errors, silently defeating the tool.

Fixed by:
- Using `git config --system --add safe.directory` instead of `--global`
  (system config is read regardless of active user, so it survives the
  `USER` switch).
- Adding `ARG UID=1000` / `ARG GID=1000` build-args, passed from
  `pre-commit-hook` as `--build-arg UID="$(id -u)" --build-arg
  GID="$(id -g)"`.
- Switching to `USER ${UID}:${GID}` (a bare numeric UID:GID, no named
  account) instead of creating a named `appuser`/`appgroup`. A named-user
  attempt (`addgroup -g "${GID}" ... && adduser -u "${UID}" ...`) turned out
  to have a real gap: Alpine reserves low GIDs for system groups, and
  `dialout` happens to be GID 20 — which is also macOS's default non-admin
  group (`staff`). On a stock Mac, `addgroup -g 20` collides with the
  existing `dialout` group and fails; swallowing that failure (`|| true`,
  to tolerate the *host UID* already existing) silently skipped user
  creation entirely, and the container then failed outright at run time
  with `unable to find user appuser`. This was only caught by actually
  running the built image, not by a clean `docker build`. The numeric
  `USER uid:gid` form sidesteps the whole naming/collision problem — Docker
  doesn't require an `/etc/passwd` entry for it — with `HOME` set
  explicitly via `ENV` since there's no passwd entry for tools to resolve
  it from.
- Verified against the actual bind-mounted invocation, not just a clean
  `docker build`: built the image with the real host UID/GID build-args,
  bind-mounted a real git checkout with a deliberately dirty file (trailing
  whitespace) outside the container, and inside the container ran `git
  status` (no dubious-ownership error) and an in-place `sed -i` write
  (standing in for `ruff --fix`/`end-of-file-fixer`) — confirmed the fix
  landed on the host file, owned by the host user, on disk after the
  container exited.

### `inspector.Dockerfile` — chown target bug + base image

This file already had `USER appuser` at the end, but the preceding `chown`
line referenced `${PROJECT_DIR}` and `${PROMETHEUS_MULTIPROC_DIR}` —
neither defined anywhere in this file — plus a Python `site-packages` path
that doesn't exist in this Node-based image. All of that is leftover from
copying a Python service's Dockerfile without adapting it. Net effect:
`/app` (this image's actual `WORKDIR`, containing the cloned+built
inspector) was never chowned to `appuser`, so the non-root switch didn't
give the runtime user ownership of the files it needs. Fixed by chowning
the real paths this image uses (`/app`, npm's global module/bin dirs).

Also switched the base image from `node:20-alpine` (pulled directly from
Docker Hub) to the internal Root.io/JFrog ECR mirror
(`root-mirror/node:20-alpine`), consistent with the same substitution
already applied across this workspace (`baileyai-skills-service`,
`bwell-fhir-server`, `consent`, etc.) for generic language base images.

### `open-webui.Dockerfile` — non-root user; base image judgment call

No `USER` directive existed at all, so the final image ran as root. Added
a dedicated `appuser`/`appgroup` (Debian `useradd`/`groupadd`, matching
this Debian-based image) and `chown`'d the app directory before switching.
This is a long-running service image, not bind-mounted dev tooling, so —
unlike `pre-commit.Dockerfile` — a plain `USER` without UID/GID
host-alignment build-args is sufficient.

Left the base image (`ghcr.io/open-webui/open-webui:v0.8.10-slim`)
unchanged: Root.io's ECR mirror covers generic OS/language base images
(python, node, alpine, debian), not pre-built third-party application
images. There's no `root-mirror` equivalent of the open-webui project to
substitute, and grepping the rest of the workspace found no precedent for
migrating a vendor application image this way. Documented in the Dockerfile
as an explicit exception rather than guessed at, flagged for whoever owns
image-approval policy to decide if a JFrog Docker pull-through cache is
warranted for this vendor image.
