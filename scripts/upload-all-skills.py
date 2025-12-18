#!/usr/bin/env python3
"""
ABOUTME: Upload all Claude Skills to Claude Console via API in a single command.
Validates all skills first, then uploads each to Anthropic via the Skills API.

Usage:
  # Upload all skills with specific version
  python scripts/upload-all-skills.py --version v1.0.0

  # Upload all skills with git version
  python scripts/upload-all-skills.py --version $(git describe --tags --always)

  # Upload only skills with configured IDs
  python scripts/upload-all-skills.py --version v1.0.0 --skip-missing-ids
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple


def load_skills_config(config_path: Path = None) -> dict:
    """Load skills configuration from skills-config.json."""
    import json

    if config_path is None:
        config_path = Path(__file__).parent.parent / 'skills-config.json'

    if not config_path.exists():
        raise FileNotFoundError(f"Skills config not found: {config_path}")

    with open(config_path, 'r') as f:
        return json.load(f)


def validate_all_skills(verbose: bool = False) -> bool:
    """
    Run validation on all skills.

    Returns:
        True if validation passed, False otherwise
    """
    print("🔍 Validating all skills...")

    validate_script = Path(__file__).parent / 'validate-skill.py'
    cmd = ['python3', str(validate_script), '--all']

    if verbose:
        cmd.append('--verbose')

    result = subprocess.run(cmd)

    return result.returncode == 0


def upload_skill(skill_name: str, version: str, api_key: str, config_path: Path = None) -> Tuple[bool, str]:
    """
    Upload a single skill to Claude Console.

    Returns:
        Tuple of (success: bool, message: str)
    """
    upload_script = Path(__file__).parent / 'upload-skill.py'

    cmd = [
        'python3',
        str(upload_script),
        '--skill-name', skill_name,
        '--version', version,
        '--api-key', api_key
    ]

    if config_path:
        cmd.extend(['--config', str(config_path)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True, f"✅ {skill_name} uploaded successfully"
    else:
        error_msg = result.stderr if result.stderr else result.stdout
        return False, f"❌ {skill_name} upload failed:\n{error_msg}"


def main():
    parser = argparse.ArgumentParser(
        description='Upload all Claude Skills to Claude Console',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload all skills with version tag
  python scripts/upload-all-skills.py --version v1.0.0

  # Upload all skills with git-generated version
  python scripts/upload-all-skills.py --version $(git describe --tags --always)

  # Skip skills without IDs configured
  python scripts/upload-all-skills.py --version v1.0.0 --skip-missing-ids

  # Skip validation (not recommended)
  python scripts/upload-all-skills.py --version v1.0.0 --no-validate
        """
    )

    parser.add_argument(
        '--version',
        required=True,
        help='Version tag for all skills (e.g., "v1.0.0" or git commit SHA)'
    )
    parser.add_argument(
        '--config',
        help='Path to skills-config.json (default: auto-detect)'
    )
    parser.add_argument(
        '--api-key',
        help='Anthropic API key (defaults to ANTHROPIC_API_KEY env var)'
    )
    parser.add_argument(
        '--skip-missing-ids',
        action='store_true',
        help='Skip skills that do not have skill_id configured'
    )
    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip validation step (not recommended)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output'
    )

    args = parser.parse_args()

    # Get API key
    import os
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not set")
        print("   Set via --api-key flag or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    # Load config
    try:
        config_path = Path(args.config) if args.config else None
        config = load_skills_config(config_path)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    all_skills = list(config['skills'].items())

    # Filter out skills without IDs if requested
    if args.skip_missing_ids:
        skills_to_upload = [(name, cfg) for name, cfg in all_skills if cfg.get('skill_id') is not None]
        skipped = len(all_skills) - len(skills_to_upload)
        if skipped > 0:
            print(f"⏭️  Skipping {skipped} skills without IDs configured")
    else:
        skills_to_upload = all_skills

    skill_names = [name for name, _ in skills_to_upload]

    print("=" * 60)
    print(f"🚀 Uploading All Skills to Claude Console")
    print("=" * 60)
    print(f"Version: {args.version}")
    print(f"Skills: {', '.join(skill_names)}")
    print("=" * 60)

    # Step 1: Validate (unless skipped)
    if not args.no_validate:
        if not validate_all_skills(verbose=args.verbose):
            print("\n❌ Validation failed - aborting upload")
            print("   Fix validation errors or use --no-validate to skip")
            sys.exit(1)
        print("\n✅ Validation passed\n")
    else:
        print("\n⚠️  Skipping validation (--no-validate)\n")

    # Step 2: Check for missing IDs
    skills_without_ids = [name for name, cfg in skills_to_upload if cfg.get('skill_id') is None]
    if skills_without_ids and not args.skip_missing_ids:
        print(f"❌ Error: The following skills do not have skill_id configured:")
        for skill_name in skills_without_ids:
            print(f"   - {skill_name}")
        print("\nOptions:")
        print("  1. Create these skills in Claude Console and update skills-config.json")
        print("  2. Use --skip-missing-ids to upload only configured skills")
        sys.exit(1)

    # Step 3: Upload each skill
    results: List[Tuple[str, bool, str]] = []

    for skill_name, skill_config in skills_to_upload:
        print(f"\n{'=' * 60}")
        print(f"Uploading: {skill_name}")
        print('=' * 60)

        success, message = upload_skill(
            skill_name=skill_name,
            version=args.version,
            api_key=api_key,
            config_path=config_path
        )

        results.append((skill_name, success, message))

        if not success and args.verbose:
            print(message)

    # Step 4: Summary
    print("\n" + "=" * 60)
    print("📊 UPLOAD SUMMARY")
    print("=" * 60)

    successful = sum(1 for _, success, _ in results if success)
    failed = len(results) - successful

    print(f"Total skills: {len(results)}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print()

    for skill_name, success, message in results:
        print(f"  {message}")

    if failed > 0:
        print("\n❌ Some uploads failed - check output above")
        print(f"   Successful uploads: {successful}/{len(results)}")
        sys.exit(1)
    else:
        print(f"\n✅ All skills uploaded successfully!")
        print(f"   View at: https://console.anthropic.com/skills")
        sys.exit(0)


if __name__ == "__main__":
    main()
