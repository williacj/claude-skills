#!/usr/bin/env python3
"""
Prepare Claude Skill deployment package for manual upload

This script creates a deployment-ready zip file and metadata for manual upload
to Claude Console until the Skills API supports programmatic uploads.

Usage:
  # Using skill name from config
  python scripts/prepare-skill.py --skill-name grammar --version v1.0.0

  # Using explicit skill path and ID (legacy)
  python scripts/prepare-skill.py --skill-path skills/grammar --skill-id skill_01XYZ --version v1.0.0 --output-dir deployments
"""

import os
import sys
import argparse
import json
import zipfile
from pathlib import Path
from datetime import datetime
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

def create_deployment_package(skill_path: Path, skill_id: str, version: str, output_dir: Path):
    """
    Create a deployment package for manual upload.
    
    Args:
        skill_path: Path to skill folder containing SKILL.md and references/
        skill_id: The skill ID from Claude Console
        version: Version tag (e.g., 'v1.0.0' or git commit SHA)
        output_dir: Directory to save deployment packages
    
    Returns:
        Path to created zip file
    """
    
    print(f"📦 Creating deployment package for {skill_path.name}")
    print(f"   Skill ID: {skill_id}")
    print(f"   Version: {version}")
    print(f"   Output: {output_dir}")
    
    # Verify SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_path}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create zip filename
    skill_name = skill_path.name
    zip_filename = f"{skill_name}-{version}.zip"
    zip_path = output_dir / zip_filename
    
    # Create deployment metadata
    metadata = {
        "skill_name": skill_name,
        "skill_id": skill_id,
        "version": version,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "files_included": [],
        "upload_instructions": {
            "console_url": "https://console.anthropic.com/skills",
            "steps": [
                f"1. Go to {skill_id} in Claude Console",
                "2. Click 'Upload New Version' or similar",
                f"3. Upload the {zip_filename} file",
                "4. Verify the upload and activate the new version"
            ]
        }
    }
    
    # Create the zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                arcname = file_path.relative_to(skill_path)
                print(f"   Adding: {arcname}")
                zip_file.write(file_path, arcname)
                metadata["files_included"].append(str(arcname))
    
    # Save metadata file
    metadata_path = output_dir / f"{skill_name}-{version}.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Deployment package created:")
    print(f"   📦 Skill archive: {zip_path}")
    print(f"   📋 Metadata: {metadata_path}")
    print(f"   📊 Size: {zip_path.stat().st_size} bytes")
    print(f"   📁 Files: {len(metadata['files_included'])}")
    
    return zip_path

def main():
    parser = argparse.ArgumentParser(
        description='Prepare Claude Skill deployment package for manual upload',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using skill name from config (recommended)
  python scripts/prepare-skill.py --skill-name grammar --version v1.0.0

  # Using explicit paths (legacy)
  python scripts/prepare-skill.py --skill-path skills/grammar --skill-id skill_01ABC --version v1.0.0
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
        '--output-dir',
        default='deployments',
        help='Output directory for deployment packages (default: deployments)'
    )
    parser.add_argument(
        '--config',
        help='Path to skills-config.json (default: auto-detect in repo root)'
    )

    args = parser.parse_args()

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
            print(f"⚠️  Warning: Skill '{args.skill_name}' has no skill_id in config")
            print(f"   You'll need to create this skill in Claude Console first")
            print(f"   Package will still be created for manual upload")
            skill_id = f"skill_PENDING_{args.skill_name}"

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

    output_dir = Path(args.output_dir)

    # Create deployment package
    try:
        zip_path = create_deployment_package(
            skill_path=skill_path,
            skill_id=skill_id,
            version=args.version,
            output_dir=output_dir
        )

        print(f"\n🚀 Ready for manual upload!")
        print(f"   1. Download: {zip_path}")
        print(f"   2. Go to: https://console.anthropic.com/skills")
        print(f"   3. Find skill: {skill_id}")
        print(f"   4. Upload new version")

    except Exception as e:
        print(f"❌ Error creating deployment package: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()