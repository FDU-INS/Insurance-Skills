# Skills Format v2.0 Migration Guide

## Overview

The Skills format has been upgraded to v2.0 with Claude-first design principles. This guide documents the changes, backward compatibility, and migration path.

## What Changed

### v1.0 → v2.0 Key Differences

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Design Philosophy** | Schema documentation | Claude knowledge transfer |
| **Primary Audience** | Human developers + Claude | Claude (with human maintenance) |
| **Knowledge Section** | "Knowledge" | "Domain Knowledge" (narrative style) |
| **Examples Section** | "Examples" | "Example Requests and Interpretations" |
| **Intent Recognition** | None | "For Claude" + "When to Use This Skill" |
| **Application Guidance** | None | "Generation Guidelines" |
| **Parameter Style** | Type definitions | Natural language questions |

### New v2.0 Sections

1. **For Claude** (Required for v2.0)
   - Direct instructions to Claude about when and how to use the skill
   - Written in second person: "Use this skill when..."
   - Critical for skill discoverability

2. **When to Use This Skill** (Required for v2.0)
   - Structured intent recognition with:
     - Direct Keywords
     - Clinical Cohorts
     - Implicit Indicators
     - Co-occurring Mentions
   - Helps Claude identify when to apply this knowledge

3. **Domain Knowledge** (Replaces "Knowledge")
   - Narrative teaching style vs schema listing
   - Includes "Why this matters for generation" sidebars
   - Explains patterns and relationships, not just facts

4. **Generation Guidelines** (New optional section)
   - Shows Claude how to apply domain knowledge
   - Includes coherence checks and selection logic
   - May include pseudocode for complex decisions

5. **Example Requests and Interpretations** (Replaces "Examples")
   - Shows user request → Claude's interpretation → generated features
   - Demonstrates reasoning process, not just outputs
   - Includes 3-5 diverse examples per skill

## Version Detection

Skills are automatically detected as v2.0 when they include both:
- "For Claude" section
- "When to Use This Skill" section

```python
from healthsim.skills.loader import SkillLoader

loader = SkillLoader()
skill = loader.load_file("skills/sepsis.md")

if skill.is_v2_format():
    print(f"v2.0 skill with intent keywords: {skill.when_to_use}")
else:
    print("v1.0 skill")

# Or check version directly
print(f"Format version: {skill.get_format_version()}")  # "1.0" or "2.0"
```

## Backward Compatibility

**v2.0 is fully backward compatible with v1.0**

- All v1.0 sections remain valid in v2.0 format
- v1.0 skills load and work exactly as before
- v2.0 sections are additive, not replacements
- Tools can handle both formats transparently

### Section Name Mapping

The loader automatically handles both naming conventions:

| v1.0 Section Name | v2.0 Section Name | Loader Behavior |
|-------------------|-------------------|-----------------|
| "Knowledge" | "Domain Knowledge" | Tries v2.0 first, falls back to v1.0 |
| "Examples" | "Example Requests and Interpretations" | Tries v2.0 first, falls back to v1.0 |
| N/A | "For Claude" | v2.0 only, stored in `skill.for_claude` |
| N/A | "When to Use This Skill" | v2.0 only, stored in `skill.when_to_use` |
| N/A | "Generation Guidelines" | v2.0 only, stored in `skill.generation_guidelines` |

## Migration Path

### Option 1: Keep v1.0 Skills As-Is
If your v1.0 skills work well, you can continue using them indefinitely. The system fully supports v1.0 format.

### Option 2: Gradual Migration
Migrate skills incrementally as you update them:

1. Add "For Claude" section with direct instructions
2. Add "When to Use This Skill" with keywords
3. Optionally rename "Knowledge" → "Domain Knowledge" and improve narrative
4. Optionally rename "Examples" → "Example Requests and Interpretations"
5. Optionally add "Generation Guidelines"

### Option 3: Hybrid Approach
Create v2.0 skills that also include v1.0 sections for maximum compatibility:

