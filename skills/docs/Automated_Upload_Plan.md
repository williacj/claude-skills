Automation Plan: Claude Skills → GitHub Actions
Overview
Goal: Automatically sync skills from GitHub to Claude Console on every commit to main branch. Repository: williacj/claude-skills Skills to Sync:
skills/grammar/ (already exists)
skills/sermon-writer/ (already exists)
📋 Phase 1: Research & Setup (First)
Step 1.1: Verify Skills API Endpoint
Action: Test the Skills API to confirm exact endpoint structure. Test Script (scripts/test-skills-api.py):
#!/usr/bin/env python3
"""
Test Claude Skills API to verify endpoint structure
"""
import os
from anthropic import Anthropic

def test_list_skills():
    """Test listing skills to verify API access"""
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    try:
        # Try to list skills
        response = client.beta.skills.list(
            betas=["code-execution-2025-08-25", "skills-2025-10-02"]
        )
        print("✅ Skills API is accessible!")
        print(f"Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Error accessing Skills API: {e}")
        return False

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        exit(1)
    
    test_list_skills()
Expected Output:
List of existing skills with their IDs
Confirmation of API structure
Any limitations or requirements
Step 1.2: Create Skills Manually (One Time)
Claude Console Steps:
Go to https://console.anthropic.com/skills
Create "grammar" skill:
Upload grammar/ folder
Copy skill_id (e.g., skill_01GrammarXyZ123)
Create "sermon-writer" skill:
Upload sermon-writer/ folder
Copy skill_id (e.g., skill_01SermonXyZ456)
Save Skill IDs for GitHub secrets.
📋 Phase 2: Implementation Files
File 1: Upload Script (scripts/upload-skill.py)
#!/usr/bin/env python3
"""
Upload Claude Skill to Anthropic via Skills API

Usage:
  python scripts/upload-skill.py --skill-path grammar --skill-id skill_01XYZ --version v1.0.0
"""

