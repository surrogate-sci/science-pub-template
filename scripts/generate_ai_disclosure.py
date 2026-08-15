#!/usr/bin/env python3
"""Validate ai-use.yml and render its author-approved manuscript disclosure."""

import argparse
from pathlib import Path
from typing import Any

import yaml


class AIUseError(ValueError):
    """Raised when an AI-use disclosure is incomplete or malformed."""


def load_config(path: Path) -> dict[str, Any]:
    """Load an AI-use YAML mapping."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AIUseError("The disclosure must be a YAML mapping")
    if data.get("schema_version") != 1:
        raise AIUseError("schema_version must be 1")
    if data.get("status") not in {"draft", "complete"}:
        raise AIUseError("status must be draft or complete")
    if not isinstance(data.get("manuscript"), str) or not data["manuscript"].strip():
        raise AIUseError("manuscript must be a non-empty title or identifier")
    for group in ("first_authors", "last_authors", "other_authors"):
        if not isinstance(data.get(group), list):
            raise AIUseError(f"{group} must be a YAML list")
    return data


def author_name(entry: Any, group: str) -> str:
    """Return a non-empty author name from a group entry."""
    if not isinstance(entry, dict):
        raise AIUseError(f"Each {group} entry must be a YAML mapping")
    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        raise AIUseError(f"Each {group} entry must include a non-empty name")
    return name.strip()


def draft_reminder() -> str:
    """Return the visible reminder shown until the disclosure is complete."""
    return """:::{.callout-note title="AI usage disclosure" collapse="true"}
**AI usage disclosure incomplete.** Before submission or release, complete `ai-use.yml`. Every
first and last author must describe their exact AI usage, and every remaining author must read the
complete disclosure and confirm it in that file.
:::
"""


def render_complete(data: dict[str, Any]) -> str:
    """Validate a complete disclosure and preserve each required author's statement."""
    first = data["first_authors"]
    last = data["last_authors"]
    others = data["other_authors"]
    if not first:
        raise AIUseError("A complete disclosure requires at least one first author")
    if not last:
        raise AIUseError("A complete disclosure requires at least one last author")

    lines: list[str] = []
    names: list[str] = []
    for group, heading, entries in (
        ("first_authors", "First-author statements", first),
        ("last_authors", "Last-author statements", last),
    ):
        lines.append(f"**{heading}**")
        for entry in entries:
            name = author_name(entry, group)
            statement = entry.get("statement")
            if not isinstance(statement, str) or not statement.strip():
                raise AIUseError(f"{name} must provide an AI usage statement")
            names.append(name)
            lines.append(f"- {name}: {statement.strip()}")

    reviewers: list[str] = []
    for entry in others:
        name = author_name(entry, "other_authors")
        if entry.get("reviewed_full_disclosure") is not True:
            raise AIUseError(f"{name} must read the full disclosure and confirm review")
        names.append(name)
        reviewers.append(name)

    normalized = [name.casefold() for name in names]
    if len(normalized) != len(set(normalized)):
        raise AIUseError("The disclosure contains a duplicate author name")

    reviewer_text = ""
    if reviewers:
        reviewer_text = (
            "\n\nAll remaining authors read the complete disclosure: " + ", ".join(reviewers) + "."
        )
    return (
        ':::{.callout-note title="AI usage disclosure" collapse="true"}\n'
        + "\n".join(lines)
        + reviewer_text
        + "\n:::\n"
    )


def render_disclosure(data: dict[str, Any]) -> str:
    """Render either the draft reminder or a validated complete disclosure."""
    if data["status"] == "draft":
        return draft_reminder()
    return render_complete(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and render an AI usage disclosure.")
    parser.add_argument("config", type=Path, help="Path to ai-use.yml")
    parser.add_argument("output", type=Path, nargs="?", help="Generated Markdown path")
    parser.add_argument(
        "--check", action="store_true", help="Validate without writing generated Markdown"
    )
    args = parser.parse_args(argv)

    try:
        data = load_config(args.config)
        rendered = render_disclosure(data)
        if not args.check:
            if args.output is None:
                raise AIUseError("An output path is required unless --check is used")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        if data["status"] == "draft":
            print("AI usage disclosure is still draft; complete ai-use.yml before submission.")
    except (AIUseError, OSError, UnicodeError, yaml.YAMLError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
