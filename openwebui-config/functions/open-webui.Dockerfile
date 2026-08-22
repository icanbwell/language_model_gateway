# Stage 1: Download models
# https://github.com/open-webui/open-webui/releases
#
# Base image note (Aikido "use root images from our repositories", BAI-441): unlike the
# python/node base images elsewhere in this workspace (root-mirror/python:*,
# root-mirror/node:*), Root.io's ECR mirror covers generic OS/language base images, not
# pre-built third-party application images like open-webui — there is no root-mirror
# equivalent of this image to switch to. Treated as a documented exception rather than
# fixed here; flagged for whoever owns image-approval policy to decide whether a JFrog
# Docker pull-through cache should be set up for this vendor image.
FROM ghcr.io/open-webui/open-webui:v0.8.10-slim AS model-downloader

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install sentence-transformers faster-whisper tiktoken

RUN python -c "import os; from sentence_transformers import SentenceTransformer; SentenceTransformer(os.environ['RAG_EMBEDDING_MODEL'], device='cpu')" && \
    python -c "import os; from faster_whisper import WhisperModel; WhisperModel(os.environ['WHISPER_MODEL'], device='cpu', compute_type='int8', download_root=os.environ['WHISPER_MODEL_DIR'])" && \
    python -c "import os; import tiktoken; tiktoken.get_encoding(os.environ['TIKTOKEN_ENCODING_NAME'])"

# Stage 2: Final image
FROM ghcr.io/open-webui/open-webui:v0.8.10-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install sentence-transformers faster-whisper tiktoken

# Copy models and cache folders from the builder stage
COPY --from=model-downloader /app/backend/data/cache/embedding/models /app/backend/data/cache/embedding/models
COPY --from=model-downloader /app/backend/data/cache/whisper/models /app/backend/data/cache/whisper/models
COPY --from=model-downloader /app/backend/data/cache/tiktoken /app/backend/data/cache/tiktoken

RUN ls -halt /app/backend/data/cache/embedding/models && \
    ls -halt /app/backend/data/cache/whisper/models && \
    ls -halt /app/backend/data/cache/tiktoken

# Security fix (Aikido "container runs as root", BAI-441): unlike pre-commit.Dockerfile,
# this image IS also used with real bind mounts in local dev (see
# docker-compose-openwebui.yml: `~/.aws:/home/appuser/.aws:ro` for S3 credential discovery
# and `./caches/open-webui-models:/app/backend/data/cache` for the model cache), so the same
# UID/GID host-alignment this repo already uses for pre-commit.Dockerfile applies here too --
# a fixed in-image UID wouldn't match the host caller's UID for either bind-mounted path.
# Passed as `--build-arg UID="$(id -u)" --build-arg GID="$(id -g)"` by docker-compose-openwebui.yml.
ARG UID=1000
ARG GID=1000
ENV HOME=/home/appuser
RUN mkdir -p "${HOME}" && chown -R "${UID}:${GID}" "${HOME}" /app

USER ${UID}:${GID}