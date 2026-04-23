"""
start-session.py — Create a HealthSim Managed Agent session and interact with it.

Creates an agent, environment, vault, and session on first run.
Saves IDs to deploy/agent-ids.json for reuse.

Usage:
    .venv/bin/python3 deploy/start-session.py
    .venv/bin/python3 deploy/start-session.py --fresh   # recreate agent/env/vault

Environment:
    ANTHROPIC_API_KEY, HEALTHSIM_MCP_TOKEN must be set (via .env).
"""

import json
import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Load config
WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

AGENT_IDS_FILE = Path(__file__).parent / "agent-ids.json"
SKILL_IDS_FILE = Path(__file__).parent / "skill-ids.json"
RAILWAY_URL_FILE = Path(__file__).parent / "railway-url.txt"

MCP_TOKEN = os.environ.get("HEALTHSIM_MCP_TOKEN", "")


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2) + "\n")


def get_railway_url() -> str:
    if not RAILWAY_URL_FILE.exists():
        print("ERROR: deploy/railway-url.txt not found", file=sys.stderr)
        sys.exit(1)
    return RAILWAY_URL_FILE.read_text().strip()


def setup(client: anthropic.Anthropic, fresh: bool = False) -> dict:
    """Create or load agent, environment, and vault."""
    ids = {} if fresh else load_json(AGENT_IDS_FILE)
    skill_ids = load_json(SKILL_IDS_FILE)
    railway_url = get_railway_url()

    # Build skill references (all uploaded custom skills)
    skills = [
        {"type": "custom", "skill_id": sid, "version": "latest"}
        for sid in skill_ids.values()
    ]

    # MCP endpoint — append /mcp for streamable-http path
    mcp_url = railway_url.rstrip("/") + "/mcp"

    if "agent_id" not in ids:
        print("Creating agent...")
        agent = client.beta.agents.create(
            name="HealthSim Spike",
            model="claude-sonnet-4-6",
            system=(
                "You are HealthSim, a synthetic healthcare data generation platform. "
                "You can generate realistic patient cohorts, claims data, clinical trial "
                "data, and provider networks. Use the healthsim MCP tools to query "
                "reference data and manage cohorts. Be helpful and precise."
            ),
            tools=[
                {"type": "agent_toolset_20260401", "default_config": {"enabled": True}},
                {
                    "type": "mcp_toolset",
                    "mcp_server_name": "healthsim-mcp",
                    "default_config": {
                        "enabled": True,
                        "permission_policy": {"type": "always_allow"},
                    },
                },
            ],
            skills=skills,
            mcp_servers=[
                {"type": "url", "name": "healthsim-mcp", "url": mcp_url},
            ],
        )
        ids["agent_id"] = agent.id
        ids["agent_version"] = agent.version
        print(f"  Agent: {agent.id} (version {agent.version})")
    else:
        print(f"  Agent: {ids['agent_id']} (cached)")

    if "environment_id" not in ids:
        print("Creating environment...")
        env = client.beta.environments.create(
            name="healthsim-spike-env",
            config={
                "type": "cloud",
                "networking": {"type": "unrestricted"},
            },
        )
        ids["environment_id"] = env.id
        print(f"  Environment: {env.id}")
    else:
        print(f"  Environment: {ids['environment_id']} (cached)")

    if "vault_id" not in ids:
        print("Creating vault + MCP credential...")
        vault = client.beta.vaults.create(display_name="healthsim-mcp-vault")
        client.beta.vaults.credentials.create(
            vault.id,
            display_name="healthsim-mcp-bearer",
            auth={
                "type": "static_bearer",
                "token": MCP_TOKEN,
                "mcp_server_url": mcp_url,
            },
        )
        ids["vault_id"] = vault.id
        print(f"  Vault: {vault.id}")
    else:
        print(f"  Vault: {ids['vault_id']} (cached)")

    save_json(AGENT_IDS_FILE, ids)
    return ids


