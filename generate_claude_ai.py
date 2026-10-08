#!/usr/bin/env python3
"""Generate pasteable claude.ai instructions from the maintained local files.

Run: python3 generate_claude_ai.py
Check freshness without writing: python3 generate_claude_ai.py --check

Paths default to this script's directory, regardless of the working directory.
Edit AGENTS.md and skills/grimoire/SKILL.md, not the generated chat_AGENTS.md.
When adding or renaming a main-file section, update SECTION_POLICY below.
Only Python's standard library is required.
"""

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SECTION_POLICY = {
    "On-demand instructions": False,
    "Conversation": True,
    "Fictional stories": True,
    "Files and documents": True,
    "Scope and filesystem": False,
    "No host or system introspection": False,
    "Subagents, workflows, background agents": False,
    "Browsers and other processes": False,
    "Transparency and confirmation": True,
    "Em dashes": True,
    "Verify by behaviour, not by state": True,
    "Emphasis around inline math": True,
}


def headings(text):
    """Yield ATX headings outside fenced code, including their line indexes."""
    fence = None
    for index, line in enumerate(text.splitlines(keepends=True)):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if marker:
            run, rest = marker.groups()
            if fence is None:
                if run[0] != "`" or "`" not in rest:
                    fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not rest.strip():
                fence = None
            continue
        if fence is None:
            match = re.match(r"^(#{1,6})[ \t]+(.+?)\s*$", line)
            if match:
                title = re.sub(r"[ \t]+#+[ \t]*$", "", match[2])
                yield index, len(match[1]), title
    if fence is not None:
        raise ValueError("Unclosed Markdown code fence")


def chat_sections(main):
    lines = main.splitlines(keepends=True)
    structure = list(headings(main))
    titles = [(index, title) for index, level, title in structure if level == 1]
    if len(titles) != 1 or titles[0][0] != 0:
        raise ValueError("Main file must begin with exactly one level-one title")
    sections = [(index, title) for index, level, title in structure if level == 2]
    seen = set()
    for _, title in sections:
        if title in seen:
            raise ValueError(f"Duplicate section: {title}")
        seen.add(title)
    unknown = seen - SECTION_POLICY.keys()
    missing = SECTION_POLICY.keys() - seen
    if unknown or missing:
        raise ValueError(
            "Review SECTION_POLICY before generating. "
            f"Unclassified sections: {sorted(unknown)}; missing sections: {sorted(missing)}"
        )
    if "".join(lines[1:sections[0][0]]).strip():
        raise ValueError("Move main-file introductory text into a classified section")
    chunks = [lines[0].strip()]
    for position, (start, title) in enumerate(sections):
        end = sections[position + 1][0] if position + 1 < len(sections) else len(lines)
        if SECTION_POLICY[title]:
            chunks.append("".join(lines[start:end]).strip())
    return "\n\n".join(chunks)


def embedded_skill(skill):
    lines = skill.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("Grimoire skill must begin with YAML frontmatter")
    closing = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if closing is None:
        raise ValueError("Grimoire skill has unclosed YAML frontmatter")
    body = "".join(lines[closing + 1:]).strip()
    structure = list(headings(body))
    if not structure or structure[0][:2] != (0, 1):
        raise ValueError("Grimoire skill body must begin with a level-one title")
    if sum(level == 1 for _, level, _ in structure) != 1:
        raise ValueError("Grimoire skill must contain exactly one level-one title")
    body_lines = body.splitlines(keepends=True)
    for index, level, _ in structure:
        if level == 6:
            raise ValueError("Cannot nest a level-six Grimoire heading")
        body_lines[index] = "#" + body_lines[index]
    return "".join(body_lines)


def render(main, skill):
    return chat_sections(main) + "\n\n" + embedded_skill(skill) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=ROOT / "AGENTS.md")
    parser.add_argument("--grimoire", type=Path, default=ROOT / "skills/grimoire/SKILL.md")
    parser.add_argument("--output", type=Path, default=ROOT / "chat_AGENTS.md")
    parser.add_argument("--check", action="store_true", help="Exit nonzero if the output is missing or stale; do not write")
    args = parser.parse_args()
    try:
        if args.output.is_symlink():
            raise ValueError("Output must be a regular file, not a symlink")
        if args.output.resolve() in {args.source.resolve(), args.grimoire.resolve()}:
            raise ValueError("Output must not overwrite a source file")
        result = render(args.source.read_text(encoding="utf-8"), args.grimoire.read_text(encoding="utf-8"))
        if args.check:
            if not args.output.is_file() or args.output.read_bytes() != result.encode("utf-8"):
                print(f"Missing or stale: {args.output}", file=sys.stderr)
                return 1
            print(f"Up to date: {args.output}")
        else:
            args.output.write_text(result, encoding="utf-8")
            print(f"Generated {args.output} ({len(result):,} characters)")
    except (OSError, ValueError) as error:
        print(f"Cannot generate chat instructions: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
