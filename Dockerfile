# Multi-stage Dockerfile for Greenville Infrastructure Lakehouse
# Stage 1: Pipeline Builder & Model Executor
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt* ./
RUN pip install --no-cache-dir pydantic pytest

# Copy source code and test suite
COPY src/ ./src/
COPY tests/ ./tests/
COPY greenville_infrastructure_pipeline.md ./
COPY pytest.ini ./

# Execute full Medallion pipeline (Bronze -> Silver -> Gold) and build dashboard
RUN python src/processing/delta_lakehouse.py && \
    python src/visualization/build_dashboard.py && \
    mkdir -p /app/docs && \
    cp -r data/gold/* /app/docs/ || true

# Stage 2: Ultra-Lightweight Production Runtime
FROM python:3.11-alpine AS runtime

WORKDIR /app

# Create non-root security user (CIS / DoD DevSecOps standard)
RUN addgroup -g 10001 lakehouse && \
    adduser -u 10001 -G lakehouse -s /bin/sh -D lakehouse

# Copy compiled dashboard and gold artifacts from builder
COPY --from=builder --chown=lakehouse:lakehouse /app/docs /app/docs
COPY --from=builder --chown=lakehouse:lakehouse /app/data/gold /app/data/gold

USER 10001:10001

EXPOSE 8810

# Serve dashboard on port 8810
CMD ["python", "-m", "http.server", "8810", "--directory", "/app/docs"]
