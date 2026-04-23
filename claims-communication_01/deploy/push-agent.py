"""
push-agent.py — Create or update the HealthSim Managed Agent definition.

Reads config from agent-config.yaml, system prompt from deploy/system-prompt.md,
skill IDs from deploy/skill-ids.json, and MCP server URL from deploy/railway-url.txt.

Usage:
    .venv/bin/python3 deploy/push-agent.py            # create or update agent
    .venv/bin/python3 deploy/push-agent.py --info      # show current agent info

Environment:
    ANTHROPIC_API_KEY, HEALTHSIM_MCP_TOKEN must be set (via .env).
"""

import argparse
import json
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

DEPLOY_DIR = Path(__file__).parent
AGENT_IDS_FILE = DEPLOY_DIR / "agent-ids.json"
SKILL_IDS_FILE = DEPLOY_DIR / "skill-ids.json"
RAILWAY_URL_FILE = DEPLOY_DIR / "railway-url.txt"
CONFIG_FILE = WORKSPACE_ROOT / "agent-config.yaml"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2) + "\n")


def get_client():
    import anthropic
    return anthropic.Anthropic()


def push_agent():
    """Create or update the Managed Agent."""
    config = yaml.safe_load(CONFIG_FILE.read_text())
    skill_ids = load_json(SKILL_IDS_FILE)
    agent_ids = load_json(AGENT_IDS_FILE)
    mcp_token = os.environ.get("HEALTHSIM_MCP_TOKEN", "")

    # System prompt
    prompt_source = WORKSPACE_ROOT / config.get("system_prompt_source", "deploy/system-prompt.md")
    if not prompt_source.exists():
        print(f"ERROR: System prompt not found: {prompt_source}", file=sys.stderr)
        sys.exit(1)
    system_prompt = prompt_source.read_text()

    # MCP server URL
    if not RAILWAY_URL_FILE.exists():
        print("ERROR: deploy/railway-url.txt not found", file=sys.stderr)
        sys.exit(1)
    mcp_url = RAILWAY_URL_FILE.read_text().strip().rstrip("/") + "/mcp"

    # Skills — reference all uploaded custom skills
    skills = [
        {"type": "custom", "skill_id": sid, "version": "latest"}
        for sid in skill_ids.values()
    ]

    # Tools
    tools = [
        {"type": "agent_toolset_20260401", "default_config": {"enabled": True}},
        {
            "type": "mcp_toolset",
            "mcp_server_name": "healthsim-mcp",
            "default_config": {
                "enabled": True,
                "permission_policy": {"type": "always_allow"},
            },
        },
    ]

    # MCP servers
    mcp_servers = [
        {"type": "url", "name": "healthsim-mcp", "url": mcp_url},
    ]

    client = get_client()

    if "agent_id" in agent_ids:
        # Update existing agent
        print(f"Updating agent {agent_ids['agent_id']}...")
        agent = client.beta.agents.update(
            agent_ids["agent_id"],
            version=agent_ids["agent_version"],
            name=config.get("name", "HealthSim"),
            model=config.get("model", "claude-sonnet-4-6"),
            system=system_prompt,
            tools=tools,
            skills=skills,
            mcp_servers=mcp_servers,
            description=config.get("description", ""),
        )
        print(f"  Updated: {agent.id} (version {agent.version})")
    else:
        # Create new agent
        print("Creating agent...")
        agent = client.beta.agents.create(
            name=config.get("name", "HealthSim"),
            model=config.get("model", "claude-sonnet-4-6"),
            system=system_prompt,
            tools=tools,
            skills=skills,
            mcp_servers=mcp_servers,
            description=config.get("description", ""),
        )
        print(f"  Created: {agent.id} (version {agent.version})")

    # Save IDs
    agent_ids["agent_id"] = agent.id
    agent_ids["agent_version"] = agent.version
    save_json(AGENT_IDS_FILE, agent_ids)
    print(f"  Saved to {AGENT_IDS_FILE}")


def show_info():
    """Show current agent info."""
    agent_ids = load_json(AGENT_IDS_FILE)
    if "agent_id" not in agent_ids:
        print("No agent deployed yet.")
        return

    client = get_client()
    agent = client.beta.agents.retrieve(agent_ids["agent_id"])
    print(f"Agent: {agent.name}")
    print(f"  ID:      {agent.id}")
    print(f"  Version: {agent.version}")
    print(f"  Model:   {agent.model}")
    print(f"  Skills:  {len(agent.skills or [])}")
    print(f"  MCP:     {len(agent.mcp_servers or [])}")
    print(f"  Created: {agent.created_at}")


def main():
    parser = argparse.ArgumentParser(description="Deploy HealthSim Managed Agent")
    parser.add_argument("--info", action="store_true", help="Show current agent info")
    args = parser.parse_args()

    if args.info:
        show_info()
    else:
        push_agent()


if __name__ == "__main__":
    main()
