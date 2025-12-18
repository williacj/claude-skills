# Build Automation Documentation

## Overview

The skills build automation system automatically validates, builds, and packages Claude skills for deployment to Claude Console. The system is fully config-driven and supports all skills defined in [skills-config.json](../skills-config.json).

## Quick Start

### Validate Skills

```bash
# Validate a specific skill
python3 scripts/validate-skill.py --skill-name grammar

# Validate all skills
python3 scripts/validate-skill.py --all

# Verbose output
python3 scripts/validate-skill.py --skill-name sermon-writer --verbose
```

### Build Skill Packages

```bash
# Build ALL skills at once (recommended)
python3 scripts/build-all-skills.py --version v1.0.0

# Build all skills with git version
python3 scripts/build-all-skills.py --version $(git describe --tags --always)

# Build a single skill
python3 scripts/prepare-skill.py --skill-name grammar --version v1.0.0

# Legacy mode with explicit paths
python3 scripts/prepare-skill.py --skill-path skills/grammar --skill-id skill_01ABC --version v1.0.0
```

## Components

### 1. Skills Configuration ([skills-config.json](../skills-config.json))

Central configuration file that defines all skills:

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

**Adding a New Skill:**

1. Create skill directory with `SKILL.md` file
2. Add entry to `skills-config.json`:
   ```json
   "your-skill-name": {
     "skill_id": null,  // Will be filled after creating in Console
     "display_title": "Your Skill Display Name",
     "path": "skills/your-skill-directory"
   }
   ```
3. Create the skill in Claude Console manually
4. Update `skill_id` in config with the ID from Console

### 2. Validation Script ([scripts/validate-skill.py](../scripts/validate-skill.py))

Validates skill structure before building:

**Checks Performed:**
- ✅ Skill directory exists
- ✅ `SKILL.md` exists and is not empty
- ✅ `SKILL.md` has proper frontmatter
- ✅ Skill ID is valid format
- ✅ Display title is configured
- ⚠️ Warns about missing skill IDs (for new skills)
- ⚠️ Warns about hidden files (`.DS_Store`, etc.)
- ⚠️ Warns about large package sizes (>5MB)
- ℹ️ Reports references directory and file counts

**Exit Codes:**
- `0` - All validations passed (or passed with warnings only)
- `1` - Validation failed with errors

### 3. Build Scripts

#### Build All Skills ([scripts/build-all-skills.py](../scripts/build-all-skills.py))

Builds all skills at once with validation:

**Features:**
- Validates all skills before building
- Builds all skills from config in one command
- Parallel-friendly architecture
- Comprehensive build summary
- Optional validation skip (not recommended)

**Usage:**
```bash
python3 scripts/build-all-skills.py --version v1.0.0
```

#### Build Single Skill ([scripts/prepare-skill.py](../scripts/prepare-skill.py))

Creates deployment-ready zip packages for individual skills:

**Features:**
- Config-driven (reads from `skills-config.json`)
- Automatically packages all skill files (excluding hidden files)
- Generates metadata JSON with deployment instructions
- Handles skills without IDs (for new skills not yet in Console)
- Supports both new config-based mode and legacy explicit-path mode

**Output:**
- `deployments/{skill-name}-{version}.zip` - Skill package
- `deployments/{skill-name}-{version}.json` - Deployment metadata

### 4. GitHub Actions Workflow ([.github/workflows/build-skills.yml](../.github/workflows/build-skills.yml))

Automated CI/CD pipeline that:

1. **Validates** all skills before building
2. **Detects** which skills changed (or builds all if config changed)
3. **Builds** packages for each changed skill in parallel
4. **Uploads** artifacts for manual deployment

**Triggers:**
- Push to `main` branch with changes to:
  - `skills/**` directories
  - `skills-config.json`
  - Build scripts or workflow files
- Manual dispatch with optional skill selection

**Workflow Jobs:**

| Job | Purpose | Outputs |
|-----|---------|---------|
| `validate` | Run validation checks | `validation_passed` |
| `detect-changes` | Determine which skills to build | `changed_skills`, `version` |
| `build-skills` | Build packages (matrix job) | Artifacts per skill |
| `summary` | Create summary report | N/A |

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
4. Builds only `grammar` package
5. Uploads artifact: `grammar-{version}`

### Scenario 2: Manual Build of All Skills

**Via GitHub UI:**
1. Go to Actions → Build Skills Packages
2. Click "Run workflow"
3. Select skill: `all`
4. Click "Run workflow"

**What Happens:**
1. Validates all skills
2. Builds all skills in parallel
3. Uploads separate artifacts for each

### Scenario 3: Update Config File

```bash
# Add new skill to config
vim skills-config.json

git commit -m "Add new critical-listener skill"
git push origin main
```

**What Happens:**
1. Workflow detects config changed
2. Rebuilds **ALL** skills (to ensure consistency)
3. Uploads all artifacts

## Deployment Process

### Automatic (Via GitHub Actions)

