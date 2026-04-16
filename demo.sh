#!/usr/bin/env bash
# mem9-demo runner: live + --replay + --reset + --record + --offline modes.
#
# live (default)
#   No MNEMO_DSN → hosted path: provisions via api.mem9.ai, no Docker needed.
#   MNEMO_DSN set → self-hosted path: runs mnemo-server in Docker against TiDB.
set -euo pipefail

MODE="${1:-live}"
cd "$(dirname "$0")"

# Load .env if present — not required (hosted path works without it).
load_env() {
  [ -f .env ] && { set -a; . ./.env; set +a; } || true
}

ensure_mem9_clone() {
  if [ ! -d mem9 ]; then
    echo "==> Cloning mem9-ai/mem9@${MEM9_GIT_REF:-main}"
    git clone --depth 1 --branch "${MEM9_GIT_REF:-main}" https://github.com/mem9-ai/mem9 mem9
  fi
}

install_python_deps() {
  python3 -m venv .venv 2>/dev/null || true
  . .venv/bin/activate
  pip install -q -r requirements.txt
}

case "$MODE" in
  live|"")
    load_env

    if [ -z "${MNEMO_DSN:-}" ]; then
      # ── Hosted path: api.mem9.ai (no Docker, no TiDB account needed) ──────
      echo "==> No MNEMO_DSN — using api.mem9.ai"
      install_python_deps
      pip install -q -r booth_dashboard/requirements.txt

      export MEM9_API_URL_HOST=https://api.mem9.ai
      echo "==> provisioning tenant and seeding memories"
      python seed_memories.py
      # seed_memories.py writes MEM9_TENANT_ID back to .env
      set -a; . ./.env; set +a

      echo "==> starting booth dashboard"
      lsof -ti :"${BOOTH_DASHBOARD_PORT:-7001}" | xargs kill -9 2>/dev/null || true
      (cd booth_dashboard && \
        MEM9_API_URL=https://api.mem9.ai \
        uvicorn server:app --host 0.0.0.0 --port "${BOOTH_DASHBOARD_PORT:-7001}") &

      for i in $(seq 1 30); do
        curl -sf "http://localhost:${BOOTH_DASHBOARD_PORT:-7001}/healthz" > /dev/null && break
        [ "$i" -eq 30 ] && { echo "ERROR: booth dashboard never became healthy" >&2; exit 1; }
        sleep 1
      done

      echo "==> opening booth dashboard"
      (command -v open > /dev/null && open "http://localhost:${BOOTH_DASHBOARD_PORT:-7001}") || true
      echo "Open: http://localhost:${BOOTH_DASHBOARD_PORT:-7001}   (booth dashboard)"

    else
      # ── Self-hosted path: mnemo-server in Docker against TiDB ─────────────
      ensure_mem9_clone
      echo "==> docker compose up"
      docker compose up -d --build
      echo "==> waiting for services"
      for svc in "http://localhost:8080/healthz" "http://localhost:${BOOTH_DASHBOARD_PORT:-7001}/healthz"; do
        for i in $(seq 1 60); do
          curl -sf "$svc" > /dev/null && break
          [ "$i" -eq 60 ] && { echo "ERROR: $svc never became healthy" >&2; exit 1; }
          sleep 1
        done
      done
      echo "==> seeding memories"
      install_python_deps
      python seed_memories.py
      echo "==> opening booth dashboard"
      (command -v open > /dev/null && open "http://localhost:${BOOTH_DASHBOARD_PORT:-7001}") || true
      echo "Screens to open:"
      echo "  1) http://localhost:${BOOTH_DASHBOARD_PORT:-7001}   (booth dashboard)"
      echo "  2) http://localhost:3000   (mem9 dashboard)"
      echo "  3) Claude Code + mem9 plugin (see README step 8)"
    fi
    ;;

  --replay)
    test -f recordings/demo.mp4 || { echo "no recordings/demo.mp4 - record one first"; exit 1; }
    open recordings/demo.mp4
    ;;

  --reset)
    load_env
    docker compose down -v 2>/dev/null || true
    if [ -f .env ] && grep -q 'MEM9_TENANT_ID=' .env 2>/dev/null; then
      echo "==> clearing tenant from .env"
      sed -i.bak '/^MEM9_TENANT_ID=/d; /^MEM9_PROVISION_MS=/d' .env && rm -f .env.bak
    fi
    echo "reset complete"
    ;;

  --record)
    echo "macOS: press cmd+shift+5, choose 'Record Selected Portion', save as recordings/demo.mp4."
    ;;

  --offline)
    load_env
    . .venv/bin/activate 2>/dev/null || python3 -m venv .venv && . .venv/bin/activate
    pip install -q -r booth_dashboard/requirements.txt
    lsof -ti :"${BOOTH_DASHBOARD_PORT:-7001}" | xargs kill -9 2>/dev/null || true
    (cd booth_dashboard && MEM9_TENANT_ID="${MEM9_TENANT_ID:-demo}" \
      uvicorn server:app --host 0.0.0.0 --port "${BOOTH_DASHBOARD_PORT:-7001}") &
    sleep 2
    open "http://localhost:${BOOTH_DASHBOARD_PORT:-7001}/?offline=1"
    ;;

  *)
    echo "usage: $0 [ | --replay | --reset | --record | --offline]" >&2
    exit 2
    ;;
esac
