import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
GENERATOR = ROOT / "scripts/generate_credit_statement.py"
ISSUE_FORM = ROOT / ".github/ISSUE_TEMPLATE/credit-contributions.yml"
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


def issue_body(*, approval: bool = True, methodology: str = "Grace Hopper\nAda Lovelace") -> str:
    assignments = {role: "N/A" for role in ROLES}
    assignments.update(
        {
            "Conceptualization": "Ada Lovelace",
            "Methodology": methodology,
            "Software": "Ada Lovelace",
            "Supervision": "Grace Hopper",
            "Writing – original draft": "Ada Lovelace",
            "Writing – review & editing": "Grace Hopper",
        }
    )
    role_sections = "\n\n".join(f"### {role}\n\n{assignments[role]}" for role in ROLES)
    checked = "x" if approval else " "
    return f"""### Manuscript identifier or title

Analytical Engine Notes

### Ordered author roster

Ada Lovelace
Grace Hopper

{role_sections}

### Author approval confirmation

- [{checked}] All authors reviewed and approved the contribution statement.
"""


def run_generator(tmp_path: Path, body: str) -> subprocess.CompletedProcess[str]:
    body_path = tmp_path / "issue.md"
    body_path.write_text(body)
    return subprocess.run(
        [sys.executable, str(GENERATOR), str(body_path)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_generator_inverts_assignments_in_roster_and_official_role_order(tmp_path):
    result = run_generator(tmp_path, issue_body())

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == (
        "Ada Lovelace: Conceptualization, Methodology, Software, "
        "Writing – original draft; "
        "Grace Hopper: Methodology, Supervision, Writing – review & editing"
    )


def test_generator_rejects_an_assigned_name_not_in_the_roster(tmp_path):
    result = run_generator(tmp_path, issue_body(methodology="Katherine Johnson"))

    assert result.returncode == 2
    assert "Katherine Johnson" in result.stderr
    assert "not in the ordered author roster" in result.stderr


def test_generator_requires_explicit_author_approval(tmp_path):
    result = run_generator(tmp_path, issue_body(approval=False))

    assert result.returncode == 2
    assert "All authors must review and approve" in result.stderr


def test_credit_issue_form_collects_all_required_information():
    form = ISSUE_FORM.read_text()

    assert "Manuscript identifier or title" in form
    assert "Ordered author roster" in form
    assert "one author per line" in form.lower()
    for role in ROLES:
        assert role in form
    assert "All authors reviewed and approved" in form
