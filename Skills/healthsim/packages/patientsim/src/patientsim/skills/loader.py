"""Skill file loader and parser.

This module provides functionality to load and parse Skills files from Markdown.
"""

import re
from pathlib import Path
from typing import Any

from patientsim.skills.schema import (
    GenerationRules,
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

    Example:
        >>> loader = SkillLoader()
        >>> skill = loader.load_file("skills/scenarios/sepsis.md")
        >>> print(skill.name)
        'Septic Patient Scenario'
    """

    def load_file(self, path: str | Path) -> Skill:
        """Load a skill from a file.

        Args:
            path: Path to skill markdown file

        Returns:
            Parsed Skill object

        Raises:
            SkillParseError: If file cannot be parsed
            FileNotFoundError: If file doesn't exist
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Skill file not found: {path}")

        with open(path, encoding="utf-8") as f:
            content = f.read()

        return self.load_string(content, source_path=str(path))

    def load_string(self, content: str, source_path: str | None = None) -> Skill:
        """Load a skill from a markdown string.

        Args:
            content: Markdown content
            source_path: Optional source file path for error messages

        Returns:
            Parsed Skill object

        Raises:
            SkillParseError: If content cannot be parsed
        """
        try:
            # Parse markdown sections
            sections = self._parse_sections(content)

            # Extract required elements
            name = self._extract_title(content, source_path)
            description = self._extract_description(sections, source_path)
            metadata = self._parse_metadata(sections, source_path)
            purpose = self._parse_purpose(sections, source_path)

            # Extract optional elements based on skill type
            parameters = []
            generation_rules = None
            knowledge = {}
            variations = []

            if metadata.type == SkillType.SCENARIO_TEMPLATE:
                parameters = self._parse_parameters(sections)
                generation_rules = self._parse_generation_rules(sections)
                variations = self._parse_variations(sections)
            elif metadata.type == SkillType.DOMAIN_KNOWLEDGE:
                knowledge = self._parse_knowledge(sections)

            # Extract universal optional sections
            examples = self._parse_examples(sections)
            references = self._parse_references(sections)
            dependencies = self._parse_dependencies(sections)

            # Extract v2.0 format sections
            for_claude = self._parse_for_claude(sections)
            when_to_use = self._parse_when_to_use(sections)
            generation_guidelines = self._parse_generation_guidelines(sections)

            return Skill(
                name=name,
                description=description,
                metadata=metadata,
                purpose=purpose,
                parameters=parameters,
                generation_rules=generation_rules,
                knowledge=knowledge,
                variations=variations,
                examples=examples,
                references=references,
                dependencies=dependencies,
                raw_text=content,
                content=sections,
                for_claude=for_claude,
                when_to_use=when_to_use,
                generation_guidelines=generation_guidelines,
            )

        except Exception as e:
            source = f" in {source_path}" if source_path else ""
            raise SkillParseError(f"Failed to parse skill{source}: {e}") from e

    def _parse_sections(self, content: str) -> dict[str, Any]:
        """Parse markdown into sections by heading.

        Args:
            content: Markdown content

        Returns:
            Dictionary of section name -> content
        """
        sections: dict[str, Any] = {}
        current_section = None
        current_content: list[str] = []

        lines = content.split("\n")

        for line in lines:
            # Check for heading
            heading_match = re.match(r"^##\s+(.+)$", line)
            if heading_match:
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                # Start new section
                current_section = heading_match.group(1).strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

    def _extract_title(self, content: str, source_path: str | None) -> str:
        """Extract H1 title from markdown.

        Args:
            content: Markdown content
            source_path: Source file path for errors

        Returns:
            Title text

        Raises:
            SkillParseError: If no H1 found
        """
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if not match:
            source = f" in {source_path}" if source_path else ""
            raise SkillParseError(f"No H1 title found{source}")
        return match.group(1).strip()

    def _extract_description(self, sections: dict[str, Any], _source_path: str | None) -> str:
        """Extract description (first paragraph after title).

        Args:
            sections: Parsed sections
            _source_path: Source file path for errors (reserved for future use)

        Returns:
            Description text
        """
        # Description should be before first ## heading
        # We'll look for it in the raw content
        # For now, use a placeholder - will improve in next iteration
        desc = sections.get("_description", "No description provided")
        return str(desc)

    def _parse_metadata(self, sections: dict[str, Any], source_path: str | None) -> SkillMetadata:
        """Parse metadata section.

        Args:
            sections: Parsed sections
            source_path: Source file path for errors

        Returns:
            SkillMetadata object

        Raises:
            SkillParseError: If metadata is invalid
        """
        if "Metadata" not in sections:
            source = f" in {source_path}" if source_path else ""
            raise SkillParseError(f"Required 'Metadata' section not found{source}")

        metadata_text = sections["Metadata"]
        metadata_dict: dict[str, Any] = {}

        # Parse bullet list format: - **Key**: value
        for line in metadata_text.split("\n"):
            match = re.match(r"-\s+\*\*(.+?)\*\*:\s*(.+)", line.strip())
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()

                # Convert key to lowercase with underscores
                key_normalized = key.lower().replace(" ", "_")

                if key_normalized == "tags":
                    # Split comma-separated tags
                    metadata_dict["tags"] = [t.strip() for t in value.split(",")]
                else:
                    metadata_dict[key_normalized] = value

        # Validate required fields
        if "type" not in metadata_dict:
            raise SkillParseError("Metadata missing required field: Type")
        if "version" not in metadata_dict:
            raise SkillParseError("Metadata missing required field: Version")

        return SkillMetadata(**metadata_dict)

    def _parse_purpose(self, sections: dict[str, Any], source_path: str | None) -> str:
        """Parse purpose section.

        Args:
            sections: Parsed sections
            source_path: Source file path for errors

        Returns:
            Purpose text

        Raises:
            SkillParseError: If purpose section missing
        """
        if "Purpose" not in sections:
            source = f" in {source_path}" if source_path else ""
            raise SkillParseError(f"Required 'Purpose' section not found{source}")
        purpose = sections["Purpose"]
        return str(purpose)

    def _parse_parameters(self, sections: dict[str, Any]) -> list[SkillParameter]:
        """Parse parameters table.

        Args:
            sections: Parsed sections

        Returns:
            List of SkillParameter objects
        """
        if "Parameters" not in sections:
            return []

        parameters_text = sections["Parameters"]
        parameters = []

        # Parse markdown table
        lines = [line.strip() for line in parameters_text.split("\n") if line.strip()]

        # Skip table header and separator
        if len(lines) < 3:
            return []

        for line in lines[2:]:  # Skip header and separator
            # Parse table row: | param | type | default | description |
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 5:  # Including empty cells at start/end
                param_name = cells[1]
                param_type_str = cells[2]
                param_default = cells[3]
                param_desc = cells[4]

                # Convert type string to ParameterType
                try:
                    param_type = ParameterType(param_type_str)
                except ValueError:
                    # Skip invalid types
                    continue

                # Convert default value based on type
                default_value: Any = param_default
                if param_type == ParameterType.INTEGER:
                    # Try to convert to int, keep as string if it fails
                    if param_default.isdigit() or (
                        param_default.startswith("-") and param_default[1:].isdigit()
                    ):
                        default_value = int(param_default)
                elif param_type == ParameterType.BOOLEAN:
                    default_value = param_default.lower() in ("true", "yes", "1")

                parameters.append(
                    SkillParameter(
                        name=param_name,
                        type=param_type,
                        default=default_value,
                        description=param_desc,
                    )
                )

        return parameters

    def _parse_generation_rules(self, sections: dict[str, Any]) -> GenerationRules | None:
        """Parse generation rules section.

        Args:
            sections: Parsed sections

        Returns:
            GenerationRules object or None if not present
        """
        if "Generation Rules" not in sections:
            return None

        rules_text = sections["Generation Rules"]

        # Parse subsections within Generation Rules
        # Look for ### headings
        subsections: dict[str, str] = {}
        current_subsection = None
        current_content: list[str] = []

        for line in rules_text.split("\n"):
            subsection_match = re.match(r"^###\s+(.+)$", line)
            if subsection_match:
                if current_subsection:
                    subsections[current_subsection] = "\n".join(current_content).strip()
                current_subsection = subsection_match.group(1).strip()
                current_content = []
            elif current_subsection:
                current_content.append(line)

        if current_subsection:
            subsections[current_subsection] = "\n".join(current_content).strip()

        # Extract specific rule types
        demographics = {}
        conditions = {}
        vital_signs = {}
        laboratory = {}
        medications = []
        timeline = []

        # Parse Demographics
        if "Demographics" in subsections:
            demographics = self._parse_key_value_list(subsections["Demographics"])

        # Parse Conditions
        if "Conditions" in subsections:
            conditions = self._parse_conditions_section(subsections["Conditions"])

        # Parse Vital Signs
        if "Vital Signs" in subsections:
            vital_signs = self._parse_key_value_list(subsections["Vital Signs"])

        # Parse Laboratory
        if "Laboratory" in subsections:
            laboratory = self._parse_key_value_list(subsections["Laboratory"])

        # Parse Medications
        if "Medications" in subsections:
            medications = [
                line.strip() for line in subsections["Medications"].split("\n") if line.strip()
            ]

        # Parse Timeline
        if "Timeline" in subsections:
            timeline = [
                line.strip() for line in subsections["Timeline"].split("\n") if line.strip()
            ]

        return GenerationRules(
            demographics=demographics,
            conditions=conditions,
            vital_signs=vital_signs,
            laboratory=laboratory,
            medications=medications,
            timeline=timeline,
            raw_sections=subsections,
        )

    def _parse_key_value_list(self, text: str) -> dict[str, Any]:
        """Parse key-value bullet list.

        Args:
            text: Text content with "- Key: value" or "**Key**: value" format

        Returns:
            Dictionary of parsed values
        """
        result = {}
        for line in text.split("\n"):
            # Match "- Key: value" or "**Key**: value"
            match = re.match(r"-\s+(?:\*\*)?(.+?)(?:\*\*)?:\s*(.+)", line.strip())
            if not match:
                # Try without the leading dash for "**Key**: value" format
                match = re.match(r"(?:\*\*)?(.+?)(?:\*\*)?:\s*(.+)", line.strip())
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                # Only add if key and value are non-empty and not markers
                if key and value and not key.startswith("*") and not value.startswith("*"):
                    result[key] = value
        return result

    def _parse_conditions_section(self, text: str) -> dict[str, Any]:
        """Parse conditions section with primary/comorbidities.

        Args:
            text: Conditions section text

        Returns:
            Dictionary with primary and comorbidities
        """
        result: dict[str, Any] = {"primary": [], "comorbidities": []}

        current_category = None
        for line in text.split("\n"):
            line = line.strip()

            # Check for category headers
            if line.startswith("**Primary"):
                current_category = "primary"
            elif line.startswith("**Comorbidities"):
                current_category = "comorbidities"
            elif line.startswith("-") and current_category:
                # Extract diagnosis (ICD code or name)
                result[current_category].append(line[1:].strip())

        return result

    def _parse_knowledge(self, sections: dict[str, Any]) -> dict[str, str]:
        """Parse knowledge section.

        Supports both v1.0 "Knowledge" and v2.0 "Domain Knowledge".

        Args:
            sections: Parsed sections

        Returns:
            Dictionary of knowledge subsections
        """
        # Try v2.0 section name first, fall back to v1.0
        knowledge_text = sections.get("Domain Knowledge", sections.get("Knowledge"))

        if not knowledge_text:
            return {}

        # Parse subsections within Knowledge (### headings)
        subsections: dict[str, str] = {}
        current_subsection = None
        current_content: list[str] = []

        for line in knowledge_text.split("\n"):
            subsection_match = re.match(r"^###\s+(.+)$", line)
            if subsection_match:
                if current_subsection:
                    subsections[current_subsection] = "\n".join(current_content).strip()
                current_subsection = subsection_match.group(1).strip()
                current_content = []
            elif current_subsection:
                current_content.append(line)

        if current_subsection:
            subsections[current_subsection] = "\n".join(current_content).strip()

        return subsections

    def _parse_variations(self, sections: dict[str, Any]) -> list[SkillVariation]:
        """Parse variations section.

        Args:
            sections: Parsed sections

        Returns:
            List of SkillVariation objects
        """
        if "Variations" not in sections:
            return []

        variations_text = sections["Variations"]
        variations = []

        # Parse variations (### Variation: Name format)
        current_variation = None
        current_description: list[str] = []
        current_overrides: dict[str, str] = {}

        for line in variations_text.split("\n"):
            variation_match = re.match(r"^###\s+Variation:\s+(.+)$", line)
            if variation_match:
                # Save previous variation
                if current_variation:
                    variations.append(
                        SkillVariation(
                            name=current_variation,
                            description="\n".join(current_description).strip(),
                            overrides=current_overrides,
                        )
                    )

                # Start new variation
                current_variation = variation_match.group(1).strip()
                current_description = []
                current_overrides = {}
            elif current_variation:
                # Parse override lines (- Key: value)
                override_match = re.match(r"-\s+(.+?):\s*(.+)", line.strip())
                if override_match:
                    key = override_match.group(1).strip()
                    value = override_match.group(2).strip()
                    current_overrides[key] = value
                else:
                    current_description.append(line)

        # Save last variation
        if current_variation:
            variations.append(
                SkillVariation(
                    name=current_variation,
                    description="\n".join(current_description).strip(),
                    overrides=current_overrides,
                )
            )

        return variations

    def _parse_examples(self, sections: dict[str, Any]) -> list[str]:
        """Parse examples section.

        Supports both v1.0 "Examples" and v2.0 "Example Requests and Interpretations".

        Args:
            sections: Parsed sections

        Returns:
            List of example texts
        """
        # Try v2.0 section name first, fall back to v1.0
        examples_text = sections.get(
            "Example Requests and Interpretations", sections.get("Examples")
        )

        if not examples_text:
            return []

        examples = []

        # Split by ### Example headings
        current_example: list[str] = []

        for line in examples_text.split("\n"):
            if re.match(r"^###\s+Example", line):
                if current_example:
                    examples.append("\n".join(current_example).strip())
                current_example = [line]
            else:
                current_example.append(line)

        if current_example:
            examples.append("\n".join(current_example).strip())

        return examples

    def _parse_references(self, sections: dict[str, Any]) -> list[str]:
        """Parse references section.

        Args:
            sections: Parsed sections

        Returns:
            List of reference strings
        """
        if "References" not in sections and "Clinical References" not in sections:
            return []

        ref_section = sections.get("References", sections.get("Clinical References", ""))

        references = []
        for line in ref_section.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                references.append(line[1:].strip())
            elif line:  # Non-empty, non-bullet lines
                references.append(line)

        return references

    def _parse_dependencies(self, sections: dict[str, Any]) -> list[str]:
        """Parse dependencies section.

        Args:
            sections: Parsed sections

        Returns:
            List of dependency paths
        """
        if "Dependencies" not in sections:
            return []

        deps_text = sections["Dependencies"]
        dependencies = []

        for line in deps_text.split("\n"):
            line = line.strip()
            if line.startswith("-"):
                dependencies.append(line[1:].strip())
            elif line and line.lower() != "none":
                dependencies.append(line)

        # Filter out "None - ..." type entries
        return [d for d in dependencies if not d.lower().startswith("none")]

    def _parse_for_claude(self, sections: dict[str, Any]) -> str | None:
        """Parse 'For Claude' section (v2.0 format).

        Args:
            sections: Parsed sections

        Returns:
            For Claude text or None if not present
        """
        return sections.get("For Claude")

    def _parse_when_to_use(self, sections: dict[str, Any]) -> str | None:
        """Parse 'When to Use This Skill' section (v2.0 format).

        Args:
            sections: Parsed sections

        Returns:
            When to Use text or None if not present
        """
        return sections.get("When to Use This Skill")

    def _parse_generation_guidelines(self, sections: dict[str, Any]) -> str | None:
        """Parse 'Generation Guidelines' section (v2.0 format).

        Args:
            sections: Parsed sections

        Returns:
            Generation Guidelines text or None if not present
        """
        return sections.get("Generation Guidelines")
