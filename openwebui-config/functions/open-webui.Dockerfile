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

# Security fix (Aikido "container runs as root", BAI-441): this is a long-running service
# image, not dev tooling invoked with a bind mount, so a plain non-root USER (without the
# UID/GID host-alignment build-args used in pre-commit.Dockerfile) is sufficient here — see
# the "non-root-user-breaks-bind-mounted-dev-tooling-images" caveat for why that distinction
# matters. Give appuser ownership of the app/cache directories written above before
# dropping out of root.
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser \
    && chown -R appuser:appgroup /app

USER appuser