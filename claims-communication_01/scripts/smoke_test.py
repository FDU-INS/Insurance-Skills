#!/usr/bin/env python3
"""
Smoke test for HealthSim skills integration.
Validates that all components work together correctly.
"""

import json
import os
import re
import sys
from pathlib import Path

# Colors for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(text: str):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{text}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")


def print_pass(text: str):
    print(f"  {GREEN}✓{RESET} {text}")


def print_fail(text: str):
    print(f"  {RED}✗{RESET} {text}")


def print_warn(text: str):
    print(f"  {YELLOW}⚠{RESET} {text}")


class SmokeTest:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, condition: bool, pass_msg: str, fail_msg: str) -> bool:
        if condition:
            print_pass(pass_msg)
            self.passed += 1
            return True
        else:
            print_fail(fail_msg)
            self.failed += 1
            return False

    def warn(self, msg: str):
        print_warn(msg)
        self.warnings += 1


def test_directory_structure(test: SmokeTest):
    """Verify required directories exist."""
    print_header("1. Directory Structure")

    required_dirs = [
        "skills/patientsim",
        "skills/patientsim/oncology",
        "skills/membersim",
        "skills/rxmembersim",
        "references/oncology",
        "formats",
        "hello-healthsim",
        "hello-healthsim/examples",
    ]

    for dir_path in required_dirs:
        full_path = test.base_path / dir_path
        test.check(
            full_path.is_dir(),
            f"{dir_path}/ exists",
            f"{dir_path}/ MISSING",
        )


def test_oncology_skills(test: SmokeTest):
    """Verify oncology skill files exist and have content."""
    print_header("2. Oncology Skills")

    oncology_skills = [
        "references/oncology-domain.md",  # Foundational oncology knowledge (in references/)
        "skills/patientsim/oncology/breast-cancer.md",
        "skills/patientsim/oncology/lung-cancer.md",
        "skills/patientsim/oncology/colorectal-cancer.md",
    ]

    for skill_path in oncology_skills:
        full_path = test.base_path / skill_path
        if test.check(full_path.exists(), f"{skill_path} exists", f"{skill_path} MISSING"):
            content = full_path.read_text()
            # Check for key sections
            has_metadata = "## Metadata" in content or "---" in content[:100]
            has_purpose = "## Purpose" in content or "## Overview" in content
            test.check(
                has_metadata and has_purpose,
                f"  └─ Has required sections",
                f"  └─ Missing metadata or purpose section",
            )


def test_reference_data(test: SmokeTest):
    """Verify oncology reference data files exist and are valid."""
    print_header("3. Reference Data")

    reference_files = [
        ("references/oncology/oncology-icd10-codes.csv", "csv"),
        ("references/oncology/oncology-medications.csv", "csv"),
        ("references/oncology/oncology-regimens.csv", "csv"),
        ("references/oncology/oncology-tumor-markers.csv", "csv"),
        ("references/oncology/oncology-staging-templates.yaml", "yaml"),
    ]

    for ref_path, file_type in reference_files:
        full_path = test.base_path / ref_path
        if test.check(full_path.exists(), f"{ref_path} exists", f"{ref_path} MISSING"):
            content = full_path.read_text()
            # Basic validation
            if file_type == "csv":
                lines = content.strip().split("\n")
                test.check(
                    len(lines) > 1,
                    f"  └─ Has {len(lines)-1} data rows",
                    f"  └─ Empty or header-only CSV",
                )
            elif file_type == "yaml":
                test.check(
                    ":" in content,
                    f"  └─ Valid YAML structure",
                    f"  └─ Invalid YAML structure",
                )


def test_skill_cross_references(test: SmokeTest):
    """Verify cross-references between skills resolve correctly."""
    print_header("4. Cross-References")

    # Check PatientSim SKILL.md references oncology
    patientsim_skill = test.base_path / "skills/patientsim/SKILL.md"
    if patientsim_skill.exists():
        content = patientsim_skill.read_text()
        test.check(
            "oncology/breast-cancer.md" in content,
            "PatientSim SKILL.md references oncology skills",
            "PatientSim SKILL.md missing oncology references",
        )

    # Check MemberSim SKILL.md references oncology
    membersim_skill = test.base_path / "skills/membersim/SKILL.md"
    if membersim_skill.exists():
        content = membersim_skill.read_text()
        test.check(
            "patientsim/oncology" in content or "PatientSim" in content,
            "MemberSim SKILL.md references PatientSim oncology",
            "MemberSim SKILL.md missing PatientSim oncology references",
        )
        test.check(
            "J9267" in content or "oncology" in content.lower(),
            "MemberSim SKILL.md has oncology claim example",
            "MemberSim SKILL.md missing oncology claim example",
        )

    # Check relative links resolve
    oncology_readme = test.base_path / "skills/patientsim/oncology/README.md"
    if oncology_readme.exists():
        content = oncology_readme.read_text()
        # Extract markdown links
        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
        broken_links = []
        for link_text, link_path in links:
            if link_path.startswith("http"):
                continue
            if link_path.startswith("../"):
                resolved = (oncology_readme.parent / link_path).resolve()
            else:
                resolved = (oncology_readme.parent / link_path).resolve()
            if not resolved.exists():
                broken_links.append(link_path)

        test.check(
            len(broken_links) == 0,
            f"All README links resolve ({len(links)} checked)",
            f"Broken links: {broken_links[:3]}...",
        )


