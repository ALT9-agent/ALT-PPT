#!/bin/bash
# SessionStart hook — install the Python pipeline dependencies so extraction and
# Claude Design packaging work in Claude Code on the web. Synchronous + idempotent.
set -euo pipefail

# Web (remote) sessions only; skip locally.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

# Prefer a normal install (works in the ephemeral container); fall back to
# --break-system-packages for PEP 668 externally-managed environments.
python3 -m pip install -q -r requirements.txt \
  || python3 -m pip install -q --break-system-packages -r requirements.txt

# Let `python -m src.*` resolve from the repo root for the whole session.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PYTHONPATH="."' >> "$CLAUDE_ENV_FILE"
fi
