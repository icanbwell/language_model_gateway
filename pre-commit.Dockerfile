# syntax=docker/dockerfile:1
FROM public.ecr.aws/docker/library/python:3.12-alpine3.20

# Set terminal width (COLUMNS) and height (LINES)
ENV COLUMNS=300

ARG GITHUB_TOKEN

# UID/GID of the host user invoking this image, so files written back through the
# `-v $(pwd):/sourcecode` bind mount (see pre-commit-hook) end up owned by the host
# caller instead of an in-image UID that doesn't exist on the host. Passed as
# `--build-arg UID="$(id -u)" --build-arg GID="$(id -g)"` from pre-commit-hook.
ARG UID=1000
ARG GID=1000

# Install git, build-essential, and uv
RUN apk add --no-cache git build-base
# Install uv from the official image (fast, single binary)
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /uvx /usr/local/bin/

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy pyproject.toml and uv.lock
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache \
    uv sync --frozen --all-extras --group dev --no-install-project

# Set the working directory
WORKDIR /sourcecode

# Security note (Aikido "container runs as root" finding, BAI-441): this image is run via
# `docker run -v "$(pwd):/sourcecode" ...` (see pre-commit-hook), which is a *bind* mount —
# it replaces /sourcecode's contents and ownership with the host directory's, it does not
# inherit any build-time chown. Two things follow from that, both required for the
# non-root user below to actually work against a bind mount instead of just moving the
# "runs as root" finding into a broken container:
#   1. `--system` (not `--global`) so the safe.directory entry lives in /etc/gitconfig,
#      which every user reads, and survives the USER switch below. A `--global` entry
#      would be written to root's own .gitconfig and invisible to the new non-root user.
#   2. The non-root user's UID/GID (below) must match the host caller's, via the UID/GID
#      build-args above, rather than a fixed in-image UID — otherwise its ownership of
#      /sourcecode's bind-mounted, host-owned files won't line up and auto-fixer hooks
#      (ruff --fix, end-of-file-fixer, etc.) will fail to write back with EACCES.
RUN git config --system --add safe.directory /sourcecode

# Drop to the host caller's UID:GID numerically, rather than creating a named
# `appuser`/`appgroup`. A named-user approach (`addgroup -g "${GID}" ... | adduser -u
# "${UID}" ...`) turned out to have a real gap here: Alpine reserves low GIDs for system
# groups (e.g. GID 20 is `dialout`), and macOS's default non-admin group ("staff") is also
# GID 20 — so on a stock Mac, `addgroup -g 20` collides and fails. A silently-swallowed
# failure there (`|| true`) left `appuser` never created, and the container failed outright
# at run time with "unable to find user appuser". Docker accepts a bare numeric `USER
# uid:gid` with no /etc/passwd entry at all, which sidesteps the collision entirely — set
# HOME explicitly since there's no passwd entry for tools to resolve it from.
ENV HOME=/home/appuser
RUN mkdir -p "${HOME}" && chown -R "${UID}:${GID}" "${HOME}" /opt/venv

USER ${UID}:${GID}

CMD ["pre-commit", "run", "--all-files"]
