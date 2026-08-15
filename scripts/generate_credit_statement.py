#!/usr/bin/env python3
"""Generate an author-ordered CRediT statement from a GitHub issue body."""

import argparse
import re
import sys
from pathlib import Path

ROSTER_HEADING = "Ordered author roster"
APPROVAL_HEADING = "Author approval confirmation"
ROLES = (
    "Conceptualization",
    "Data curation",
    "Formal analysis",
    "Funding acquisition",
    "Investigation",
    "Methodology",
    "Project administration",
    "Resources",
    "Software",
    "Supervision",
    "Validation",
    "Visualization",
    "Writing – original draft",
    "Writing – review & editing",
)
SECTION_HEADING = re.compile(r"^###\s+(.+?)\s*$")
CHECKED_BOX = re.compile(r"^-\s*\[[xX]]\s+All authors reviewed and approved\b")


class CreditStatementError(ValueError):
    """Raised when an issue body cannot produce a valid statement."""


def parse_sections(body: str) -> dict[str, list[str]]:
    """Return third-level Markdown sections keyed by heading text."""
    sections: dict[str, list[str]] = {}
    current_heading: str | None = None

    for line in body.splitlines():
        heading = SECTION_HEADING.match(line)
        if heading:
            current_heading = heading.group(1)
            if current_heading in sections:
                raise CreditStatementError(f"Duplicate section heading: {current_heading}")
            sections[current_heading] = []
        elif current_heading is not None:
            sections[current_heading].append(line.strip())

    return sections


def content_lines(sections: dict[str, list[str]], heading: str) -> list[str]:
    """Return nonblank lines from a required section."""
    if heading not in sections:
        raise CreditStatementError(f"Missing required section: {heading}")
    return [line for line in sections[heading] if line]


def generate_statement(body: str) -> str:
    """Validate and invert a role-to-authors issue body into a CRediT statement."""
    sections = parse_sections(body)
    roster = content_lines(sections, ROSTER_HEADING)
    if not roster:
        raise CreditStatementError("The ordered author roster is empty")
    if len(roster) != len(set(roster)):
        raise CreditStatementError("The ordered author roster contains duplicate names")

    approval = content_lines(sections, APPROVAL_HEADING)
    if not any(CHECKED_BOX.match(line) for line in approval):
        raise CreditStatementError("All authors must review and approve the contribution statement")

    contributions = {author: [] for author in roster}
    roster_names = set(roster)
    for role in ROLES:
        assigned = content_lines(sections, role)
        if not assigned:
            raise CreditStatementError(
                f"{role} must contain one or more roster authors or exactly N/A"
            )
        if len(assigned) == 1 and assigned[0].casefold() == "n/a":
            continue
        for author in assigned:
            if author not in roster_names:
                raise CreditStatementError(
                    f"Assigned author {author!r} is not in the ordered author roster"
                )
            if role not in contributions[author]:
                contributions[author].append(role)

    statements = [
        f"{author}: {', '.join(contributions[author])}"
        for author in roster
        if contributions[author]
    ]
    if not statements:
        raise CreditStatementError("No CRediT role assignments were provided")
    return "; ".join(statements)


def read_body(path: str) -> str:
    """Read an issue body from a file path or standard input."""
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate an author-ordered CRediT contribution statement."
    )
    parser.add_argument("issue_body", help="Exported GitHub issue Markdown file, or - for stdin")
    args = parser.parse_args(argv)

    try:
        print(generate_statement(read_body(args.issue_body)))
    except (CreditStatementError, OSError, UnicodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
