# Surrogate Science Extension Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the fork a complete Surrogate Science publication template without deleting required upstream attribution.

**Architecture:** Rename the vendored Quarto extension and all active references as one atomic change. Replace Arcadia-specific template metadata and operational documentation with reusable Surrogate Science placeholders, while retaining the Arcadia MIT copyright notice and CSL author/license metadata required for attribution.

**Tech Stack:** Quarto YAML, CSS, CSL XML, Citation File Format YAML, Markdown, pytest.

---

### Task 1: Rename and complete the Surrogate Science template

**Files:**
- Move: `_extensions/Arcadia-Science/arcadia-pub-theme/` to `_extensions/surrogate-sci/ss-pub-theme/`
- Modify: `_quarto.yml`, `_quarto-warm-journal.yml`, `_quarto-technical-notebook.yml`, `_variables.yml`
- Modify: `CITATION.cff`, `LICENSE`, `README.md`, `developer-docs/*.md`, `pages/*.qmd`
- Modify: `_extensions/surrogate-sci/ss-pub-theme/**/*`
- Test: `tests/test_surrogate_brand.py`

- [ ] **Step 1: Write failing contract tests**

Add tests requiring the new extension path and format identifier, reusable Surrogate Science citation placeholders without a fake DOI, Surrogate Science template variables and URLs, and no active Arcadia references outside attribution-bearing files and historical implementation plans.

- [ ] **Step 2: Verify the contract fails**

Run: `uvx pytest -q`

Expected: failure because the extension still lives under `Arcadia-Science/arcadia-pub-theme` and template metadata/docs still contain Arcadia-specific values.

- [ ] **Step 3: Apply the atomic rename and replacements**

Use `_extensions/surrogate-sci/ss-pub-theme` and the Quarto format key `surrogate-sci/ss-pub-theme-html`. Use Surrogate Science names and `surrogate-sci` GitHub organization references throughout active configuration and documentation. Rename active `arcadia-*` CSS custom properties to `surrogate-*`. Rename the bundled CSL file to `surrogate-science.csl` and its style title/id, but retain its original named authors and CC BY-SA rights metadata. Replace `CITATION.cff` with a valid reusable publication template, omit DOI until one exists, and use obvious author/repository placeholders. Retain Arcadia's MIT copyright line in `LICENSE` and add `Copyright (c) 2026 Surrogate Science` for this fork. Do not invent scientific claims or publication metadata.

- [ ] **Step 4: Verify tests and both themes**

Run:

```bash
uvx pytest -q
quarto render --profile warm-journal
quarto render --profile technical-notebook
```

Expected: all tests pass and both renders complete successfully.

- [ ] **Step 5: Review the complete diff and commit**

Run `git diff --check`, confirm that Arcadia remains only where needed for upstream attribution/provenance, then commit with message `refactor: rename Surrogate Science publication extension`.