1. **Make Changes** - Edit skills locally
2. **Commit & Push** - Workflow triggers automatically
3. **Download Artifacts** - From GitHub Actions run
4. **Upload to Console** - Manual upload to Claude Console

### Manual (Local Build)

1. **Validate First:**
   ```bash
   python3 scripts/validate-skill.py --skill-name your-skill
   ```

2. **Build Package:**
   ```bash
   python3 scripts/prepare-skill.py --skill-name your-skill --version v1.0.0
   ```

3. **Upload to Console:**
   - Go to https://console.anthropic.com/skills
   - Find your skill by skill ID
   - Upload the zip file from `deployments/`

## Skills Without IDs (New Skills)

For skills that don't have a `skill_id` yet:

1. **Build Package Anyway:**
   ```bash
   python3 scripts/prepare-skill.py --skill-name biblical-accuracy --version v1.0.0
   ```
   - Script will warn but still create package
   - Uses placeholder ID: `skill_PENDING_{skill-name}`

2. **Create Skill in Console:**
   - Go to https://console.anthropic.com/skills
   - Click "Create New Skill"
   - Fill in details, upload package
   - Copy the generated `skill_id`

3. **Update Config:**
   ```bash
   # Update skills-config.json with real ID
   vim skills-config.json
   ```

4. **Rebuild:**
   ```bash
   python3 scripts/prepare-skill.py --skill-name biblical-accuracy --version v1.0.1
   ```

## Troubleshooting

### Validation Fails

```bash
# Run validation with verbose output
python3 scripts/validate-skill.py --skill-name your-skill --verbose
```

**Common Issues:**
- Missing `SKILL.md` - Create the file
- Empty `SKILL.md` - Add content with frontmatter
- No frontmatter - Add YAML frontmatter to top of SKILL.md
- Hidden files warning - Safe to ignore, they're automatically excluded

### Build Fails

**Check Skill Path:**
```bash
# Verify path in config matches actual directory
ls -la skills/your-skill-directory/
```

**Check for Spaces:**
- Skill paths with spaces work but may need quotes in shell commands
- Example: `"skills/biblical accuracy skill"` is valid

### GitHub Actions Fails

1. **Check validation logs** in the `validate` job
2. **Check matrix builds** - individual skills may fail separately
3. **Check summary** - workflow creates detailed summary in Actions UI

## Best Practices

### Version Naming

- **Git tags**: `v1.0.0`, `v1.1.0` (semantic versioning)
- **Auto-generated**: `v0.0.0-abc123` (git describe)
- **Manual**: `test-v1.0.0`, `hotfix-v1.0.1`

### Skill Structure

```
skills/your-skill/
├── SKILL.md              # Required - main skill definition
└── references/           # Optional - supporting files
    ├── examples.md
    ├── guidelines.md
    └── templates.md
```

### Config Management

- Always validate after editing config:
  ```bash
  python3 scripts/validate-skill.py --all
  ```
- Keep skill IDs in sync between config and Console
- Use descriptive `display_title` values

### Git Workflow

- **Feature branches** for skill development
- **Validate** before committing
- **Commit** skill changes separately from config changes
- **Tag** releases for important versions

## Upload Automation

The upload automation is now available! After building packages, you can automatically upload them to Claude Console via the API:

**See [UPLOAD_AUTOMATION.md](./UPLOAD_AUTOMATION.md) for complete upload documentation.**

**Quick start:**
```bash
# Upload all skills
python3 scripts/upload-all-skills.py --version v1.0.0

# Upload single skill
python3 scripts/upload-skill.py --skill-name grammar --version v1.0.0
```

**Requirements:**
- `ANTHROPIC_API_KEY` environment variable
- Skills must have `skill_id` configured in [skills-config.json](../skills-config.json)

## Files Reference

| File | Purpose |
|------|---------|
| [skills-config.json](../skills-config.json) | Central skills configuration |
| [scripts/validate-skill.py](../scripts/validate-skill.py) | Validation script |
| [scripts/build-all-skills.py](../scripts/build-all-skills.py) | Build all skills at once |
| [scripts/prepare-skill.py](../scripts/prepare-skill.py) | Build single skill |
| [scripts/upload-all-skills.py](../scripts/upload-all-skills.py) | Upload all skills at once |
| [scripts/upload-skill.py](../scripts/upload-skill.py) | Upload single skill |
| [.github/workflows/build-skills.yml](../.github/workflows/build-skills.yml) | CI/CD build workflow |
| [.github/workflows/upload-skills.yml](../.github/workflows/upload-skills.yml) | CI/CD upload workflow |
| [docs/UPLOAD_AUTOMATION.md](./UPLOAD_AUTOMATION.md) | Upload automation documentation |

## Getting Help

- **Validation errors**: Run with `--verbose` flag
- **Build issues**: Check [scripts/prepare-skill.py](../scripts/prepare-skill.py:1) source
- **Workflow issues**: Check Actions logs and summary
- **Config syntax**: Validate JSON at https://jsonlint.com
