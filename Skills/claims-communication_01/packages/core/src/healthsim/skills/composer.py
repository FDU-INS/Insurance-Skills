"""Skill composition and merging logic.

This module provides functionality to compose multiple skills together,
resolving dependencies and merging configurations.
"""

from pathlib import Path
from typing import Any

from healthsim.skills.loader import SkillLoader
from healthsim.skills.schema import (
    Skill,
    SkillParameter,
    SkillType,
    SkillVariation,
)


class SkillCompositionError(Exception):
    """Error composing skills together."""

    pass


class SkillComposer:
    """Composes multiple skills together.

    Handles dependency resolution, parameter merging, and content composition.

    Example:
        >>> composer = SkillComposer()
        >>> skill = composer.compose([
        ...     "skills/base-generator.md",
        ...     "skills/person-details.md"
        ... ])
    """

    def __init__(self, skills_dir: str | Path | None = None) -> None:
        """Initialize the composer.

        Args:
            skills_dir: Base directory for resolving relative skill paths.
                       If None, uses current directory.
        """
        self.loader = SkillLoader()
        self.skills_dir = Path(skills_dir) if skills_dir else Path.cwd()
        self._loaded_skills: dict[str, Skill] = {}

    def compose(
        self,
        skill_paths: list[str | Path],
        resolve_dependencies: bool = True,
    ) -> Skill:
        """Compose multiple skills into one.

        Args:
            skill_paths: List of paths to skill files
            resolve_dependencies: Whether to automatically load dependencies

        Returns:
            Composed Skill object

        Raises:
            SkillCompositionError: If skills cannot be composed
        """
        if not skill_paths:
            raise SkillCompositionError("No skills provided")

        # Load all skills
        skills = []
        for path in skill_paths:
            skill = self._load_skill(path)
            skills.append(skill)

            # Resolve dependencies if requested
            if resolve_dependencies and skill.dependencies:
                for dep_path in skill.dependencies:
                    if dep_path not in self._loaded_skills:
                        dep_skill = self._load_skill(dep_path)
                        skills.insert(0, dep_skill)  # Dependencies go first

        if len(skills) == 1:
            return skills[0]

        # Validate compatibility
        self._validate_compatibility(skills)

        # Merge skills
        return self._merge_skills(skills)

    def _load_skill(self, path: str | Path) -> Skill:
        """Load a skill, using cache if available.

        Args:
            path: Path to skill file

        Returns:
            Loaded Skill object
        """
        path_str = str(path)

        if path_str in self._loaded_skills:
            return self._loaded_skills[path_str]

        # Resolve relative paths against skills_dir
        full_path = self.skills_dir / path if not Path(path).is_absolute() else Path(path)

        skill = self.loader.load_file(full_path)
        self._loaded_skills[path_str] = skill
        return skill

    def _validate_compatibility(self, skills: list[Skill]) -> None:
        """Validate that skills can be composed together.

        Args:
            skills: List of skills to validate

        Raises:
            SkillCompositionError: If skills are incompatible
        """
        # Check for circular dependencies
        self._check_circular_dependencies(skills)

        # Check type compatibility
        types = {s.metadata.type for s in skills}
        if SkillType.COHORT_TEMPLATE in types and SkillType.DOMAIN_KNOWLEDGE in types:
            # This is fine - domain knowledge can enhance cohorts
            pass
        elif len(types) > 1:
            # Other combinations might be problematic but allow them
            pass

    def _check_circular_dependencies(self, skills: list[Skill]) -> None:
        """Check for circular dependencies.

        Args:
            skills: List of skills to check

        Raises:
            SkillCompositionError: If circular dependency detected
        """
        # Build path to skill name mapping
        path_to_name = {path: skill.name for path, skill in self._loaded_skills.items()}
        for skill in skills:
            path_to_name[skill.name] = skill.name

        # Build dependency graph using skill names
        dep_graph: dict[str, set[str]] = {}
        for skill in skills:
            dep_names = set()
            for dep_path in skill.dependencies:
                dep_name = path_to_name.get(dep_path, dep_path)
                dep_names.add(dep_name)
            dep_graph[skill.name] = dep_names

        # Check for cycles using DFS
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            if node in dep_graph:
                for neighbor in dep_graph[node]:
                    if neighbor not in visited:
                        if has_cycle(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True

            rec_stack.remove(node)
            return False

        for skill_name in dep_graph:
            if skill_name not in visited and has_cycle(skill_name):
                raise SkillCompositionError(f"Circular dependency detected involving: {skill_name}")

    def _merge_skills(self, skills: list[Skill]) -> Skill:
        """Merge multiple skills into one.

        Later skills override earlier skills for conflicting elements.

        Args:
            skills: List of skills to merge (order matters)

        Returns:
            Merged Skill object
        """
        if not skills:
            raise SkillCompositionError("Cannot merge empty skill list")

        # Start with the last skill as base (it has highest priority)
        base = skills[-1]

        # Build merged skill
        merged_name = " + ".join(s.name for s in skills)
        merged_description = base.description

        # Metadata from last skill
        merged_metadata = base.metadata

        # Combine purposes
        purposes = [s.purpose for s in skills if s.purpose]
        merged_purpose = "\n\n".join(purposes)

        # Merge parameters (later overrides earlier)
        merged_parameters = self._merge_parameters(skills)

        # Merge knowledge (additive)
        merged_knowledge = self._merge_knowledge(skills)

        # Merge variations (additive)
        merged_variations = self._merge_variations(skills)

        # Combine examples (additive)
        merged_examples = []
        for skill in skills:
            merged_examples.extend(skill.examples)

        # Combine references (additive, unique)
        merged_references = []
        seen_refs: set[str] = set()
        for skill in skills:
            for ref in skill.references:
                if ref not in seen_refs:
                    merged_references.append(ref)
                    seen_refs.add(ref)

        # Combine dependencies (unique)
        merged_dependencies = []
        seen_deps: set[str] = set()
        for skill in skills:
            for dep in skill.dependencies:
                if dep not in seen_deps:
                    merged_dependencies.append(dep)
                    seen_deps.add(dep)

        # Combine raw text
        merged_raw_text = "\n\n---\n\n".join(s.raw_text for s in skills)

        # Merge content
        merged_content = self._merge_content(skills)

        # Merge for_claude and when_to_use
        for_claude_parts = [s.for_claude for s in skills if s.for_claude]
        when_to_use_parts = [s.when_to_use for s in skills if s.when_to_use]

        return Skill(
            name=merged_name,
            description=merged_description,
            metadata=merged_metadata,
            purpose=merged_purpose,
            parameters=merged_parameters,
            knowledge=merged_knowledge,
            variations=merged_variations,
            examples=merged_examples,
            references=merged_references,
            dependencies=merged_dependencies,
            raw_text=merged_raw_text,
            content=merged_content,
            for_claude="\n\n".join(for_claude_parts) if for_claude_parts else None,
            when_to_use="\n\n".join(when_to_use_parts) if when_to_use_parts else None,
        )

    def _merge_parameters(self, skills: list[Skill]) -> list[SkillParameter]:
        """Merge parameters from multiple skills.

        Later skills override earlier ones for same parameter name.

        Args:
            skills: List of skills

        Returns:
            Merged parameter list
        """
        params_by_name: dict[str, SkillParameter] = {}

        for skill in skills:
            for param in skill.parameters:
                params_by_name[param.name] = param

        return list(params_by_name.values())

    def _merge_knowledge(self, skills: list[Skill]) -> dict[str, str]:
        """Merge knowledge sections from multiple skills.

        Args:
            skills: List of skills

        Returns:
            Merged knowledge dictionary
        """
        merged: dict[str, str] = {}

        for skill in skills:
            for section, content in skill.knowledge.items():
                if section in merged:
                    merged[section] += "\n\n" + content
                else:
                    merged[section] = content

        return merged

    def _merge_variations(self, skills: list[Skill]) -> list[SkillVariation]:
        """Merge variations from multiple skills.

        Args:
            skills: List of skills

        Returns:
            Combined variation list
        """
        merged_variations = []
        seen_names: set[str] = set()

        for skill in skills:
            for variation in skill.variations:
                if variation.name not in seen_names:
                    merged_variations.append(variation)
                    seen_names.add(variation.name)

        return merged_variations

    def _merge_content(self, skills: list[Skill]) -> dict[str, Any]:
        """Merge content dictionaries from multiple skills.

        Args:
            skills: List of skills

        Returns:
            Merged content dictionary
        """
        merged: dict[str, Any] = {}

        for skill in skills:
            for key, value in skill.content.items():
                if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                    merged[key].update(value)
                else:
                    merged[key] = value

        return merged
