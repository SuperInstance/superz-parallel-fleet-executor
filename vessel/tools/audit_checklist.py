#!/usr/bin/env python3
"""
Super Z Audit Checklist — Systematic code audit methodology.

Usage:
    python vessel/tools/audit_checklist.py run <file_or_dir>
    python vessel/tools/audit_checklist.py template

Generates a structured audit checklist for any code file or directory.
This is a PLANNING tool — it generates the checklist, the agent performs the audit.
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path


AUDIT_CATEGORIES = [
    {
        "name": "Static Analysis",
        "description": "Check for common coding errors without executing the code",
        "checks": [
            "Off-by-one errors in loop bounds and array indexing",
            "Missing bounds checks for array/buffer access",
            "Type confusion (implicit conversions, signed/unsigned mixing)",
            "Null/undefined dereferences",
            "Unused variables and dead code",
            "Incorrect operator precedence",
            "Missing error handling (try/catch, Result types, error codes)"
        ]
    },
    {
        "name": "Logic Verification",
        "description": "Trace execution paths for correctness against specification",
        "checks": [
            "Control flow matches specification",
            "State transitions are correct and complete",
            "Error paths return appropriate error values",
            "Edge cases are handled (empty input, max values, zero, negative)",
            "Recursion has valid base cases and terminates",
            "Conditional branches cover all cases"
        ]
    },
    {
        "name": "Security Review",
        "description": "Check for security vulnerabilities",
        "checks": [
            "All external input is validated and sanitized",
            "No sensitive data in logs, error messages, or debug output",
            "No hardcoded credentials or API keys",
            "SQL/command injection vectors are blocked",
            "Path traversal is prevented",
            "Authentication/authorization checks are present where needed",
            "Cryptographic operations use secure algorithms and parameters"
        ]
    },
    {
        "name": "Performance Review",
        "description": "Identify performance bottlenecks",
        "checks": [
            "Algorithm complexity is appropriate (no O(n^2) where O(n) suffices)",
            "No unnecessary memory allocations or copies",
            "No redundant computations in loops",
            "Data structures are appropriate for access patterns",
            "No blocking operations in hot paths",
            "Caching is used where appropriate",
            "Memory layout is cache-friendly"
        ]
    },
    {
        "name": "Documentation Review",
        "description": "Verify documentation matches implementation",
        "checks": [
            "Public APIs are documented",
            "Comments explain 'why', not just 'what'",
            "README is current and accurate",
            "Changelog reflects recent changes",
            "Error messages are descriptive and actionable",
            "Examples in docs actually work"
        ]
    },
    {
        "name": "Test Coverage",
        "description": "Assess test adequacy",
        "checks": [
            "Unit tests cover core logic paths",
            "Edge case tests exist for boundary conditions",
            "Error case tests exist for failure modes",
            "Integration tests cover component interactions",
            "Performance benchmarks exist for critical paths",
            "Test descriptions clearly state expected behavior"
        ]
    }
]


def generate_checklist(target):
    """Generate audit checklist for a target file/directory."""
    lines = []
    lines.append(f"# Audit Checklist: {target}")
    lines.append(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"Auditor: Super Z")
    lines.append("")

    # Target info
    target_path = Path(target)
    if target_path.exists():
        if target_path.is_file():
            size = target_path.stat().st_size
            lines.append(f"Target: {target} ({size} bytes)")
        elif target_path.is_dir():
            file_count = sum(1 for _ in target_path.rglob("*") if _.is_file())
            lines.append(f"Target: {target}/ ({file_count} files)")
    else:
        lines.append(f"Target: {target} (NOT FOUND)")
    lines.append("")

    # Findings section
    lines.append("## Findings")
    lines.append("")
    lines.append("### CRITICAL")
    lines.append("*(Issues that will cause data loss, security breach, or crash)*")
    lines.append("")
    lines.append("| # | File:Line | Description | Fix |")
    lines.append("|---|-----------|-------------|-----|")
    lines.append("|   |           |             |     |")
    lines.append("")

    lines.append("### MAJOR")
    lines.append("*(Issues that cause incorrect behavior or significant performance degradation)*")
    lines.append("")
    lines.append("| # | File:Line | Description | Fix |")
    lines.append("|---|-----------|-------------|-----|")
    lines.append("|   |           |             |     |")
    lines.append("")

    lines.append("### MINOR")
    lines.append("*(Issues that affect code quality, readability, or maintainability)*")
    lines.append("")
    lines.append("| # | File:Line | Description | Fix |")
    lines.append("|---|-----------|-------------|-----|")
    lines.append("|   |           |             |     |")
    lines.append("")

    # Checklist section
    lines.append("## Checklist")
    lines.append("")
    for cat in AUDIT_CATEGORIES:
        lines.append(f"### {cat['name']}")
        lines.append(f"*{cat['description']}*")
        lines.append("")
        for check in cat["checks"]:
            lines.append(f"- [ ] {check}")
        lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | CRITICAL | MAJOR | MINOR |")
    lines.append("|----------|----------|-------|-------|")
    lines.append("| Static Analysis    |    0    |   0   |   0   |")
    lines.append("| Logic Verification |    0    |   0   |   0   |")
    lines.append("| Security Review    |    0    |   0   |   0   |")
    lines.append("| Performance Review |    0    |   0   |   0   |")
    lines.append("| Documentation      |    0    |   0   |   0   |")
    lines.append("| Test Coverage      |    0    |   0   |   0   |")
    lines.append("| **TOTAL**          |  **0**  | **0** | **0** |")
    lines.append("")

    return "\n".join(lines)


def run(args):
    """Generate checklist for a target."""
    if len(args) < 2:
        print("Usage: audit_checklist.py run <file_or_directory>")
        return 1
    target = args[1]
    checklist = generate_checklist(target)
    print(checklist)
    return 0


def template(args):
    """Print the audit methodology template."""
    print("=== Super Z Audit Methodology ===")
    print()
    for cat in AUDIT_CATEGORIES:
        print(f"## {cat['name']}")
        print(f"{cat['description']}")
        print()
        for check in cat["checks"]:
            print(f"  - {check}")
        print()
    return 0


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    if not args or args[0] == "help":
        print("Super Z Audit Checklist v1.0.0")
        print()
        print("Commands:")
        print("  run <file_or_dir>  Generate audit checklist for target")
        print("  template           Print audit methodology")
        print("  help               Show this help")
        return 0

    if args[0] == "run":
        return run(args)
    elif args[0] == "template":
        return template(args)
    else:
        print(f"Unknown command: {args[0]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
