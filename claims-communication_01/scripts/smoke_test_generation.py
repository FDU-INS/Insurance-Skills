#!/usr/bin/env python3
"""
Smoke test for HealthSim Generative Framework.

Validates that all generation skills are properly structured and accessible.
Run after any changes to generation skills.

Usage:
    python scripts/smoke_test_generation.py
"""

import os
import sys
import json
import re
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

def check_mark():
    return f'{GREEN}✓{RESET}'

def x_mark():
    return f'{RED}✗{RESET}'

def warning_mark():
    return f'{YELLOW}⚠{RESET}'


class GenerationSmokeTest:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.generation_path = self.base_path / 'skills' / 'generation'
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def run_all(self):
        print(f"\n{BOLD}HealthSim Generative Framework Smoke Test{RESET}")
        print(f"Base path: {self.base_path}\n")

        self.test_directory_structure()
        self.test_readme_files()
        self.test_builder_skills()
        self.test_executor_skills()
        self.test_distribution_skills()
        self.test_journey_skills()
        self.test_profile_templates()
        self.test_journey_templates()
        self.test_schemas()
        self.test_skill_frontmatter()

        self.print_summary()
        return self.failed == 0

    def test_directory_structure(self):
        print(f"{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}1. Directory Structure{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_dirs = [
            'skills/generation',
            'skills/generation/builders',
            'skills/generation/executors',
            'skills/generation/distributions',
            'skills/generation/journeys',
            'skills/generation/templates',
            'skills/generation/templates/profiles',
            'skills/generation/templates/journeys',
            'schemas',
        ]

        for dir_path in required_dirs:
            full_path = self.base_path / dir_path
            if full_path.exists():
                print(f"  {check_mark()} {dir_path}/ exists")
                self.passed += 1
            else:
                print(f"  {x_mark()} {dir_path}/ missing")
                self.failed += 1

    def test_readme_files(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}2. README Files{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        readme_locations = [
            'skills/generation',
            'skills/generation/builders',
            'skills/generation/executors',
            'skills/generation/distributions',
            'skills/generation/journeys',
            'skills/generation/templates',
            'skills/generation/templates/profiles',
            'skills/generation/templates/journeys',
        ]

        for dir_path in readme_locations:
            readme_path = self.base_path / dir_path / 'README.md'
            if readme_path.exists():
                print(f"  {check_mark()} {dir_path}/README.md exists")
                self.passed += 1
            else:
                print(f"  {x_mark()} {dir_path}/README.md missing")
                self.failed += 1

    def test_builder_skills(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}3. Builder Skills{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_skills = [
            'profile-builder.md',
            'journey-builder.md',
            'quick-generate.md',
        ]

        builders_path = self.generation_path / 'builders'
        for skill in required_skills:
            skill_path = builders_path / skill
            if skill_path.exists():
                content = skill_path.read_text()
                if 'triggers:' in content or 'Trigger' in content:
                    print(f"  {check_mark()} {skill} exists with triggers")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {skill} exists but no triggers found")
                    self.warnings += 1
            else:
                print(f"  {x_mark()} {skill} missing")
                self.failed += 1

    def test_executor_skills(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}4. Executor Skills{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_skills = [
            'profile-executor.md',
            'journey-executor.md',
            'cross-domain-sync.md',
        ]

        executors_path = self.generation_path / 'executors'
        for skill in required_skills:
            skill_path = executors_path / skill
            if skill_path.exists():
                print(f"  {check_mark()} {skill} exists")
                self.passed += 1
            else:
                print(f"  {x_mark()} {skill} missing")
                self.failed += 1

    def test_distribution_skills(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}5. Distribution Skills{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_skills = [
            'distribution-types.md',
        ]

        dist_path = self.generation_path / 'distributions'
        for skill in required_skills:
            skill_path = dist_path / skill
            if skill_path.exists():
                content = skill_path.read_text()
                # Check for required distribution types
                dist_types = ['categorical', 'normal', 'log_normal', 'conditional']
                found = [dt for dt in dist_types if dt.lower() in content.lower()]
                if len(found) >= 3:
                    print(f"  {check_mark()} {skill} exists with {len(found)} distribution types")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {skill} exists but only {len(found)} distribution types found")
                    self.warnings += 1
            else:
                print(f"  {x_mark()} {skill} missing")
                self.failed += 1

    def test_journey_skills(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}6. Journey Pattern Skills{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_skills = [
            'journey-patterns.md',
        ]

        journeys_path = self.generation_path / 'journeys'
        for skill in required_skills:
            skill_path = journeys_path / skill
            if skill_path.exists():
                content = skill_path.read_text()
                # Check for required patterns
                patterns = ['linear', 'branching', 'cyclic', 'protocol']
                found = [p for p in patterns if p.lower() in content.lower()]
                if len(found) >= 3:
                    print(f"  {check_mark()} {skill} exists with {len(found)} patterns")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {skill} exists but only {len(found)} patterns found")
                    self.warnings += 1
            else:
                print(f"  {x_mark()} {skill} missing")
                self.failed += 1

    def test_profile_templates(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}7. Profile Templates{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_templates = [
            'medicare-diabetic.md',
            'commercial-healthy.md',
            'medicaid-pediatric.md',
        ]

        profiles_path = self.generation_path / 'templates' / 'profiles'
        for template in required_templates:
            template_path = profiles_path / template
            if template_path.exists():
                content = template_path.read_text()
                if '"profile"' in content or 'profile:' in content:
                    print(f"  {check_mark()} {template} exists with profile spec")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {template} exists but no profile spec found")
                    self.warnings += 1
            else:
                print(f"  {x_mark()} {template} missing")
                self.failed += 1

        # Count total templates
        if profiles_path.exists():
            all_templates = list(profiles_path.glob('*.md'))
            templates = [t for t in all_templates if t.name != 'README.md']
            print(f"  {check_mark()} Total profile templates: {len(templates)}")
            self.passed += 1

    def test_journey_templates(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}8. Journey Templates{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_templates = [
            'diabetic-first-year.md',
            'surgical-episode.md',
            'new-member-onboarding.md',
        ]

        journeys_path = self.generation_path / 'templates' / 'journeys'
        for template in required_templates:
            template_path = journeys_path / template
            if template_path.exists():
                content = template_path.read_text()
                if '"journey"' in content or 'journey:' in content or 'phases' in content:
                    print(f"  {check_mark()} {template} exists with journey spec")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {template} exists but no journey spec found")
                    self.warnings += 1
            else:
                print(f"  {x_mark()} {template} missing")
                self.failed += 1

        # Count total templates
        if journeys_path.exists():
            all_templates = list(journeys_path.glob('*.md'))
            templates = [t for t in all_templates if t.name != 'README.md']
            print(f"  {check_mark()} Total journey templates: {len(templates)}")
            self.passed += 1

    def test_schemas(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}9. JSON Schemas{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        required_schemas = [
            'profile-spec-v1.json',
            'journey-spec-v1.json',
        ]

        schemas_path = self.base_path / 'schemas'
        for schema in required_schemas:
            schema_path = schemas_path / schema
            if schema_path.exists():
                try:
                    content = schema_path.read_text()
                    json.loads(content)
                    print(f"  {check_mark()} {schema} exists and is valid JSON")
                    self.passed += 1
                except json.JSONDecodeError as e:
                    print(f"  {x_mark()} {schema} exists but invalid JSON: {e}")
                    self.failed += 1
            else:
                print(f"  {x_mark()} {schema} missing")
                self.failed += 1

    def test_skill_frontmatter(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}10. Skill Frontmatter Validation{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")

        # Check key skills have proper frontmatter
        key_skills = [
            'skills/generation/builders/profile-builder.md',
            'skills/generation/builders/journey-builder.md',
            'skills/generation/executors/profile-executor.md',
        ]

        frontmatter_pattern = re.compile(r'^---\s*\n.*?name:.*?\n.*?---', re.DOTALL)

        for skill_path in key_skills:
            full_path = self.base_path / skill_path
            if full_path.exists():
                content = full_path.read_text()
                if frontmatter_pattern.match(content):
                    print(f"  {check_mark()} {skill_path.split('/')[-1]} has valid frontmatter")
                    self.passed += 1
                else:
                    print(f"  {warning_mark()} {skill_path.split('/')[-1]} missing frontmatter")
                    self.warnings += 1

    def print_summary(self):
        print(f"\n{BOLD}{'='*60}{RESET}")
        print(f"{BOLD}Summary{RESET}")
        print(f"{BOLD}{'='*60}{RESET}")
        print(f"  Passed:   {GREEN}{self.passed}{RESET}")
        print(f"  Failed:   {RED}{self.failed}{RESET}")
        print(f"  Warnings: {YELLOW}{self.warnings}{RESET}")

        if self.failed == 0:
            print(f"\n{GREEN}{BOLD}✓ All generation smoke tests passed!{RESET}")
        else:
            print(f"\n{RED}{BOLD}✗ Some tests failed. See above for details.{RESET}")


def main():
    tester = GenerationSmokeTest()
    success = tester.run_all()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
