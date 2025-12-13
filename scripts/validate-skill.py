#!/usr/bin/env python3
"""
ABOUTME: Validates Claude Skill structure before building deployment packages.
Checks for required files, proper structure, and common issues.

Usage:
  # Validate specific skill
  python scripts/validate-skill.py --skill-name grammar

  # Validate all skills
  python scripts/validate-skill.py --all

  # Validate with detailed output
  python scripts/validate-skill.py --skill-name grammar --verbose
"""

import sys
import argparse
import json
from pathlib import Path
from typing import List, Tuple


def load_skills_config(config_path: Path = None) -> dict:
    """Load skills configuration from skills-config.json."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / 'skills-config.json'

    if not config_path.exists():
        raise FileNotFoundError(f"Skills config not found: {config_path}")

    with open(config_path, 'r') as f:
        return json.load(f)


class ValidationResult:
    """Represents the result of validating a skill."""

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def add_error(self, message: str):
        """Add a critical error (blocks deployment)."""
        self.errors.append(message)

    def add_warning(self, message: str):
        """Add a warning (should be fixed but doesn't block)."""
        self.warnings.append(message)

    def add_info(self, message: str):
        """Add informational message."""
        self.info.append(message)

    def is_valid(self) -> bool:
        """Check if skill passed validation (no errors)."""
        return len(self.errors) == 0

    def print_summary(self, verbose: bool = False):
        """Print validation summary."""
        status = "✅ PASS" if self.is_valid() else "❌ FAIL"
        print(f"\n{status} {self.skill_name}")
        print("=" * 60)

        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")

        if verbose and self.info:
            print(f"\nℹ️  Info ({len(self.info)}):")
            for info in self.info:
                print(f"   • {info}")


def validate_skill(skill_name: str, skill_config: dict, verbose: bool = False) -> ValidationResult:
    """
    Validate a single skill's structure and configuration.

    Args:
        skill_name: Name of the skill from config
        skill_config: Skill configuration from skills-config.json
        verbose: Enable verbose output

    Returns:
        ValidationResult with errors, warnings, and info
    """
    result = ValidationResult(skill_name)
    skill_path = Path(skill_config['path'])

    # Check 1: Skill directory exists
    if not skill_path.exists():
        result.add_error(f"Skill directory does not exist: {skill_path}")
        return result  # Can't continue validation if directory missing

    if not skill_path.is_dir():
        result.add_error(f"Skill path is not a directory: {skill_path}")
        return result

    result.add_info(f"Directory exists: {skill_path}")

    # Check 2: SKILL.md exists and is not empty
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result.add_error("SKILL.md not found - this is required for Claude Skills")
    elif skill_md.stat().st_size == 0:
        result.add_error("SKILL.md is empty")
    else:
        size_kb = skill_md.stat().st_size / 1024
        result.add_info(f"SKILL.md found ({size_kb:.1f} KB)")

        # Check SKILL.md has frontmatter
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.startswith('---'):
                result.add_warning("SKILL.md missing frontmatter (should start with '---')")

    # Check 3: Skill ID configuration
    skill_id = skill_config.get('skill_id')
    if skill_id is None:
        result.add_warning(
            "No skill_id in config - you'll need to create this skill in Claude Console first"
        )
    elif not skill_id.startswith('skill_'):
        result.add_error(f"Invalid skill_id format: {skill_id} (should start with 'skill_')")
    else:
        result.add_info(f"Skill ID: {skill_id}")

    # Check 4: Display title
    display_title = skill_config.get('display_title')
    if not display_title:
        result.add_warning("No display_title in config")
    else:
        result.add_info(f"Display title: {display_title}")

    # Check 5: References directory (common but optional)
    references_dir = skill_path / "references"
    if references_dir.exists():
        if not references_dir.is_dir():
            result.add_warning("references exists but is not a directory")
        else:
            ref_files = list(references_dir.glob('*.md'))
            result.add_info(f"References directory found with {len(ref_files)} markdown files")

            if len(ref_files) == 0:
                result.add_warning("references/ directory exists but is empty")
    else:
        result.add_info("No references/ directory (optional)")

    # Check 6: Hidden files that shouldn't be packaged
    hidden_files = list(skill_path.glob('.*'))
    if hidden_files:
        hidden_names = [f.name for f in hidden_files]
        result.add_warning(f"Hidden files found (will be excluded): {', '.join(hidden_names)}")

    # Check 7: Total package size estimate
    total_size = sum(f.stat().st_size for f in skill_path.rglob('*') if f.is_file() and not f.name.startswith('.'))
    total_size_kb = total_size / 1024
    result.add_info(f"Estimated package size: {total_size_kb:.1f} KB")

    if total_size_kb > 5000:  # 5MB
        result.add_warning(f"Package size is large ({total_size_kb:.1f} KB) - consider reducing")

    # Check 8: File count
    file_count = len([f for f in skill_path.rglob('*') if f.is_file() and not f.name.startswith('.')])
    result.add_info(f"Total files: {file_count}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Validate Claude Skill structure before building',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate specific skill
  python scripts/validate-skill.py --skill-name grammar

  # Validate all skills in config
  python scripts/validate-skill.py --all

  # Verbose output with all info messages
  python scripts/validate-skill.py --skill-name sermon-writer --verbose
        """
    )

    parser.add_argument(
        '--skill-name',
        help='Skill name from skills-config.json to validate'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all skills in config'
    )
    parser.add_argument(
        '--config',
        help='Path to skills-config.json (default: auto-detect)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show verbose output including info messages'
    )

    args = parser.parse_args()

    if not args.skill_name and not args.all:
        print("❌ Error: Must specify either --skill-name or --all")
        parser.print_help()
        sys.exit(1)

    # Load config
    try:
        config_path = Path(args.config) if args.config else None
        config = load_skills_config(config_path)
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)

    # Determine which skills to validate
    if args.all:
        skills_to_validate = list(config['skills'].items())
        print(f"🔍 Validating all {len(skills_to_validate)} skills...")
    else:
        if args.skill_name not in config['skills']:
            print(f"❌ Error: Skill '{args.skill_name}' not found in config")
            print(f"   Available skills: {', '.join(config['skills'].keys())}")
            sys.exit(1)
        skills_to_validate = [(args.skill_name, config['skills'][args.skill_name])]
        print(f"🔍 Validating skill: {args.skill_name}...")

    # Validate each skill
    results = []
    for skill_name, skill_config in skills_to_validate:
        result = validate_skill(skill_name, skill_config, verbose=args.verbose)
        results.append(result)
        result.print_summary(verbose=args.verbose)

    # Print overall summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)

    total_skills = len(results)
    passed = sum(1 for r in results if r.is_valid())
    failed = total_skills - passed
    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    print(f"Total skills: {total_skills}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")

    if failed > 0:
        print("\n❌ Validation failed - fix errors before deploying")
        sys.exit(1)
    elif total_warnings > 0:
        print("\n⚠️  Validation passed with warnings - review before deploying")
        sys.exit(0)
    else:
        print("\n✅ All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
