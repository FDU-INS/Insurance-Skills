"""Skill reference system for journey events.

This module enables journey templates to reference skills for parameter
values instead of hardcoding clinical codes. This allows:

1. Single source of truth: Clinical codes defined in skills
2. Context-aware resolution: Different codes based on entity attributes
3. Maintainability: Update codes in one place

Example - Before (hardcoded):
    {
        "event_type": "diagnosis",
        "parameters": {"icd10": "E11.9", "description": "Type 2 diabetes"}
    }

Example - After (skill reference):
    {
        "event_type": "diagnosis",
        "parameters": {
            "skill_ref": {
                "skill": "diabetes-management",
                "lookup": "diagnosis_code",
                "context": {"control_status": "${entity.control_status}"}
            }
        }
    }
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from healthsim.skills.loader import SkillLoader
from healthsim.skills.schema import Skill


# =============================================================================
# Skill Reference Schema
# =============================================================================

class SkillReference(BaseModel):
    """Reference to a skill for parameter resolution.
    
    Attributes:
        skill: Name of the skill to reference (e.g., "diabetes-management")
        lookup: What to look up in the skill (e.g., "diagnosis_code", "medication")
        context: Context variables for resolution (can include ${entity.x} refs)
        fallback: Default value if lookup fails
    """
    
    skill: str = Field(..., description="Skill name to reference")
    lookup: str = Field(..., description="What to look up in the skill")
    context: dict[str, Any] = Field(default_factory=dict, description="Context for resolution")
    fallback: Any = Field(default=None, description="Fallback if lookup fails")


class ResolvedParameters(BaseModel):
    """Result of resolving skill references in parameters."""
    
    parameters: dict[str, Any] = Field(default_factory=dict)
    skill_used: str | None = None
    lookup_path: str | None = None
    resolved_from: str = "direct"  # "direct", "skill", "fallback"


# =============================================================================
# Skills Directory Configuration
# =============================================================================

def get_skills_root() -> Path:
    """Get the root directory for skills.
    
    Looks for skills in order:
    1. HEALTHSIM_SKILLS_PATH environment variable
    2. skills/ relative to workspace root
    3. Default to current working directory / skills
    """
    import os
    
    if env_path := os.environ.get("HEALTHSIM_SKILLS_PATH"):
        return Path(env_path)
    
    # Try to find workspace root by looking for pyproject.toml
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() and (parent / "skills").exists():
            return parent / "skills"
    
    return current / "skills"


# =============================================================================
# Skill Resolver
# =============================================================================

class SkillResolver:
    """Resolves skill references to concrete parameter values.
    
    This class loads skills and provides methods to look up values
    based on the skill's knowledge sections and structured data.
    
    Example:
        >>> resolver = SkillResolver()
        >>> params = resolver.resolve(
        ...     SkillReference(
        ...         skill="diabetes-management",
        ...         lookup="diagnosis_code",
        ...         context={"control_status": "poorly-controlled"}
        ...     )
        ... )
        >>> print(params)
        {'icd10': 'E11.65', 'description': 'Type 2 diabetes with hyperglycemia'}
    """
    
    # Lookup mappings define how to extract values from skills
    # Format: lookup_name -> (knowledge_section, extraction_rule)
    LOOKUP_MAPPINGS = {
        # Diagnosis lookups
        "diagnosis_code": {
            "sections": ["conditions", "generation rules"],
            "pattern": r"(E\d{2}\.\d+)\s*[-–]\s*(.+)",
            "fields": ["icd10", "description"],
        },
        "diagnosis_by_stage": {
            "sections": ["disease progression stages"],
            "context_key": "stage",
        },
        
        # Medication lookups
        "medication": {
            "sections": ["medication patterns", "medications"],
            "json_key": "code",
            "fields": ["rxnorm", "name", "dose", "frequency"],
        },
        "first_line_medication": {
            "sections": ["medication patterns"],
            "subsection": "first-line therapy",
        },
        
        # Lab lookups
        "lab_order": {
            "sections": ["lab patterns by control status"],
            "context_key": "control_status",
            "fields": ["loinc", "test_name", "range"],
        },
        
        # General code lookups
        "icd10": {
            "sections": ["conditions", "comorbidities"],
            "pattern": r"(E\d{2}\.\d+|I\d{2}(?:\.\d+)?|N\d{2}\.\d+)",
        },
        "loinc": {
            "sections": ["labs", "lab patterns"],
            "pattern": r"(\d{4,5}-\d)",
        },
        "rxnorm": {
            "sections": ["medications", "medication patterns"],
            "pattern": r'"code":\s*"(\d+)"',
        },
    }
    
    def __init__(self, skills_root: Path | None = None):
        """Initialize resolver.
        
        Args:
            skills_root: Root directory for skills. Defaults to auto-detect.
        """
        self.skills_root = skills_root or get_skills_root()
        self.loader = SkillLoader()
        self._cache: dict[str, Skill] = {}
    
    def load_skill(self, skill_name: str) -> Skill | None:
        """Load a skill by name.
        
        Args:
            skill_name: Name of skill (e.g., "diabetes-management")
            
        Returns:
            Loaded Skill or None if not found
        """
        if skill_name in self._cache:
            return self._cache[skill_name]
        
        # Search for skill file
        skill_path = self._find_skill_file(skill_name)
        if not skill_path:
            return None
        
        try:
            skill = self.loader.load_file(skill_path)
            self._cache[skill_name] = skill
            return skill
        except Exception:
            return None
    
    def _find_skill_file(self, skill_name: str) -> Path | None:
        """Find skill file by name.
        
        Searches in order:
        1. Direct match: skills/{product}/{skill_name}.md
        2. Search all subdirectories
        """
        # Normalize name
        normalized = skill_name.lower().replace("_", "-")
        
        # Try common locations
        for product in ["patientsim", "membersim", "rxmembersim", "trialsim", "common", "networksim", "populationsim"]:
            path = self.skills_root / product / f"{normalized}.md"
            if path.exists():
                return path
        
        # Search all .md files
        for md_file in self.skills_root.rglob("*.md"):
            if md_file.stem.lower() == normalized:
                return md_file
        
        return None
    
    def resolve(
        self,
        ref: SkillReference,
        entity_context: dict[str, Any] | None = None,
    ) -> ResolvedParameters:
        """Resolve a skill reference to concrete parameters.
        
        Args:
            ref: The skill reference to resolve
            entity_context: Entity attributes for ${entity.x} substitution
            
        Returns:
            ResolvedParameters with resolved values
        """
        # Load the skill
        skill = self.load_skill(ref.skill)
        if not skill:
            return ResolvedParameters(
                parameters={"value": ref.fallback} if ref.fallback else {},
                resolved_from="fallback",
            )
        
        # Resolve context variables
        resolved_context = self._resolve_context(ref.context, entity_context or {})
        
        # Look up the value
        result = self._lookup_value(skill, ref.lookup, resolved_context)
        
        if result:
            return ResolvedParameters(
                parameters=result,
                skill_used=ref.skill,
                lookup_path=ref.lookup,
                resolved_from="skill",
            )
        
        # Fallback
        return ResolvedParameters(
            parameters={"value": ref.fallback} if ref.fallback else {},
            resolved_from="fallback",
        )
    
    def _resolve_context(
        self,
        context: dict[str, Any],
        entity_context: dict[str, Any],
    ) -> dict[str, Any]:
        """Resolve ${entity.x} references in context."""
        resolved = {}
        
        for key, value in context.items():
            if isinstance(value, str) and value.startswith("${entity."):
                # Extract entity attribute name
                attr_name = value[9:-1]  # Remove ${entity. and }
                resolved[key] = entity_context.get(attr_name, value)
            else:
                resolved[key] = value
        
        return resolved
    
    def _lookup_value(
        self,
        skill: Skill,
        lookup: str,
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Look up a value in the skill."""
        mapping = self.LOOKUP_MAPPINGS.get(lookup)
        
        if not mapping:
            # Try direct knowledge section lookup
            return self._direct_lookup(skill, lookup, context)
        
        # Get relevant sections from skill
        sections = mapping.get("sections", [])
        content = self._get_sections_content(skill, sections)
        
        if not content:
            return None
        
        # Context-based lookup
        if context_key := mapping.get("context_key"):
            context_value = context.get(context_key, "").lower().replace("_", "-")
            return self._context_lookup(content, context_value, mapping)
        
        # Pattern-based lookup
        if pattern := mapping.get("pattern"):
            return self._pattern_lookup(content, pattern, mapping.get("fields"))
        
        # JSON-based lookup
        if json_key := mapping.get("json_key"):
            return self._json_lookup(content, json_key)
        
        return None
    
    def _direct_lookup(
        self,
        skill: Skill,
        lookup: str,
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Direct lookup in skill knowledge sections."""
        # Check knowledge dict
        if lookup in skill.knowledge:
            return {"value": skill.knowledge[lookup]}
        
        # Check content sections
        if lookup in skill.content:
            return {"value": skill.content[lookup]}
        
        # Check parameters
        param = skill.get_parameter(lookup)
        if param:
            return {"value": param.default}
        
        return None
    
    def _get_sections_content(self, skill: Skill, sections: list[str]) -> str:
        """Get combined content from specified sections."""
        content_parts = []
        
        for section in sections:
            # Check knowledge
            if section in skill.knowledge:
                content_parts.append(skill.knowledge[section])
            # Check content
            normalized = section.lower().replace(" ", "-")
            if normalized in skill.content:
                content_parts.append(str(skill.content[normalized]))
            # Also try with spaces
            if section in skill.content:
                content_parts.append(str(skill.content[section]))
        
        # Also include raw text if no sections found
        if not content_parts:
            content_parts.append(skill.raw_text)
        
        return "\n".join(content_parts)
    
    def _context_lookup(
        self,
        content: str,
        context_value: str,
        mapping: dict,
    ) -> dict[str, Any] | None:
        """Look up based on context value (e.g., control_status)."""
        # Find section matching context value
        # Look for headers like "### Well-Controlled" or "### Poorly Controlled"
        section_pattern = rf"###\s*{re.escape(context_value)}.*?\n(.*?)(?=###|\Z)"
        match = re.search(section_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            section_content = match.group(1)
            # Try to extract JSON from section
            json_match = re.search(r"\{[^}]+\}", section_content, re.DOTALL)
            if json_match:
                import json
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
        
        return None
    
    def _pattern_lookup(
        self,
        content: str,
        pattern: str,
        fields: list[str] | None,
    ) -> dict[str, Any] | None:
        """Look up using regex pattern."""
        match = re.search(pattern, content)
        if match:
            groups = match.groups()
            if fields and len(groups) >= len(fields):
                return dict(zip(fields, groups))
            return {"value": groups[0] if groups else match.group()}
        return None
    
    def _json_lookup(self, content: str, json_key: str) -> dict[str, Any] | None:
        """Look up a key from JSON in content."""
        import json
        
        # Find JSON blocks
        json_pattern = r"```json\s*([\s\S]*?)```"
        for match in re.finditer(json_pattern, content):
            try:
                data = json.loads(match.group(1))
                if isinstance(data, dict) and json_key in data:
                    return data
            except json.JSONDecodeError:
                continue
        
        return None
    
    def list_skills(self) -> list[str]:
        """List available skills."""
        skills = []
        if self.skills_root.exists():
            for md_file in self.skills_root.rglob("*.md"):
                if md_file.stem not in ("README", "SKILL"):
                    skills.append(md_file.stem)
        return sorted(set(skills))


# =============================================================================
# Parameter Resolver for Journey Events
# =============================================================================

class ParameterResolver:
    """Resolves parameters in journey events, handling skill references.
    
    This class processes event parameters, resolving:
    1. Skill references (skill_ref) to concrete values
    2. Entity variable references (${entity.x})
    3. Default values
    
    Example:
        >>> resolver = ParameterResolver()
        >>> params = resolver.resolve_event_parameters(
        ...     {
        ...         "skill_ref": {
        ...             "skill": "diabetes-management",
        ...             "lookup": "diagnosis_code"
        ...         },
        ...         "severity": "${entity.control_status}"
        ...     },
        ...     entity={"control_status": "poorly-controlled"}
        ... )
    """
    
    def __init__(self, skill_resolver: SkillResolver | None = None):
        """Initialize resolver.
        
        Args:
            skill_resolver: SkillResolver instance. Created if not provided.
        """
        self.skill_resolver = skill_resolver or SkillResolver()
    
    def resolve_event_parameters(
        self,
        parameters: dict[str, Any],
        entity: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Resolve all parameters for an event.
        
        Args:
            parameters: Raw event parameters (may contain skill_ref)
            entity: Entity attributes for variable substitution
            
        Returns:
            Resolved parameters with concrete values
        """
        entity = entity or {}
        resolved = {}
        
        for key, value in parameters.items():
            if key == "skill_ref":
                # Resolve skill reference
                ref = SkillReference.model_validate(value) if isinstance(value, dict) else value
                result = self.skill_resolver.resolve(ref, entity)
                resolved.update(result.parameters)
            elif isinstance(value, str) and "${entity." in value:
                # Resolve entity variable
                resolved[key] = self._resolve_entity_var(value, entity)
            elif isinstance(value, dict):
                # Recursively resolve nested dicts
                resolved[key] = self.resolve_event_parameters(value, entity)
            else:
                resolved[key] = value
        
        return resolved
    
    def _resolve_entity_var(self, value: str, entity: dict[str, Any]) -> Any:
        """Resolve ${entity.x} variables."""
        pattern = r"\$\{entity\.(\w+)\}"
        
        def replacer(match):
            attr = match.group(1)
            return str(entity.get(attr, match.group(0)))
        
        result = re.sub(pattern, replacer, value)
        
        # If entire string was a variable, return the actual value (not stringified)
        if value.startswith("${entity.") and value.endswith("}"):
            attr = value[9:-1]
            return entity.get(attr, value)
        
        return result


# =============================================================================
# Convenience Functions
# =============================================================================

_default_skill_resolver: SkillResolver | None = None
_default_parameter_resolver: ParameterResolver | None = None


def get_skill_resolver() -> SkillResolver:
    """Get the default skill resolver (singleton)."""
    global _default_skill_resolver
    if _default_skill_resolver is None:
        _default_skill_resolver = SkillResolver()
    return _default_skill_resolver


def get_parameter_resolver() -> ParameterResolver:
    """Get the default parameter resolver (singleton)."""
    global _default_parameter_resolver
    if _default_parameter_resolver is None:
        _default_parameter_resolver = ParameterResolver(get_skill_resolver())
    return _default_parameter_resolver


def resolve_skill_ref(
    skill: str,
    lookup: str,
    context: dict[str, Any] | None = None,
    entity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Convenience function to resolve a skill reference.
    
    Args:
        skill: Skill name
        lookup: What to look up
        context: Context for resolution
        entity: Entity attributes
        
    Returns:
        Resolved parameters
        
    Example:
        >>> params = resolve_skill_ref(
        ...     "diabetes-management",
        ...     "diagnosis_code",
        ...     context={"stage": "new_diagnosis"}
        ... )
    """
    ref = SkillReference(skill=skill, lookup=lookup, context=context or {})
    result = get_skill_resolver().resolve(ref, entity)
    return result.parameters


__all__ = [
    "SkillReference",
    "ResolvedParameters",
    "SkillResolver",
    "ParameterResolver",
    "get_skill_resolver",
    "get_parameter_resolver",
    "resolve_skill_ref",
    "get_skills_root",
]
