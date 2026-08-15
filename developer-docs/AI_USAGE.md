# AI usage disclosure

Every manuscript must include an AI usage disclosure. Complete the root-level `ai-use.yml`; do not
edit the generated `disclosures/ai-use.md` directly.

The Surrogate Science policy permits AI use for editorial feedback, checking for mistakes, and
grammar. Record coding or computational assistance separately within the same author's statement.
Human authors remain responsible for the manuscript and its final wording.

## Required author review

- Every first author, including each co-first author, must provide an individual statement.
- Every last or senior author, including each co-last or co-senior author, must provide an
  individual statement.
- Every remaining author must read the complete disclosure and set
  `reviewed_full_disclosure: true` beside their name.

Each statement should identify the tool or model, explain its exact usage, identify the affected
writing, code, analysis, or figures, and state how the author checked the resulting work. Preserve
the author's wording; do not combine authors into a generic statement.

## Completing the file

1. Replace the placeholder names in `ai-use.yml` with the complete author roster.
2. Add every first author's and last author's individual `statement`.
3. List every other author under `other_authors` after they read the complete disclosure.
4. Change `status: draft` to `status: complete`.
5. Validate and regenerate the manuscript include:

   ```bash
   python3 scripts/generate_ai_disclosure.py ai-use.yml disclosures/ai-use.md
   ```

The generated Markdown is included in the publication automatically. While the YAML remains a
draft, the site displays a visible reminder instead of a disclosure. The validation workflow checks
the YAML but never commits, comments, opens a pull request, or publishes disclosure text.
