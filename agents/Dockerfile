# ---------- Stage 1: Builder ----------
FROM python:3.13-alpine AS builder

WORKDIR /app

# Install build dependencies (only in builder)
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base

# Upgrade pip and install dependencies into isolated folder
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Stage 2: Final runtime ----------
FROM python:3.13-alpine

WORKDIR /app

# Install only runtime dependencies
RUN apk add --no-cache \
    libffi \
    openssl

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy agent code
COPY agents/ ./agents/

WORKDIR /app/agents

EXPOSE 8080
# Run agent via ADK CLI
# CMD ["adk", "web", "--host", "0.0.0.0", "agents", "--allow_origins", "*"]
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "--allow_origins", "*"]

