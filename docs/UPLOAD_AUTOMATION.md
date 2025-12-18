# Upload Automation Documentation

## Overview

The skills upload automation system automatically validates and uploads Claude skills to Claude Console via the Anthropic Skills API. The system is fully config-driven and only uploads skills that have a `skill_id` configured.

## Quick Start

### Upload Skills

```bash
# Upload all skills with configured IDs
python3 scripts/upload-all-skills.py --version v1.0.0

# Upload all skills with git version
python3 scripts/upload-all-skills.py --version $(git describe --tags --always)

# Upload a single skill
python3 scripts/upload-skill.py --skill-name grammar --version v1.0.0
```

## Components

### 1. Upload Single Skill ([scripts/upload-skill.py](../scripts/upload-skill.py))

Uploads a single skill to Claude Console via the Anthropic Skills API.

**Features:**
- Config-driven (reads from `skills-config.json`)
- Validates skill has a `skill_id` before uploading
- Creates zip archive on-the-fly
- Uploads via Anthropic Skills API
- Supports both new config-based mode and legacy explicit-path mode

**Usage:**
```bash
# Using skill name from config (recommended)
python3 scripts/upload-skill.py --skill-name grammar --version v1.0.0

# Legacy mode with explicit paths
python3 scripts/upload-skill.py --skill-path skills/grammar --skill-id skill_01ABC --version v1.0.0
```

**Requirements:**
- `ANTHROPIC_API_KEY` environment variable or `--api-key` flag
- Skill must have `skill_id` configured in `skills-config.json`
- Skill must pass validation

### 2. Upload All Skills ([scripts/upload-all-skills.py](../scripts/upload-all-skills.py))

Uploads all skills with configured IDs to Claude Console.

**Features:**
- Validates all skills before uploading
- Automatically skips skills without `skill_id`
- Uploads each skill sequentially
- Comprehensive upload summary
- Optional validation skip (not recommended)

**Usage:**
```bash
# Upload all configured skills
python3 scripts/upload-all-skills.py --version v1.0.0

# Skip skills without IDs (automatic)
python3 scripts/upload-all-skills.py --version v1.0.0 --skip-missing-ids
```

**What Gets Uploaded:**
- Only skills with `skill_id` configured in `skills-config.json`
- Skills without IDs are automatically skipped with a warning

### 3. GitHub Actions Workflow ([.github/workflows/upload-skills.yml](../.github/workflows/upload-skills.yml))

Automated CI/CD pipeline that:

1. **Validates** all skills before uploading
2. **Detects** which skills changed
3. **Filters** to only upload skills with configured IDs
4. **Uploads** skills to Claude Console in parallel
5. **Reports** upload status and results

**Triggers:**
- Push to `main` branch with changes to:
  - `skills/**` directories
  - `skills-config.json`
  - Upload scripts or workflow files
- Manual dispatch with optional skill selection

**Workflow Jobs:**

| Job | Purpose | Outputs |
|-----|---------|---------|
| `validate` | Run validation checks | `validation_passed` |
| `detect-changes` | Determine which skills to upload | `changed_skills`, `version` |
| `upload-skills` | Upload skills (matrix job) | N/A |
| `summary` | Create summary report | N/A |

## Setup Requirements

### 1. API Key Configuration

**In GitHub (for CI/CD):**
1. Go to repository Settings → Secrets and variables → Actions
2. Add secret: `ANTHROPIC_API_KEY`
3. Value: Your Anthropic API key (format: `sk-ant-api03-...`)

**Locally:**
```bash
# Add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env
```

### 2. Skill ID Configuration

Each skill must have a `skill_id` in `skills-config.json`:

```json
{
  "skills": {
    "grammar": {
      "skill_id": "skill_01LEoRLHpcopdFfXjv9gj9hj",
      "display_title": "Grammar and Proofreading",
      "path": "skills/grammar"
    }
  }
}
```

**To get a skill ID:**
1. Go to https://console.anthropic.com/skills
2. Click "Create New Skill"
3. Fill in name and description
4. Upload initial version manually (or use build script)
5. Copy the `skill_id` (format: `skill_01XXXXX`)
6. Update `skills-config.json`

## Workflow Examples

### Scenario 1: Push Changes to One Skill

```bash
# Make changes to grammar skill
vim skills/grammar/SKILL.md

# Commit and push
git add skills/grammar/
git commit -m "Update grammar skill prompts"
git push origin main
```

**What Happens:**
1. Workflow triggers automatically
2. Validates all skills
3. Detects only `grammar` changed
4. Checks if `grammar` has a `skill_id`
5. Uploads `grammar` to Claude Console
6. Provides upload confirmation in workflow summary

### Scenario 2: Manual Upload of All Skills

**Via GitHub UI:**
1. Go to Actions → "Upload Skills to Claude Console"
2. Click "Run workflow"
3. Select skill: `all`
4. Click "Run workflow"

**What Happens:**
1. Validates all skills
2. Filters to skills with `skill_id` configured
3. Uploads all configured skills in parallel
4. Skips skills without IDs

### Scenario 3: Local Upload for Testing

```bash
# Upload grammar skill locally
python3 scripts/upload-skill.py --skill-name grammar --version test-v1.0.0
```

**When to Use:**
- Testing API integration
- Quick updates without CI/CD
- Debugging upload issues

