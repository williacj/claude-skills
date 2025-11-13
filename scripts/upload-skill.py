#!/usr/bin/env python3
"""
ABOUTME: Upload or create Claude Skills via Anthropic API
Handles both creating new skills and updating existing skills with new versions.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def prepare_skill_files(skill_path: Path) -> list:
    """
    Prepare skill files for upload to Anthropic API.

    Args:
        skill_path: Path to skill folder containing SKILL.md

    Returns:
        List of file tuples (filename, file_content) for API upload
    """
    print(f"📦 Preparing skill files from {skill_path}")

    # Verify SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")

    files = []
    for file_path in skill_path.rglob('*'):
        if file_path.is_file() and not file_path.name.startswith('.'):
            relative_path = file_path.relative_to(skill_path.parent)
            print(f"   Adding: {relative_path}")
            with open(file_path, 'rb') as f:
                files.append((str(relative_path), f.read()))

    print(f"✅ Prepared {len(files)} files for upload")
    return files


def create_new_skill(skill_path: Path, display_title: str, api_key: str):
    """
    Create a new skill in Anthropic.

    Args:
        skill_path: Path to skill folder
        display_title: Display name for the skill
        api_key: Anthropic API key

    Returns:
        Skill object with skill_id
    """
    client = Anthropic(api_key=api_key)

    print(f"\n🆕 Creating new skill in Anthropic")
    print(f"   Title: {display_title}")
    print(f"   Path: {skill_path}")

    # Prepare files
    files = prepare_skill_files(skill_path)

    try:
        response = client.beta.skills.create(
            display_title=display_title,
            files=files,
            betas=["skills-2025-10-02"]
        )

        print(f"\n✅ Skill created successfully!")
        print(f"   Skill ID: {response.id}")
        print(f"   Latest Version: {response.latest_version}")
        print(f"\n⚠️  IMPORTANT: Add this skill_id to skills-config.json:")
        print(f'   "skill_id": "{response.id}"')

        return response

    except Exception as e:
        print(f"\n❌ Create failed: {e}")
        sys.exit(1)


def update_skill_version(skill_id: str, skill_path: Path, api_key: str):
    """
    Upload a new version of an existing skill to Anthropic.

    Args:
        skill_id: The skill ID from Claude Console
        skill_path: Path to skill folder
        api_key: Anthropic API key

    Returns:
        Version object
    """
    client = Anthropic(api_key=api_key)

    print(f"\n🔄 Updating skill in Anthropic")
    print(f"   Skill ID: {skill_id}")
    print(f"   Path: {skill_path}")

    # Prepare files
    files = prepare_skill_files(skill_path)

    try:
        response = client.beta.skills.versions.create(
            skill_id=skill_id,
            files=files,
            betas=["skills-2025-10-02"]
        )

        print(f"\n✅ Skill version updated successfully!")
        print(f"   Skill ID: {skill_id}")
        print(f"   New Version: {response.version}")

        return response

    except Exception as e:
        print(f"\n❌ Update failed: {e}")
        sys.exit(1)


def load_config() -> dict:
    """Load skills configuration from skills-config.json"""
    config_path = Path(__file__).parent.parent / 'skills-config.json'
    if not config_path.exists():
        print(f"❌ Error: Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description='Upload or create Claude Skill via Anthropic API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update existing skill (has skill_id in config)
  python scripts/upload-skill.py --skill-name grammar

  # Create new skill (skill_id is null in config)
  python scripts/upload-skill.py --skill-name biblical-accuracy

  # Override config with explicit skill-id
  python scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01ABC --display-title "Grammar Checker"
        """
    )

    parser.add_argument(
        '--skill-name',
        help='Skill name from skills-config.json (e.g., "grammar", "sermon-writer")'
    )
    parser.add_argument(
        '--skill-path',
        help='Path to skill folder (overrides config)'
    )
    parser.add_argument(
        '--skill-id',
        help='Skill ID (overrides config, use "create" to force creation)'
    )
    parser.add_argument(
        '--display-title',
        help='Display title for new skills (overrides config)'
    )
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (defaults to ANTHROPIC_API_KEY env var)'
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set via --api-key flag or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Load configuration
    config = load_config()

    # Determine skill parameters
    if args.skill_name:
        if args.skill_name not in config['skills']:
            print(f"❌ Error: Skill '{args.skill_name}' not found in skills-config.json")
            print(f"   Available skills: {', '.join(config['skills'].keys())}")
            sys.exit(1)

        skill_config = config['skills'][args.skill_name]
        skill_path = Path(skill_config['path'])
        skill_id = args.skill_id if args.skill_id else skill_config['skill_id']
        display_title = args.display_title if args.display_title else skill_config['display_title']
    elif args.skill_path:
        skill_path = Path(args.skill_path)
        skill_id = args.skill_id
        display_title = args.display_title

        if not skill_id or not display_title:
            print("❌ Error: When using --skill-path, must also provide --skill-id and --display-title")
            sys.exit(1)
    else:
        print("❌ Error: Must provide either --skill-name or --skill-path")
        sys.exit(1)

    # Verify skill path exists
    if not skill_path.exists():
        print(f"❌ Error: Skill path '{skill_path}' does not exist")
        sys.exit(1)

    # Create or update
    if skill_id == "create" or skill_id is None:
        create_new_skill(
            skill_path=skill_path,
            display_title=display_title,
            api_key=api_key
        )
    else:
        update_skill_version(
            skill_id=skill_id,
            skill_path=skill_path,
            api_key=api_key
        )


if __name__ == "__main__":
    main()