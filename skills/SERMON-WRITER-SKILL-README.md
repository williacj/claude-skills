# Sermon Writer Skill - Quick Reference

## What This Skill Does

The Sermon Writer skill generates biblically faithful, intellectually engaging messages for United Church of God (UCG) worship services. It produces:

- **Sermonettes** (1,400-1,600 words) - Short messages, often before offerings
- **Split Sermons** (2,400-2,600 words) - Medium-length messages for two-speaker services
- **Sermons** (3,500-4,000 words) - Full-length main teaching messages

## Key Features

✅ **UCG theological framework** - Non-Trinitarian, Sabbatarian, Torah-observant perspectives
✅ **Holy Day expertise** - Specific guidance for all seven biblical festivals
✅ **Balanced pastoral tone** - Law + Grace, Truth + Grace, Christ-centered, Father-focused
✅ **Quality evaluation** - Four-dimension rubric (Theological Depth, Teaching Clarity, Engagement, Relevance)
✅ **Example-driven** - Five example sermonettes showing proven patterns
✅ **Grows with you** - Add your own sermons, topics, and insights over time

## What's Inside the Skill

### SKILL.md
The main instruction file that tells Claude how to:
- Determine which message type to write (sermonette, split sermon, or sermon)
- Follow proven structural patterns for each length
- Maintain UCG theological positions
- Balance exposition and application appropriately
- Evaluate completed work against quality benchmarks

### Reference Files (in `references/` folder)

#### Core References (Always Available)

1. **theological-framework.md** - UCG doctrinal positions and pastoral communication principles
   - Core doctrinal positions (never violate)
   - UCG distinctive practices (Sabbath, dietary laws, Holy Days)
   - Pastoral tone requirements (Law+Grace balance, accessible language, etc.)
   - Interpretive principles
   - What to avoid (theological errors, tone problems)

2. **example-sermonettes.md** - Five complete example sermonettes showing style and structure
   - Aaron's Glad Heart (Character study)
   - Creation to New Creation (Biblical theology arc)
   - Rejoicing at the Feast (Command exploration)
   - Honor (Word study)
   - Gleaning and the Great Commission (Foreshadowing/fulfillment)

3. **evaluation-rubric.md** - Detailed criteria for reviewing completed sermons
   - Four evaluation dimensions with "Excellent/Good/Needs Work" rubrics
   - Common issues to flag
   - Self-evaluation checklist
   - How to provide constructive feedback

