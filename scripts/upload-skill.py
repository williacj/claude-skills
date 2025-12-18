#!/usr/bin/env python3
"""
Upload Claude Skill to Anthropic via Skills API

Usage:
  # Using skill name from config (recommended)
  python scripts/upload-skill.py --skill-name grammar --version v1.0.0

  # Using explicit skill path and ID (legacy)
  python scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01XYZ --version v1.0.0
"""

import os
import sys
import argparse
import base64
import json
import zipfile
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


def load_skills_config(config_path: Path = None) -> dict:
    """
    Load skills configuration from skills-config.json.

    Args:
        config_path: Optional path to config file. Defaults to skills-config.json in repo root.

    Returns:
        Dict containing skills configuration
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'skills-config.json'

    if not config_path.exists():
        raise FileNotFoundError(f"Skills config not found: {config_path}")

    with open(config_path, 'r') as f:
        return json.load(f)

def create_skill_zip(skill_path: Path) -> bytes:
    """
    Create a zip archive of the skill folder.
    
    Args:
        skill_path: Path to skill folder containing SKILL.md and references/
    
    Returns:
        Base64 encoded zip bytes
    """
    import io
    
    print(f"📦 Creating zip archive of {skill_path}")
    
    # Verify SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                arcname = file_path.relative_to(skill_path)
                print(f"   Adding: {arcname}")
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    encoded = base64.b64encode(zip_buffer.read()).decode('utf-8')
    print(f"✅ Zip created ({len(encoded)} bytes)")
    
    return encoded


def upload_skill_version(skill_id: str, skill_path: Path, version: str, api_key: str):
    """
    Upload a new version of a skill to Anthropic.
    
    Args:
        skill_id: The skill ID from Claude Console
        skill_path: Path to skill folder
        version: Version tag (e.g., 'v1.0.0' or git commit SHA)
        api_key: Anthropic API key
    """
    client = Anthropic(api_key=api_key)
    
    print(f"\n🚀 Uploading skill to Anthropic")
    print(f"   Skill ID: {skill_id}")
    print(f"   Version: {version}")
    print(f"   Path: {skill_path}")
    
    # Create zip
    skill_zip = create_skill_zip(skill_path)
    
    try:
        # Upload skill version
        # Using the correct API structure discovered from exploration
        response = client.beta.skills.versions.create(
            skill_id=skill_id,
            files=skill_zip,
            betas=["code-execution-2025-08-25", "skills-2025-10-02"]
        )
        
        print(f"\n✅ Skill uploaded successfully!")
        print(f"   Skill ID: {skill_id}")
        print(f"   Version: {version}")
        print(f"   Response: {response}")
        
        return response
        
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Upload Claude Skill to Anthropic API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using skill name from config (recommended)
  python scripts/upload-skill.py --skill-name grammar --version v1.0.0

  # Using explicit paths (legacy)
  python scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01ABC --version v1.0.0
        """
    )

    parser.add_argument(
        '--skill-name',
        help='Skill name from skills-config.json (e.g., "grammar", "sermon-writer")'
    )
    parser.add_argument(
        '--skill-path',
        help='Path to skill folder (legacy - use --skill-name instead)'
    )
    parser.add_argument(
        '--skill-id',
        help='Skill ID from Claude Console (legacy - use --skill-name instead)'
    )
    parser.add_argument(
        '--version',
        required=True,
        help='Version tag (e.g., "v1.0.0" or git commit SHA)'
    )
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (defaults to ANTHROPIC_API_KEY env var)'
    )
    parser.add_argument(
        '--config',
        help='Path to skills-config.json (default: auto-detect in repo root)'
    )

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set via --api-key flag or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Determine skill path and ID
    if args.skill_name:
        # Load from config
        config_path = Path(args.config) if args.config else None
        config = load_skills_config(config_path)

        if args.skill_name not in config['skills']:
            print(f"❌ Error: Skill '{args.skill_name}' not found in config")
            print(f"   Available skills: {', '.join(config['skills'].keys())}")
            sys.exit(1)

        skill_config = config['skills'][args.skill_name]
        skill_path = Path(skill_config['path'])
        skill_id = skill_config['skill_id']

        if skill_id is None:
            print(f"❌ Error: Skill '{args.skill_name}' has no skill_id in config")
            print(f"   Cannot upload without skill_id. Create the skill in Claude Console first.")
            sys.exit(1)

        print(f"📋 Using config for skill: {args.skill_name}")
        print(f"   Path: {skill_path}")
        print(f"   ID: {skill_id}")

    elif args.skill_path and args.skill_id:
        # Legacy mode - use explicit arguments
        skill_path = Path(args.skill_path)
        skill_id = args.skill_id
        print(f"⚠️  Using legacy mode with explicit path and ID")

    else:
        print(f"❌ Error: Must provide either --skill-name OR both --skill-path and --skill-id")
        parser.print_help()
        sys.exit(1)

    # Validate skill path exists
    if not skill_path.exists():
        print(f"❌ Error: Skill path '{skill_path}' does not exist")
        sys.exit(1)

    # Upload
    upload_skill_version(
        skill_id=skill_id,
        skill_path=skill_path,
        version=args.version,
        api_key=api_key
    )


if __name__ == "__main__":
    main()