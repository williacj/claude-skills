# Critical Biblical Listener Skill

A comprehensive Claude skill for evaluating sermons and biblical teaching from a biblically literate perspective.

## What This Skill Does

The Critical Biblical Listener skill transforms Claude into a careful, biblically literate reviewer who:

- **Tests claims against Scripture**: Evaluates whether theological assertions are explicitly supported by biblical text or merely inferred
- **Checks contextual integrity**: Ensures passages are used within their proper literary, historical, and covenantal context
- **Identifies overextensions**: Points out where sermons stretch beyond what the biblical text clearly says
- **Detects imported assumptions**: Flags where modern or denominational assumptions are being read into Scripture
- **Maintains theological neutrality**: Evaluates biblical alignment without advocating for specific denominations

## Skill Structure

### Main File: SKILL.md
The core skill provides:
- **Core Evaluation Principles**: Textual fidelity, contextual integrity, exegetical accuracy, theological neutrality
- **Step-by-step evaluation process**: How to identify claims, test them, and document concerns
- **Severity guidelines**: Critical issues, important concerns, suggestions for improvement
- **Output format**: Structured review template
- **Tone guidance**: Analytical, fair, charitable, but skeptical in service of truth

### Reference Files (loaded as needed)

1. **common-misapplications.md** (1,900+ words)
   - Frequently misinterpreted passages like Romans 8:28, Jeremiah 29:11, Matthew 7:1
   - Contextual reality vs. common misapplication
   - Balancing texts and interpretive principles

2. **genre-guidelines.md** (2,600+ words)
   - How to interpret different biblical genres: narrative, law, wisdom, poetry, prophecy, gospels, epistles, apocalyptic
   - DO/DON'T lists for each genre
   - Application principles across genres

3. **covenant-context.md** (2,400+ words)
   - Old vs. New Covenant distinctions
   - How to apply Old Testament texts appropriately
   - Common errors in covenant application
   - Progressive revelation principles

## How to Use This Skill

1. **Install the skill** in Claude by uploading the `critical-biblical-listener.skill` file
2. **Trigger the skill** by asking Claude to review sermon content for biblical accuracy
3. **Provide sermon text** you want evaluated
4. **Receive structured feedback** with:
   - Summary of the sermon's message
   - Strengths and faithful elements
   - Scriptural misalignments or weak supports (with severity ratings)
   - Doctrinal ambiguities or overextensions
   - Suggestions for greater textual clarity

## Example Usage

```
"Please review this sermon using the Critical Biblical Listener skill. Here's the text:

[Sermon content]
```

Claude will automatically:
1. Identify key theological claims
2. Test each claim against Scripture
3. Check contextual usage of passages
4. Flag overextensions or misapplications
5. Provide detailed feedback with biblical references

## What Makes This Different

This skill is **not**:
- A grammar or writing style reviewer
- An engagement or flow assessor
- A denominational advocate
- An SEO optimizer

This skill **is**:
- Focused on biblical faithfulness
- Grounded in original languages and context
- Balanced and charitable while maintaining scrutiny
- Equipped with deep reference material on common interpretive issues

## Severity Levels Explained

- **Critical**: Direct contradiction of Scripture, misquoting passages, reversing meaning through decontextualization
- **Important**: Overextending biblical support, ignoring balancing texts, theological leaps requiring unproven assumptions
- **Suggestion**: Opportunities to strengthen exegetical foundation, add cross-references, acknowledge interpretive limitations

## Integration with Other Sermon Review Skills

This skill complements:
- **Critical Listener Reviewer**: Evaluates engagement, flow, and practical application
- **Grammar Reviewer**: Checks spelling, grammar, and writing mechanics
- **SEO Reviewer**: Optimizes content for search and discoverability

Together, these provide comprehensive sermon review from biblical, communicative, and technical perspectives.

## Technical Details

- **Skill Size**: ~15KB packaged
- **Main Content**: ~1,800 words in SKILL.md
- **Reference Material**: ~6,900 words across 3 reference files
- **Format**: Standard .skill package (zip with .skill extension)

## Credits

Based on the sermon reviewer agent framework and adapted from the original Critical Listener Reviewer documentation.

---

**Ready to use**: Simply upload `critical-biblical-listener.skill` to Claude and start reviewing sermons for biblical faithfulness!
