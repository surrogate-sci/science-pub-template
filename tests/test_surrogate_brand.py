from pathlib import Path
import re


ROOT = Path(__file__).parents[1]
THEME = ROOT / "_extensions/Arcadia-Science/arcadia-pub-theme"
ALLOWED = {"#F5F0E2", "#235F66", "#F28A1C", "#FFB83E", "#30332F"}


def test_active_css_uses_only_approved_hex_palette():
    css = "\n".join(path.read_text() for path in (THEME / "css").rglob("*.css"))
    found = {value.upper() for value in re.findall(r"#[0-9a-fA-F]{3,8}\b", css)}
    assert found == ALLOWED
    assert not re.findall(r":\s*(?:white|black)\b", css, flags=re.IGNORECASE)


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
    assert "technical-notebook.css" in (
        ROOT / "_quarto-technical-notebook.yml"
    ).read_text()


def test_active_logo_is_transparent():
    logo = (THEME / "assets/logo_surrogate_mark.svg").read_text()
    assert "<rect" not in logo
