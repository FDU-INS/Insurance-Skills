#!/usr/bin/env python3
"""Validate a bond verification report JSON.
Exits 0 if valid, 1 if invalid."""
import json, sys

VALID_STATUSES = {"VERIFIED", "FAILED", "PARTIAL"}
VALID_CHECK_RESULTS = {"PASS", "FAIL", "WARNING", "SKIPPED"}

def validate(report):
    errors = []
    if report.get("verification_status") not in VALID_STATUSES:
        errors.append(f"Invalid verification_status: {report.get('verification_status')}")
    if not report.get("bond_number"):
        errors.append("Missing bond_number")
    surety = report.get("surety", {})
    if not surety.get("name"):
        errors.append("Missing surety.name")
    if "circular_570_listed" not in surety:
        errors.append("Missing surety.circular_570_listed")
    if not report.get("principal"):
        errors.append("Missing principal")
    if not report.get("penal_sum"):
        errors.append("Missing penal_sum")
    for check in report.get("checks", []):
        if check.get("result") not in VALID_CHECK_RESULTS:
            errors.append(f"Invalid check result: {check.get('result')} for {check.get('check')}")
    if not report.get("requires_human"):
        errors.append("Missing requires_human — every report must list what needs human follow-up")
    return errors

def main():
    data = json.load(open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin)
    errors = validate(data)
    if errors:
        for e in errors: print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: Bond verification report valid — status: {data['verification_status']}")

if __name__ == "__main__":
    main()
