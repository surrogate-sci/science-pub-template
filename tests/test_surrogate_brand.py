import re
from pathlib import Path

ROOT = Path(__file__).parents[1]
THEME = ROOT / "_extensions/surrogate-sci/ss-pub-theme"
ALLOWED = {"#F5F0E2", "#235F66", "#F28A1C", "#FFB83E", "#30332F"}


def test_active_css_uses_only_approved_hex_palette():
    css = "\n".join(path.read_text() for path in (THEME / "css").rglob("*.css"))
    found = {value.upper() for value in re.findall(r"#[0-9a-fA-F]{3,8}\b", css)}
    assert found == ALLOWED
    assert not re.findall(r":\s*(?:white|black)\b", css, flags=re.IGNORECASE)


def test_syntax_highlighter_uses_only_approved_palette():
    syntax_theme = (THEME / "surrogate-light.theme").read_text()
    found = {value.upper() for value in re.findall(r"#[0-9a-fA-F]{3,8}\b", syntax_theme)}
    assert found <= ALLOWED


def test_typography_uses_approved_families():
    fonts = (THEME / "includes/fonts.html").read_text()
    main = (THEME / "css/main.css").read_text()
    for family in ("Cormorant Garamond", "Assistant", "Fira Sans", "Fira Mono"):
        assert family in fonts + main


def test_theme_profiles_are_mutually_exclusive_and_default_to_warm():
    base = (ROOT / "_quarto.yml").read_text()
    assert "default: warm-journal" in base
    assert "- [warm-journal, technical-notebook]" in base
    assert "warm-journal.css" in (ROOT / "_quarto-warm-journal.yml").read_text()
    assert "technical-notebook.css" in (ROOT / "_quarto-technical-notebook.yml").read_text()


def test_active_logo_is_transparent():
    logo = (THEME / "assets/logo_surrogate_mark.svg").read_text()
    assert "<rect" not in logo


def test_no_upstream_theme_updater_can_overwrite_custom_theme():
    active_automation = (ROOT / "Makefile").read_text()
    active_automation += "\n".join(
        path.read_text() for path in (ROOT / ".github/workflows").glob("*.yml")
    )
    assert "Arcadia-Science/notebook-pub-theme" not in active_automation


def test_surrogate_extension_uses_the_published_quarto_identifier():
    old_theme = ROOT / "_extensions/Arcadia-Science/arcadia-pub-theme"
    assert THEME.is_dir()
    assert not old_theme.exists()

    for config in (
        ROOT / "_quarto.yml",
        ROOT / "_quarto-warm-journal.yml",
        ROOT / "_quarto-technical-notebook.yml",
    ):
        contents = config.read_text()
        assert "surrogate-sci/ss-pub-theme-html" in contents
        assert "Arcadia-Science/arcadia-pub-theme-html" not in contents
        assert "_extensions/Arcadia-Science/arcadia-pub-theme" not in contents


def test_extension_metadata_and_csl_are_surrogate_science_branded_with_attribution():
    extension = (THEME / "_extension.yml").read_text()
    csl = (THEME / "assets/surrogate-science.csl").read_text()

    assert 'quarto-required: ">=1.8.25"' in extension
    assert "<title>Surrogate Science</title>" in csl
    assert "surrogate-science" in csl
    assert "Feridun Mert Celebi" in csl
    assert "Megan Hochstrasser" in csl
    assert "Creative Commons Attribution-ShareAlike 3.0" in csl


def test_active_theme_uses_only_surrogate_css_custom_properties():
    css = "\n".join(path.read_text() for path in (THEME / "css").rglob("*.css"))
    assert "--arcadia-" not in css
    assert "--surrogate-" in css


def test_template_metadata_uses_reusable_surrogate_placeholders():
    variables = (ROOT / "_variables.yml").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    license_text = (ROOT / "LICENSE").read_text()

    assert 'org: "surrogate-sci"' in variables
    assert 'repo: "science-pub-template"' in variables
    assert "Surrogate Science Publication Template" in citation
    assert "[AUTHOR" in citation
    assert "doi:" not in citation.lower()
    assert "repository-code: https://github.com/surrogate-sci/[REPOSITORY-NAME]" in citation
    assert "science-pub-template" not in citation
    assert "Copyright (c) 2024 Arcadia Science" in license_text
    assert "Copyright (c) 2026 Surrogate Science" in license_text


