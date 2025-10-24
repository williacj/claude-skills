# Quick Start Guide: Critical Biblical Listener Skill

## Installation (2 minutes)

1. Download `critical-biblical-listener.skill` from this folder
2. In Claude, go to your Skills settings
3. Upload the .skill file
4. The skill is now available and will auto-trigger when appropriate

## Basic Usage (5 minutes)

### Simple Review Request

```
Please review this sermon for biblical accuracy:

[Paste sermon text here]
```

Claude will automatically use the Critical Biblical Listener skill to evaluate the sermon.

### Specify Focus Areas

```
Using the Critical Biblical Listener skill, please review this sermon 
with special attention to how Old Testament passages are applied:

[Paste sermon text here]
```

### Request Specific Severity Level

```
Review this sermon and flag only Critical and Important issues 
(skip minor suggestions):

[Paste sermon text here]
```

## What You'll Get Back

Claude will provide:

1. **Summary** — Brief overview of the sermon's theological argument
2. **Strengths** — 2-3 things the sermon does well biblically
3. **Issues** — Detailed critique organized by severity:
   - Location in the sermon
   - What claim was made
   - Why it misaligns with Scripture
   - Biblical evidence with references
   - Alternative faithful reading
4. **Suggestions** — How to strengthen the biblical foundation

## Common Use Cases

### Case 1: Quick Spot-Check
**Scenario**: You want to verify a specific claim or passage usage

```
Does this sermon handle Romans 8:28 correctly?

[Paste relevant section]
```

### Case 2: Comprehensive Review
**Scenario**: Full sermon evaluation before delivery

```
Please provide a comprehensive biblical review of this sermon, 
including all severity levels:

[Paste full sermon]
```

### Case 3: Comparative Analysis
**Scenario**: Check if two interpretations align with Scripture

```
I have two different interpretations of Jeremiah 29:11. 
Which aligns better with the biblical context?

Interpretation A: [...]
Interpretation B: [...]
```

### Case 4: Teaching Preparation
**Scenario**: Verify your biblical support before teaching

```
I'm preparing to teach on spiritual warfare. Review my 
use of Ephesians 6:12 to ensure I'm not misapplying it:

[Paste teaching notes]
```

## Understanding Reference Files

The skill includes three deep reference files that Claude will automatically load when needed:

### 1. Common Misapplications (auto-loads for frequently misused verses)
- Romans 8:28 (prosperity gospel)
- Jeremiah 29:11 (personal success promises)
- Matthew 7:1 (judgment issues)
- Philippians 4:13 (achievement theology)
- And 10+ more

### 2. Genre Guidelines (auto-loads for genre-specific questions)
- How to interpret narrative vs. law vs. poetry
- When to use literal vs. figurative readings
- Handling apocalyptic literature
- Applying wisdom literature appropriately

### 3. Covenant Context (auto-loads for OT/NT application questions)
- Old vs. New Covenant distinctions
- How to apply OT law today
- Progressive revelation principles
- Common covenant-related errors

**You don't need to manually trigger these**—Claude will read them when encountering relevant interpretive challenges.

## Pro Tips

### Tip 1: Provide Context
Include the sermon's target audience for better evaluation:

```
Review this sermon for biblical accuracy. 
Target audience: New believers / General congregation / Youth group

[Sermon text]
```

### Tip 2: Ask Follow-Up Questions
The skill enables deep biblical discussion:

```
You flagged the use of Proverbs 22:6 as potentially overextended. 
Can you explain more about how Proverbs should be interpreted?
```

### Tip 3: Request Specific Output
Customize the review format if needed:

```
Review this sermon but organize feedback by passage 
(not by severity level):

[Sermon text]
```

### Tip 4: Compare with Your Own Analysis
Test your biblical reasoning:

```
I think this sermon misuses Matthew 18:20. Here's why: [your reasoning]
Do you agree with my assessment?

[Sermon excerpt]
```

## Troubleshooting

### "The review seems too harsh"
Claude maintains analytical rigor while being charitable. If feedback seems harsh, remember:
- Critical issues represent serious biblical misalignment
- The skill distinguishes between definite error and debatable interpretation
- Tone is analytical, not combative

### "I disagree with the assessment"
Good! Biblical interpretation involves careful reasoning. Ask:
```
I disagree with your assessment of [passage]. Here's my reasoning: [...]
Can you explain your perspective more fully?
```

### "The review missed something"
Point it out:
```
You didn't mention [specific issue]. Can you evaluate that as well?
```

### "I need more detail"
Request deeper analysis:
```
Can you load the covenant-context reference file and explain 
the Old/New Covenant distinction related to [passage]?
```

## Next Steps

1. **Start simple**: Try reviewing a short sermon excerpt first
2. **Read the example**: Check `EXAMPLE_USAGE.md` to see a full review
3. **Explore references**: Ask Claude about specific biblical topics
4. **Integrate**: Use alongside other sermon review skills for comprehensive feedback

## Support

- Review `README.md` for full skill documentation
- Check `EXAMPLE_USAGE.md` for detailed example
- Ask Claude questions about biblical interpretation—the skill enables sophisticated theological dialogue

---

**Ready to start?** Just paste your sermon text and ask Claude to review it for biblical accuracy!
