#!/usr/bin/env python3
"""
HealthSim Link Validator

Validates all markdown links in the repository.

Usage:
    python scripts/validate_links.py [options]

Options:
    --fix       Attempt to fix simple issues (add .md extensions, etc.)
    --verbose   Show all checked links, not just errors
    --skip-external  Skip validation of external URLs
    
Exit codes:
    0 - All links valid
    1 - Broken links found
    2 - Script error
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class LinkInfo:
    """Information about a link found in a markdown file."""
    source_file: Path
    line_number: int
    link_text: str
    link_target: str
    link_type: str  # 'internal', 'anchor', 'external'


@dataclass
class ValidationResult:
    """Result of validating a link."""
    link: LinkInfo
    valid: bool
    error: str = ""
    suggestion: str = ""


class MarkdownLinkValidator:
    """Validates links in markdown files."""
    
    # Regex patterns
    MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    HEADER_PATTERN = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
    
    def __init__(self, root_dir: Path, skip_external: bool = False):
        self.root_dir = root_dir
        self.skip_external = skip_external
        self.all_files: Set[Path] = set()
        self.file_headers: Dict[Path, Set[str]] = {}
        self.links_found: List[LinkInfo] = []
        self.results: List[ValidationResult] = []
        
    def scan_repository(self) -> None:
        """Scan repository for all markdown files and their headers."""
        for md_file in self.root_dir.rglob('*.md'):
            # Skip hidden directories and common non-documentation folders
            parts = md_file.relative_to(self.root_dir).parts
            if any(part.startswith('.') or part in ['node_modules', '.venv', 'venv', '__pycache__'] for part in parts):
                continue
                
            self.all_files.add(md_file)
            self.file_headers[md_file] = self._extract_headers(md_file)
            
    def _extract_headers(self, file_path: Path) -> Set[str]:
        """Extract all headers from a markdown file and convert to anchor format."""
        headers = set()
        try:
            content = file_path.read_text(encoding='utf-8')
            for match in self.HEADER_PATTERN.finditer(content):
                header_text = match.group(1).strip()
                # Convert header to anchor format (lowercase, spaces to hyphens, remove special chars)
                anchor = re.sub(r'[^\w\s-]', '', header_text.lower())
                anchor = re.sub(r'\s+', '-', anchor)
                headers.add(anchor)
        except Exception:
            pass
        return headers
        
    def find_links(self) -> None:
        """Find all links in markdown files."""
        for md_file in self.all_files:
            try:
                content = md_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    for match in self.MD_LINK_PATTERN.finditer(line):
                        link_text = match.group(1)
                        link_target = match.group(2)
                        
                        # Determine link type
                        if link_target.startswith('http://') or link_target.startswith('https://'):
                            link_type = 'external'
                        elif link_target.startswith('#'):
                            link_type = 'anchor'
                        else:
                            link_type = 'internal'
                            
                        self.links_found.append(LinkInfo(
                            source_file=md_file,
                            line_number=line_num,
                            link_text=link_text,
                            link_target=link_target,
                            link_type=link_type
                        ))
            except Exception as e:
                print(f"Warning: Could not read {md_file}: {e}", file=sys.stderr)
                
    def validate_links(self) -> None:
        """Validate all found links."""
        for link in self.links_found:
            if link.link_type == 'external':
                if self.skip_external:
                    self.results.append(ValidationResult(link, True))
                else:
                    # Just check URL format, don't actually fetch
                    valid = link.link_target.startswith('http://') or link.link_target.startswith('https://')
                    self.results.append(ValidationResult(
                        link, valid,
                        error="" if valid else "Invalid URL format"
                    ))
            elif link.link_type == 'anchor':
                # Check anchor in same file
                anchor = link.link_target[1:]  # Remove leading #
                if anchor in self.file_headers.get(link.source_file, set()):
                    self.results.append(ValidationResult(link, True))
                else:
                    self.results.append(ValidationResult(
                        link, False,
                        error=f"Anchor '{anchor}' not found in file",
                        suggestion=self._suggest_anchor(link.source_file, anchor)
                    ))
            else:
                # Internal link
                result = self._validate_internal_link(link)
                self.results.append(result)
                
    def _validate_internal_link(self, link: LinkInfo) -> ValidationResult:
        """Validate an internal markdown link."""
        target = link.link_target
        
        # Split path and anchor
        anchor = None
        if '#' in target:
            target, anchor = target.split('#', 1)
            
        # Resolve relative path
        if target:
            if target.startswith('/'):
                # Absolute path from repo root
                target_path = self.root_dir / target.lstrip('/')
            else:
                # Relative path from source file
                target_path = link.source_file.parent / target
            target_path = target_path.resolve()
        else:
            # Anchor-only link to same file
            target_path = link.source_file
            
        # Check if file exists
        if not target_path.exists():
            # Try adding .md extension
            if not target.endswith('.md') and (target_path.parent / (target_path.name + '.md')).exists():
                return ValidationResult(
                    link, False,
                    error=f"File not found: {target}",
                    suggestion=f"Did you mean '{target}.md'?"
                )
            return ValidationResult(
                link, False,
                error=f"File not found: {target_path.relative_to(self.root_dir) if target_path.is_relative_to(self.root_dir) else target}"
            )
            
        # Check anchor if present
        if anchor:
            if target_path in self.file_headers:
                if anchor not in self.file_headers[target_path]:
                    return ValidationResult(
                        link, False,
                        error=f"Anchor '{anchor}' not found in {target_path.name}",
                        suggestion=self._suggest_anchor(target_path, anchor)
                    )
                    
        return ValidationResult(link, True)
        
    def _suggest_anchor(self, file_path: Path, anchor: str) -> str:
        """Suggest a similar anchor from the file."""
        headers = self.file_headers.get(file_path, set())
        if not headers:
            return ""
            
        # Simple similarity check
        for header in headers:
            if anchor in header or header in anchor:
                return f"Did you mean '#{header}'?"
        return ""
        
    def report(self, verbose: bool = False) -> Tuple[int, int]:
        """Print validation report. Returns (total, errors) count."""
        broken_links = [r for r in self.results if not r.valid]
        
        if verbose:
            print(f"\nScanned {len(self.all_files)} markdown files")
            print(f"Found {len(self.links_found)} links")
            print(f"Broken: {len(broken_links)}")
            print()
            
        if broken_links:
            print("❌ BROKEN LINKS FOUND:\n")
            
            # Group by source file
            by_file = defaultdict(list)
            for result in broken_links:
                by_file[result.link.source_file].append(result)
                
            for source_file, results in sorted(by_file.items()):
                rel_path = source_file.relative_to(self.root_dir)
                print(f"📄 {rel_path}")
                for result in results:
                    print(f"   Line {result.link.line_number}: [{result.link.link_text}]({result.link.link_target})")
                    print(f"   └─ {result.error}")
                    if result.suggestion:
                        print(f"      💡 {result.suggestion}")
                print()
        else:
            print("✅ All links valid!")
            
        return len(self.links_found), len(broken_links)


def main():
    parser = argparse.ArgumentParser(description="Validate markdown links in HealthSim repository")
    parser.add_argument('--fix', action='store_true', help='Attempt to fix simple issues')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--skip-external', action='store_true', help='Skip external URL validation')
    parser.add_argument('--root', type=str, default='.', help='Repository root directory')
    args = parser.parse_args()
    
    root_dir = Path(args.root).resolve()
    
    if not (root_dir / 'SKILL.md').exists():
        print("Error: Not in HealthSim workspace root (SKILL.md not found)")
        sys.exit(2)
        
    validator = MarkdownLinkValidator(root_dir, skip_external=args.skip_external)
    
    print("🔍 Scanning repository...")
    validator.scan_repository()
    
    print("🔗 Finding links...")
    validator.find_links()
    
    print("✓ Validating links...")
    validator.validate_links()
    
    total, errors = validator.report(verbose=args.verbose)
    
    if errors > 0:
        print(f"\n⚠️  {errors} broken links found out of {total} total links")
        sys.exit(1)
    else:
        print(f"\n✅ All {total} links validated successfully")
        sys.exit(0)


if __name__ == '__main__':
    main()
