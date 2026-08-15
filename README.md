# Surrogate Science Publication Template

This repository is a Surrogate Science template for computational publications authored in Quarto. It supports Jupyter notebooks, executable Python or R content, reproducible figures, and a GitHub Pages HTML publication.

[View the live demo](https://surrogate-sci.github.io/science-pub-template/)

## Publication themes

The template includes two separate themes built from the same Surrogate Science palette and type system:

- **Warm Journal** is the default. It uses Cormorant Garamond for editorial display, Assistant for interface text, and Fira for labels and code.
- **Technical Notebook** uses Assistant Semibold for technical display, a teal masthead, and Fira for labels and code.

Preview or render either theme explicitly:

```bash
make preview-warm
make preview-technical
make render-warm
make render-technical
```

For CI or hosting, set `QUARTO_PROFILE=technical-notebook` to select Theme B. Without an explicit profile, Quarto uses `warm-journal`.

## Template Documentation

All the learning resources for this template can be found in `developer-docs/`.

- [Quickstart Guide](developer-docs/QUICKSTART.md) - **The most efficient way to get started** is to follow this guide (the rest can wait)
- [Environment Setup Guide](developer-docs/ENVIRONMENT_SETUP.md) - How to set up your development environment
- [Publishing Guide](developer-docs/PUBLISHING_GUIDE.md) - How to publish your notebook publication
- [Template Architecture](developer-docs/TEMPLATE_ARCHITECTURE.md) - Understanding the template's structure

---

**NOTE: When ready to publish, fill in the information below, then delete this line and everything above it.**

# [PUB-TITLE]

This code repository contains or points to all materials required for creating and hosting the publication entitled, *"[PUB-TITLE]"*.

The publication is hosted at [this URL](https://surrogate-sci.dev/[REPO-NAME]/).

## Data Description

[DESCRIPTION OF THE DATA]

## Reproduce

Please see [SETUP.qmd](pages/SETUP.qmd).

## Contribute

Please see [CONTRIBUTING.qmd](pages/CONTRIBUTING.qmd).
