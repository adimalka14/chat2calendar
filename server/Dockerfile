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
    apt-get install -y --no-install-recommends curl build-essential bash && \
    rm -rf /var/lib/apt/lists/*

# ===== Install Poetry =====
RUN curl -sSL https://install.python-poetry.org | python - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# ===== Install Python deps with Poetry =====
# Copy only dependency files first for better build cache
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-ansi --no-interaction --no-root

# ===== Copy project code =====
COPY . .

# ===== Install root package =====
RUN poetry install --no-ansi --no-interaction

# ===== Copy entrypoint script =====
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# ===== Expose & run =====
EXPOSE 8000

# Use PORT env var if set, otherwise default to 8000
# Render and other platforms set $PORT
CMD ["/docker-entrypoint.sh"]