def create_session(client: anthropic.Anthropic, ids: dict) -> str:
    """Create a new session."""
    print("Creating session...")
    session = client.beta.sessions.create(
        agent={
            "type": "agent",
            "id": ids["agent_id"],
            "version": ids["agent_version"],
        },
        environment_id=ids["environment_id"],
        vault_ids=[ids["vault_id"]],
        title="HealthSim Session",
    )
    print(f"  Session: {session.id} (status: {session.status})")
    return session.id


def _extract_text(content_blocks) -> str:
    """Extract text from content blocks (handles SDK objects and dicts)."""
    parts = []
    if not content_blocks:
        return ""
    for block in content_blocks:
        if hasattr(block, "text"):
            parts.append(block.text)
        elif hasattr(block, "type") and block.type == "text":
            parts.append(getattr(block, "text", ""))
    return "".join(parts)


def stream_response_from(client: anthropic.Anthropic, session_id: str, stream):
    """Consume an already-opened event stream until idle or terminated."""
    showed_tool = False  # Track if we need a newline before text

    with stream:
        for event in stream:
            t = event.type

            if t == "agent.message":
                text = _extract_text(getattr(event, "content", []))
                if text:
                    if showed_tool:
                        print()  # newline after tool activity before text
                        showed_tool = False
                    print(text, end="", flush=True)

            elif t == "agent.thinking":
                if not showed_tool:
                    print("\n  thinking...", end="", flush=True)
                    showed_tool = True

            elif t == "agent.tool_use":
                name = getattr(event, "name", "unknown")
                print(f"\n  [tool: {name}]", end="", flush=True)
                showed_tool = True

            elif t == "agent.tool_result":
                print(" done.", end="", flush=True)

            elif t == "agent.mcp_tool_use":
                name = getattr(event, "name", "unknown")
                print(f"\n  [mcp: {name}]", end="", flush=True)
                showed_tool = True

            elif t == "agent.mcp_tool_result":
                print(" done.", end="", flush=True)

            elif t == "span.model_request_start":
                if showed_tool:
                    print("\n  processing...", end="", flush=True)

            elif t == "session.status_idle":
                stop = getattr(event, "stop_reason", None)
                if stop and getattr(stop, "type", "") == "requires_action":
                    continue
                print()
                break

            elif t == "session.status_terminated":
                print("\n[Session terminated]")
                return False

            elif t == "session.error":
                msg = getattr(event, "message", str(event))
                print(f"\n  [error] {msg}", flush=True)

    return True


def interactive_loop(client: anthropic.Anthropic, session_id: str):
    """Send messages and stream responses in a loop."""
    while True:
        try:
            user_input = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Exiting]")
            break

        if not user_input:
            continue

        # Built-in commands
        if user_input.lower() in ("quit", "exit"):
            break
        if user_input.lower() == "session":
            print(f"  Session ID: {session_id}")
            continue

        # Stream-first: open stream before sending so no events are missed
        stream_handle = client.beta.sessions.events.stream(session_id=session_id)

        client.beta.sessions.events.send(
            session_id,
            events=[{
                "type": "user.message",
                "content": [{"type": "text", "text": user_input}],
            }],
        )

        print()
        alive = stream_response_from(client, session_id, stream_handle)
        if not alive:
            break


def main():
    import argparse

    parser = argparse.ArgumentParser(description="HealthSim Managed Agent session")
    parser.add_argument("--fresh", action="store_true", help="Recreate agent/env/vault")
    parser.add_argument("--session", metavar="SESSION_ID", help="Resume existing session")
    args = parser.parse_args()

    client = anthropic.Anthropic()

    print("=== HealthSim Managed Agent ===\n")

    if args.session:
        session_id = args.session
        print(f"  Resuming session: {session_id}\n")
    else:
        ids = setup(client, fresh=args.fresh)
        session_id = create_session(client, ids)
        print()

    print(f"Session: {session_id}")
    print("Commands: 'session' (show ID), 'quit' (exit)")
    print("Resume later: .venv/bin/python3 deploy/start-session.py "
          f"--session {session_id}\n")
    interactive_loop(client, session_id)

    print(f"\nSession ID: {session_id}")


if __name__ == "__main__":
    main()
