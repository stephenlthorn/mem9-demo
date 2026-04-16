#!/usr/bin/env bash
# mem9-demo runner: live + --replay + --reset + --record + --offline modes.
set -euo pipefail

MODE="${1:-live}"
cd "$(dirname "$0")"

require_env() {
  if [ ! -f .env ]; then
    echo "ERROR: .env missing. Copy .env.example and fill MNEMO_DSN." >&2
    exit 1
  fi
  set -a; . ./.env; set +a
}

ensure_mem9_clone() {
  if [ ! -d mem9 ]; then
    echo "==> Cloning mem9-ai/mem9@${MEM9_GIT_REF:-main}"
    git clone --depth 1 --branch "${MEM9_GIT_REF:-main}" https://github.com/mem9-ai/mem9 mem9
  fi
}

case "$MODE" in
  live|"")
    require_env
    ensure_mem9_clone
    echo "==> docker compose up"
    docker compose up -d --build
    echo "==> waiting for services"
    for svc in "http://localhost:8080/healthz" "http://localhost:7000/healthz"; do
      for i in $(seq 1 60); do
        curl -sf "$svc" > /dev/null && break
        sleep 1
      done
    done
    echo "==> seeding memories"
    python3 -m venv .venv 2>/dev/null || true
    . .venv/bin/activate
    pip install -q -r requirements.txt
    python seed_memories.py
    echo "==> opening booth dashboard"
    (command -v open > /dev/null && open http://localhost:7000) || true
    echo "Screens to open:"
    echo "  1) http://localhost:7000   (booth dashboard)"
    echo "  2) http://localhost:3000   (mem9 dashboard)"
    echo "  3) Claude Code + mem9 plugin (see README step 8)"
    ;;
  --replay)
    test -f recordings/demo.mp4 || { echo "no recordings/demo.mp4 - record one first"; exit 1; }
    open recordings/demo.mp4
    ;;
  --reset)
    require_env
    docker compose down -v || true
    if [ -n "${MEM9_TENANT_ID:-}" ]; then
      echo "==> tenant $MEM9_TENANT_ID removed from .env (no DELETE endpoint in upstream)"
    fi
    sed -i.bak '/^MEM9_TENANT_ID=/d; /^MEM9_PROVISION_MS=/d' .env && rm -f .env.bak
    echo "reset complete"
    ;;
  --record)
    echo "macOS: press cmd+shift+5, choose 'Record Selected Portion', save as recordings/demo.mp4."
    ;;
  --offline)
    require_env
    . .venv/bin/activate 2>/dev/null || python3 -m venv .venv && . .venv/bin/activate
    pip install -q -r booth_dashboard/requirements.txt
    (cd booth_dashboard && MEM9_TENANT_ID="${MEM9_TENANT_ID:-demo}" \
      uvicorn server:app --host 0.0.0.0 --port "${BOOTH_DASHBOARD_PORT:-7000}") &
    sleep 2
    open "http://localhost:${BOOTH_DASHBOARD_PORT:-7000}/?offline=1"
    ;;
  *)
    echo "usage: $0 [ | --replay | --reset | --record | --offline]" >&2
    exit 2
    ;;
esac