```markdown
# Sepsis Cohort

## For Claude
Use this skill when the user requests septic patients...

## When to Use This Skill
**Direct Keywords**: "sepsis", "septic shock"...

## Metadata
- **Type**: cohort-template
- **Version**: 2.0

## Purpose
...

## Domain Knowledge
[Narrative teaching style...]

## Generation Rules
[Keep v1.0 structured rules too]

### Demographics
- Age: 60-85
```

## Code Changes

### Schema Updates

Three new optional fields added to `Skill` model:

```python
class Skill(BaseModel):
    # ... existing v1.0 fields ...

    # v2.0 format fields
    for_claude: str | None = None
    when_to_use: str | None = None
    generation_guidelines: str | None = None
```

### New Methods

```python
# Version detection
skill.is_v2_format() -> bool
skill.get_format_version() -> str  # "1.0" or "2.0"
```

### Loader Changes

The `SkillLoader` now:
- Parses v2.0 sections: `_parse_for_claude()`, `_parse_when_to_use()`, `_parse_generation_guidelines()`
- Handles section name variants: `_parse_knowledge()` tries both names
- Maintains full v1.0 compatibility

## Testing

Comprehensive test coverage ensures both formats work correctly:

- **18 v1.0 tests** - Ensure backward compatibility
- **8 v2.0 tests** - Validate new format features
- **All 69 skill tests passing** - Full integration validation

Key test cohorts:
- v1.0 skills load and parse correctly
- v2.0 skills detected and parsed with new sections
- v1.0 skills not falsely detected as v2.0
- Hybrid skills (v1.0 + v2.0 sections) work correctly
- Section name variants handled properly
- All existing cohort skills still work

## Best Practices

### When Creating New Skills

**For v2.0 skills:**
1. Start with the template: `skills/SKILL_TEMPLATE_V2.md`
2. Write "For Claude" section first - it clarifies the skill's purpose
3. Fill out "When to Use This Skill" with comprehensive keywords
4. Write "Domain Knowledge" in narrative style, not as schemas
5. Include 3-5 diverse examples showing interpretation
6. Add "Generation Guidelines" for complex decision logic

**Voice and tone:**
- "For Claude" and "When to Use" - Second person ("Use this when you...")
- "Domain Knowledge" - Teaching/explanatory ("Sepsis occurs when...")
- "Examples" - Show reasoning ("Claude interprets this as...")

### When Updating Existing Skills

**Minimal v2.0 upgrade:**
```markdown
# [Keep existing title]

## For Claude
Use this skill when [summarize from Purpose].

## When to Use This Skill
**Keywords**: [extract from Purpose/Metadata tags]

## [Keep all existing v1.0 sections]
```

This minimal upgrade enables v2.0 detection while preserving all existing content.

## FAQ

**Q: Do I need to migrate my v1.0 skills?**
A: No. v1.0 skills will continue to work indefinitely. Migrate only when beneficial.

**Q: Can I mix v1.0 and v2.0 skills in composition?**
A: Yes. The SkillComposer handles both formats transparently.

**Q: What if I have both "Knowledge" and "Domain Knowledge" sections?**
A: The loader prefers "Domain Knowledge" (v2.0) but falls back to "Knowledge" (v1.0). Having both is redundant.

**Q: How do I know if my skill is v2.0?**
A: It must have both "For Claude" AND "When to Use This Skill" sections.

**Q: Can I use v2.0 section names without v2.0 content style?**
A: Yes. The section names alone trigger v2.0 detection. The narrative style is a best practice, not a requirement.

**Q: Will old tools break with v2.0 skills?**
A: No. All new fields are optional. Tools that don't know about v2.0 will simply ignore the new fields.

## Summary

v2.0 provides a Claude-optimized format while maintaining full backward compatibility. The migration is optional, incremental, and risk-free. Both formats coexist harmoniously in the same codebase.

**Key Principles:**
- Backward compatible - v1.0 skills still work
- Additive - v2.0 adds features, doesn't remove
- Gradual - Migrate skills at your own pace
- Optional - v1.0 remains fully supported
- Claude-first - Optimized for LLM comprehension

## See Also

- [Skills Format v1.0](format-specification.md) - Original specification
- [Skills Format v2.0](format-specification-v2.md) - Claude-optimized format
- [Creating Skills](creating-skills.md) - Guide to authoring skills