import os
import sys
import argparse
import base64
import zipfile
from pathlib import Path
from anthropic import Anthropic

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
        # NOTE: Exact endpoint may vary - check Anthropic docs
        response = client.beta.skills.versions.create(
            skill_id=skill_id,
            version_tag=version,
            skill_folder=skill_zip,
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
        help='Path to skill folder (e.g., "grammar" or "sermon-writer")'
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
File 2: GitHub Actions Workflow (.github/workflows/sync-skills.yml)
name: Sync Skills to Claude Console

on:
  push:
    branches:
      - main
    paths:
      - 'grammar/**'
      - 'sermon-writer/**'
      - '.github/workflows/sync-skills.yml'
  
  workflow_dispatch:
    inputs:
      skill:
        description: 'Skill to upload (grammar, sermon-writer, or all)'
        required: false
        default: 'all'
        type: choice
        options:
          - all
          - grammar
          - sermon-writer

jobs:
  detect-changes:
    name: Detect Changed Skills
    runs-on: ubuntu-latest
    outputs:
      grammar_changed: ${{ steps.changes.outputs.grammar }}
      sermon_writer_changed: ${{ steps.changes.outputs.sermon_writer }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2
      
      - name: Detect changed skills
        id: changes
        run: |
          if [ "${{ github.event_name }}" == "workflow_dispatch" ]; then
            # Manual trigger - upload specified skill(s)
            if [ "${{ github.event.inputs.skill }}" == "all" ] || [ "${{ github.event.inputs.skill }}" == "grammar" ]; then
              echo "grammar=true" >> $GITHUB_OUTPUT
            fi
            if [ "${{ github.event.inputs.skill }}" == "all" ] || [ "${{ github.event.inputs.skill }}" == "sermon-writer" ]; then
              echo "sermon_writer=true" >> $GITHUB_OUTPUT
            fi
          else
            # Auto trigger - detect changed files
            if git diff --name-only HEAD~1 HEAD | grep -q '^grammar/'; then
              echo "grammar=true" >> $GITHUB_OUTPUT
            fi
            if git diff --name-only HEAD~1 HEAD | grep -q '^sermon-writer/'; then
              echo "sermon_writer=true" >> $GITHUB_OUTPUT
            fi
          fi

  upload-grammar:
    name: Upload Grammar Skill
    needs: detect-changes
    if: needs.detect-changes.outputs.grammar_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install anthropic
      
      - name: Upload Grammar Skill
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          VERSION=$(git describe --tags --always --dirty)
          python scripts/upload-skill.py \
            --skill-path grammar \
            --skill-id ${{ secrets.GRAMMAR_SKILL_ID }} \
            --version $VERSION
      
      - name: Create release tag (if on main)
        if: github.ref == 'refs/heads/main'
        run: |
          VERSION=$(git describe --tags --always)
          echo "✅ Grammar skill uploaded as version: $VERSION"

  upload-sermon-writer:
    name: Upload Sermon Writer Skill
    needs: detect-changes
    if: needs.detect-changes.outputs.sermon_writer_changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install anthropic
      
      - name: Upload Sermon Writer Skill
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          VERSION=$(git describe --tags --always --dirty)
          python scripts/upload-skill.py \
            --skill-path sermon-writer \
            --skill-id ${{ secrets.SERMON_WRITER_SKILL_ID }} \
            --version $VERSION
      
      - name: Create release tag (if on main)
        if: github.ref == 'refs/heads/main'
        run: |
          VERSION=$(git describe --tags --always)
          echo "✅ Sermon Writer skill uploaded as version: $VERSION"

  summary:
    name: Upload Summary
    needs: [detect-changes, upload-grammar, upload-sermon-writer]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Summary
        run: |
          echo "## Skills Upload Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          
          if [ "${{ needs.detect-changes.outputs.grammar_changed }}" == "true" ]; then
            if [ "${{ needs.upload-grammar.result }}" == "success" ]; then
              echo "✅ Grammar skill uploaded successfully" >> $GITHUB_STEP_SUMMARY
            else
              echo "❌ Grammar skill upload failed" >> $GITHUB_STEP_SUMMARY
            fi
          else
            echo "⏭️  Grammar skill - no changes detected" >> $GITHUB_STEP_SUMMARY
          fi
          
          if [ "${{ needs.detect-changes.outputs.sermon_writer_changed }}" == "true" ]; then
            if [ "${{ needs.upload-sermon-writer.result }}" == "success" ]; then
              echo "✅ Sermon Writer skill uploaded successfully" >> $GITHUB_STEP_SUMMARY
            else
              echo "❌ Sermon Writer skill upload failed" >> $GITHUB_STEP_SUMMARY
            fi
          else
            echo "⏭️  Sermon Writer skill - no changes detected" >> $GITHUB_STEP_SUMMARY
          fi
File 3: Requirements File (scripts/requirements.txt)
anthropic>=0.40.0
File 4: Documentation (docs/SKILLS_AUTOMATION.md)
# Skills Automation

This repository automatically syncs skills to Claude Console via the Anthropic Skills API.

## How It Works

1. **Trigger**: On every commit to `main` that changes `grammar/` or `sermon-writer/` folders
2. **Detection**: GitHub Actions detects which skills changed
3. **Upload**: Changed skills are uploaded to Claude Console via Skills API
4. **Versioning**: Each upload is tagged with git commit SHA or tag

## Setup Instructions

### 1. Create Skills in Claude Console

First time only - manually create skills in Claude Console:

1. Go to https://console.anthropic.com/skills
2. Create "grammar" skill by uploading `grammar/` folder
3. Copy the generated `skill_id` (looks like `skill_01AbCdEfGhIj`)
4. Create "sermon-writer" skill by uploading `sermon-writer/` folder
5. Copy the generated `skill_id`

### 2. Configure GitHub Secrets

Add these secrets to your repository settings:

**Settings → Secrets and variables → Actions → New repository secret**

- `ANTHROPIC_API_KEY` - Your Anthropic API key from https://console.anthropic.com/settings/keys
- `GRAMMAR_SKILL_ID` - The skill ID from step 1 (grammar)
- `SERMON_WRITER_SKILL_ID` - The skill ID from step 1 (sermon-writer)

### 3. Test the Automation

Option A: Make a commit to `grammar/` or `sermon-writer/`
```bash
cd grammar
echo "# Test change" >> SKILL.md
git add SKILL.md
git commit -m "test: trigger skills automation"
git push origin main
Option B: Manually trigger the workflow
Go to Actions tab in GitHub
Select "Sync Skills to Claude Console"
Click "Run workflow"
Choose which skill(s) to upload
Click "Run workflow"
4. Monitor Uploads
Check the Actions tab to see upload status:
Green checkmark = uploaded successfully
Red X = upload failed (check logs)
Versioning
Skills are versioned using git tags/commits:
Tagged commits: v1.0.0, v1.1.0, etc.
Untagged commits: abc1234 (short SHA)
Dirty working tree: abc1234-dirty
Create a version tag:
git tag -a v1.0.0 -m "Grammar skill v1.0.0"
git push origin v1.0.0
Manual Upload
You can also upload skills manually using the script:
# Install dependencies
pip install -r scripts/requirements.txt

# Upload grammar skill
export ANTHROPIC_API_KEY=sk-ant-...
python scripts/upload-skill.py \
  --skill-path grammar \
  --skill-id skill_01ABC \
  --version v1.0.0

# Upload sermon-writer skill
python scripts/upload-skill.py \
  --skill-path sermon-writer \
  --skill-id skill_01XYZ \
  --version v1.0.0
Troubleshooting
Upload Fails with "401 Unauthorized"
Check that ANTHROPIC_API_KEY secret is set correctly
Verify API key is valid at https://console.anthropic.com/settings/keys
Upload Fails with "Skill Not Found"
Check that GRAMMAR_SKILL_ID and SERMON_WRITER_SKILL_ID secrets match the skill IDs from Claude Console
Skills must be created manually first before automation can update them
No Upload Triggered
Check that files changed are in grammar/ or sermon-writer/ folders
Check the "Detect Changed Skills" job output in Actions tab
API Reference
Skills API documentation:
https://docs.claude.com/en/api/skills-guide
Beta headers required: code-execution-2025-08-25, skills-2025-10-02

---

## 📋 Phase 3: Setup & Testing

### Step 3.1: Add Files to `claude-skills` Repo

```bash
cd /path/to/claude-skills

# Create scripts directory
mkdir -p scripts docs

# Create files (you'll copy content from above)
touch scripts/upload-skill.py
touch scripts/test-skills-api.py
touch scripts/requirements.txt
touch .github/workflows/sync-skills.yml
touch docs/SKILLS_AUTOMATION.md

# Make scripts executable
chmod +x scripts/upload-skill.py scripts/test-skills-api.py
Step 3.2: Test Upload Script Locally
# Install dependencies
pip install -r scripts/requirements.txt

# Test with grammar skill
export ANTHROPIC_API_KEY=your_api_key_here
python scripts/upload-skill.py \
  --skill-path grammar \
  --skill-id skill_01YourGrammarSkillID \
  --version test-v1.0.0
Step 3.3: Configure GitHub Secrets
In GitHub repo settings (williacj/claude-skills):
Go to Settings → Secrets and variables → Actions
Add three secrets:
ANTHROPIC_API_KEY = sk-ant-api03-...
GRAMMAR_SKILL_ID = skill_01... (from Claude Console)
SERMON_WRITER_SKILL_ID = skill_01... (from Claude Console)
Step 3.4: Test GitHub Action
Option A: Trigger manually
Go to Actions tab
Select "Sync Skills to Claude Console"
Click "Run workflow"
Select "all" or specific skill
Monitor output
Option B: Trigger via commit
cd grammar
echo "" >> SKILL.md  # Make a trivial change
git add SKILL.md
git commit -m "test: trigger skills automation"
git push origin main
📋 Phase 4: Production Rollout
Step 4.1: Version Tagging Strategy
Use semantic versioning for skill releases:
# After validating grammar skill (issue #1 complete)
git tag -a grammar-v1.0.0 -m "Grammar skill v1.0.0 - production ready"
git push origin grammar-v1.0.0

# After validating sermon-writer skill (issues #1-#13 complete)
git tag -a sermon-writer-v1.0.0 -m "Sermon Writer skill v1.0.0 - production ready"
git push origin sermon-writer-v1.0.0
Step 4.2: Update sermon-pipeline Submodule
In sermon-pipeline repo, update to latest skills:
cd /path/to/sermon-pipeline/.claude/skills
git pull origin main
cd ../..
git add .claude/skills
git commit -m "chore: update claude-skills submodule to latest"
git push
📋 Summary: Implementation Checklist
Update Todos

Test Skills API with test script

Create skills manually in Claude Console and save skill IDs

Create scripts/upload-skill.py in claude-skills repo

Create .github/workflows/sync-skills.yml in claude-skills repo

Create scripts/requirements.txt in claude-skills repo

Create docs/SKILLS_AUTOMATION.md documentation

Configure GitHub secrets (ANTHROPIC_API_KEY, skill IDs)

Test upload script locally

Test GitHub Action with manual trigger

Verify automation works with actual commit
Would you like me to:
Create a GitHub issue in claude-skills repo to track this automation implementation?
Create these files directly in the claude-skills submodule in your current working directory?
Research the exact Skills API format first before implementing (safer approach)?