def test_hello_healthsim_examples(test: SmokeTest):
    """Verify hello-healthsim examples are valid."""
    print_header("5. Hello-HealthSim Examples")

    examples_dir = test.base_path / "hello-healthsim/examples"
    if not examples_dir.exists():
        test.check(False, "", "examples/ directory missing")
        return

    example_files = list(examples_dir.glob("*.md"))
    test.check(
        len(example_files) >= 5,
        f"Found {len(example_files)} example files",
        f"Expected at least 5 example files, found {len(example_files)}",
    )

    # Check oncology examples specifically
    oncology_examples = examples_dir / "oncology-examples.md"
    if test.check(
        oncology_examples.exists(),
        "oncology-examples.md exists",
        "oncology-examples.md MISSING",
    ):
        content = oncology_examples.read_text()

        # Check for key cancer types
        cancer_types = ["breast", "lung", "colorectal", "colon"]
        found = [ct for ct in cancer_types if ct.lower() in content.lower()]
        test.check(
            len(found) >= 3,
            f"Covers {len(found)} cancer types: {', '.join(found)}",
            f"Missing cancer type coverage",
        )

        # Check for JSON examples
        json_blocks = re.findall(r"```json\s*([\s\S]*?)```", content)
        valid_json = 0
        for block in json_blocks:
            try:
                json.loads(block)
                valid_json += 1
            except json.JSONDecodeError:
                pass

        test.check(
            valid_json >= 3,
            f"{valid_json} valid JSON examples",
            f"Only {valid_json} valid JSON examples (expected 3+)",
        )


def test_json_examples_in_skills(test: SmokeTest):
    """Verify JSON examples in skill files are valid."""
    print_header("6. JSON Example Validation")

    skill_files = [
        "skills/patientsim/oncology/breast-cancer.md",
        "skills/patientsim/oncology/lung-cancer.md",
        "skills/patientsim/oncology/colorectal-cancer.md",
        "skills/membersim/SKILL.md",
    ]

    for skill_path in skill_files:
        full_path = test.base_path / skill_path
        if not full_path.exists():
            continue

        content = full_path.read_text()
        json_blocks = re.findall(r"```json\s*([\s\S]*?)```", content)

        valid = 0
        invalid = 0
        for block in json_blocks:
            try:
                json.loads(block)
                valid += 1
            except json.JSONDecodeError:
                invalid += 1

        if valid + invalid > 0:
            test.check(
                invalid == 0,
                f"{Path(skill_path).name}: {valid} valid JSON blocks",
                f"{Path(skill_path).name}: {invalid} invalid JSON blocks",
            )


def test_cross_product_integration(test: SmokeTest):
    """Test cross-product integration scenarios."""
    print_header("7. Cross-Product Integration")

    # Check that oncology spans all three products
    products = {
        "PatientSim": "skills/patientsim/oncology/breast-cancer.md",
        "MemberSim": "skills/membersim/SKILL.md",
        "RxMemberSim": "skills/rxmembersim/SKILL.md",
    }

    oncology_coverage = {}
    for product, path in products.items():
        full_path = test.base_path / path
        if full_path.exists():
            content = full_path.read_text()
            # Check for oncology-related content
            has_oncology = any(
                term in content.lower()
                for term in ["oncology", "cancer", "chemotherapy", "tumor", "j9"]
            )
            oncology_coverage[product] = has_oncology

    covered = [p for p, has in oncology_coverage.items() if has]
    test.check(
        len(covered) >= 2,
        f"Oncology coverage: {', '.join(covered)}",
        f"Limited oncology coverage: only {', '.join(covered)}",
    )

    # Check cross-domain examples
    cross_domain = test.base_path / "hello-healthsim/examples/cross-domain-examples.md"
    if cross_domain.exists():
        content = cross_domain.read_text()
        test.check(
            "oncology" in content.lower() or "cancer" in content.lower(),
            "Cross-domain examples include oncology",
            "Cross-domain examples missing oncology",
        )


def main():
    # Determine base path
    script_dir = Path(__file__).parent
    base_path = script_dir.parent  # healthsim-common root

    print(f"\n{BOLD}HealthSim Smoke Test{RESET}")
    print(f"Base path: {base_path}")

    test = SmokeTest(base_path)

    # Run all tests
    test_directory_structure(test)
    test_oncology_skills(test)
    test_reference_data(test)
    test_skill_cross_references(test)
    test_hello_healthsim_examples(test)
    test_json_examples_in_skills(test)
    test_cross_product_integration(test)

    # Summary
    print_header("Summary")
    print(f"  Passed:   {GREEN}{test.passed}{RESET}")
    print(f"  Failed:   {RED}{test.failed}{RESET}")
    print(f"  Warnings: {YELLOW}{test.warnings}{RESET}")

    if test.failed == 0:
        print(f"\n{GREEN}{BOLD}✓ All smoke tests passed!{RESET}")
        return 0
    else:
        print(f"\n{RED}{BOLD}✗ {test.failed} test(s) failed{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
