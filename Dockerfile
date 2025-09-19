# Use official Python Alpine image
FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    build-base \
    curl

COPY req.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r req.txt

COPY agents/ ./agents/

CMD ["adk", "web", "--host", "0.0.0.0", "agents/root"]
