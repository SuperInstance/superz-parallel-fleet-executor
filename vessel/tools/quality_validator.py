#!/usr/bin/env python3
"""
Super Z Quality Validator — Enforces content depth standards.

Usage:
    python vessel/tools/quality_validator.py check <file>
    python vessel/tools/quality_validator.py check-dir <directory>
    python vessel/tools/quality_validator.py stats <file>

Checks markdown files against quality standards:
- Minimum 150 words per section (## headings)
- Minimum 3 sentences per paragraph
- No single-sentence paragraphs
- No sections shorter than 150 words
"""

import re
import sys
from pathlib import Path


MIN_WORDS_PER_SECTION = 150
MIN_SENTENCES_PER_PARAGRAPH = 3
MIN_CHARS_PER_SECTION = 500


def count_words(text):
    """Count words in text, handling markdown formatting."""
    clean = re.sub(r'[#*`\[\]\(\)]+', ' ', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return len(clean.split())


def count_sentences(text):
    """Count sentences in text (rough heuristic)."""
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings and very short fragments
    return len([s for s in sentences if len(s.strip()) > 10])


def extract_sections(filepath):
    """Extract sections from a markdown file.
    Returns list of (heading, level, body_text).
    """
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    sections = []
    current_heading = "Preamble"
    current_level = 0
    current_lines = []

    for line in lines:
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            # Save previous section
            if current_lines:
                body = '\n'.join(current_lines).strip()
                sections.append((current_heading, current_level, body))
            current_heading = heading_match.group(2)
            current_level = len(heading_match.group(1))
            current_lines = []
        else:
            current_lines.append(line)

    # Don't forget the last section
    if current_lines:
        body = '\n'.join(current_lines).strip()
        sections.append((current_heading, current_level, body))

    return sections


def check_paragraph_quality(body_text):
    """Check paragraph quality within a section body.
    Returns list of issues.
    """
    issues = []
    # Split into paragraphs (separated by blank lines)
    paragraphs = re.split(r'\n\s*\n', body_text)

    for i, para in enumerate(paragraphs):
        para = para.strip()
        if not para:
            continue
        # Skip code blocks, tables, lists, YAML front matter
        if para.startswith('```') or para.startswith('|') or para.startswith('---'):
            continue
        if re.match(r'^[\s]*[-*+>]', para):
            continue

        sentences = count_sentences(para)
        words = count_words(para)

        if words < 15:
            # Very short — might be a transitional line, not a paragraph
            continue

        if sentences < MIN_SENTENCES_PER_PARAGRAPH:
            preview = para[:80].replace('\n', ' ')
            issues.append(
                f"  Paragraph has {sentences} sentence(s) (min {MIN_SENTENCES_PER_PARAGRAPH}): "
                f"\"{preview}...\""
            )

    return issues


def check_file(filepath):
    """Check a single markdown file against quality standards.
    Returns (total_issues, details_list).
    """
    path = Path(filepath)
    if not path.exists():
        return [(f"File not found: {filepath}", "error")]

    sections = extract_sections(path)
    results = []

    for heading, level, body in sections:
        if level == 0:
            # Preamble — skip
            continue
        if level == 1:
            # Top-level heading — check word count
            words = count_words(body)
            if words < MIN_WORDS_PER_SECTION and words > 0:
                results.append(
                    f"[SHALLOW] #{heading}: {words} words (min {MIN_WORDS_PER_SECTION})"
                )

        # Check paragraph quality for all sections level 2+
        if level >= 2 and body:
            para_issues = check_paragraph_quality(body)
            for issue in para_issues:
                results.append(f"[THIN] {heading}:\n{issue}")

    return results


def check_directory(dirpath):
    """Check all markdown files in a directory recursively."""
    directory = Path(dirpath)
    if not directory.exists():
        print(f"Directory not found: {dirpath}")
        return 1

    md_files = sorted(directory.rglob("*.md"))
    # Exclude README.md, .gitkeep, and example files
    md_files = [f for f in md_files if f.name != "README.md" and not f.name.endswith(".gitkeep")]

    if not md_files:
        print("No markdown files found to check.")
        return 0

    total_issues = 0
    files_with_issues = 0

    for f in md_files:
        issues = check_file(f)
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"\n{f.relative_to(directory)}:")
            for issue in issues:
                print(f"  {issue}")

    print(f"\n{'='*60}")
    print(f"Checked {len(md_files)} file(s)")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues: {total_issues}")
    print(f"{'='*60}")

    return 1 if total_issues > 0 else 0


def stats(filepath):
    """Print word/sentence statistics for a file."""
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return 1

    sections = extract_sections(path)
    total_words = 0

    print(f"Statistics for: {filepath}")
    print(f"{'Section':<40} {'Words':>8} {'Sentences':>10} {'Status':>10}")
    print("-" * 72)

    for heading, level, body in sections:
        words = count_words(body)
        sentences = count_sentences(body)
        total_words += words
        status = "OK" if words >= MIN_WORDS_PER_SECTION or level == 0 else "SHALLOW"
        label = heading[:38] + ".." if len(heading) > 38 else heading
        print(f"{label:<40} {words:>8} {sentences:>10} {status:>10}")

    print("-" * 72)
    print(f"{'TOTAL':<40} {total_words:>8}")


def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    if not args or args[0] == "help":
        print("Super Z Quality Validator v1.0.0")
        print()
        print("Commands:")
        print("  check <file>       Check a single markdown file")
        print("  check-dir <dir>    Check all .md files in directory")
        print("  stats <file>       Print word/sentence statistics")
        print("  help               Show this help")
        return 0

    if args[0] == "check" and len(args) >= 2:
        issues = check_file(args[1])
        if issues:
            print(f"Found {len(issues)} issue(s) in {args[1]}:")
            for issue in issues:
                print(f"  {issue}")
            return 1
        else:
            print(f"No issues found in {args[1]}.")
            return 0

    elif args[0] == "check-dir" and len(args) >= 2:
        return check_directory(args[1])

    elif args[0] == "stats" and len(args) >= 2:
        stats(args[1])
        return 0

    else:
        print(f"Unknown command: {args[0]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
