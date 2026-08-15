import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
CONFIG = ROOT / "ai-use.yml"
GENERATOR = ROOT / "scripts/generate_ai_disclosure.py"
OUTPUT = ROOT / "disclosures/ai-use.md"
WORKFLOW = ROOT / ".github/workflows/validate-ai-use.yml"
DOCS = ROOT / "developer-docs/AI_USAGE.md"


def disclosure_config(*, status: str = "complete") -> str:
    return f"""schema_version: 1
status: {status}
manuscript: Analytical Engine Notes
first_authors:
  - name: Ada Lovelace
    statement: Used an AI assistant for editorial feedback and grammar review.
last_authors:
  - name: Grace Hopper
    statement: Used an AI assistant to check code for mistakes.
other_authors:
  - name: Katherine Johnson
    reviewed_full_disclosure: true
"""


def run_generator(tmp_path: Path, config: str, *args: str) -> subprocess.CompletedProcess[str]:
    config_path = tmp_path / "ai-use.yml"
    output_path = tmp_path / "ai-use.md"
    config_path.write_text(config)
    return subprocess.run(
        [sys.executable, str(GENERATOR), str(config_path), str(output_path), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_generator_preserves_required_author_statements_and_records_reviewers(tmp_path):
    result = run_generator(tmp_path, disclosure_config())
    output = (tmp_path / "ai-use.md").read_text()

    assert result.returncode == 0, result.stderr
    assert "Ada Lovelace: Used an AI assistant for editorial feedback and grammar review." in output
    assert "Grace Hopper: Used an AI assistant to check code for mistakes." in output
    assert "Katherine Johnson" in output
    assert output.index("Ada Lovelace") < output.index("Grace Hopper")


def test_complete_disclosure_requires_each_first_and_last_author_statement(tmp_path):
    config = disclosure_config().replace(
        "    statement: Used an AI assistant to check code for mistakes.\n", "    statement: ''\n"
    )
    result = run_generator(tmp_path, config)

    assert result.returncode == 2
    assert "Grace Hopper" in result.stderr
    assert "statement" in result.stderr


def test_complete_disclosure_requires_other_authors_to_confirm_review(tmp_path):
    config = disclosure_config().replace(
        "reviewed_full_disclosure: true", "reviewed_full_disclosure: false"
    )
    result = run_generator(tmp_path, config)

    assert result.returncode == 2
    assert "Katherine Johnson" in result.stderr
    assert "read the full disclosure" in result.stderr


def test_disclosure_rejects_duplicate_author_names_across_groups(tmp_path):
    config = disclosure_config().replace("Katherine Johnson", "Ada Lovelace")
    result = run_generator(tmp_path, config)

    assert result.returncode == 2
    assert "duplicate author" in result.stderr.lower()


def test_draft_config_generates_a_visible_author_reminder(tmp_path):
    result = run_generator(tmp_path, disclosure_config(status="draft"))
    output = (tmp_path / "ai-use.md").read_text()

    assert result.returncode == 0, result.stderr
    assert "AI usage disclosure incomplete" in output
    assert "ai-use.yml" in output
    assert ':::{.callout-note title="AI usage disclosure" collapse="true"}' in output
    assert "callout-warning" not in output


def test_repository_provides_documented_config_and_validation_only_action():
    config = yaml.safe_load(CONFIG.read_text())
    docs = DOCS.read_text()
    workflow = WORKFLOW.read_text()
    notebook = (ROOT / "index.ipynb").read_text()
    frozen = (ROOT / "_freeze/index/execute-results/html.json").read_text()

    assert config["schema_version"] == 1
    assert config["status"] == "draft"
    assert "editorial feedback" in docs
    assert "checking for mistakes" in docs
    assert "grammar" in docs
    assert "first author" in docs.lower()
    assert "last author" in docs.lower()
    assert "read the complete disclosure" in docs.lower()
    assert "generate_ai_disclosure.py" in workflow
    for forbidden in ("git commit", "git push", "gh pr", "issues: write", "pull-requests: write"):
        assert forbidden not in workflow
    assert "Airtable" not in notebook
    assert "SlackBot" not in notebook
    assert "Airtable" not in frozen
    assert "SlackBot" not in frozen
    assert "disclosures/ai-use.md" in notebook
    assert OUTPUT.exists()
