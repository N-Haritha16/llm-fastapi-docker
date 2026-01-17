# Stage 1: build
FROM python:3.10-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use PyPI as main index, and add PyTorch CPU wheels as extra index
RUN pip install --default-timeout=1000 --no-cache-dir --prefix=/install \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt


# Stage 2: runtime
FROM python:3.10-slim
WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
