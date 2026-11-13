# syntax=docker/dockerfile:1
FROM python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5
WORKDIR /app
COPY . /app
# One installation layer also avoids excessive copies with the VFS storage driver.
RUN --mount=type=secret,id=proxy_ca \
    set -eu; \
    if [ -f /run/secrets/proxy_ca ]; then export PIP_CERT=/run/secrets/proxy_ca; fi; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      build-essential pkg-config libcairo2-dev libpango1.0-dev ffmpeg \
      texlive-latex-extra texlive-fonts-recommended texlive-science dvisvgm fonts-dejavu-core; \
    pip install --no-cache-dir -r requirements.lock; \
    pip install --no-deps --no-build-isolation -e .; \
    useradd -m -u 1000 animator; \
    rm -rf /var/lib/apt/lists/*; \
    fc-match 'DejaVu Sans'; latex --version; dvisvgm --version; ffmpeg -version
USER animator
ENV PYTHONPATH=/app/src:/app
ENTRYPOINT ["python", "-m", "rendering.cli"]
CMD ["integration", "--mode", "preview"]
