"""
push-skills.py — Upload skills to the Anthropic Skills API.

Reads skill definitions from agent-config.yaml and uploads them.
Supports idempotent updates — existing skills are versioned, not duplicated.

Usage:
    .venv/bin/python3 deploy/push-skills.py --all          # upload all from manifest
    .venv/bin/python3 deploy/push-skills.py --path ./skills/common/
    .venv/bin/python3 deploy/push-skills.py --list          # list uploaded skills
    .venv/bin/python3 deploy/push-skills.py --delete SKILL_ID

Environment:
    ANTHROPIC_API_KEY must be set (via .env or shell export).
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

SKILL_IDS_FILE = Path(__file__).parent / "skill-ids.json"
CONFIG_FILE = WORKSPACE_ROOT / "agent-config.yaml"


def load_skill_ids() -> dict:
    if SKILL_IDS_FILE.exists():
        return json.loads(SKILL_IDS_FILE.read_text())
    return {}


def save_skill_ids(ids: dict):
    SKILL_IDS_FILE.write_text(json.dumps(ids, indent=2) + "\n")


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        print(f"ERROR: {CONFIG_FILE} not found", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(CONFIG_FILE.read_text())


def get_client():
    import anthropic
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    return anthropic.Anthropic(api_key=api_key)


def find_existing_skill(client, display_title: str):
    """Find an existing skill by display_title for idempotent updates."""
    for skill in client.beta.skills.list(source="custom"):
        if skill.display_title == display_title:
            return skill
    return None


def upload_skill(client, skill_path: Path, skill_id_key: str) -> dict:
    """Upload or update a skill. Returns {id, version}."""
    if not skill_path.exists():
        print(f"  SKIP — path not found: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"  SKIP — no SKILL.md in {skill_path}")
        return None

    files = sorted(skill_path.glob("*.md"))
    dir_name = skill_path.name

    file_tuples = [
        (f"{dir_name}/{f.name}", open(f, "rb"), "text/markdown")
        for f in files
    ]

    # Check for existing skill (idempotent update via new version)
    existing = find_existing_skill(client, skill_id_key)
    if existing:
        # Create new version on existing skill
        result = client.beta.skills.versions.create(
            existing.id,
            files=file_tuples,
        )
        print(f"  Updated {skill_id_key}")
        print(f"    ID:      {existing.id}")
        print(f"    Version: {result.version}")
        return {"id": existing.id, "version": result.version}
    else:
        # Create new skill
        result = client.beta.skills.create(
            display_title=skill_id_key,
            files=file_tuples,
        )
        print(f"  Created {skill_id_key}")
        print(f"    ID:      {result.id}")
        print(f"    Version: {result.latest_version}")
        return {"id": result.id, "version": result.latest_version}


def cmd_upload_all():
    """Upload all skills from agent-config.yaml."""
    config = load_config()
    client = get_client()
    ids = load_skill_ids()

    skills = config.get("skills", [])
    print(f"Uploading {len(skills)} skills from {CONFIG_FILE.name}\n")

    for entry in skills:
        path = WORKSPACE_ROOT / entry["path"]
        # If path points to a file, use its parent directory
        if path.is_file():
            path = path.parent
        key = entry.get("skill_id", path.name)

        print(f"--- {key} ({path}) ---")
        result = upload_skill(client, path, key)
        if result:
            ids[key] = result["id"]

    save_skill_ids(ids)
    print(f"\nSaved {len(ids)} skill IDs to {SKILL_IDS_FILE}")


def cmd_upload_path(skill_path: Path, name: str = None):
    """Upload a single skill by path."""
    client = get_client()
    ids = load_skill_ids()

    skill_path = skill_path.resolve()
    if skill_path.is_file():
        skill_path = skill_path.parent

    key = name or skill_path.name
    print(f"--- {key} ({skill_path}) ---")
    result = upload_skill(client, skill_path, key)
    if result:
        ids[key] = result["id"]
        save_skill_ids(ids)
        print(f"\nSaved to {SKILL_IDS_FILE}")


def cmd_list():
    """List all custom skills."""
    client = get_client()
    skills = list(client.beta.skills.list(source="custom"))

    if not skills:
        print("No custom skills found.")
        return

    print(f"Custom skills ({len(skills)}):\n")
    for skill in skills:
        print(f"  {skill.id}")
        print(f"    Title:   {skill.display_title}")
        print(f"    Version: {skill.latest_version}")
        print(f"    Created: {skill.created_at}")
        print()


def cmd_delete(skill_id: str):
    """Delete a skill by ID."""
    client = get_client()
    client.beta.skills.delete(skill_id)
    print(f"Deleted: {skill_id}")

    # Remove from skill-ids.json if present
    ids = load_skill_ids()
    ids = {k: v for k, v in ids.items() if v != skill_id}
    save_skill_ids(ids)


def main():
    parser = argparse.ArgumentParser(description="Upload skills to Anthropic Skills API")
    parser.add_argument("--all", action="store_true", help="Upload all skills from agent-config.yaml")
    parser.add_argument("--path", type=Path, help="Upload a single skill directory")
    parser.add_argument("--name", help="Skill identifier (with --path)")
    parser.add_argument("--list", action="store_true", help="List existing skills")
    parser.add_argument("--delete", metavar="SKILL_ID", help="Delete a skill by ID")
    args = parser.parse_args()

    if args.list:
        cmd_list()
    elif args.delete:
        cmd_delete(args.delete)
    elif args.all:
        cmd_upload_all()
    elif args.path:
        cmd_upload_path(args.path, args.name)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
