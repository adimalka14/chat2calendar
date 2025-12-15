# ===== Base image =====
FROM python:3.9-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# ===== Install Poetry =====
RUN curl -sSL https://install.python-poetry.org | python - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# ===== Install Python deps with Poetry =====
# Copy only dependency files first for better build cache
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-ansi --no-interaction --no-root

# ===== Copy project code =====
COPY . .

# ===== Expose & run =====
EXPOSE 8000

# Render sets $PORT, locally - 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