4. **liturgical-overview.md** - The UCG annual calendar and Holy Day cycle
   - Weekly Sabbath overview
   - All seven Holy Days with meanings and themes
   - The annual narrative arc (God's plan from Passover to Last Great Day)
   - Special occasions (Thanksgiving, etc.)
   - What UCG does NOT observe (Christmas, Easter, Halloween) and why

#### Holy Day Files (in `references/holy-days/` folder)

Detailed guidance for each biblical festival:
- **passover.md** - Christ's sacrifice
- **unleavened-bread.md** - Coming out of sin
- **pentecost.md** - Church and firstfruits
- **trumpets.md** - Christ's return
- **atonement.md** - Satan bound
- **tabernacles.md** - Millennial reign
- **last-great-day.md** - Final judgment

Each Holy Day file includes:
- Central meaning and key themes
- Scripture passages (OT foundation and NT fulfillment)
- Common sermon topics (theological, practical, historical)
- Pastoral considerations (tone, challenges, what to avoid)
- Application angles
- Space to add your own sermons over time

#### Special Occasions (in `references/` folder)

5. **special-occasions.md** - Non-Holy Day occasions
   - What UCG may observe (Thanksgiving, weddings, funerals)
   - What UCG does NOT observe and why
   - How to address questions about non-biblical holidays
   - Tone guidelines for special occasions

#### Topics Directory (in `references/topics/` folder)

6. **README.md** - Instructions for building topic-specific reference files
   - Template for creating topic files (faith, love, grace, etc.)
   - How to organize Scripture passages, illustrations, and past sermons
   - Examples of topics worth building
   - How Claude uses topic files to avoid repetition

**Note**: The topics directory starts empty. You add files as you write sermons on specific topics, building your resource library over time.

## How to Use the Skill

### Writing a New Sermon

Simply request what you need:

**For a sermonette** (1,400-1,600 words):
- "Write me a sermonette on faith"
- "Create a sermonette for Pentecost about the Great Commission"
- "Write a sermonette on Romans 12:1-2"

**For a split sermon** (2,400-2,600 words):
- "Write me a split sermon on grace and law"
- "Create a split sermon for the Feast of Tabernacles about God's kingdom"
- "Write a split sermon on overcoming sin"

**For a full sermon** (3,500-4,000 words):
- "Write me a sermon on the Holy Spirit"
- "Create a sermon for Passover exploring Christ's sacrifice"
- "Write a sermon on 1 Corinthians 13"

Claude will automatically:
1. Determine the message type and target word count
2. Read relevant reference files (theological framework, Holy Day files if applicable, topic files if they exist)
3. Write in your established style (based on example sermonettes)
4. Ensure UCG theological positions are maintained
5. Balance exposition and application appropriately
6. Hit the target word count

### Reviewing an Existing Sermon

Submit your sermon with:
- "Review this sermonette using the evaluation rubric"
- "Evaluate this sermon for theological depth and clarity"
- "Check if this Passover sermon aligns with UCG theology"

Claude will:
1. Read the evaluation rubric
2. Check theological framework compliance
3. Assess all four dimensions (Theological Depth, Teaching Clarity, Engagement, Relevance)
4. Provide specific, constructive feedback
5. Suggest concrete improvements

### Writing for Specific Holy Days

Mention the Holy Day and Claude will load the relevant reference file:
- "Write a sermonette for the Day of Atonement"
- "Create a Feast of Tabernacles sermon about rejoicing"
- "Write a Passover sermonette on self-examination"

### Getting Help with Split Sermons

If you're writing a split sermon where another speaker will handle the other half:
- "Write Part 1 of a split sermon on prayer. Part 2 will cover intercessory prayer."
- "Create Part 2 of a split sermon on love. Part 1 covered God's love for us."

Claude will ensure your part complements the other speaker's focus.

## Growing the Skill Over Time

The sermon-writer skill is designed to grow with your ministry. Here's how:

### Adding Your Sermons to Holy Day Files

After writing a sermon for a specific Holy Day:

1. Open the relevant Holy Day file (e.g., `references/holy-days/passover.md`)
2. Scroll to the "Past Sermons/Sermonettes" section
3. Add your sermon with:
   - Date and title
   - Main point (one sentence)
   - Primary Scripture passages
   - Key illustration (if particularly effective)
   - Link or full text if desired

This builds your resource library so Claude can:
- See what angles you've already covered
- Suggest fresh approaches for future sermons
- Reference your best illustrations
- Maintain consistency in your teaching

### Creating Topic Files

After writing 2-3 sermons on the same topic (faith, love, grace, etc.):

1. Create a new file in `references/topics/` (e.g., `faith.md`)
2. Use the template in `references/topics/README.md`
3. Include:
   - Key Scripture passages
   - UCG perspective on this topic
   - Your past sermons on this topic
   - Effective illustrations
   - Application angles you've used
   - Things to avoid

Claude will then:
- Reference your past sermons when writing on this topic again
- Avoid repeating the same angles
- Use illustrations you've found effective
- Build on themes you've already developed

### Updating Examples

If you write a particularly strong sermon that exemplifies a new pattern:
- Add it to `references/example-sermonettes.md`
- Claude will study it when writing future sermons
- Helps maintain consistency in your voice and style

## UCG Theological Distinctives

This skill is specifically designed for United Church of God theology. Key distinctives:

### Core Positions
- **Non-Trinitarian**: Holy Spirit is God's power, not a separate person
- **Sabbatarian**: Saturday (seventh-day) Sabbath worship
- **Torah-observant**: Old Testament dietary laws and festivals remain binding
- **Premillennial**: Christ will return to establish a literal 1,000-year kingdom on earth

### Pastoral Balance
- **Law + Grace**: Always pair God's law with His grace working together
- **Truth + Grace**: Speak honestly about sin while pointing to transformation
- **Christ-centered**: Emphasize Christ's empowerment through the Holy Spirit
- **Father-focused**: Maintain God the Father as supreme, Jesus as the way to Him

### What UCG Observes
- Weekly Sabbath (Friday sunset to Saturday sunset)
- Seven annual Holy Days: Passover, Unleavened Bread, Pentecost, Trumpets, Atonement, Tabernacles, Last Great Day

### What UCG Does NOT Observe
- Christmas, Easter, Halloween (pagan origins, not biblical)
- Sunday worship (not commanded in Scripture)
- Trinity doctrine (not biblical)

## Quality Benchmarks

Every sermon is evaluated against four dimensions:

1. **Theological Depth** - Faithful Scripture interpretation, sound doctrine, theological connections
2. **Teaching Clarity** - Logical structure, clear main point, effective illustrations, smooth transitions
3. **Emotional & Spiritual Engagement** - Speaks to mind and heart, invites reflection, balances hope and challenge
4. **Resonance & Relevance** - Addresses real questions, grounded application, speaks across demographics

## Message Structure Overview

### Sermonette (1,400-1,600 words)
- Opening Hook: 100-200 words
- Exposition: 600-800 words (3-5 sections)
- Application: 400-600 words
- Conclusion: 100-200 words
- Scope: Single focused insight

### Split Sermon (2,400-2,600 words per part)
- Opening Hook: 150-250 words
- Exposition: 1,200-1,500 words (4-6 sections)
- Application: 800-1,000 words
- Conclusion: 150-250 words
- Scope: 2-3 related themes with moderate depth

### Sermon (3,500-4,000 words)
- Opening Hook: 200-400 words
- Exposition: 1,800-2,200 words (5-8 sections)
- Application: 1,200-1,400 words
- Conclusion: 300-400 words
- Scope: Multiple related themes with significant depth

## Installation

1. Download the `sermon-writer.zip` file
2. In Claude, go to the Skills menu
3. Click "Upload Skill"
4. Select the `sermon-writer.zip` file
5. The skill will be available for use immediately

## Example Requests

These phrases will activate the sermon-writer skill:

**Writing**:
- "Write me a sermonette on [topic/passage]"
- "Create a sermon for [Holy Day] about [theme]"
- "Write a split sermon on [topic]"
- "Generate a Passover sermonette exploring [angle]"

**Reviewing**:
- "Review this sermon using the rubric"
- "Evaluate this sermonette for theological accuracy"
- "Check if this aligns with UCG doctrine"
- "Give me feedback on this Feast sermon"

**Holy Day Specific**:
- "Write a Tabernacles sermon about God's kingdom"
- "Create a Day of Atonement sermonette on repentance"
- "Write a Pentecost message about the Church"

## Best Practices

- **Specify message type** - Sermonette, split sermon, or sermon
- **Mention Holy Day context** - Claude will load relevant reference files
- **Indicate your focus** - What angle or passage you want to explore
- **Share audience needs** - Any specific issues the congregation is facing
- **Request depth level** - Introductory vs. deep theological exploration

## Maintenance and Updates

### Regular Updates (Recommended)
- After each Holy Day season, add your sermons to the relevant Holy Day files
- Create topic files after writing 2-3 sermons on the same subject
- Update examples if you write a particularly strong sermon

### Annual Review
- Review theological-framework.md to ensure it reflects current UCG positions
- Update liturgical-overview.md with any changes to Holy Day emphases
- Refresh evaluation-rubric.md based on what you've learned about effective preaching

### Backup Your Changes
- Keep a backup copy of your customized skill
- Export updated reference files periodically
- Preserve your sermon library in the Holy Day and topic files

## Troubleshooting

**If sermons don't match UCG theology**:
- Check that theological-framework.md is being loaded
- Explicitly mention "according to UCG doctrine" in your request
- Review the sermon and point out specific doctrinal concerns

**If the style doesn't match**:
- Reference specific example sermonettes: "Write in the style of the Aaron's Glad Heart sermonette"
- Add your best sermons to example-sermonettes.md
- Provide feedback on what to adjust

**If word count is off**:
- Specify the exact range: "Write a sermonette, 1400-1600 words"
- Ask Claude to check word count before finishing
- Request adjustments: "This is too long, trim to 1500 words"

## Questions?

The skill is designed to adapt to your needs and grow with your ministry. Claude will:
- Ask clarifying questions if needed
- Explain theological choices made
- Suggest improvements based on the evaluation rubric
- Help you build your reference library over time

Start using it today and watch it become an increasingly valuable tool for your sermon preparation!