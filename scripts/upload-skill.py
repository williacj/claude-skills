#!/usr/bin/env python3
"""
Upload Claude Skill to Anthropic via Skills API

Usage:
  python scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01XYZ --version v1.0.0
"""

import os
import sys
import argparse
import base64
import zipfile
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

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
  # Upload grammar skill with git tag
  python scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01ABC --version v1.0.0
  
  # Upload sermon-writer skill with commit SHA
  python scripts/upload-skill.py --skill-path skills/sermon-writer --skill-id skill_01XYZ --version $(git rev-parse --short HEAD)
        """
    )
    
    parser.add_argument(
        '--skill-path',
        required=True,
        help='Path to skill folder (e.g., "skills/grammar" or "skills/sermon-writer")'
    )
    parser.add_argument(
        '--skill-id',
        required=True,
        help='Skill ID from Claude Console (e.g., skill_01AbCdEfGh)'
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
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set via --api-key flag or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    # Resolve skill path
    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"❌ Error: Skill path '{skill_path}' does not exist")
        sys.exit(1)
    
    # Upload
    upload_skill_version(
        skill_id=args.skill_id,
        skill_path=skill_path,
        version=args.version,
        api_key=api_key
    )


if __name__ == "__main__":
    main()