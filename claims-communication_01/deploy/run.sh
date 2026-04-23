#!/bin/bash
# Convenience wrapper for starting a HealthSim Managed Agent session.
# Usage:
#   ./deploy/run.sh                          # new session
#   ./deploy/run.sh --session sesn_01abc     # resume session
#   ./deploy/run.sh --fresh                  # recreate agent/env/vault

set -e
cd "$(dirname "$0")/.."
source .env
.venv/bin/python3 deploy/start-session.py "$@"
