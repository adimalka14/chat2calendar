#!/bin/bash
set -e

# Use PORT env var if set, otherwise default to 8000
PORT=${PORT:-8000}

echo "Starting Chat2Calendar server on port $PORT..."

# Run uvicorn with poetry
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port "$PORT"

