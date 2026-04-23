#!/usr/bin/env bash
# BuildAI Database Query — read-only SQL executor
# Usage: query.sh "SELECT * FROM projects LIMIT 5"
#
# Environment:
#   DB_HOST (default: /var/run/postgresql)
#   DB_PORT (default: 5432)
#   DB_NAME (default: buildai_demo)
#   DB_USER (default: $USER)
#   DB_PASSWORD (optional)

set -euo pipefail

SQL="${1:-}"

if [ -z "$SQL" ]; then
  echo '{"error": "No SQL query provided. Usage: query.sh \"SELECT ...\""}' >&2
  exit 1
fi

# ── Safety check: only allow SELECT/WITH ──────────────────────────
# Normalize: strip leading whitespace, collapse spaces
NORMALIZED=$(echo "$SQL" | sed 's/^[[:space:]]*//' | tr '[:lower:]' '[:upper:]')
FIRST_WORD=$(echo "$NORMALIZED" | awk '{print $1}')

if [ "$FIRST_WORD" != "SELECT" ] && [ "$FIRST_WORD" != "WITH" ]; then
  echo '{"error": "Only SELECT and WITH (CTE) queries are allowed. Rejected: '"$FIRST_WORD"'"}' >&2
  exit 1
fi

# Check for dangerous keywords anywhere in the query
DANGEROUS_PATTERN='\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|EXEC)\b'
if echo "$SQL" | grep -iEq "$DANGEROUS_PATTERN"; then
  echo '{"error": "Query contains prohibited keywords (INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/CREATE/GRANT/REVOKE/EXEC)"}' >&2
  exit 1
fi

# ── Database connection ───────────────────────────────────────────
DB_HOST="${DB_HOST:-/var/run/postgresql}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-buildai_demo}"
DB_USER="${DB_USER:-$(whoami)}"

# Build connection string
export PGHOST="$DB_HOST"
export PGPORT="$DB_PORT"
export PGDATABASE="$DB_NAME"
export PGUSER="$DB_USER"
if [ -n "${DB_PASSWORD:-}" ]; then
  export PGPASSWORD="$DB_PASSWORD"
fi

# ── Execute query with timeout ────────────────────────────────────
# Use psql with JSON output format
# -t = tuples only (no header/footer)
# -A = unaligned output
# --csv for CSV output, then we convert
# Actually, let's use psql's JSON capabilities

# First, wrap the query to return JSON
JSON_QUERY="SELECT json_agg(row_to_json(t)) AS result FROM ($SQL) t;"

RESULT=$(timeout 30 psql -t -A -c "$JSON_QUERY" 2>&1) || {
  EXIT_CODE=$?
  if [ $EXIT_CODE -eq 124 ]; then
    echo '{"error": "Query timed out (30 second limit)"}' >&2
    exit 1
  fi
  echo "{\"error\": \"SQL execution failed: $(echo "$RESULT" | tr '"' "'" | tr '\n' ' ')\"}" >&2
  exit 1
}

# Handle null result (empty result set)
if [ -z "$RESULT" ] || [ "$RESULT" = "null" ] || [ "$RESULT" = "" ]; then
  echo '{"rows": [], "rowCount": 0}'
  exit 0
fi

# Output the result
ROW_COUNT=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d) if isinstance(d,list) else 0)" 2>/dev/null || echo "0")
echo "{\"rows\": $RESULT, \"rowCount\": $ROW_COUNT}"
