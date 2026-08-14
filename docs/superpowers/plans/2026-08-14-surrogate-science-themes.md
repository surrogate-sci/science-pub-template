# Surrogate Science Themes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the draft PR's placeholder blue/gray branding with the approved Surrogate Science logo, five-color palette, and two separately selectable Quarto blog themes.

**Architecture:** Keep the existing Arcadia-derived Quarto format as the shared structural base. Define one canonical Surrogate token layer and typography layer, then use a mutually exclusive Quarto profile group to load either `warm-journal.css` or `technical-notebook.css`; `warm-journal` is the default. Static contract tests prevent palette drift, font drift, broken profile wiring, and background-bearing logo assets.

**Tech Stack:** Quarto profiles and custom HTML format, CSS custom properties, Google Fonts, pytest, GitHub Pages.

---

### Task 1: Add the visual contract tests

**Files:**
- Create: `tests/test_surrogate_brand.py`

- [ ] **Step 1: Write tests that encode the approved design**

```python
from pathlib import Path
import re

ROOT = Path(__file__).parents[1]
THEME = ROOT / "_extensions/Arcadia-Science/arcadia-pub-theme"
ALLOWED = {"#F5F0E2", "#235F66", "#F28A1C", "#FFB83E", "#30332F"}


def test_active_css_uses_only_approved_hex_palette():
    css = "\n".join(path.read_text() for path in (THEME / "css").rglob("*.css"))
    found = {value.upper() for value in re.findall(r"#[0-9a-fA-F]{6}", css)}
    assert found == ALLOWED


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
```

- [ ] **Step 2: Run the tests and verify the expected failures**

Run: `uv run --with pytest pytest tests/test_surrogate_brand.py -q`

Expected: FAIL because the current CSS contains unapproved blue/gray/white values, the approved fonts and profile files are missing, and the official transparent mark is not wired in.

- [ ] **Step 3: Commit the test contract**

```bash
git add tests/test_surrogate_brand.py
git commit -m "test: define Surrogate Science visual contract"
```

### Task 2: Install the official mark and canonical palette

**Files:**
- Create: `_extensions/Arcadia-Science/arcadia-pub-theme/assets/logo_surrogate_mark.svg`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/colors.css`
- Modify: `_quarto.yml`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/includes/mini-title.html`
- Delete: `_extensions/Arcadia-Science/arcadia-pub-theme/assets/logo_text_surrogate.svg`
- Delete: `_extensions/Arcadia-Science/arcadia-pub-theme/assets/logo_white_surrogate.svg`

- [ ] **Step 1: Copy the supplied transparent SVG mark into the extension assets**

Use `logo-surrogate-science-mark.svg` from `Surrogate Science Design-08-2026.zip` without adding a background rectangle.

- [ ] **Step 2: Replace `colors.css` with the five canonical tokens and legacy aliases**

```css
:root {
  --surrogate-paper: #F5F0E2;
  --surrogate-teal: #235F66;
  --surrogate-orange: #F28A1C;
  --surrogate-amber: #FFB83E;
  --surrogate-charcoal: #30332F;

  --arcadia-body-color: var(--surrogate-charcoal);
  --arcadia-label-color: var(--surrogate-teal);
  --arcadia-muted-color: color-mix(in srgb, var(--surrogate-charcoal) 68%, transparent);
  --arcadia-link-color: var(--surrogate-teal);
  --arcadia-black: var(--surrogate-charcoal);
  --arcadia-white: var(--surrogate-paper);
  --arcadia-charcoal: var(--surrogate-charcoal);
  --arcadia-paper: var(--surrogate-paper);
  --arcadia-dusk: var(--surrogate-teal);
  --arcadia-lapis: var(--surrogate-teal);
  --arcadia-mustard: var(--surrogate-amber);
  --arcadia-dragon: var(--surrogate-orange);
  --arcadia-teal: var(--surrogate-teal);
  --arcadia-tumbleweed: var(--surrogate-orange);
  --arcadia-pewter: var(--surrogate-teal);
}
```

- [ ] **Step 3: Point Quarto, footer, and mini-title at the transparent mark**

Use `logo_surrogate_mark.svg`, set the navbar background to `#F5F0E2`, set the footer background to `#30332F`, and retain `https://github.com/surrogate-sci` as the brand destination.

- [ ] **Step 4: Remove the two generated placeholder logo files**

Run: `git rm _extensions/Arcadia-Science/arcadia-pub-theme/assets/logo_text_surrogate.svg _extensions/Arcadia-Science/arcadia-pub-theme/assets/logo_white_surrogate.svg`

