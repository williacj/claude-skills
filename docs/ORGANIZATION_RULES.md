# Repository Organization Rules

## 📁 File Organization Standards

### Documentation Files
- **ALL documentation** must go in `docs/` folder
- **Never** create `.md` files in root directory
- **Exception:** Only `README.md` belongs in root

### Correct Structure:
```
claude-skills/
├── README.md                    # ✅ Only markdown file in root
├── docs/                        # ✅ ALL other documentation here
│   ├── PROJECT_STATUS.md
│   ├── SKILLS_AUTOMATION.md
│   └── Automated_Upload_Plan.md
├── skills/                      # ✅ Skill content
├── scripts/                     # ✅ Automation scripts
└── .github/                     # ✅ GitHub workflows
```

### ❌ NEVER DO:
- Create `SOME_DOC.md` in root directory
- Put documentation anywhere except `docs/`
- Mix documentation with code files

### ✅ ALWAYS DO:
- Check if creating documentation → use `docs/` folder
- Ask "Is this a README for the whole repo?" → if no, use `docs/`
- Maintain clean root directory

## 🤖 AI Assistant Reminder

**BEFORE creating any `.md` file:**
1. Is this the main repository README? 
   - YES → Create in root as `README.md`
   - NO → Create in `docs/` folder
2. Double-check the path includes `docs/`
3. Verify file organization follows this standard

**Remember:** Good organization makes the repository professional and maintainable!