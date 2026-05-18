#!/usr/bin/env python3
"""
Check status of NPPES filtering process
"""

from pathlib import Path
import subprocess
import time

base_dir = Path("/Users/markoswald/Developer/projects/healthsim-workspace/scenarios/networksim")
output_file = base_dir / "data/processed/nppes_filtered.csv"

print("=" * 80)
print("NPPES FILTER STATUS CHECK")
print("=" * 80)

# Check if process is running
print("\n1. PROCESS STATUS:")
result = subprocess.run(
    ["ps", "aux"],
    capture_output=True,
    text=True
)
filter_processes = [line for line in result.stdout.split('\n') if 'filter_nppes.py' in line and 'grep' not in line]

if filter_processes:
    print("   ✓ Filter process is RUNNING")
    for proc in filter_processes:
        # Extract relevant info from ps output
        parts = proc.split()
        if len(parts) >= 11:
            cpu = parts[2]
            mem = parts[3]
            time_used = parts[9]
            print(f"   • CPU: {cpu}%  Memory: {mem}%  Time: {time_used}")
else:
    print("   ✗ No filter process found (may have finished or not started)")

# Check output file
print("\n2. OUTPUT FILE STATUS:")
if output_file.exists():
    size_mb = output_file.stat().st_size / (1024**2)
    print(f"   ✓ File exists: {output_file.name}")
    print(f"   • Current size: {size_mb:.1f} MB")
    print(f"   • Expected final size: ~500-700 MB")
    
    if size_mb > 0:
        progress_pct = min((size_mb / 600) * 100, 100)
        print(f"   • Estimated progress: {progress_pct:.0f}%")
        
        # Show a progress bar
        bar_length = 50
        filled = int(bar_length * progress_pct / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"   [{bar}] {progress_pct:.0f}%")
else:
    print("   ⏳ Output file not created yet")
    print("   • This is normal - file is created when data starts being written")
    print("   • Process may still be loading the input CSV (takes 2-3 minutes)")

# Estimate time remaining
print("\n3. ESTIMATED TIME:")
if output_file.exists():
    size_mb = output_file.stat().st_size / (1024**2)
    if size_mb > 10:  # Has meaningful data
        # Rough estimate: ~600 MB final size, ~5-8 minutes total
        progress_pct = min((size_mb / 600) * 100, 100)
        if progress_pct < 100:
            # Estimate ~6 minutes total processing time
            estimated_remaining = (100 - progress_pct) / 100 * 6
            print(f"   • Estimated time remaining: ~{estimated_remaining:.0f} minutes")
        else:
            print("   • Should be finishing up...")
    else:
        print("   • Still in early stages (loading/filtering)")
        print("   • Estimated time remaining: 5-8 minutes")
else:
    print("   • Still loading input file (2-3 minutes)")
    print("   • Total expected time: 5-10 minutes from start")

print("\n" + "=" * 80)
print("TIP: Run this script again in 1-2 minutes to see progress")
print("     Or watch the file size grow:")
print(f"     ls -lh {output_file}")
print("=" * 80)