### Task 3: Add approved typography and separate A/B profiles

**Files:**
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/includes/fonts.html`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/main.css`
- Create: `_extensions/Arcadia-Science/arcadia-pub-theme/css/themes/warm-journal.css`
- Create: `_extensions/Arcadia-Science/arcadia-pub-theme/css/themes/technical-notebook.css`
- Create: `_quarto-warm-journal.yml`
- Create: `_quarto-technical-notebook.yml`
- Modify: `_quarto.yml`

- [ ] **Step 1: Load only the approved type families**

Load `Cormorant Garamond`, `Assistant`, `Fira Sans`, and `Fira Mono` from Google Fonts. Map the shared variables as follows:

```css
--nb-font-serif: "Cormorant Garamond", Georgia, serif;
--nb-font-sans: "Assistant", ui-sans-serif, system-ui, sans-serif;
--nb-font-label: "Fira Sans", ui-sans-serif, system-ui, sans-serif;
--nb-font-mono: "Fira Mono", ui-monospace, monospace;
```

- [ ] **Step 2: Create Theme A as a Paper-dominant editorial treatment**

Use Cormorant Garamond Semibold for the publication title, Fira Sans for uppercase metadata, Charcoal body text, teal structural accents, orange emphasis, and amber highlights.

- [ ] **Step 3: Create Theme B as a technical treatment without darkening the article body**

Use Assistant Semibold for the publication title, Fira Sans/Mono for metadata and code, a teal masthead with Paper text and Paper logo tile, and a Paper article background.

- [ ] **Step 4: Wire the themes through mutually exclusive Quarto profiles**

```yaml
# _quarto.yml
profile:
  default: warm-journal
  group:
    - [warm-journal, technical-notebook]
```

```yaml
# _quarto-warm-journal.yml
format:
  Arcadia-Science/arcadia-pub-theme-html:
    css: _extensions/Arcadia-Science/arcadia-pub-theme/css/themes/warm-journal.css
```

```yaml
# _quarto-technical-notebook.yml
format:
  Arcadia-Science/arcadia-pub-theme-html:
    css: _extensions/Arcadia-Science/arcadia-pub-theme/css/themes/technical-notebook.css
```

### Task 4: Remove off-palette literals from active CSS

**Files:**
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/main.css`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/navbar.css`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/mini-title.css`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/frontmatter.css`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/citation-box.css`
- Modify: `_extensions/Arcadia-Science/arcadia-pub-theme/css/footer.css`

- [ ] **Step 1: Replace literal white, gray, blue, and black values with canonical variables**

Use the five tokens directly or alpha/color-mix derivatives of those tokens. Do not introduce a sixth named or hex color.

- [ ] **Step 2: Run the visual contract tests**

Run: `uv run --with pytest pytest tests/test_surrogate_brand.py -q`

Expected: PASS.

### Task 5: Document theme selection for local authors and CI

**Files:**
- Modify: `README.md`
- Modify: `developer-docs/QUICKSTART.md`
- Modify: `Makefile`

- [ ] **Step 1: Add explicit preview and render commands**

```make
preview-warm:
	quarto preview --profile warm-journal

preview-technical:
	quarto preview --profile technical-notebook

render-warm:
	quarto render --profile warm-journal

render-technical:
	quarto render --profile technical-notebook
```

- [ ] **Step 2: Explain that Warm Journal is the default and Technical Notebook is opt-in**

Document the four commands above and `QUARTO_PROFILE=technical-notebook` for GitHub Actions or other hosts.

### Task 6: Render and visually verify both themes

**Files:**
- No tracked file changes expected.

- [ ] **Step 1: Render Theme A with Quarto 1.10.18**

Run: `quarto render --profile warm-journal`

Expected: successful render to `_site/` with no missing asset errors.

- [ ] **Step 2: Render Theme B with Quarto 1.10.18**

Run: `quarto render --profile technical-notebook`

Expected: successful render to `_site/` with no missing asset errors.

- [ ] **Step 3: Inspect both rendered home pages in a browser**

Verify the transparent logo, Paper page background, title family/weight, navbar treatment, code styling, responsive layout, and absence of blue/mint/white drift.

- [ ] **Step 4: Run the complete local checks**

Run: `uv run --with pytest pytest -q && git diff --check`

Expected: all tests pass and `git diff --check` produces no output.

- [ ] **Step 5: Commit, push, and update draft PR #1**

```bash
git add .
git commit -m "feat: add approved Surrogate Science publication themes"
git push origin copilot/remove-arcadia-logos
```
