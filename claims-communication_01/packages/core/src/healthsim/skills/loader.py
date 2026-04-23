"""Skill loader for parsing skill files.

Loads and parses skill definitions from markdown files.
"""

import re
from pathlib import Path
from typing import Any

import yaml

from healthsim.skills.schema import (
    ParameterType,
    Skill,
    SkillMetadata,
    SkillParameter,
    SkillType,
    SkillVariation,
)


class SkillParseError(Exception):
    """Error parsing a skill file."""

    pass


class SkillLoader:
    """Loads and parses skill files from Markdown.

    Skill files use a Markdown format with YAML frontmatter for metadata
    and structured sections for content.

    Example:
        >>> loader = SkillLoader()
        >>> skill = loader.load_file(Path("skills/my-skill.md"))
        >>> print(skill.name)
        'My Skill'
    """

    # Section headers to look for
    SECTION_HEADERS = [
        "purpose",
        "parameters",
        "knowledge",
        "variations",
        "examples",
        "references",
        "dependencies",
        "for claude",
        "when to use",
    ]

    def load_file(self, path: Path) -> Skill:
        """Load a skill from a file.

        Args:
            path: Path to skill file

        Returns:
            Parsed Skill object

        Raises:
            SkillParseError: If file cannot be parsed
            FileNotFoundError: If file doesn't exist
        """
        if not path.exists():
            raise FileNotFoundError(f"Skill file not found: {path}")

        content = path.read_text(encoding="utf-8")
        return self.load_string(content, source_path=str(path))

    def load_string(self, content: str, source_path: str = "<string>") -> Skill:
        """Load a skill from a string.

        Args:
            content: Skill content as string
            source_path: Source path for error messages

        Returns:
            Parsed Skill object

        Raises:
            SkillParseError: If content cannot be parsed
        """
        try:
            # Extract frontmatter and body
            frontmatter, body = self._extract_frontmatter(content)

            # Parse metadata from frontmatter
            metadata = self._parse_metadata(frontmatter)

            # Get name and description from frontmatter
            name = frontmatter.get("name", source_path)
            description = frontmatter.get("description", "")

            # Parse sections from body
            sections = self._parse_sections(body)

            # Build skill object
            return Skill(
                name=name,
                description=description,
                metadata=metadata,
                purpose=sections.get("purpose", ""),
                parameters=self._parse_parameters(sections.get("parameters", "")),
                knowledge=self._parse_knowledge(sections),
                variations=self._parse_variations(sections.get("variations", "")),
                examples=self._parse_list_section(sections.get("examples", "")),
                references=self._parse_list_section(sections.get("references", "")),
                dependencies=frontmatter.get("dependencies", []),
                raw_text=content,
                content=sections,
                for_claude=sections.get("for claude", ""),
                when_to_use=sections.get("when to use", ""),
            )

        except Exception as e:
            raise SkillParseError(f"Failed to parse skill from {source_path}: {e}") from e

    def _extract_frontmatter(self, content: str) -> tuple[dict[str, Any], str]:
        """Extract YAML frontmatter from content.

        Args:
            content: Full content string

        Returns:
            Tuple of (frontmatter dict, remaining body)
        """
        # Match YAML frontmatter (between --- markers)
        pattern = r"^---\s*\n(.*?)\n---\s*\n"
        match = re.match(pattern, content, re.DOTALL)

        if match:
            frontmatter_text = match.group(1)
            body = content[match.end() :]
            try:
                frontmatter = yaml.safe_load(frontmatter_text) or {}
            except yaml.YAMLError:
                frontmatter = {}
        else:
            frontmatter = {}
            body = content

        return frontmatter, body

    def _parse_metadata(self, frontmatter: dict[str, Any]) -> SkillMetadata:
        """Parse metadata from frontmatter.

        Args:
            frontmatter: Frontmatter dictionary

        Returns:
            SkillMetadata object
        """
        # Map string to SkillType enum
        type_str = frontmatter.get("type", "cohort-template")
        try:
            skill_type = SkillType(type_str)
        except ValueError:
            skill_type = SkillType.COHORT_TEMPLATE

        return SkillMetadata(
            type=skill_type,
            version=frontmatter.get("version", "1.0"),
            author=frontmatter.get("author"),
            tags=frontmatter.get("tags", []),
            requires_version=frontmatter.get("requires_version"),
        )

    def _parse_sections(self, body: str) -> dict[str, str]:
        """Parse sections from body text.

        Args:
            body: Body text after frontmatter

        Returns:
            Dictionary of section name to content
        """
        sections: dict[str, str] = {}
        current_section = "intro"
        current_content: list[str] = []

        for line in body.split("\n"):
            # Check for section header (## or ###)
            header_match = re.match(r"^#{2,3}\s+(.+)$", line)

            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                section_name = header_match.group(1).lower().strip()
                current_section = section_name
                current_content = []
            else:
                current_content.append(line)

        # Save final section
        if current_content:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _parse_parameters(self, content: str) -> list[SkillParameter]:
        """Parse parameters from section content.

        Args:
            content: Parameters section content

        Returns:
            List of SkillParameter objects
        """
        if not content.strip():
            return []

        parameters = []

        # Try to parse as YAML first
        try:
            data = yaml.safe_load(content)
            if isinstance(data, list):
                for item in data:
                    param = self._dict_to_parameter(item)
                    if param:
                        parameters.append(param)
                return parameters
        except yaml.YAMLError:
            pass

        # Fall back to markdown list parsing
        # Pattern: - **name** (type): description [default: value]
        # Use [^\[\n]+ to stop at '[' or newline to prevent multi-line matching
        pattern = r"-\s+\*\*(\w+)\*\*\s*(?:\((\w+)\))?:\s*([^\[\n]+)(?:\[default:\s*([^\]]+)\])?"

        for match in re.finditer(pattern, content):
            name = match.group(1)
            type_str = match.group(2) or "string"
            description = match.group(3).strip()
            default_str = match.group(4)

            # Map type string to enum
            try:
                param_type = ParameterType(type_str.lower())
            except ValueError:
                param_type = ParameterType.STRING

            # Parse default value
            default = None
            if default_str:
                try:
                    default = yaml.safe_load(default_str)
                except yaml.YAMLError:
                    default = default_str.strip()

            parameters.append(
                SkillParameter(
                    name=name,
                    type=param_type,
                    default=default,
                    description=description,
                )
            )

        return parameters

    def _dict_to_parameter(self, data: dict[str, Any]) -> SkillParameter | None:
        """Convert a dictionary to SkillParameter.

        Args:
            data: Parameter dictionary

        Returns:
            SkillParameter or None if invalid
        """
        if not isinstance(data, dict) or "name" not in data:
            return None

        type_str = data.get("type", "string")
        try:
            param_type = ParameterType(type_str.lower())
        except ValueError:
            param_type = ParameterType.STRING

        return SkillParameter(
            name=data["name"],
            type=param_type,
            default=data.get("default"),
            description=data.get("description", ""),
            required=data.get("required", False),
            options=data.get("options"),
            min_value=data.get("min_value"),
            max_value=data.get("max_value"),
        )

    def _parse_variations(self, content: str) -> list[SkillVariation]:
        """Parse variations from section content.

        Args:
            content: Variations section content

        Returns:
            List of SkillVariation objects
        """
        if not content.strip():
            return []

        variations = []

        # Try YAML first
        try:
            data = yaml.safe_load(content)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "name" in item:
                        variations.append(
                            SkillVariation(
                                name=item["name"],
                                description=item.get("description", ""),
                                parameter_overrides=item.get("parameters", {}),
                            )
                        )
                return variations
        except yaml.YAMLError:
            pass

        # Fall back to markdown parsing
        # Pattern: ### variation_name
        current_variation: dict[str, Any] | None = None

        for line in content.split("\n"):
            header_match = re.match(r"^###\s+(.+)$", line)
            if header_match:
                if current_variation:
                    variations.append(
                        SkillVariation(
                            name=current_variation["name"],
                            description=current_variation.get("description", ""),
                            parameter_overrides=current_variation.get("parameters", {}),
                        )
                    )
                current_variation = {"name": header_match.group(1).strip()}
            elif current_variation and line.strip():
                if "description" not in current_variation:
                    current_variation["description"] = line.strip()

        if current_variation:
            variations.append(
                SkillVariation(
                    name=current_variation["name"],
                    description=current_variation.get("description", ""),
                    parameter_overrides=current_variation.get("parameters", {}),
                )
            )

        return variations

    def _parse_knowledge(self, sections: dict[str, str]) -> dict[str, str]:
        """Extract knowledge sections.

        Args:
            sections: All parsed sections

        Returns:
            Dictionary of knowledge topic to content
        """
        knowledge = {}

        # Look for knowledge section or domain-specific sections
        for key, value in sections.items():
            if key == "knowledge":
                # Parse sub-sections within knowledge
                subsections = self._parse_subsections(value)
                knowledge.update(subsections)
            elif key not in self.SECTION_HEADERS and key != "intro":
                # Treat unknown sections as knowledge
                knowledge[key] = value

        return knowledge

    def _parse_subsections(self, content: str) -> dict[str, str]:
        """Parse subsections (### headers) within a section.

        Args:
            content: Section content

        Returns:
            Dictionary of subsection name to content
        """
        subsections: dict[str, str] = {}
        current_name = "general"
        current_content: list[str] = []

        for line in content.split("\n"):
            header_match = re.match(r"^###\s+(.+)$", line)
            if header_match:
                if current_content:
                    subsections[current_name] = "\n".join(current_content).strip()
                current_name = header_match.group(1).lower().strip()
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            subsections[current_name] = "\n".join(current_content).strip()

        return subsections

    def _parse_list_section(self, content: str) -> list[str]:
        """Parse a section as a list of items.

        Args:
            content: Section content

        Returns:
            List of items
        """
        if not content.strip():
            return []

        items = []

        # Look for markdown list items
        for line in content.split("\n"):
            # Match - item or * item or 1. item
            match = re.match(r"^[\-\*\d\.]+\s+(.+)$", line.strip())
            if match:
                items.append(match.group(1).strip())
            elif line.strip() and not line.startswith("#"):
                # Non-empty, non-header line
                items.append(line.strip())

        return items