def test_active_documentation_has_no_arcadia_operations_or_urls():
    active_paths = [
        ROOT / "README.md",
        ROOT / "CITATION.cff",
        ROOT / "_quarto.yml",
        ROOT / "_quarto-warm-journal.yml",
        ROOT / "_quarto-technical-notebook.yml",
        ROOT / "_variables.yml",
        ROOT / "examples/demo.bib",
        *(ROOT / "developer-docs").glob("*.md"),
        *(ROOT / "pages").glob("*.qmd"),
    ]
    active_docs = "\n".join(path.read_text() for path in active_paths)

    assert "arcadia" not in active_docs.lower()
    assert "https://surrogate-sci.dev/" in active_docs


def test_cookie_banner_controls_use_brand_tokens():
    main = (THEME / "css/main.css").read_text()
    assert ".cc-nb-okagree" in main
    assert ".cc-nb-changep" in main
    assert "var(--surrogate-teal)" in main
    assert "var(--surrogate-paper)" in main


def test_note_callout_icon_does_not_use_bootstrap_blue():
    article = (THEME / "css/article.css").read_text()
    assert ".callout-note .callout-icon" in article
    pseudo = re.search(
        r"\.callout-note \.callout-icon::before\s*\{(?P<body>[^}]*)\}",
        article,
        flags=re.DOTALL,
    )
    assert pseudo
    assert "background-image: none" in pseudo.group("body")
    assert "var(--surrogate-teal)" in article


def test_citation_box_omits_missing_cff_year_and_doi_without_undefined_values():
    citation = (ROOT / "CITATION.cff").read_text()
    citation_box = (THEME / "includes/citation-box.html").read_text()

    assert "year:" not in citation
    assert "doi:" not in citation.lower()
    assert "String(year)" not in citation_box
    assert "String(doi)" not in citation_box
    assert "const valueOrEmpty" in citation_box
    assert "pubData.year ?" in citation_box
    assert "pubData.doi ?" in citation_box
    assert "...(pubData.doi ? [`doi = {${pubData.doi}}`] : [])" in citation_box
    assert "valueOrEmpty(cffData['repository-code'])" in citation_box


def test_includes_resolve_project_resources_from_quarto_offset_and_base_uri():
    for include_name in ("citation-box.html", "author-reveal.html", "mini-title.html"):
        include = (THEME / "includes" / include_name).read_text()

        assert 'meta[name="quarto:offset"]' in include
        assert "document.baseURI" in include
        assert "github.io" not in include
        assert "window.location.hostname" not in include


def test_active_template_uses_the_canonical_science_pub_template_name():
    active_paths = [
        ROOT / "pyproject.toml",
        ROOT / "uv.lock",
        *(ROOT / "developer-docs").glob("*.md"),
        ROOT / "index.ipynb",
        ROOT / "examples/demo.ipynb",
    ]
    active_text = "\n".join(path.read_text() for path in active_paths)

    assert "notebook-pub-template" not in active_text
    assert 'name = "science-pub-template"' in (ROOT / "pyproject.toml").read_text()


def test_documented_environment_installs_make_test_dependencies():
    environment = (ROOT / "env.yml").read_text()

    assert re.search(r"^\s*- pytest(?:[=<>]|$)", environment, flags=re.MULTILINE)


def test_quickstart_does_not_copy_development_branches():
    quickstart = (ROOT / "developer-docs/QUICKSTART.md").read_text()

    assert "check the box" not in quickstart
    assert "Leave *Include all branches* unchecked" in quickstart


def test_public_template_excludes_internal_agent_artifacts():
    ignored = (ROOT / ".gitignore").read_text()

    assert not (ROOT / "docs/superpowers").exists()
    for rule in (
        "/.codex/",
        "/.agents/",
        "/.claude/",
        "/.superpowers/",
        "/docs/superpowers/",
        "/session-notes/",
    ):
        assert rule in ignored
