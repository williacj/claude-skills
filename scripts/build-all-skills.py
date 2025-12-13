#!/usr/bin/env python3
"""
ABOUTME: Build all Claude Skills packages from skills-config.json in a single command.
Validates all skills first, then builds deployment packages for each.

Usage:
  # Build all skills with specific version
  python scripts/build-all-skills.py --version v1.0.0

  # Build all skills with git version
  python scripts/build-all-skills.py --version $(git describe --tags --always)

  # Build to custom output directory
  python scripts/build-all-skills.py --version v1.0.0 --output-dir releases
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


def build_skill(skill_name: str, version: str, output_dir: str, config_path: Path = None) -> Tuple[bool, str]:
    """
    Build a single skill package.

    Returns:
        Tuple of (success: bool, message: str)
    """
    prepare_script = Path(__file__).parent / 'prepare-skill.py'

    cmd = [
        'python3',
        str(prepare_script),
        '--skill-name', skill_name,
        '--version', version,
        '--output-dir', output_dir
    ]

    if config_path:
        cmd.extend(['--config', str(config_path)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True, f"✅ {skill_name} built successfully"
    else:
        return False, f"❌ {skill_name} build failed:\n{result.stderr}"


def main():
    parser = argparse.ArgumentParser(
        description='Build all Claude Skills packages from config',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build all skills with version tag
  python scripts/build-all-skills.py --version v1.0.0

  # Build all skills with git-generated version
  python scripts/build-all-skills.py --version $(git describe --tags --always)

  # Build to custom output directory
  python scripts/build-all-skills.py --version v1.0.0 --output-dir releases

  # Skip validation (not recommended)
  python scripts/build-all-skills.py --version v1.0.0 --no-validate
        """
    )

    parser.add_argument(
        '--version',
        required=True,
        help='Version tag for all skills (e.g., "v1.0.0" or git commit SHA)'
    )
    parser.add_argument(
        '--output-dir',
        default='deployments',
        help='Output directory for deployment packages (default: deployments)'
    )
    parser.add_argument(
        '--config',
        help='Path to skills-config.json (default: auto-detect)'
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

    # Load config
    try:
        config_path = Path(args.config) if args.config else None
        config = load_skills_config(config_path)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    skills = list(config['skills'].keys())

    print("=" * 60)
    print(f"📦 Building All Skills")
    print("=" * 60)
    print(f"Version: {args.version}")
    print(f"Output: {args.output_dir}")
    print(f"Skills: {', '.join(skills)}")
    print("=" * 60)

    # Step 1: Validate (unless skipped)
    if not args.no_validate:
        if not validate_all_skills(verbose=args.verbose):
            print("\n❌ Validation failed - aborting build")
            print("   Fix validation errors or use --no-validate to skip")
            sys.exit(1)
        print("\n✅ Validation passed\n")
    else:
        print("\n⚠️  Skipping validation (--no-validate)\n")

    # Step 2: Build each skill
    results: List[Tuple[str, bool, str]] = []

    for skill_name in skills:
        print(f"\n{'=' * 60}")
        print(f"Building: {skill_name}")
        print('=' * 60)

        success, message = build_skill(
            skill_name=skill_name,
            version=args.version,
            output_dir=args.output_dir,
            config_path=config_path
        )

        results.append((skill_name, success, message))

        if not success and args.verbose:
            print(message)

    # Step 3: Summary
    print("\n" + "=" * 60)
    print("📊 BUILD SUMMARY")
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
        print("\n❌ Some builds failed - check output above")
        print(f"   Successful packages are in: {args.output_dir}/")
        sys.exit(1)
    else:
        print(f"\n✅ All skills built successfully!")
        print(f"   Packages saved to: {args.output_dir}/")
        print(f"\n🚀 Next steps:")
        print(f"   1. Review packages in {args.output_dir}/")
        print(f"   2. Go to https://console.anthropic.com/skills")
        print(f"   3. Upload each skill's zip file")
        sys.exit(0)


if __name__ == "__main__":
    main()
