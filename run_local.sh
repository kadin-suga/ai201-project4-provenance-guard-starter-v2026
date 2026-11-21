#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_dir"

if [[ ! -f .env ]]; then
  echo "Missing .env. Copy .example.env to .env and fill in PostgreSQL values." >&2
  exit 1
fi
if [[ ! -x .venv/bin/python || ! -x .venv/bin/gunicorn ]]; then
  echo "Missing .venv dependencies. Follow RUNNING.md once before starting." >&2
  exit 1
fi

docker compose up -d --wait postgres redis
set -a
source .env
set +a

.venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 1 app:app &
api_pid=$!
.venv/bin/python worker.py &
worker_pid=$!

cleanup() {
  kill "$api_pid" "$worker_pid" 2>/dev/null || true
  wait "$api_pid" "$worker_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Provenance Guard is running at http://127.0.0.1:5000"
echo "Press Ctrl-C to stop the API and worker; PostgreSQL and Redis remain running."

wait "$api_pid"
