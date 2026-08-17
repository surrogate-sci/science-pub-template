# Publication repository guidance

## Human authorship boundary

Publications created from this template and any related blog posts must remain
human-authored. Agents may operate the publishing machinery, but they must not
supply the writing, analysis, or scientific reasoning.

- Do not draft, rewrite, paraphrase, polish, translate, or autocomplete
  publication or blog prose. This includes titles, summaries, body text,
  captions, appendices, disclosures, contribution statements, and repository
  prose such as README or CONTRIBUTING text.
- Do not invent or add scientific claims, methods, results, interpretations,
  citations, examples, mathematical arguments, or analysis code whose output
  supports a scientific conclusion.
- Do not directly apply grammar, style, clarity, citation, or mathematical
  corrections to authored content. A human author must decide and make the
  final change.
- Text or analysis code supplied by a human may be inserted verbatim when the
  user explicitly directs where it belongs. Do not silently revise it while
  inserting it.
- Do not author AI-use disclosures or CRediT statements on anyone else's
  behalf. Agents may validate author-supplied records and report omissions.

Agents may:

- Compile, render, convert, package, and debug Quarto, Jupyter, LaTeX, HTML,
  and PDF outputs.
- Work on CI, configuration, templates, stylesheets, layout, accessibility,
  and web design without changing authored prose, analyses, or scientific
  meaning.
- Run human-authored analysis code to reproduce outputs and report failures
  without changing the analysis.
- Inspect human-authored writing and return a checklist of possible grammar
  problems, awkward sentences, unclear passages, citation problems, or
  mathematical inconsistencies. Give that checklist in chat or an untracked
  local review artifact; never commit or push it, and never apply its proposed
  edits automatically.

Before every commit or push, inspect the complete diff. If it contains
agent-authored publication or blog prose, scientific analysis, or scientific
reasoning, remove that content from the change and stop for a human author to
provide it. Do not transfer AI-written prose between this template, a derived
publication repository, or a blog repository. This `AGENTS.md` policy is an
explicitly authorized exception.

## Repository safety

- Do not commit generated `_site/`, `.quarto/`, rendered notebook support
  directories, local caches, or environment directories.
- Do not commit session notes, design drafts, implementation plans, private
  correspondence, credentials, or other agent-specific artifacts.
- Preserve author-approved metadata and disabled-by-default tracking and
  comment settings.
- Work on a focused branch and submit changes through a pull request.

## Verification

Before requesting review, run the relevant tests and render both publication
profiles:

```bash
make test
make render-warm
make render-technical
```

Review the rendered pages for layout, links, citations, metadata, and
disclosure placement without editing the authored content.
