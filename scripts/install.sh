#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[ERROR] Missing command: $1"
    exit 1
  fi
}

if [[ ! -f "$ENV_FILE" ]]; then
  cp "$ROOT_DIR/.env.example" "$ENV_FILE"
  python3 - <<'PY' "$ENV_FILE"
from pathlib import Path
import secrets
import sys
path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
text = text.replace('replace-with-a-very-long-random-secret-key-32-chars-min', secrets.token_urlsafe(48))
text = text.replace('change-this-db-password', secrets.token_urlsafe(24))
text = text.replace('change-this-n8n-password', secrets.token_urlsafe(20))
path.write_text(text, encoding='utf-8')
PY
  echo "[INFO] Created .env. Fill BOT_TOKEN before first launch."
fi

require_command docker
if ! docker compose version >/dev/null 2>&1; then
  echo "[ERROR] docker compose plugin is required"
  exit 1
fi

mkdir -p "$ROOT_DIR/.data/uploads"

echo "[INFO] Starting stack"
docker compose -f "$ROOT_DIR/docker-compose.yml" up --build -d

echo "[OK] Stack is running"
echo "API: http://<server-ip>/docs"
echo "n8n: http://<server-ip>:5678"
