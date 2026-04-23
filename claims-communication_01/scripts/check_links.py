#!/usr/bin/env python3
"""Check for broken markdown links in documentation."""

import os
import re
from pathlib import Path
from collections import defaultdict

def find_md_links(content, file_path):
    """Find all markdown links in content."""
    # Match [text](path) but not images ![text](path)
    pattern = r'(?<!\!)\[([^\]]+)\]\(([^)]+)\)'
    links = []
    for match in re.finditer(pattern, content):
        text = match.group(1)
        target = match.group(2)
        # Skip URLs
        if target.startswith(('http://', 'https://', 'mailto:')):
            continue
        # Skip pure anchors
        if target.startswith('#'):
            continue
        links.append((text, target, match.start()))
    return links

def resolve_link(link_target, source_file, repo_root):
    """Resolve a relative link to absolute path."""
    # Remove anchor if present
    target = link_target.split('#')[0]
    if not target:
        return None, 'anchor-only'
    
    source_dir = source_file.parent
    
    # Handle absolute paths from repo root
    if target.startswith('/'):
        resolved = repo_root / target.lstrip('/')
    else:
        resolved = (source_dir / target).resolve()
    
    return resolved, None

def check_links(repo_root):
    """Check all markdown links in the repository."""
    repo_root = Path(repo_root)
    docs_dir = repo_root / 'docs'
    
    broken = []
    valid = 0
    
    for md_file in docs_dir.rglob('*.md'):
        try:
            content = md_file.read_text(encoding='utf-8')
        except:
            continue
            
        links = find_md_links(content, md_file)
        
        for text, target, pos in links:
            resolved, err = resolve_link(target, md_file, repo_root)
            
            if err:
                continue
                
            if resolved and not resolved.exists():
                # Get line number
                line_num = content[:pos].count('\n') + 1
                rel_file = md_file.relative_to(repo_root)
                broken.append({
                    'file': str(rel_file),
                    'line': line_num,
                    'text': text,
                    'target': target,
                    'resolved': str(resolved)
                })
            else:
                valid += 1
    
    return broken, valid

if __name__ == '__main__':
    repo = '/Users/markoswald/Developer/projects/healthsim-workspace'
    broken, valid = check_links(repo)
    
    print(f"Valid links: {valid}")
    print(f"Broken links: {len(broken)}")
    print()
    
    if broken:
        # Group by file
        by_file = defaultdict(list)
        for b in broken:
            by_file[b['file']].append(b)
        
        for file, items in sorted(by_file.items()):
            print(f"\n{file}:")
            for item in items:
                print(f"  Line {item['line']}: [{item['text']}]({item['target']})")
