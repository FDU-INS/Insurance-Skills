#!/usr/bin/env bash
# connect-apps/scripts/setup.sh — Build and verify the connect-apps MCP plugin
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")/../../.." && pwd)/connect-apps-plugin"

echo "==> Installing dependencies..."
cd "$PLUGIN_DIR"
npm install --silent

echo "==> Building TypeScript..."
npm run build

echo "==> Verifying output..."
if [[ -f dist/index.js ]]; then
  echo "✓ dist/index.js exists"
else
  echo "✗ Build failed — dist/index.js not found"
  exit 1
fi

echo ""
echo "==> Plugin ready. Launch with:"
echo "    claude --plugin-dir ./connect-apps-plugin"
