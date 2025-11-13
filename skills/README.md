# Claude Skills

This directory contains custom Claude skills that are automatically uploaded to Claude Console via the Anthropic Skills API.

## Available Skills

### Active Skills
- **grammar** - Grammar and proofreading for biblical/theological writing
- **sermon-writer** - Sermon, sermonette, and split sermon generation
- **biblical-accuracy** - Biblical accuracy verification with original language analysis
- **critical-biblical-listener** - Skeptical biblical listener evaluating sermon content

## Structure

```
skills/
├── grammar/                      # Grammar and writing style skill
│   ├── SKILL.md                 # Main skill definition
│   └── references/              # Supporting documentation
├── sermon-writer/               # Sermon writing assistant skill
│   ├── SKILL.md                # Main skill definition
│   └── references/             # Supporting documentation
├── biblical accuracy skill/     # Biblical accuracy checker
│   └── SKILL.md                # Main skill definition
└── critical-biblical-listener/  # Critical sermon evaluator
    └── SKILL.md                # Main skill definition
```

## How Skills Work

Each skill folder must contain:
- `SKILL.md` - The main skill definition and instructions (required)
- `references/` - Supporting documentation, examples, and context (optional)

## Automated CI/CD Pipeline

Skills are automatically uploaded to Claude Console when:
1. Changes are pushed to `main` branch
2. Files in `skills/**` folders are modified
3. Configuration in `skills-config.json` is updated
4. Manual workflow trigger in GitHub Actions

**Key Features:**
- Automatically creates new skills (when `skill_id` is `null`)
- Automatically updates existing skills (when `skill_id` is set)
- Parallel upload of multiple changed skills
- Detailed workflow summaries

See `../docs/CI-CD-PIPELINE.md` for complete automation documentation.

## Adding New Skills

1. Create a new folder under `skills/` with your skill name
2. Add `SKILL.md` with skill definition (see existing skills for format)
3. Add entry to `../skills-config.json`:
   ```json
   "your-skill-name": {
     "skill_id": null,
     "display_title": "Your Skill Display Name",
     "path": "skills/your-skill-name"
   }
   ```
4. Commit and push to `main`
5. CI/CD will create the skill and output the skill ID
6. Update `skills-config.json` with the new skill ID
7. Commit the config update

## Updating Existing Skills

1. Edit files in `skills/your-skill/`
2. Commit and push to `main`
3. CI/CD automatically uploads new version

No manual steps required for updates!