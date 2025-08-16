# ---------- builder: compile wheels ----------
FROM python:3.10-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /wheels

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir=/wheels/wheels -r requirements.txt

# ---------- final: production image ----------
FROM python:3.10-slim AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only wheels and requirements.txt first
COPY --from=builder /wheels/wheels /wheels/wheels
COPY requirements.txt .

# Install from wheels and remove wheel files & pip cache in the same RUN
RUN python -m pip install --upgrade pip && \
    pip install --no-index --no-cache-dir --find-links=/wheels/wheels -r requirements.txt && \
    rm -rf /wheels/wheels /root/.cache/pip

COPY . .

EXPOSE 8003

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8003"]
