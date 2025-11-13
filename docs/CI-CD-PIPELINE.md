# CI/CD Pipeline for Claude Skills

ABOUTME: Documentation for automated skill upload pipeline using GitHub Actions and Anthropic Skills API.

This repository uses GitHub Actions to automatically upload and update Claude Skills via the Anthropic Skills API whenever changes are pushed to the `main` branch.

## Overview

**Automated Upload Pipeline:**
- Detects skill changes on push to `main`
- Automatically creates new skills (if `skill_id` is null)
- Automatically updates existing skills (if `skill_id` is set)
- Supports manual trigger for specific skills or all skills

## Configuration

### 1. Skills Configuration File

`skills-config.json` - Central configuration mapping skill names to IDs and metadata:

```json
{
  "skills": {
    "grammar": {
      "skill_id": "skill_01LEoRLHpcopdFfXjv9gj9hj",
      "display_title": "Grammar and Proofreading",
      "path": "skills/grammar"
    },
    "sermon-writer": {
      "skill_id": "skill_017hvH95CWyhykzXbG542B3B",
      "display_title": "Sermon Writer",
      "path": "skills/sermon-writer"
    },
    "biblical-accuracy": {
      "skill_id": null,
      "display_title": "Biblical Accuracy Checker",
      "path": "skills/biblical accuracy skill"
    }
  }
}
```

**Fields:**
- `skill_id`: Anthropic skill ID (set to `null` for new skills)
- `display_title`: Human-readable name shown in Claude Console
- `path`: Relative path to skill directory containing `SKILL.md`

### 2. GitHub Secrets

Required secret in repository settings:

- `ANTHROPIC_API_KEY` - Your Anthropic API key with skills management permissions

**Setup:**
1. Go to repository Settings → Secrets and variables → Actions
2. Add new secret: `ANTHROPIC_API_KEY`
3. Paste your Anthropic API key

## Workflows

### Automated Upload (`upload-skills.yml`)

**Triggers:**
- Push to `main` with changes to `skills/**` or `skills-config.json`
- Manual trigger via GitHub Actions UI

**What it does:**
1. Detects which skills changed
2. For each changed skill:
   - If `skill_id` is `null` → Creates new skill, outputs ID to add to config
   - If `skill_id` exists → Updates skill with new version
3. Provides summary of upload status

**Matrix build:**
- Uploads multiple changed skills in parallel
- Each skill uploads independently (fail-fast disabled)

### Manual Trigger

Trigger the workflow manually from GitHub Actions UI:

1. Go to Actions → "Upload Skills to Anthropic"
2. Click "Run workflow"
3. Select skill:
   - `all` - Upload all skills
   - `grammar` - Upload only grammar skill
   - `sermon-writer` - Upload only sermon-writer skill
   - etc.

## Usage

### Adding a New Skill

1. Create skill directory under `skills/` with `SKILL.md`
2. Add entry to `skills-config.json`:
   ```json
   "new-skill-name": {
     "skill_id": null,
     "display_title": "My New Skill",
     "path": "skills/new-skill-name"
   }
   ```
3. Commit and push to `main`
4. CI/CD creates the skill automatically
5. Check workflow output for skill ID
6. Update `skills-config.json` with the new skill ID
7. Commit the updated config

### Updating an Existing Skill

1. Edit files in `skills/your-skill/`
2. Commit and push to `main`
3. CI/CD automatically uploads new version

### Local Testing

Test the upload script locally:

```bash
# Install dependencies
pip install anthropic python-dotenv

# Create .env file with API key
echo "ANTHROPIC_API_KEY=your-key-here" > .env

# Update existing skill
python scripts/upload-skill.py --skill-name grammar

# Create new skill
python scripts/upload-skill.py --skill-name biblical-accuracy

# Override config manually
python scripts/upload-skill.py \
  --skill-path skills/grammar \
  --skill-id skill_01ABC \
  --display-title "Grammar Checker"
```

## File Structure

```
.
├── .github/workflows/
│   ├── upload-skills.yml          # Automated upload pipeline (NEW)
│   └── prepare-skills.yml         # Legacy manual workflow (kept for reference)
├── skills/
│   ├── grammar/
│   │   └── SKILL.md
│   ├── sermon-writer/
│   │   └── SKILL.md
│   ├── biblical accuracy skill/
│   │   └── SKILL.md
│   └── critical-biblical-listener/
│       └── SKILL.md
├── scripts/
│   ├── upload-skill.py            # Upload/create skills via API
│   ├── prepare-skill.py           # Legacy preparation script
│   └── test-skills-api.py         # API connectivity test
├── skills-config.json             # Central skill configuration
└── docs/
    └── CI-CD-PIPELINE.md          # This file
```

## API Reference

The upload script uses the Anthropic Skills API:

**Create new skill:**
```python
client.beta.skills.create(
    display_title="Skill Name",
    files=[(filename, content), ...],
    betas=["skills-2025-10-02"]
)
```

**Update skill version:**
```python
client.beta.skills.versions.create(
    skill_id="skill_01ABC",
    files=[(filename, content), ...],
    betas=["skills-2025-10-02"]
)
```

**List skills:**
```python
client.beta.skills.list(
    betas=["skills-2025-10-02"]
)
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

**Cause:** GitHub secret not configured
**Fix:** Add `ANTHROPIC_API_KEY` to repository secrets

### "Skill 'name' not found in skills-config.json"

**Cause:** Skill name doesn't match config
**Fix:** Check spelling in config file and workflow trigger

### "SKILL.md not found in path"

**Cause:** Skill directory missing required `SKILL.md` file
**Fix:** Add `SKILL.md` to skill directory

### Skill created but need to save ID

**Symptom:** Workflow creates skill but doesn't update config automatically
**Expected behavior:** This is intentional for safety
**Fix:**
1. Check workflow output for new skill ID
2. Manually update `skills-config.json` with the ID
3. Commit and push the config update

### Upload fails with API error

**Debug steps:**
1. Check API key has correct permissions
2. Verify skill structure (must have `SKILL.md`)
3. Check file size (max 8MB total)
4. Review workflow logs for detailed error message

## Migration from Old Workflow

The old `prepare-skills.yml` workflow is kept for reference but is superseded by `upload-skills.yml`.

**Key differences:**
- Old: Creates zip artifacts for manual upload
- New: Automatically uploads via API

**Migration steps:**
1. Ensure `ANTHROPIC_API_KEY` secret is set
2. Update `skills-config.json` with all skill IDs
3. New workflow will automatically run on next push to `main`
4. (Optional) Disable or delete `prepare-skills.yml`

## Security Considerations

- API key is stored as GitHub secret (never in code)
- Skills are uploaded to organization-wide Claude workspace
- All skill versions are retained by Anthropic
- Skill IDs are not sensitive (safe to commit to repo)

## Future Enhancements

Potential improvements:
- Automatic skill_id update in config after creation
- Version tagging based on git tags
- Skill validation before upload
- Dry-run mode for testing
- Rollback to previous version
- Automated testing of skills after upload
