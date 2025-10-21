# Claude Skills

This directory contains custom Claude skills that are automatically synced to Claude Console.

## Structure

```
skills/
├── grammar/           # Grammar and writing style skill
│   ├── SKILL.md      # Main skill definition
│   └── references/   # Supporting documentation
└── sermon-writer/    # Sermon writing assistant skill
    ├── SKILL.md      # Main skill definition
    └── references/   # Supporting documentation
```

## How Skills Work

Each skill folder must contain:
- `SKILL.md` - The main skill definition and instructions
- `references/` - Supporting documentation, examples, and context

## Automation

Skills are automatically uploaded to Claude Console when:
1. Changes are committed to `main` branch
2. Files in `skills/*/` folders are modified
3. Manual workflow trigger in GitHub Actions

See `../docs/SKILLS_AUTOMATION.md` for full automation details.

## Adding New Skills

1. Create a new folder under `skills/`
2. Add `SKILL.md` with skill definition
3. Add `references/` folder with supporting docs
4. Update GitHub workflow in `../.github/workflows/sync-skills.yml`
5. Create the skill manually in Claude Console first
6. Add skill ID to GitHub secrets