## Skills Without IDs

Skills that don't have a `skill_id` are **automatically skipped** during uploads:

```bash
# These skills will be skipped in upload
python3 scripts/upload-all-skills.py --version v1.0.0

# Output:
# ⏭️  Skipping biblical-accuracy - no skill_id configured
# ⏭️  Skipping critical-biblical-listener - no skill_id configured
```

**To upload these skills:**
1. Create them in Claude Console first
2. Get the `skill_id`
3. Update `skills-config.json`
4. Run upload again

## Troubleshooting

### Upload Fails with "ANTHROPIC_API_KEY not set"

**Solution:**
```bash
# Check if API key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env
```

### Upload Fails with "no skill_id in config"

**Solution:**
1. Check `skills-config.json` for the skill
2. If `skill_id` is `null`, create the skill in Console first
3. Update config with the real ID

### Upload Fails with API Error

**Common Issues:**
- **Invalid skill_id**: Verify ID matches Console
- **API key expired**: Generate new key in Console
- **Rate limiting**: Wait and retry
- **Network issues**: Check internet connection

**Check API Response:**
```bash
# Run with verbose output to see full error
python3 scripts/upload-skill.py --skill-name grammar --version v1.0.0 2>&1 | tee upload.log
```

### GitHub Actions Upload Fails

1. **Check validation logs** in the `validate` job
2. **Check API key secret** is set correctly in repository settings
3. **Check skill IDs** in `skills-config.json`
4. **Check summary** - workflow creates detailed summary in Actions UI

## Build vs Upload

**When to use which:**

| Task | Tool | Purpose |
|------|------|---------|
| Create deployment packages | `build-all-skills.py` | Manual upload to Console |
| Upload to Console via API | `upload-all-skills.py` | Automated upload |
| CI/CD build workflow | `build-skills.yml` | Create artifacts for manual upload |
| CI/CD upload workflow | `upload-skills.yml` | Automatic upload to Console |

**Typical Workflow:**
1. **Develop locally** - Edit skills, test locally
2. **Commit & push** - Push to main branch
3. **Auto-upload** - GitHub Actions uploads to Console automatically
4. **Verify in Console** - Check skills in Claude Console

**Alternative Workflow (Manual Upload):**
1. **Build locally** - `python3 scripts/build-all-skills.py --version v1.0.0`
2. **Review packages** - Check `deployments/` folder
3. **Upload manually** - Go to Console, upload zip files

## API Details

### Skills API Endpoint

The upload script uses the Anthropic Skills API:

```python
client.beta.skills.versions.create(
    skill_id=skill_id,
    files=skill_zip,  # Base64 encoded zip
    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
)
```

### Versioning

Versions are tracked in the upload metadata but **not enforced** by the API:
- Each upload creates a new version in Console
- Use semantic versioning: `v1.0.0`, `v1.1.0`, `v2.0.0`
- Git tags recommended for production releases

### Rate Limits

The API has rate limits:
- Uploads are sequential (not parallel) to avoid limits
- If rate-limited, wait and retry
- GitHub Actions respects matrix concurrency limits

## Best Practices

### Version Naming

- **Production releases**: `v1.0.0`, `v2.0.0` (semantic versioning)
- **Auto-generated**: `v0.0.0-abc123` (git describe)
- **Testing**: `test-v1.0.0`, `dev-v1.0.0`

### Skill Development Workflow

1. **Create skill locally** - Add to `skills/` directory
2. **Validate** - `python3 scripts/validate-skill.py --skill-name new-skill`
3. **Build** - `python3 scripts/prepare-skill.py --skill-name new-skill --version v0.1.0`
4. **Create in Console** - Upload first version manually to get skill ID
5. **Update config** - Add skill ID to `skills-config.json`
6. **Commit** - Push to git
7. **Auto-upload** - GitHub Actions handles future uploads

### Security

- **Never commit API keys** - Use `.env` file (gitignored)
- **Use repository secrets** - For GitHub Actions
- **Rotate keys regularly** - Generate new keys periodically
- **Limit key scope** - Use keys with minimal required permissions

### Testing

**Before pushing to main:**
```bash
# Validate
python3 scripts/validate-skill.py --all

# Test build (doesn't upload)
python3 scripts/build-all-skills.py --version test-$(date +%Y%m%d)

# Test upload (only if you have API key)
python3 scripts/upload-skill.py --skill-name grammar --version test-upload
```

## Files Reference

| File | Purpose |
|------|---------|
| [skills-config.json](../skills-config.json) | Central skills configuration with IDs |
| [scripts/upload-skill.py](../scripts/upload-skill.py) | Upload single skill |
| [scripts/upload-all-skills.py](../scripts/upload-all-skills.py) | Upload all skills at once |
| [.github/workflows/upload-skills.yml](../.github/workflows/upload-skills.yml) | CI/CD upload workflow |
| [scripts/validate-skill.py](../scripts/validate-skill.py) | Validation script |

## Getting Help

- **API errors**: Check error message in script output
- **GitHub Actions**: Check Actions tab for workflow logs
- **Skill IDs**: Verify in Claude Console settings
- **Config syntax**: Validate JSON at https://jsonlint.com
- **API docs**: https://docs.anthropic.com/claude/docs/skills-api
