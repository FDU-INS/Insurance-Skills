"""
test_mcp_motherduck.py — Integration tests for MCP tools against MotherDuck.

Starts the MCP server locally pointing at MotherDuck, then exercises
all key tools: reads, writes, CRUD cycle, and reference data queries.

Usage:
    .venv/bin/python3 scripts/test_mcp_motherduck.py

Environment:
    MOTHERDUCK_TOKEN must be set (via .env or shell export).

Reusable pattern: adapt this script for BioScience Agent and Vantage
by changing the tool names and test data.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

MCP_PORT = 8099  # Use a non-standard port to avoid conflicts
BASE = f"http://localhost:{MCP_PORT}/mcp"
MCP_TOKEN = os.environ.get("HEALTHSIM_MCP_TOKEN", "")
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}
if MCP_TOKEN:
    HEADERS["Authorization"] = f"Bearer {MCP_TOKEN}"


def start_server():
    """Start MCP server against MotherDuck in a subprocess."""
    token = os.environ.get("MOTHERDUCK_TOKEN")
    if not token:
        print("ERROR: MOTHERDUCK_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    env = {
        **os.environ,
        "HEALTHSIM_DB_PATH": f"md:healthsim_ref?motherduck_token={token}",
        "MCP_TRANSPORT": "http",
        "MCP_PORT": str(MCP_PORT),
    }
    proc = subprocess.Popen(
        [sys.executable, "packages/mcp-server/healthsim_mcp.py"],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        cwd=str(WORKSPACE_ROOT),
    )
    # Wait for server to be ready (406 means it's running — streamable-http
    # rejects plain GET but that proves the server is listening)
    for _ in range(30):
        try:
            r = requests.get(f"http://localhost:{MCP_PORT}/mcp", timeout=2)
            return proc  # Any response means server is up
        except requests.ConnectionError:
            time.sleep(0.5)
        except Exception:
            return proc  # 406 or other response = server is up
    print("ERROR: Server didn't start in time", file=sys.stderr)
    proc.kill()
    sys.exit(1)


def init_session():
    """Initialize an MCP session, return session ID."""
    # Retry init a few times — server may still be connecting to MotherDuck
    for attempt in range(5):
        r = requests.post(BASE, json={
            "jsonrpc": "2.0", "id": 0, "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {"name": "test_mcp_motherduck", "version": "1.0"},
            }
        }, headers=HEADERS)
        if "mcp-session-id" in r.headers:
            break
        time.sleep(1)
    sid = r.headers.get("mcp-session-id")
    if not sid:
        print(f"ERROR: No session ID. Status={r.status_code}", file=sys.stderr)
        print(f"  Body: {r.text[:300]}", file=sys.stderr)
        sys.exit(1)
    requests.post(
        BASE, json={"jsonrpc": "2.0", "method": "notifications/initialized"},
        headers={**HEADERS, "Mcp-Session-Id": sid},
    )
    return sid


def call_tool(sid, tool, args, msg_id=1):
    """Call an MCP tool, return (text, is_error)."""
    r = requests.post(BASE, json={
        "jsonrpc": "2.0", "id": msg_id, "method": "tools/call",
        "params": {"name": tool, "arguments": args}
    }, headers={**HEADERS, "Mcp-Session-Id": sid})
    for line in r.text.split("\n"):
        if line.startswith("data: "):
            data = json.loads(line[6:])
            text = data["result"]["content"][0]["text"]
            err = data["result"].get("isError", False)
            return text, err
    return r.text, True


def main():
    print("=== MotherDuck MCP Integration Tests ===\n")

    print("Starting MCP server against MotherDuck...", end=" ", flush=True)
    proc = start_server()
    print("OK\n")

    try:
        sid = init_session()
        results = {}

        # --- READ TESTS ---

        # 1. Tables
        text, err = call_tool(sid, "healthsim_tables", {}, 1)
        data = json.loads(text) if not err else {}
        n = data.get("total", 0)
        results["tables"] = "PASS" if n > 0 else "FAIL"
        print(f"  1. Tables: {n} found — {results['tables']}")

        # 2. List cohorts
        text, err = call_tool(sid, "healthsim_list_cohorts", {"params": {}}, 2)
        results["list_cohorts"] = "FAIL" if err else "PASS"
        print(f"  2. List cohorts — {results['list_cohorts']}")

        # 3. Search providers (CA)
        text, err = call_tool(sid, "healthsim_search_providers",
                              {"params": {"state": "CA", "limit": 3}}, 3)
        data = json.loads(text) if not err else {}
        n = data.get("result_count", 0)
        results["search_providers"] = "PASS" if n > 0 else "FAIL"
        print(f"  3. Search providers: {n} CA results — {results['search_providers']}")

        # 4. Search with taxonomy code
        text, err = call_tool(sid, "healthsim_search_providers",
                              {"params": {"state": "CA", "taxonomy_code": "207RC0000X", "limit": 3}}, 4)
        data = json.loads(text) if not err else {}
        n = data.get("result_count", 0)
        results["search_cardiology"] = "PASS" if n > 0 else "FAIL"
        print(f"  4. Cardiology search: {n} results — {results['search_cardiology']}")

        # 5. SQL query
        text, err = call_tool(sid, "healthsim_query",
                              {"params": {"sql": "SELECT COUNT(*) as n FROM network.providers", "limit": 1}}, 5)
        data = json.loads(text) if not err else {}
        n = data.get("rows", [{}])[0].get("n", 0) if not err else 0
        results["sql_query"] = "PASS" if n > 0 else "FAIL"
        print(f"  5. SQL query: {n:,} providers — {results['sql_query']}")

        # 6. Reference data query
        text, err = call_tool(sid, "healthsim_query_reference",
                              {"params": {"table": "svi_county", "filters": {"st_abbr": "CA"}, "limit": 3}}, 6)
        data = json.loads(text) if not err else {}
        results["query_ref"] = "PASS" if not err else "FAIL"
        print(f"  6. Query reference: {data.get('row_count', '?')} rows — {results['query_ref']}")

        # --- WRITE TESTS ---

        # 7. Write cohort
        text, err = call_tool(sid, "healthsim_add_entities", {"params": {
            "cohort_name": "md-integration-test",
            "entities": {"patients": [
                {"patient_id": "PAT-MD-001", "given_name": "Test", "family_name": "MotherDuck",
                 "birth_date": "1990-01-01", "gender": "female"}
            ]}
        }}, 7)
        results["write"] = "FAIL" if err else "PASS"
        print(f"  7. Write cohort — {results['write']}")

        # 8. Verify write
        text, err = call_tool(sid, "healthsim_list_cohorts", {"params": {}}, 8)
        results["verify_write"] = "PASS" if "md-integration-test" in text else "FAIL"
        print(f"  8. Verify write — {results['verify_write']}")

        # 9. Load cohort
        text, err = call_tool(sid, "healthsim_load_cohort",
                              {"params": {"name_or_id": "md-integration-test"}}, 9)
        data = json.loads(text) if not err else {}
        n = data.get("entity_count", 0)
        results["load"] = "PASS" if n > 0 else "FAIL"
        print(f"  9. Load cohort: {n} entities — {results['load']}")

        # 10. Delete cohort
        text, err = call_tool(sid, "healthsim_delete_cohort",
                              {"params": {"name_or_id": "md-integration-test", "confirm": True}}, 10)
        results["delete"] = "FAIL" if err else "PASS"
        print(f" 10. Delete cohort — {results['delete']}")

        # --- SUMMARY ---
        print(f"\n{'=' * 50}")
        all_pass = all(v == "PASS" for v in results.values())
        for k, v in results.items():
            icon = "✓" if v == "PASS" else "✗"
            print(f"  {icon} {k:25s} {v}")
        print(f"\nResult: {'ALL 10 PASS' if all_pass else 'FAILURES DETECTED'}")
        sys.exit(0 if all_pass else 1)

    finally:
        proc.terminate()
        proc.wait(timeout=5)


if __name__ == "__main__":
    main()
