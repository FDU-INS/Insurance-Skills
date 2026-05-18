"""
push-environment.py — Create or update the HealthSim Managed Agent environment.

Usage:
    .venv/bin/python3 deploy/push-environment.py            # create or update
    .venv/bin/python3 deploy/push-environment.py --info      # show current env info

Environment:
    ANTHROPIC_API_KEY must be set (via .env).
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
CONFIG_FILE = WORKSPACE_ROOT / "agent-config.yaml"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2) + "\n")


def get_client():
    import anthropic
    return anthropic.Anthropic()


def push_environment():
    """Create or reuse the Managed Agent environment."""
    agent_ids = load_json(AGENT_IDS_FILE)

    if "environment_id" in agent_ids:
        print(f"Environment already exists: {agent_ids['environment_id']}")
        print("  (Environments are reusable — no need to recreate)")
        return

    client = get_client()

    print("Creating environment...")
    env = client.beta.environments.create(
        name="healthsim-production",
        config={
            "type": "cloud",
            "networking": {"type": "unrestricted"},
        },
    )
    print(f"  Created: {env.id}")

    agent_ids["environment_id"] = env.id
    save_json(AGENT_IDS_FILE, agent_ids)
    print(f"  Saved to {AGENT_IDS_FILE}")


def show_info():
    """Show current environment info."""
    agent_ids = load_json(AGENT_IDS_FILE)
    if "environment_id" not in agent_ids:
        print("No environment deployed yet.")
        return

    client = get_client()
    env = client.beta.environments.retrieve(agent_ids["environment_id"])
    print(f"Environment: {env.name}")
    print(f"  ID:      {env.id}")
    print(f"  Created: {env.created_at}")


def main():
    parser = argparse.ArgumentParser(description="Deploy HealthSim environment")
    parser.add_argument("--info", action="store_true", help="Show current env info")
    args = parser.parse_args()

    if args.info:
        show_info()
    else:
        push_environment()


if __name__ == "__main__":
    main()
